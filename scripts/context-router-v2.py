#!/usr/bin/env python3
"""
Attentional Context Router v2.0
================================
Implements working memory dynamics for Claude Code context injection.

Architecture:
- HOT (>0.8): Full file injection - active development
- WARM (0.25-0.8): Header/summary only - background awareness  
- COLD (<0.25): Evicted from context

Features:
- Decay: Unmentioned files fade (configurable per category)
- Co-activation: Related files boost each other
- Pinned files: Critical topology always at least warm
- State persistence: Attention scores survive across turns

Usage: Called by UserPromptSubmit hook
Input: JSON from stdin with "prompt" field
Output: Tiered context to stdout
"""

import sys
import json
import os
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
from datetime import datetime
import re

# ============================================================================
# CONFIGURATION
# ============================================================================

# State file location
PROJECT_STATE = Path(".claude/attn_state.json")
GLOBAL_STATE = Path.home() / ".claude" / "attn_state.json"
HISTORY_FILE = Path.home() / ".claude" / "attention_history.jsonl"

# History retention
MAX_HISTORY_DAYS = 30  # Archive entries older than 30 days

# Decay rates per category (how fast files fade when not mentioned)
# Higher = slower decay (more persistent)
DECAY_RATES = {
    "systems/": 0.85,       # Hardware is stable, decay slow
    "modules/": 0.70,       # Code changes more frequently
    "integrations/": 0.80,  # APIs semi-stable
    "docs/": 0.75,          # Documentation medium decay
    "default": 0.70
}

# Attention thresholds
HOT_THRESHOLD = 0.8         # Full file injection
WARM_THRESHOLD = 0.25       # Header-only injection
# Below WARM = COLD (evicted)

# Boost amounts
KEYWORD_BOOST = 1.0         # Direct mention → score = 1.0
COACTIVATION_BOOST = 0.35   # Related file boost

# Limits (prevent context explosion)
MAX_HOT_FILES = 4
MAX_WARM_FILES = 8
WARM_HEADER_LINES = 25      # Lines to extract for warm context
MAX_TOTAL_CHARS = 25000     # Hard ceiling on total output

# ============================================================================
# PROJECT CONFIG LOADING
# Load keywords from project-local .claude/keywords.json if available
# ============================================================================

def load_project_config() -> Tuple[Dict[str, List[str]], Dict[str, List[str]], List[str]]:
    """
    Load keywords, co-activation, and pinned files from project config.
    Returns (keywords, co_activation, pinned_files) tuple.
    Falls back to empty defaults if no config found.
    """
    config_paths = [
        Path(".claude/keywords.json"),           # Project-local
        Path.home() / ".claude/keywords.json",   # Global fallback
    ]

    for config_path in config_paths:
        if config_path.exists():
            try:
                with open(config_path) as f:
                    config = json.load(f)
                return (
                    config.get("keywords", {}),
                    config.get("co_activation", {}),
                    config.get("pinned", [])
                )
            except (json.JSONDecodeError, IOError):
                continue

    # No config found - return empty defaults
    return ({}, {}, [])

# Load config at module level
KEYWORDS, CO_ACTIVATION, PINNED_FILES = load_project_config()


# ============================================================================
# STATE MANAGEMENT
# ============================================================================

def get_state_file() -> Path:
    """Get appropriate state file (project-local preferred)."""
    if PROJECT_STATE.parent.exists():
        return PROJECT_STATE
    GLOBAL_STATE.parent.mkdir(parents=True, exist_ok=True)
    return GLOBAL_STATE


def load_state(state_file: Path) -> dict:
    """Load attention state from file."""
    if state_file.exists():
        try:
            return json.loads(state_file.read_text())
        except json.JSONDecodeError:
            pass
    
    # Initialize fresh state
    return {
        "scores": {path: 0.0 for path in KEYWORDS},
        "turn_count": 0,
        "last_update": datetime.now().isoformat(),
    }


def save_state(state_file: Path, state: dict) -> None:
    """Save attention state to file."""
    state["last_update"] = datetime.now().isoformat()
    state_file.parent.mkdir(parents=True, exist_ok=True)
    state_file.write_text(json.dumps(state, indent=2))


# ============================================================================
# ATTENTION DYNAMICS
# ============================================================================

def get_decay_rate(file_path: str) -> float:
    """Get decay rate for a file based on its category."""
    for prefix, rate in DECAY_RATES.items():
        if file_path.startswith(prefix):
            return rate
    return DECAY_RATES["default"]


