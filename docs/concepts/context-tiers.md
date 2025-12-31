# Context Tiers - HOT/WARM/COLD Explained

**Concept:** Files exist in three tiers based on attention score, controlling how much content is injected.

---

## The Three Tiers

```
1.0  ┤ ─────── HOT ────────  (Full content)
     │
0.8  ┤ ─────── Threshold
     │
     │ ─────── WARM ────────  (Headers only)
     │
0.25 ┤ ─────── Threshold
     │
     │ ─────── COLD ────────  (Evicted)
     │
0.0  ┴
```

### HOT Tier (score ≥ 0.8)

**Behavior:** Full file content injected

**Use case:** Active development on this system

**Token cost:** 2,500-5,000 tokens per file

**Example output:**
```markdown
━━━ [🔥 HOT] systems/legion.md (score: 1.00) ━━━
# Legion - Primary Development & Inference Node

> **Role**: Primary dev, main inference, Discord bot hosting
> **Host**: `legion.local` (127.0.0.1) - **THIS MACHINE**
> **Hardware**: RTX 5090 (24GB VRAM), Ultra 9 275HX CPU
> **Critical Path**: Yes - hosts CVMP core + pipeline

## Topology
| Direction | Connected To | Protocol | Purpose |
|-----------|--------------|----------|---------|
| ← Receives | Orin | gRPC:8765 | Layer 0 sensory |
| → Sends | ASUS | gRPC:50051 | Visual perception |

## Quick Health
```bash
nvidia-smi
curl http://192.168.0.103:8765/health
```

## VRAM Budget
| Component | VRAM | Status |
|-----------|------|--------|
| Oracle 1.7B (int8) | ~4GB | Running |
| Dolphin 24B | ~18GB | On-demand |
| ES-AC v2 | ~2GB | Always loaded |

[... FULL 10KB DOCUMENT CONTINUES ...]
```

**Limit:** Max 4 HOT files to prevent token explosion

---

### WARM Tier (0.25 ≤ score < 0.8)

**Behavior:** Header-only injection (first 25 lines)

**Use case:** Topology awareness without full context

**Token cost:** 200-500 tokens per file (80-95% savings!)

**Example output:**
```markdown
━━━ [🌡️ WARM] modules/intelligence.md (score: 0.65) ━━━
# Intelligence Layer - Adaptive Reasoning & Oracle Validation

> **Purpose**: Multi-step reasoning, MCTS planning, Oracle prediction
> **Entry Point**: `intelligent_systems_integration.py`
> **Layer**: Layer 5-6 (in 8-layer pipeline)
> **Runs On**: Legion

## Topology
| Direction | Interface | Data Type |
|-----------|-----------|-----------|
| ← Input | `pre_generation_hook(ctx)` | AnalysisContext |
| → Output | `GenerationParameters` | Adaptive params |

## Key Interface
```python
class AdaptiveIntelligenceSystem:
    def pre_generation_hook(self, ctx) -> IntelligentContext
```

---
<!-- WARM CONTEXT ENDS ABOVE THIS LINE -->
... [FULL CONTENT TRUNCATED, mention to expand] ...
```

**Benefit:** See system structure and topology without loading full documentation

**Limit:** Max 8 WARM files

---

### COLD Tier (score < 0.25)

**Behavior:** Evicted from context entirely

**Use case:** Irrelevant to current work

**Token cost:** 0 tokens

**Example:** File not shown at all

**Recovery:** Mention keywords → instantly returns to HOT/WARM

---

## Why Tiers Matter

### Token Budget Enforcement

```python
MAX_TOTAL_CHARS = 25000  # Hard ceiling
```

**Without tiers:**
```
User mentions 6 systems
→ Load all 6 files fully = 60KB = 15K tokens
→ EXCEEDS BUDGET
→ Context truncated, missing info
```

**With tiers:**
```
User mentions 6 systems
→ 2 most relevant: HOT (full content) = 20KB
→ 4 related: WARM (headers only) = 2KB
→ Total: 22KB = 5.5K tokens
→ UNDER BUDGET
→ All topology visible, key systems full
```

### Topology Awareness

**The power of WARM tier:**

Even when you're not actively working on a system, you can still see:
- Where it runs (host/hardware)
- What it connects to (topology table)
- How to check health (quick commands)
- Key entry points (interface definitions)

**Example:** Working on visual systems (ASUS HOT), but pipeline integration is WARM:

```markdown
[🔥 HOT] systems/asus.md
  [Full visual server documentation]

[🌡️ WARM] integrations/pipe-to-orin.md
  > **Purpose**: Legion pipeline calls Orin Layer 0
  > **Protocol**: gRPC 192.168.0.103:8765
  > **Timeout**: 100ms
  ...
```

You can see the pipeline integration exists and how it works, without loading 10KB of implementation details.

---

## Tier Transitions

### How Files Move Between Tiers

```
Example: intelligence.md over 5 turns

Turn 1: User mentions "oracle"
  → Keyword match
  → Score: 0 → 1.0
  → Tier: COLD → HOT ✨

Turn 2: User talks about visual systems (no oracle mention)
  → Decay: 1.0 × 0.70 = 0.70
  → Tier: HOT → WARM ⚡

Turn 3: Still no mention
  → Decay: 0.70 × 0.70 = 0.49
  → Tier: WARM (still visible)

Turn 4: Still no mention
  → Decay: 0.49 × 0.70 = 0.34
  → Tier: WARM (still visible)

Turn 5: Still no mention
  → Decay: 0.34 × 0.70 = 0.24
  → Tier: WARM → COLD ❄️ (evicted)

Turn 10: User mentions "oracle" again
  → Keyword match
  → Score: 0.24 → 1.0
  → Tier: COLD → HOT ✨ (instant return!)
```

