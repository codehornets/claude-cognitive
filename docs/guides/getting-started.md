# Getting Started with claude-cognitive

**Goal:** Working memory for Claude Code in 15 minutes.

---

## Quick Install

### 1. Clone Repository

```bash
cd ~
git clone https://github.com/GMaN1911/claude-cognitive.git .claude-cognitive
```

### 2. Install Scripts

```bash
# Copy scripts to ~/.claude/
cp -r .claude-cognitive/scripts ~/.claude/scripts/

# Set up hooks
cat .claude-cognitive/hooks-config.json >> ~/.claude/settings.json
```

### 3. Set Instance ID

```bash
# Add to ~/.bashrc for persistence:
export CLAUDE_INSTANCE=A

# Or per-terminal:
export CLAUDE_INSTANCE=B
```

### 4. Initialize Your Project

```bash
cd /path/to/your/project

# Create .claude directory
mkdir -p .claude/{systems,modules,integrations,pool}

# Copy templates
cp ~/.claude-cognitive/templates/* .claude/
```

### 5. Customize for Your Project

**Edit `.claude/CLAUDE.md`:**
```markdown
# Your Project Name

> Brief description

## Quick Reference

| Component | Description |
|-----------|-------------|
| ... | ... |
```

**Edit `.claude/systems/*.md`:**
- Create docs for your infrastructure/deployment nodes
- See [templates/systems/](../../templates/systems/) for examples

**Edit `.claude/modules/*.md`:**
- Create docs for your core systems/modules
- See [templates/modules/](../../templates/modules/) for examples

**Customize keywords:**
```bash
# Edit keyword section
nano ~/.claude/scripts/context-router-v2.py

# See full guide:
cat ~/.claude-cognitive/CUSTOMIZATION.md
```

See [CUSTOMIZATION.md](../../CUSTOMIZATION.md) for detailed guidance.

### 6. Verify It's Working

```bash
# Start Claude Code
claude

# First message - check for context injection:
# Should see: "ATTENTION STATE [Turn 1]" with HOT/WARM/COLD counts

# Query pool activity:
python3 ~/.claude/scripts/pool-query.py --since 1h
```

---

## What Just Happened?

### Context Router Installed

**When you type a prompt:**
1. Hook intercepts your message
2. Context router analyzes keywords
3. Relevant docs injected automatically
4. Files fade when not mentioned
5. Token budget enforced (25KB max)

**Result:** You see relevant documentation without asking for it.

### Pool Coordinator Installed

**When you end a session:**
1. If you added a `pool` block, it's extracted
2. Coordination entry written to shared log
3. Other instances see it at their session start

**Result:** No duplicate work across terminals.

---

## Your First Coordinated Session

### Terminal 1 (Instance A)

```bash
export CLAUDE_INSTANCE=A
claude
```

**Work on something:**
```
user: "Fix the authentication bug"

assistant: [works on fix]

assistant: "Fixed! Added mutex locking to prevent race condition.

```pool
INSTANCE: A
ACTION: completed
TOPIC: Auth bug fix
SUMMARY: Fixed race condition in token refresh. Added mutex locking.
AFFECTS: auth.py, session_handler.py
BLOCKS: Session management refactor can proceed
```

All tests passing."
```

End session (Ctrl+D).

### Terminal 2 (Instance B)

```bash
export CLAUDE_INSTANCE=B
claude
```

**Session starts, you see:**
```
## Session Context
- **Instance**: B
- **Pool**: 1 recent (0 own, 1 others)

### Recent Activity
- [A] completed: Auth bug fix
```

**Now Instance B knows what A did!**

---

## Understanding Context Injection

### Example: Ask About Your System

**You type:** "How does the API work?"

**Context router:**
1. Sees keyword "api"
2. Activates `modules/api.md` → HOT (full content)
3. Co-activates related files → WARM (headers only)
4. Injects before your prompt

**Claude sees:**
```
━━━ [🔥 HOT] modules/api.md (score: 1.00) ━━━
[Full API documentation - 10KB]

━━━ [🌡️ WARM] modules/auth.md (score: 0.35) ━━━
[Header only - 500 bytes]
  > APIs use this auth system
  > Quick health: curl /api/health

━━━ [🌡️ WARM] modules/database.md (score: 0.35) ━━━
[Header only - 500 bytes]
  > APIs query this database
  > Connection string: postgres://...

[Your prompt]: "How does the API work?"
```

**Result:** Claude has full API docs + awareness of related systems, all automatically.

---

## Understanding Attention Decay

**Files fade when not mentioned:**

