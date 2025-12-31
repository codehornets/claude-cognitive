# Pool Coordination - Multi-Instance State Sharing

**Concept:** Multiple Claude Code instances coordinate work via shared activity log.

---

## The Problem

**Scenario:** You have 4 terminal windows running Claude Code:
- Terminal A: Working on pipeline
- Terminal B: Working on visual systems
- Terminal C: Working on Oracle training
- Terminal D: Working on edge deployment

**Without coordination:**
- ❌ Terminal A fixes auth bug
- ❌ Terminal B doesn't know, starts fixing same bug
- ❌ Wasted effort, potential merge conflicts

**With pool system:**
- ✅ Terminal A completes auth fix, signals to pool
- ✅ Terminal B starts session, sees "A completed: auth fix"
- ✅ Terminal B works on something else, no duplication

---

## How It Works

### The Pool File

**Location:** `~/.claude/pool/instance_state.jsonl`

**Format:** Append-only log (JSONL = one JSON object per line)

```jsonl
{"id":"uuid1","timestamp":1735145600,"source_instance":"A","action":"completed","topic":"Auth token refresh","summary":"Fixed race condition...","affects":"auth.py, session_handler.py","blocks":"Session refactor can proceed"}
{"id":"uuid2","timestamp":1735145650,"source_instance":"B","action":"claimed","topic":"Visual perception ASUS","summary":"Starting CLIP/LLaVA integration...","affects":"image_integration_v3.py"}
```

**Why JSONL?**
- ✅ Append-only = O(1) writes, no file locking
- ✅ Crash-safe = Partial writes don't corrupt
- ✅ Human-readable = Easy to tail/grep/debug
- ✅ Simple = Standard JSON per line

---

## Action Types

### `completed` - Task Finished
```pool
INSTANCE: A
ACTION: completed
TOPIC: Context router v2 migration
SUMMARY: Migrated all docs to structured headers. V2 router tested. All hooks configured.
AFFECTS: systems/*.md, modules/*.md, settings.json
BLOCKS: Other instances can use attention dynamics now
```

**Use when:** Successfully finished a task others might depend on

### `blocked` - Encountered Blocker
```pool
INSTANCE: C
ACTION: blocked
TOPIC: Oracle training data access
SUMMARY: Cannot access training_data/interactions/ - directory locked by PID 12345. Need coordination.
AFFECTS: oracle_consciousness_integration.py
BLOCKS: Oracle model fine-tuning
```

**Use when:** Hit a blocker that others should know about

### `claimed` - Starting Work
```pool
INSTANCE: B
ACTION: claimed
TOPIC: ASUS visual server refactor
SUMMARY: Starting major refactor of CLIP/LLaVA integration. ASUS unavailable 14:00-14:30.
AFFECTS: visual_perception_client/, image_integration_v3.py
BLOCKS: Visual features unavailable during refactor window
```

**Use when:** Claiming exclusive access to prevent conflicts

### `signaling` - Important Info
```pool
INSTANCE: D
ACTION: signaling
TOPIC: Hailo NPU optimization opportunity
SUMMARY: Discovered Hailo-8L running at only 40% utilization. Could 2x speedup with better batching.
AFFECTS: orin_sensory_cortex/ppe_inference.py
BLOCKS: None, just FYI
```

**Use when:** Sharing discoveries that others should know

---

## Automatic vs Manual Mode

### Automatic Mode (Future Enhancement)

**Goal:** Auto-detect completions/blockers from conversation

Currently planned, not yet implemented. Will analyze assistant responses for:
- Completion patterns: "Successfully deployed", "Fixed the bug", "All tests passing"
- Blocker patterns: "Cannot access", "Permission denied", "Service unavailable"
- Auto-generate pool entries without manual blocks

### Manual Mode (Current - v1.0)

**How it works:**

1. **Work on task** - Use Claude Code normally
2. **Add pool block at end** - Include explicit coordination signal
3. **Session ends** - Stop hook extracts pool block
4. **Other instances see it** - Shows up at their session start

**Example conversation:**