def update_attention(state: dict, prompt: str) -> Tuple[dict, Set[str]]:
    """
    Update attention scores based on prompt content.
    Returns updated state and set of directly activated files.
    """
    prompt_lower = prompt.lower()
    directly_activated: Set[str] = set()
    
    # Phase 1: Decay all scores
    for path in state["scores"]:
        decay = get_decay_rate(path)
        state["scores"][path] *= decay
    
    # Phase 2: Keyword activation (direct mentions)
    for path, keywords in KEYWORDS.items():
        if any(kw in prompt_lower for kw in keywords):
            state["scores"][path] = KEYWORD_BOOST
            directly_activated.add(path)
    
    # Phase 3: Co-activation boost
    for activated_path in directly_activated:
        if activated_path in CO_ACTIVATION:
            for related_path in CO_ACTIVATION[activated_path]:
                if related_path in state["scores"]:
                    # Boost but don't exceed 1.0
                    current = state["scores"][related_path]
                    state["scores"][related_path] = min(1.0, current + COACTIVATION_BOOST)
    
    # Phase 4: Pinned file floor
    for pinned in PINNED_FILES:
        if pinned in state["scores"]:
            state["scores"][pinned] = max(state["scores"][pinned], WARM_THRESHOLD + 0.1)
    
    state["turn_count"] = state.get("turn_count", 0) + 1
    return state, directly_activated


# ============================================================================
# CONTENT EXTRACTION
# ============================================================================

def extract_warm_header(file_path: str, docs_root: Path) -> Optional[str]:
    """
    Extract structured header for warm context.
    Returns first WARM_HEADER_LINES lines, or None if file missing.
    """
    full_path = docs_root / file_path
    if not full_path.exists():
        return None
    
    try:
        content = full_path.read_text()
        lines = content.split('\n')[:WARM_HEADER_LINES]
        header = '\n'.join(lines)
        
        # Add truncation marker if we cut content
        if len(content.split('\n')) > WARM_HEADER_LINES:
            header += "\n\n... [WARM: Content truncated, mention to expand] ..."
        
        return header
    except Exception as e:
        return f"[Error reading {file_path}: {e}]"


def get_full_content(file_path: str, docs_root: Path) -> Optional[str]:
    """Get full file content for hot context."""
    full_path = docs_root / file_path
    if not full_path.exists():
        return None
    
    try:
        return full_path.read_text()
    except Exception as e:
        return f"[Error reading {file_path}: {e}]"


# ============================================================================
# TIERED INJECTION
# ============================================================================

def get_tier(score: float) -> str:
    """Classify attention score into tier."""
    if score >= HOT_THRESHOLD:
        return "HOT"
    elif score >= WARM_THRESHOLD:
        return "WARM"
    return "COLD"


def build_context_output(state: dict, docs_root: Path) -> Tuple[str, dict]:
    """
    Build tiered context output respecting limits.
    Returns (output_string, stats_dict).
    """
    # Sort files by attention score (highest first)
    sorted_files = sorted(
        state["scores"].items(),
        key=lambda x: x[1],
        reverse=True
    )
    
    hot_blocks = []
    warm_blocks = []
    stats = {"hot": 0, "warm": 0, "cold": 0}
    total_chars = 0
    
    for file_path, score in sorted_files:
        tier = get_tier(score)
        
        if tier == "HOT" and stats["hot"] < MAX_HOT_FILES:
            content = get_full_content(file_path, docs_root)
            if content and total_chars + len(content) < MAX_TOTAL_CHARS:
                hot_blocks.append(f"━━━ [🔥 HOT] {file_path} (score: {score:.2f}) ━━━\n{content}")
                total_chars += len(content)
                stats["hot"] += 1
            elif content:
                # Demote to warm if would exceed char limit
                header = extract_warm_header(file_path, docs_root)
                if header:
                    warm_blocks.append(f"━━━ [🌡️ WARM] {file_path} (score: {score:.2f}) ━━━\n{header}")
                    total_chars += len(header)
                    stats["warm"] += 1
                    
        elif tier == "WARM" and stats["warm"] < MAX_WARM_FILES:
            header = extract_warm_header(file_path, docs_root)
            if header and total_chars + len(header) < MAX_TOTAL_CHARS:
                warm_blocks.append(f"━━━ [🌡️ WARM] {file_path} (score: {score:.2f}) ━━━\n{header}")
                total_chars += len(header)
                stats["warm"] += 1
                
        else:
            stats["cold"] += 1
    
    # Combine output
    output_parts = []
    
    # Status header
    output_parts.append(f"╔══ ATTENTION STATE [Turn {state['turn_count']}] ══╗")
    output_parts.append(f"║ 🔥 Hot: {stats['hot']} │ 🌡️ Warm: {stats['warm']} │ ❄️ Cold: {stats['cold']} ║")
    output_parts.append(f"║ Total chars: {total_chars:,} / {MAX_TOTAL_CHARS:,} ║")
    output_parts.append("╚" + "═" * 38 + "╝")
    
    # Hot files first (most relevant)
    output_parts.extend(hot_blocks)
    
    # Then warm files
    output_parts.extend(warm_blocks)
    
    return "\n\n".join(output_parts), stats


