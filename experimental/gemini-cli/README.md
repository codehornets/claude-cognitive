# Gemini CLI Integration (Experimental)

⚠️ **Status: Experimental / Proof of Concept**

This directory contains experimental work on integrating claude-cognitive's attention-based context management with Google's Gemini CLI.

## Current Status

**What Works:**
- ✅ `generate-gemini-md.py` - Converts `.claude/` attention state to static `GEMINI.md`
- ✅ Gemini CLI reads GEMINI.md automatically
- ✅ Basic context injection working

**What's Missing (Why It's Experimental):**
- ❌ No dynamic attention updates per-query (static snapshot only)
- ❌ No keyword-triggered activation
- ❌ No attention decay between turns
- ❌ No real-time token budgeting
- ❌ No MCP server for true dynamic context

## The Problem

Claude Code has hooks that let claude-cognitive inject context **dynamically on every turn**. Gemini CLI doesn't have equivalent hooks, so this implementation just generates a **static GEMINI.md file** that doesn't update during conversation.

This means you get a one-time context snapshot, not the adaptive attention system that makes claude-cognitive powerful.

## Future Work

To get true claude-cognitive behavior in Gemini CLI, we'd need to build:

1. **MCP Server** - Model Context Protocol server that:
   - Runs attention router on each Gemini query
   - Returns relevant files based on keywords
   - Updates attention state after each turn
   - Would give Gemini the same dynamic behavior as Claude Code

2. **Gemini Extension** - Native extension that:
   - Hooks into Gemini's query pipeline
   - Regenerates context automatically
   - Shows attention state in UI

## Try It Anyway

If you want to experiment with static context injection:

```bash
# From your project directory
python3 experimental/gemini-cli/generate-gemini-md.py

# Use Gemini CLI (it reads GEMINI.md automatically)
gemini "your question about the project"

# Regenerate when context changes
experimental/gemini-cli/sync-gemini-context.sh
```

See `GEMINI_SETUP.md` for more details.

## Contributing

Interested in building the MCP server or Gemini extension? Open an issue or PR! This would be a great way to make claude-cognitive truly multi-tool.

---

**For production use, stick with Claude Code.** The attention dynamics only work properly there (for now).