```
user: "Fix the authentication bug"

assistant: [works on fix, tests, verifies]

assistant: "The authentication bug is now fixed. I've added mutex locking to prevent the race condition.

```pool
INSTANCE: A
ACTION: completed
TOPIC: Auth token refresh fix
SUMMARY: Fixed race condition in token refresh. Added mutex locking to prevent concurrent refresh attempts.
AFFECTS: auth.py, session_handler.py
BLOCKS: Session management refactor can proceed safely
```

All tests are passing."
```

When this session ends:
- Stop hook extracts the `pool` block
- Writes entry to `instance_state.jsonl`
- Other instances see it at next session start

---

## Relevance Filtering

**Problem:** If Instance B is working on visual systems, they don't care about every database change Instance A makes.

**Solution:** Relevance scoring filters entries

### How Relevance Works

Each instance has a **domain** (what they typically work on):

```python
INSTANCE_DOMAINS = {
    "A": ["pipeline", "orchestration", "integration", "core"],
    "B": ["visual", "image", "clip", "llava", "asus"],
    "C": ["inference", "oracle", "model", "training"],
    "D": ["edge", "hailo", "jetson", "npu", "embedded"]
}
```

When an entry is written:
1. Combine topic + summary + affects
2. Count keyword matches for each instance
3. Compute relevance score (0.0 - 1.0)

**Example:**
```
Entry: "Oracle training data access blocked"
Topic: "Oracle training data access"
Summary: "Cannot access training_data/interactions/"
Affects: "oracle_consciousness_integration.py"

Matches:
- Instance A: "training" (1 match) → 0.12 relevance
- Instance B: (0 matches) → 0.0 relevance
- Instance C: "oracle", "training", "consciousness" (3 matches) → 0.88 relevance
- Instance D: (0 matches) → 0.0 relevance
```

When instances load pool:
- Instance C sees this entry (relevance 0.88 ≥ 0.3)
- Instances A, B, D don't see it (relevance < 0.3)

**Exception:** Entries with `BLOCKS` field are always shown (high priority)

---

## What Other Instances See

### Compact Mode (Default)

```
## Session Context
- **Instance**: B
- **Pool**: 3 recent (1 own, 2 others)
- **Status**: 2 completed, 1 blocked

### Recent Activity
- [A] completed: Auth token refresh fix
- [B] claimed: ASUS visual server refactor
- [C] blocked: Oracle training data access
```

**Benefit:** Quick overview without noise

### Full Mode (POOL_COMPACT=0)

```
## 🔄 Recent Instance Activity
> You are Instance **B** in a distributed system.
> Recent work by you and other instances:

🟢 **[A]** ✅ **completed** — Auth token refresh fix
  _Fixed race condition in token refresh. Added mutex locking._
  📂 Affects: `auth.py, session_handler.py`
  🔓 Unblocks: Session management refactor can proceed
  🕐 5m ago | Relevance: 20%

🔵 **[YOU]** 🔒 **claimed** — ASUS visual server refactor
  _Starting major refactor of CLIP/LLaVA integration._
  📂 Affects: `visual_perception_client/, image_integration_v3.py`
  🔓 Unblocks: Visual features unavailable 14:00-14:30
  🕐 2m ago | Relevance: 90%
```

**Benefit:** Full context with details

---

## Time-to-Live (TTL)

**Default:** 1 hour

Entries older than TTL are filtered out (lazy deletion).

**Why 1 hour?**
- Long enough to coordinate same-day work
- Short enough to prevent clutter
- Can be adjusted per entry if needed

**No cleanup daemon needed** - filtering happens on read

---

## Instance Identity

### Setting Your Instance ID

**Option 1: Environment Variable (Recommended)**
```bash
# Set per terminal
export CLAUDE_INSTANCE=A

# Or add to shell profile
echo "export CLAUDE_INSTANCE=A" >> ~/.bashrc
```

**Option 2: Temporary**
```bash
# Just for this session
CLAUDE_INSTANCE=B claude
```

**Instance naming:**
- Use single letters: A, B, C, D
- Or descriptive: LEGION, ORIN, DEV, PROD
- Should be unique per concurrent terminal

---

## Use Cases

### Use Case 1: Preventing Duplicate Work