**Key insight:** Files naturally fade from HOT → WARM → COLD as conversation moves on, but instantly return when mentioned.

---

## Structured Headers

All documentation files follow this format:

```markdown
# [System/Module Name]

> **Role**: [One-line description]
> **Host**: [Where it runs]
> **Hardware**: [GPU/CPU/NPU specs]
> **Critical Path**: [Yes/No - is this a single point of failure?]

## Topology
| Direction | Connected To | Protocol | Purpose |
|-----------|--------------|----------|---------|
| ← Receives | [source] | [protocol] | [what data] |
| → Sends | [target] | [protocol] | [what data] |

## Quick Health
```bash
[One-liner health check commands]
```

## Key Processes
- `process_name`: Description

---
<!-- WARM CONTEXT ENDS ABOVE THIS LINE -->

[Full documentation continues below]
```

**Why this structure?**
- **First 25 lines** = Header extracted for WARM tier
- **Topology table** = Always visible even when WARM
- **Quick health** = Commands available even when WARM
- **Marker comment** = Explicit truncation point

**Result:** WARM tier files are still useful, not just noise

---

## Token Savings Examples

### Example 1: Cold Start

**User's first message:** "How does the system work?"

**Without tiers:**
```
Load all 13 docs fully = 400KB = 100K tokens
EXCEEDS LIMIT → Fails
```

**With tiers:**
```
No keywords matched yet
→ Load project overview (pinned) = 5KB HOT
→ Load all others as WARM (headers) = 6KB
→ Total: 11KB = 2.8K tokens
→ 97% savings!
```

### Example 2: Focused Work

**User working on visual systems for 10 turns**

**Without tiers:**
```
Turn 1: Load asus.md, img-to-asus.md = 25KB
Turn 2: + legion.md = 35KB
Turn 3: + pipeline.md = 45KB
...
Turn 10: 7-8 files = 80KB
Average: ~40KB per turn
```

**With tiers:**
```
Turn 1: asus.md HOT, img-to-asus.md WARM = 15KB
Turn 2: asus.md HOT, legion.md HOT, img-to-asus.md WARM = 20KB
Turn 3: asus.md HOT, visual-adapter.md HOT, legion.md WARM = 18KB
...
Turn 10: 2 HOT, 3 WARM = 22KB
Average: ~18KB per turn
→ 55% savings
```

### Example 3: Working Memory

**10-turn conversation bouncing between topics**

**Without tiers:**
```
Each topic switch = load different files
No memory of previous topics
Total: 10 topics × 30KB = 300KB cumulative
```

**With tiers:**
```
Previous topics stay in WARM tier
→ Topology still visible
→ Can reference earlier systems
→ Natural conversation flow
Total: 25KB max at any turn (budget enforced)
→ 92% savings + better UX
```

---

## Visual Example

```
File Attention Over Time (Tiers Visualized)

1.0  ┤ ━━━━━━━ HOT ━━━━━━━
     │       asus.md
     │      ╱│╲
0.8  ┤ ─────┼─┼───────────── HOT/WARM boundary
     │    ╱  │ ╲___
     │   ╱   │     ╲___
0.6  ┤  ╱    │         ╲___ legion.md
     │ ╱     │             ╲
     │╱      │              ╲
0.4  ┤       │               ╲
     │       │
0.25 ┤───────┼──────────────── WARM/COLD boundary
     │       │                 (pipeline.md fades)
0.0  ┴───────┴────────────────
     T1     T2    T3    T4    T5

Legend:
- asus.md: Mentioned T1, stays HOT
- legion.md: Co-activated T1, decays to WARM by T3
- pipeline.md: Mentioned T1, decays to COLD by T5
```

---

## Tuning Tier Thresholds

**Default thresholds:**
```python
HOT_THRESHOLD = 0.8
WARM_THRESHOLD = 0.25
```

**Can be adjusted in `context-router-v2.py`:**

```python
# More aggressive HOT (fewer full files)
HOT_THRESHOLD = 0.9

# More generous WARM (more headers visible)
WARM_THRESHOLD = 0.15

# Faster eviction (less working memory)
WARM_THRESHOLD = 0.35
```

**Guidelines:**
- **HOT threshold higher** (0.9) = Fewer full files, more budget for WARM
- **WARM threshold lower** (0.15) = More headers visible, better topology awareness
- **Default (0.8 / 0.25)** works well for most projects

---

## Summary

**Context tiers provide intelligent budget management:**

1. **HOT (≥0.8)**: Full content for active development
2. **WARM (0.25-0.8)**: Headers for topology awareness
3. **COLD (<0.25)**: Evicted to save tokens

**Benefits:**
- 64-95% token savings vs loading everything
- Topology always visible even when files are WARM
- Natural working memory (files fade gracefully)
- Hard budget ceiling prevents explosions
- Files instantly return when mentioned

**Think of it as:**
- **HOT** = What you're actively thinking about
- **WARM** = What's in the back of your mind
- **COLD** = Completely forgotten (but quickly remembered)

---

**Next:** [Fractal Documentation](./fractal-docs.md) - Infinite zoom strategy

**See also:**
- [Attention Decay](./attention-decay.md) - How files transition between tiers
- [Token Budgets](../reference/token-budgets.md) - Optimization strategies
