# Community Launch Posts

## Reddit - r/ClaudeAI

**Title:** [Tool Release] claude-cognitive: Working memory for Claude Code (64-95% token savings)

**Post:**

```markdown
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
```

---

## Discord - Claude Developers Server

**Channel:** #show-and-tell or #tools

**Post:**

```markdown
🧠 **claude-cognitive** - Working memory for Claude Code

Built this because I was running 8 concurrent Claude instances on a 1M+ line codebase and the context rediscovery was brutal.

**What it does:**
- Attention-based context injection (HOT/WARM/COLD files)
- Multi-instance coordination (no duplicate work)
- 64-95% token savings

**Validated on production:**
- 1M+ lines, 4-node architecture, 80K+ interactions
- 8 concurrent instances, multi-day sessions

**15-minute setup, MIT licensed**

GitHub: https://github.com/GMaN1911/claude-cognitive

Looking for beta testers - especially if you have large codebases or run multiple instances. Feedback welcome! 🙏
```

---

## Twitter/X Thread

**Tweet 1:**
```
I built working memory for Claude Code.

Problem: Every new instance rediscovers your codebase from scratch, burning tokens and missing context.

Solution: claude-cognitive - attention-based context + multi-instance coordination.

Results: 64-95% token savings on 1M+ line production codebase.

🧵
```

**Tweet 2:**
```
How it works:

Context Router:
• Files activate when mentioned
• Co-activation for related files
• Attention decay when not used
• HOT/WARM/COLD tiers (25K char budget)

Pool Coordinator:
• Auto-detects completions/blockers
• Shares state across instances
• Works with persistent sessions
```

**Tweet 3:**
```
Validated on production:
• 1M+ line codebase (3,200+ Python modules)
• 4-node distributed architecture
• 8 concurrent Claude Code instances
• 80K+ real interactions
• Multi-day persistent sessions

Token savings:
• Cold start: 79%
• Warm context: 70%
• Focused work: 75%
```

**Tweet 4:**
```
15-minute setup, MIT licensed.

Looking for beta testers - especially if you:
• Work with large codebases (50k+ lines)
• Run multiple Claude Code instances
• Keep sessions open for days/weeks

Feedback shapes the docs.

GitHub: https://github.com/GMaN1911/claude-cognitive
```

---

## Hacker News - Show HN

**Title:** Show HN: claude-cognitive – Working memory for Claude Code (MIT)

**Post:**

```markdown
I've been using Claude Code on a 1M+ line distributed codebase (MirrorBot/CVMP - consciousness modeling system) with 8 concurrent instances. The context rediscovery problem was severe:

- Every new instance rediscovers architecture from scratch
- Hallucinated integrations that don't exist
- Repeated debugging across instances
- Massive token burn re-reading unchanged files

**claude-cognitive** solves this with two systems:

1. **Context Router (v2.0)**: Attention-based file injection
   - Keyword activation (mention a file → becomes HOT)
   - Co-activation (related files boost together)
   - Attention decay (unused files fade to COLD)
   - Token budget enforcement (25K char ceiling)

2. **Pool Coordinator (v2.0)**: Multi-instance state sharing
   - Automatic mode: Detects completions/blockers from conversation
   - Manual mode: Explicit coordination blocks
   - Designed for persistent sessions (days/weeks, not just short bursts)

**Results on production:**
- Cold start: 79% token savings (120K → 25K chars)
- Warm context: 70% (80K → 24K chars)
- Focused work: 75% (60K → 15K chars)
- New instances productive immediately
- Zero duplicate work across instances

**Validation:**
- 1+ million line codebase (3,200+ Python modules)
- 4-node distributed architecture
- 8 concurrent Claude Code instances
- 80,000+ real interactions processed

**Setup:** 15 minutes, hooks-based integration
**License:** MIT (use it however you want)

This is v1.0.0 - works in production, but I'm looking for beta feedback on:
- Setup experience (is SETUP.md clear?)
- Token savings in different workflows
- What docs would help most

The code is deliberately simple (5 Python scripts, no dependencies) because reliability > features when you're managing context for an AI that's editing your production code.

GitHub: https://github.com/GMaN1911/claude-cognitive

Built on experience with MirrorBot/CVMP. Funded with instructions: "use it for love."
```

---

## Tips for Community Posts

**Do:**
- ✅ Lead with the problem (context rediscovery pain)
- ✅ Show concrete results (79% token savings)
- ✅ Include production validation (1M+ lines, 80K+ interactions)
- ✅ Make installation sound easy (15 minutes)
- ✅ Ask for specific feedback (not just "thoughts?")
- ✅ Respond quickly to questions (builds trust)

**Don't:**
- ❌ Over-promise ("revolutionize your workflow!")
- ❌ Technical jargon without explanation
- ❌ Wall of text (use formatting, bullets)
- ❌ Ignore questions/feedback
- ❌ Defensive responses to criticism

**Engagement strategy:**
1. Post during high-traffic times (9am-12pm PST)
2. Respond to EVERY comment in first 2 hours
3. Update post if common questions emerge
4. Cross-link discussions to GitHub
5. Thank people who try it

**Success metrics:**
- 10+ GitHub stars in first 24 hours = good traction
- 3-5 genuine users trying it = beta success
- 1-2 testimonials in first week = validation
- Active GitHub Discussions = community forming

---

## After Posting

**Monitor:**
- GitHub Issues (bugs, questions)
- GitHub Discussions (feedback, success stories)
- Reddit comments
- Discord replies
- Twitter mentions

**Respond to:**
1. Bug reports (within 2 hours if possible)
2. Setup questions (guide them to SETUP.md, fix if unclear)
3. Feature requests (acknowledge, add to GitHub Issues)
4. Success stories (ask for testimonial, thank them!)

**Update README if:**
- Multiple people ask the same question (add FAQ)
- Installation instructions unclear (fix immediately)
- Common use case not covered (add example)

---

**Remember:** You're not selling, you're sharing a tool that helped you. Authentic problem → solution → validation is compelling.
