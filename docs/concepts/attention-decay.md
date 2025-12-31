# Attention Decay - Why Files Fade

**Concept:** Files you haven't mentioned recently fade from context automatically.

---

## The Problem

With large codebases, you can't keep ALL documentation in context at once. But you also can't manually manage what's loaded - that's tedious.

**Solution:** Attention decay - files fade when not mentioned, freeing tokens for active work.

---

## How It Works

### Mathematical Model

Every conversation turn, each file's attention score changes based on three forces:

```python
# 1. DECAY (forgetting when not mentioned)
score_new = score_old * decay_rate

# Example decay rates:
decay = {
    "systems/": 0.85,      # Hardware is stable → decays slowly
    "modules/": 0.70,      # Code changes frequently → decays faster
    "integrations/": 0.80, # APIs semi-stable
    "default": 0.70
}

# 2. KEYWORD ACTIVATION (direct mention)
if any(keyword in your_message.lower() for keyword in file_keywords):
    score = 1.0  # Instantly HOT

# 3. CO-ACTIVATION (related files boost together)
for activated_file in directly_mentioned:
    for related_file in co_activation_graph[activated_file]:
        score[related_file] = min(1.0, score[related_file] + 0.35)
```

---

## Example Evolution

### Turn 1: You ask "How does authentication work?"

**Before:**
- All files at 0 (never mentioned)

**After keyword activation:**
- `modules/auth.md`: 0 → 1.0 (keyword: "authentication")

**After co-activation:**
- `modules/api.md`: 0 → 0.35 (auth uses API)
- `modules/database.md`: 0 → 0.35 (auth stores sessions)

**Result:**
- **HOT** (full file): `auth.md`
- **WARM** (header only): `api.md`, `database.md`

---

### Turn 2: You ask "How is the database structured?"

**Decay first:**
- `auth.md`: 1.0 → 0.70 (modules decay 30%)
- `api.md`: 0.35 → 0.245 (now COLD, evicted!)
- `database.md`: 0.35 → 0.245 (COLD)

**Then keyword activation:**
- `database.md`: 0.245 → 1.0 (keyword: "database")

**Result:**
- **HOT**: `database.md`
- **WARM**: `auth.md` (still relevant from last turn)
- **COLD**: `api.md` (evicted, you haven't mentioned it)

---

### Turn 3: You ask "Show me the frontend code"

**Decay:**
- `auth.md`: 0.70 → 0.49 (WARM)
- `database.md`: 1.0 → 0.70 (WARM)

**Keyword activation:**
- `systems/frontend.md`: 0 → 1.0 (keyword: "frontend")

**Result:**
- **HOT**: `frontend.md` (new topic)
- **WARM**: `auth.md`, `database.md` (lingering from backend discussion)

**Over 5-10 turns without mentioning backend:**
- Auth and database decay to COLD
- Only frontend stays active
- **Result:** Token budget focused on current work

---

## Why Different Decay Rates?

**Systems (0.85 - slower decay):**
- Hardware/infrastructure changes rarely
- Useful background context even when not actively discussed
- Example: Network topology, deployment architecture

**Modules (0.70 - faster decay):**
- Code changes frequently
- Only needed when actively working on that feature
- Example: Auth module, API handlers

**Integrations (0.80 - medium decay):**
- API contracts semi-stable
- Useful context but not as persistent as infrastructure
- Example: Stripe integration, external APIs

---

## Tuning Decay Rates

**Edit `~/.claude/scripts/context-router-v2.py`:**

```python
DECAY_RATES = {
    "systems/": 0.85,       # Adjust if infrastructure files fade too fast
    "modules/": 0.70,       # Adjust if code files linger too long
    "integrations/": 0.80,
    "default": 0.70
}
```

**Guidelines:**
- **Higher number** (0.9) = slower decay = more persistent
- **Lower number** (0.5) = faster decay = more aggressive eviction
- **Default (0.70)** works well for most projects

---

## Pinned Files (Never Decay Below WARM)

Some files are so critical they should never fully evict:

```python
PINNED_FILES = [
    "systems/network.md",  # Network topology always warm
    # Add your critical files here
]
```

**Use for:**
- System architecture overview
- Critical topology diagrams
- Shared infrastructure everyone needs

**Don't overuse:**
- Too many pinned files defeats the purpose
- 2-3 files max recommended

---

## Attention State Persistence

Attention scores are saved between Claude Code sessions:

**State file:** `.claude/attn_state.json`

```json
{
  "systems/frontend.md": {
    "score": 0.85,
    "last_updated": 1735583400
  },
  "modules/auth.md": {
    "score": 0.49,
    "last_updated": 1735583400
  }
}
```

**Why this matters:**
- Start new Claude session → files you were working on yesterday are still WARM
- No "cold start" rediscovery every session
- Persistent working memory across days

---

## Token Savings from Decay

**Without decay (naive approach):**
- Load all 20 files = 80,000 chars
- Every turn = 80K context ceiling

**With decay:**
- Turn 1: 4 HOT files = 25,000 chars
- Turn 5: 2 HOT + 3 WARM files = 18,000 chars
- Turn 10: 1 HOT + 2 WARM files = 12,000 chars

**Result:** 70-85% reduction in context size as conversation focuses.

---

## Common Questions

### "Why did my file disappear?"

**Reason:** Decayed to COLD after not being mentioned for several turns.

**Solution:**
- Mention it again (keyword activation brings it back instantly)
- Or adjust decay rate higher for that category
- Or pin it if truly critical

### "Files activate I don't want"

**Reason:** Keyword too broad (e.g., "system" matches everything).

**Solution:**
- Edit `context-router-v2.py` keyword mappings
- Use more specific keywords
- See [CUSTOMIZATION.md](../../CUSTOMIZATION.md)

### "Co-activation not working"

**Reason:** Files not linked in CO_ACTIVATION graph.

**Solution:**
- Edit `context-router-v2.py` CO_ACTIVATION section
- Add relationships between related files

---

## Visual Example

```
File Attention Over Time

1.0  ┤        auth.md
     │       ╱│╲
     │      ╱ │ ╲___
0.8  ┤     ╱  │     ╲___
     │    ╱   │         ╲___
     │   ╱    │             ╲___
0.6  ┤  ╱     │                 ╲___
     │ ╱      │                     ╲___
     │╱       │                         ╲___ COLD (evicted)
0.4  ┤        │
     │        │        frontend.md
0.2  ┤        │              ╱│╲
     │        │             ╱ │ ╲___
0.0  ┴────────┴────────────┴──┴────────────▶
     T1      T2      T3   T4 T5    T6   T7  Conversation turns

Legend:
- auth.md: Mentioned T1, decays naturally
- frontend.md: Mentioned T4, stays HOT while discussed
- Files below 0.25 = COLD (evicted from context)
```

---

## Summary

**Attention decay keeps your context focused:**

1. **Files activate** when you mention keywords
2. **Related files co-activate** (spreading activation)
3. **Unused files decay** over turns (configurable rate)
4. **Result:** Token budget spent on active work, not stale context

**Think of it as working memory:**
- You remember what you're actively thinking about
- Background knowledge fades when not used
- Mention something → instantly recall it
- Natural focus without manual management

---

**Next:** [Context Tiers](./context-tiers.md) - How HOT/WARM/COLD actually works

**See also:**
- [CUSTOMIZATION.md](../../CUSTOMIZATION.md) - Tuning keywords and decay rates
- [Context Router source](../../scripts/context-router-v2.py) - Implementation details