**Instance A:**
```pool
INSTANCE: A
ACTION: completed
TOPIC: Auth bug fix
SUMMARY: Fixed token refresh race condition. Added mutex locking.
AFFECTS: auth.py, session_handler.py
```

**Instance B (starts 10 min later):**
```
## Session Context
- [A] completed: Auth bug fix
```

**User B:** "I want to fix the auth bug"

**Claude B:** "I see Instance A completed an auth bug fix 10 minutes ago (race condition in token refresh). Their changes are in auth.py and session_handler.py. Should I review their fix first, or are you referring to a different auth issue?"

**Result:** No duplicate work

### Use Case 2: Coordinating Downtime

**Instance B:**
```pool
INSTANCE: B
ACTION: claimed
TOPIC: ASUS visual server refactor
SUMMARY: Starting major refactor. ASUS unavailable 14:00-14:30.
AFFECTS: visual_perception_client/
BLOCKS: Visual features unavailable during window
```

**Instance A (at 14:15):**
```
- [B] claimed: ASUS visual server refactor
  ASUS unavailable 14:00-14:30
```

**User A:** "Test image generation"

**Claude A:** "Instance B has the ASUS visual server in refactor mode (unavailable until 14:30). Image generation tests will fail. Should we wait 15 minutes or test something else?"

**Result:** Avoid wasted time

### Use Case 3: Sharing Discoveries

**Instance D:**
```pool
INSTANCE: D
ACTION: signaling
TOPIC: Hailo NPU optimization
SUMMARY: Hailo-8L running at 40% utilization. Could 2x speedup with better batching.
AFFECTS: orin_sensory_cortex/ppe_inference.py
```

**Instance C (working on Orin performance):**
```
- [D] signaling: Hailo NPU optimization
  40% utilization, could 2x with batching
```

**User C:** "Why is Orin slow?"

**Claude C:** "Instance D just discovered the Hailo NPU is only at 40% utilization due to inefficient batching in ppe_inference.py. This is likely your slowdown. Want to investigate the batching optimization they mentioned?"

**Result:** Knowledge shared, faster debugging

---

## Manual Query

```bash
# Show all recent entries
python3 ~/.claude/scripts/pool-query.py

# Last 5 minutes
python3 ~/.claude/scripts/pool-query.py --since 5m

# Filter by instance
python3 ~/.claude/scripts/pool-query.py --instance A

# Filter by action
python3 ~/.claude/scripts/pool-query.py --action completed

# Verbose mode
python3 ~/.claude/scripts/pool-query.py --verbose
```

---

## Common Questions

### "Do I need to write pool blocks for everything?"

**No.** Only for:
- ✅ Completions others might depend on
- ✅ Blockers others should know about
- ✅ Claims for exclusive access
- ✅ Important discoveries

**Not for:**
- ❌ Routine file edits
- ❌ Reading/analyzing code
- ❌ Minor changes
- ❌ Answering user questions

### "What if I forget the pool block format?"

The system is forgiving:
- Missing pool blocks = no entry written (safe)
- Typos in fields = logged error, no crash
- Wrong action type = defaults to "signaling"
- Session continues normally

### "Can I see other instances' pool blocks in real-time?"

```bash
# Watch pool file live
tail -f ~/.claude/pool/instance_state.jsonl

# Pretty print new entries
tail -f ~/.claude/pool/instance_state.jsonl | jq .
```

### "What if two instances write at the same time?"

JSONL is append-only = atomic on most filesystems. No corruption, both entries written.

---

## Summary

**Pool coordination enables distributed development:**

1. **Manual pool blocks** signal completions/blockers/claims
2. **Relevance filtering** shows only what matters to your work
3. **TTL filtering** auto-expires old entries
4. **Lazy cleanup** = no background processes needed
5. **Lightweight** = JSONL file, <1MB typical

**Think of it as:**
- Shared team status board
- Automatic for long-running work
- Manual for critical coordination
- Always optional, never required

---

**Next:** [Context Tiers](./context-tiers.md) - How HOT/WARM/COLD works

**See also:**
- [Attention Decay](./attention-decay.md) - Files fade when not mentioned
- [Pool Protocol](../reference/pool-protocol.md) - Technical specification
