#!/usr/bin/env python3
"""
Generate GEMINI.md from .claude/ context files
Converts claude-cognitive attention state to Gemini-compatible context
"""
import json
import os
from pathlib import Path
from datetime import datetime

def load_attention_state():
    """Load current attention state from claude-cognitive."""
    state_files = [
        Path(".claude/attn_state.json"),
        Path.home() / ".claude/attn_state.json"
    ]

    for state_file in state_files:
        if state_file.exists():
            try:
                with open(state_file) as f:
                    return json.load(f)
            except:
                pass

    return {"scores": {}, "turn_count": 0}

def get_hot_warm_files(scores, hot_threshold=0.8, warm_threshold=0.25):
    """Categorize files by attention score."""
    hot = []
    warm = []

    for file_path, score in scores.items():
        if score >= hot_threshold:
            hot.append((file_path, score))
        elif score >= warm_threshold:
            warm.append((file_path, score))

    # Sort by score descending
    hot.sort(key=lambda x: x[1], reverse=True)
    warm.sort(key=lambda x: x[1], reverse=True)

    return hot, warm

def read_file_content(file_path, max_lines=None):
    """Read file content, optionally limited to first N lines."""
    context_paths = [
        Path(f".claude/{file_path}"),
        Path.home() / f".claude/{file_path}"
    ]

    for path in context_paths:
        if path.exists():
            try:
                with open(path) as f:
                    if max_lines:
                        lines = []
                        for i, line in enumerate(f):
                            if i >= max_lines:
                                lines.append(f"\n... [Truncated at {max_lines} lines] ...\n")
                                break
                            lines.append(line)
                        return ''.join(lines)
                    else:
                        return f.read()
            except:
                pass

    return None

def generate_gemini_md():
    """Generate GEMINI.md from claude-cognitive state."""
    state = load_attention_state()
    hot_files, warm_files = get_hot_warm_files(state.get("scores", {}))

    # Start building GEMINI.md content
    content = []

    # Header
    content.append("# Project Context for Gemini CLI\n\n")
    content.append(f"*Auto-generated from claude-cognitive attention state at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
    content.append("---\n\n")

    # Project overview from CLAUDE.md if it exists
    claude_md = read_file_content("CLAUDE.md")
    if claude_md:
        content.append("## Project Overview\n\n")
        content.append(claude_md)
        content.append("\n\n---\n\n")

    # HOT context (full content)
    if hot_files:
        content.append("## 🔥 Active Context (High Attention)\n\n")
        content.append("These files are currently highly relevant based on recent activity:\n\n")

        for file_path, score in hot_files:
            content.append(f"### {file_path} (score: {score:.2f})\n\n")
            file_content = read_file_content(file_path)
            if file_content:
                content.append(f"```markdown\n{file_content}\n```\n\n")
            else:
                content.append("*File not found*\n\n")

    # WARM context (headers only)
    if warm_files:
        content.append("## 🌡️ Background Context (Moderate Attention)\n\n")
        content.append("These files have moderate relevance - headers shown for awareness:\n\n")

        for file_path, score in warm_files:
            content.append(f"### {file_path} (score: {score:.2f})\n\n")
            file_content = read_file_content(file_path, max_lines=25)
            if file_content:
                content.append(f"```markdown\n{file_content}\n```\n\n")
            else:
                content.append("*File not found*\n\n")

    # Footer with usage instructions
    content.append("---\n\n")
    content.append("## How to Use This Context\n\n")
    content.append("This file contains project-specific context for Gemini CLI. It is automatically generated ")
    content.append("from your `.claude/` directory attention state.\n\n")
    content.append("**To update this context:**\n")
    content.append("```bash\n")
    content.append("python3 ~/.claude/scripts/generate-gemini-md.py\n")
    content.append("```\n\n")
    content.append("**Attention scores:**\n")
    content.append("- 🔥 HOT (≥0.8): Full content included - actively relevant\n")
    content.append("- 🌡️ WARM (0.25-0.8): Headers only - background awareness\n")
    content.append("- ❄️ COLD (<0.25): Not included - currently irrelevant\n\n")

    return ''.join(content)

def main():
    """Main entry point."""
    try:
        gemini_md_content = generate_gemini_md()

        # Write to current directory
        output_file = Path("GEMINI.md")
        with open(output_file, 'w') as f:
            f.write(gemini_md_content)

        print(f"✅ Generated GEMINI.md ({len(gemini_md_content)} chars)")
        print(f"📍 Location: {output_file.absolute()}")

        # Show summary
        state = load_attention_state()
        hot, warm = get_hot_warm_files(state.get("scores", {}))
        print(f"\n📊 Context Summary:")
        print(f"   🔥 HOT files: {len(hot)}")
        print(f"   🌡️ WARM files: {len(warm)}")
        print(f"   🔄 Turn count: {state.get('turn_count', 0)}")

    except Exception as e:
        print(f"❌ Error generating GEMINI.md: {e}")
        import traceback
        traceback.print_exc()
        exit(1)

if __name__ == "__main__":
    main()
