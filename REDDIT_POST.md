# Reddit r/ClaudeAI - Ready to Post

**Title:** [Tool Release] claude-cognitive: Working memory for Claude Code (64-95% token savings)

**Post:**

---

I've been running Claude Code on a 1M+ line codebase with 8 concurrent instances, and the context rediscovery was killing me. Every new instance would:
- Rediscover the architecture from scratch
- Hallucinate integrations that don't exist
- Repeat debugging I'd already tried
- Burn tokens re-reading unchanged files

So I built **claude-cognitive** - working memory for Claude Code.

## What it does

**Context Router:** Attention-based file injection with HOT/WARM/COLD tiers
- Files activate when you mention them
- Related files co-activate automatically
- Unused files decay to save tokens
- 25K character budget enforced

**Pool Coordinator:** Multi-instance state sharing
- Automatic mode: Detects completions/blockers from conversation
- Manual mode: Explicit coordination blocks
- Works with persistent sessions (days/weeks)

## Results

**Token Savings:**
- Cold start: 79% (120K → 25K chars)
- Warm context: 70% (80K → 24K chars)
- Focused work: 75% (60K → 15K chars)

**Average: 64-95% depending on codebase size**

**Developer Experience:**
- ✅ New instances productive in first message
- ✅ Zero hallucinated imports
- ✅ No duplicate work across concurrent instances
- ✅ Persistent memory across days-long sessions

## Validated on

- 1+ million line production codebase (3,200+ Python modules)
- 4-node distributed architecture
- 8 concurrent Claude Code instances
- 80,000+ real interactions

## Installation

**Takes 15 minutes:**

```bash
# Clone
cd ~
git clone https://github.com/GMaN1911/claude-cognitive.git .claude-cognitive

# Install scripts
cp -r .claude-cognitive/scripts ~/.claude/scripts/

# Set up hooks
cat .claude-cognitive/hooks-config.json >> ~/.claude/settings.json

# Set instance ID
export CLAUDE_INSTANCE=A

# Done - restart Claude Code
```

Full guide: https://github.com/GMaN1911/claude-cognitive/blob/main/SETUP.md

## License

MIT - use it however you want.

## Looking for beta testers

This is v1.0.0 - it works for me, but I'd love feedback on:
- Setup experience
- Token savings in your workflow
- What docs would help most

If you try it, drop your experience in the comments or GitHub Discussions!

---

**GitHub:** https://github.com/GMaN1911/claude-cognitive

Built on production experience with MirrorBot/CVMP. Funded with instructions: "use it for love" ❤️

---

**COPY THE TEXT ABOVE AND POST TO:**
https://www.reddit.com/r/ClaudeAI/submit

**Tips:**
- Use the title exactly (includes [Tool Release] tag)
- Paste the full post
- Monitor for 2 hours after posting
- Respond to EVERY comment quickly
- Be helpful, not defensive