# ============================================================================
# ATTENTION HISTORY TRACKING
# ============================================================================

def compute_transitions(prev_state: dict, curr_state: dict) -> dict:
    """Compute what moved between tiers."""
    transitions = {"to_hot": [], "to_warm": [], "to_cold": []}

    for path, score in curr_state["scores"].items():
        prev_score = prev_state.get("scores", {}).get(path, 0.0)
        prev_tier = get_tier(prev_score)
        curr_tier = get_tier(score)

        if curr_tier != prev_tier:
            if curr_tier == "HOT":
                transitions["to_hot"].append(path)
            elif curr_tier == "WARM":
                transitions["to_warm"].append(path)
            else:
                transitions["to_cold"].append(path)

    return transitions


def append_history(state: dict, prev_state: dict, activated: Set[str], prompt: str, stats: dict):
    """Append structured entry to history log."""

    # Extract keywords from prompt (simple: first 8 significant words)
    stop_words = {"the", "a", "an", "is", "are", "to", "for", "and", "or", "in", "on", "it", "this", "that", "with", "of"}
    words = [w.lower() for w in prompt.split() if len(w) > 2 and w.lower() not in stop_words][:8]

    entry = {
        "turn": state["turn_count"],
        "timestamp": datetime.now().isoformat(),
        "instance_id": os.environ.get("CLAUDE_INSTANCE", "default"),
        "prompt_keywords": words,
        "activated": sorted(list(activated)),
        "hot": sorted([p for p, s in state["scores"].items() if get_tier(s) == "HOT"]),
        "warm": sorted([p for p, s in state["scores"].items() if get_tier(s) == "WARM"]),
        "cold_count": stats["cold"],
        "transitions": compute_transitions(prev_state, state),
        "total_chars": stats.get("total_chars", 0)
    }

    try:
        # Ensure history file exists
        if not HISTORY_FILE.exists():
            HISTORY_FILE.parent.mkdir(exist_ok=True)
            HISTORY_FILE.touch()

        with open(HISTORY_FILE, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception:
        pass  # Don't fail hook on history write error


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main():
    """
    Main entry point for Claude Code hook.
    Reads JSON from stdin, outputs tiered context to stdout.
    """
    # Parse input
    try:
        input_data = json.loads(sys.stdin.read())
        prompt = input_data.get("prompt", "")
    except json.JSONDecodeError:
        # Fallback: treat entire stdin as prompt
        prompt = sys.stdin.read() if sys.stdin else ""
    
    if not prompt.strip():
        return
    
    # Determine docs root (configurable via env, or project-local, or global fallback)
    # Priority: CONTEXT_DOCS_ROOT env > project .claude/ > global ~/.claude/
    if os.environ.get("CONTEXT_DOCS_ROOT"):
        docs_root = Path(os.environ["CONTEXT_DOCS_ROOT"])
    elif Path(".claude").exists():
        docs_root = Path(".claude")
    else:
        docs_root = Path.home() / ".claude"

    # Load state
    state_file = get_state_file()
    prev_state = load_state(state_file)  # Keep copy before mutation
    state = json.loads(json.dumps(prev_state))  # Deep copy for modification

    # Update attention based on prompt
    state, activated = update_attention(state, prompt)

    # Build output
    output, stats = build_context_output(state, docs_root)
    stats["total_chars"] = len(output)  # Add total chars to stats

    # Append to history log (before save, so turn_count is correct)
    append_history(state, prev_state, activated, prompt, stats)

    # Save state for next turn
    save_state(state_file, state)
    
    # Log injection for debugging (append-only)
    log_file = Path.home() / ".claude" / "context_injection.log"
    try:
        with open(log_file, "a") as f:
            f.write(f"\n{'='*80}\n")
            f.write(f"[{datetime.now().isoformat()}] Turn {state['turn_count']}\n")
            f.write(f"Prompt (first 100 chars): {prompt[:100]}...\n")
            f.write(f"Stats: Hot={stats['hot']}, Warm={stats['warm']}, Cold={stats['cold']}\n")
            f.write(f"Total chars: {len(output):,}\n")
            f.write(f"Activated files: {', '.join(activated) if activated else 'none'}\n")
            f.write(f"{'='*80}\n")
            f.write(output)
            f.write(f"\n{'='*80}\n\n")
    except Exception as e:
        # Don't fail hook if logging fails
        pass

    # Output to Claude Code
    if stats["hot"] > 0 or stats["warm"] > 0:
        print(output)


if __name__ == "__main__":
    main()