```
Turn 1: "How does the API work?"
  → api.md: HOT (full content)
  → auth.md: WARM (header)

Turn 2: "What database does it use?"
  → database.md: HOT (newly activated)
  → api.md: WARM (decayed from 1.0 → 0.70)
  → auth.md: WARM (still visible)

Turn 5: "Back to the API"
  → api.md: HOT again (1.0)
  → database.md: WARM (decayed)
  → auth.md: COLD (evicted after not mentioned)
```

**Think of it as:**
- Your working memory focuses on current topic
- Related systems stay in background (WARM)
- Irrelevant systems fade away (COLD)
- Mention something → instantly returns

See [Attention Decay](../concepts/attention-decay.md) for details.

---

## Common First-Day Questions

### "I don't see any context injection"

**Check:**
```bash
# 1. Verify hooks configured
jq '.hooks.UserPromptSubmit' ~/.claude/settings.json

# 2. Test router manually
echo '{"prompt": "test"}' | python3 ~/.claude/scripts/context-router-v2.py

# 3. Check docs exist
ls .claude/systems/
ls .claude/modules/

# 4. Restart Claude Code
```

### "Pool not showing other instances' work"

**Check:**
```bash
# 1. Verify CLAUDE_INSTANCE set
echo $CLAUDE_INSTANCE

# 2. Check pool file exists
ls -lh ~/.claude/pool/instance_state.jsonl

# 3. Test manually
python3 ~/.claude/scripts/pool-query.py
```

### "Files aren't activating when I expect"

**Customize keywords:**
```bash
# Edit keyword mappings
nano ~/.claude/scripts/context-router-v2.py

# Find KEYWORDS section (~line 75)
# Add your project-specific terms
```

See [CUSTOMIZATION.md](../../CUSTOMIZATION.md) for guidance.

### "How do I know what's HOT vs WARM?"

Look for the visual header:
```
╔══ ATTENTION STATE [Turn 5] ══╗
║ 🔥 Hot: 2 │ 🌡️ Warm: 6 │ ❄️ Cold: 5 ║
╚══════════════════════════════════════╝
```

Each file shows its tier:
- `[🔥 HOT]` = Full content
- `[🌡️ WARM]` = Header only
- (Not shown) = COLD (evicted)

---

## Next Steps

### Learn the Concepts

1. [Attention Decay](../concepts/attention-decay.md) - Why files fade
2. [Context Tiers](../concepts/context-tiers.md) - HOT/WARM/COLD explained
3. [Pool Coordination](../concepts/pool-coordination.md) - Multi-instance patterns

### Customize for Your Project

1. Read [CUSTOMIZATION.md](../../CUSTOMIZATION.md)
2. Map your systems to `.claude/systems/*.md`
3. Map your modules to `.claude/modules/*.md`
4. Update keywords in `context-router-v2.py`
5. Test with real work

### Advanced Use Cases

1. [Large Codebases](./large-codebases.md) - 50k+ lines strategies
2. [Team Setup](./team-setup.md) - Multiple developers
3. [Migration Guide](./migration.md) - Adding to existing project

---

## Troubleshooting

### Logs to Check

```bash
# Context router errors
cat ~/.claude/context_injection.log

# Pool loader errors
cat ~/.claude/pool/loader_errors.log

# Pool extractor errors
cat ~/.claude/pool/extractor_errors.log
```

### Reset Everything

```bash
# Clear attention state (fresh start)
rm .claude/attn_state.json

# Clear pool (fresh coordination state)
rm ~/.claude/pool/instance_state.jsonl

# Restart Claude Code
```

### Get Help

- **GitHub Issues:** https://github.com/GMaN1911/claude-cognitive/issues
- **Discussions:** https://github.com/GMaN1911/claude-cognitive/discussions
- **Check existing docs:** Everything in `docs/` directory

---

## Summary

**You now have:**
- ✅ Context router with attention dynamics
- ✅ Pool coordinator for multi-instance work
- ✅ Project-local documentation structure
- ✅ Working memory across sessions

**What changes:**
- Claude sees relevant docs automatically
- Files fade when not mentioned (working memory)
- Other instances coordinate via pool
- Token usage drops 64-95%

**What stays the same:**
- Claude Code works normally
- No new commands to learn
- Graceful degradation if hooks fail
- Optional (use pool blocks only when needed)

---

**Ready to dive deeper?** See [Concepts](../concepts/) for how it all works.

**Want to customize?** See [CUSTOMIZATION.md](../../CUSTOMIZATION.md) for keyword mapping.

**Working on large codebase?** See [Large Codebases Guide](./large-codebases.md).
