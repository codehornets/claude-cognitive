# Gemini CLI Integration for claude-cognitive

claude-cognitive now supports **both Claude Code and Gemini CLI**! This guide shows how to use claude-cognitive's attention-based context management with Google's Gemini CLI.

---

## Quick Start (5 minutes)

### 1. Install Gemini CLI

```bash
# Requires Node.js 20+
npm install -g @google/gemini-cli
```

### 2. Generate GEMINI.md

From your project directory (where `.claude/` exists):

```bash
python3 ~/.claude/scripts/generate-gemini-md.py
```

This creates `GEMINI.md` with your current attention state (HOT/WARM files).

### 3. Use Gemini CLI

```bash
gemini "your question about the project"
```

Gemini automatically reads `GEMINI.md` and has full project context!

---

## How It Works

### Attention State → GEMINI.md

claude-cognitive tracks which files are HOT/WARM based on:
- Recent mentions in conversation
- Keyword activation
- Co-activation with related files
- Attention decay over time

The `generate-gemini-md.py` script converts this to `GEMINI.md`:

**🔥 HOT files (score ≥0.8):**
- Full content included
- Actively relevant to current work

**🌡️ WARM files (score 0.25-0.8):**
- First 25 lines included (headers/overview)
- Background awareness

**❄️ COLD files (score <0.25):**
- Not included
- Currently irrelevant

### Auto-Sync

Keep GEMINI.md fresh with automatic updates:

**Option 1: Manual sync after work sessions**
```bash
~/.claude/scripts/sync-gemini-context.sh
```

**Option 2: Cron job (every 5 minutes)**
```bash
# Add to crontab:
*/5 * * * * cd /path/to/your/project && ~/.claude/scripts/sync-gemini-context.sh > /dev/null 2>&1
```

**Option 3: Git pre-commit hook**
```bash
# .git/hooks/pre-commit
#!/bin/bash
python3 ~/.claude/scripts/generate-gemini-md.py
git add GEMINI.md
```

---

## Comparison: Claude Code vs Gemini CLI

| Feature | Claude Code | Gemini CLI | claude-cognitive Solution |
|---------|-------------|------------|--------------------------|
| **Context Injection** | Automatic (hooks) | Static (GEMINI.md) | Generate GEMINI.md from attention state |
| **Token Efficiency** | 64-95% savings | Depends on GEMINI.md | Same 64-95% if synced frequently |
| **Multi-Instance** | Pool coordination | Shared GEMINI.md | Both work (pool files shareable) |
| **Update Frequency** | Every turn | On GEMINI.md regeneration | Manual/cron sync |
| **Setup Complexity** | Hooks config | Just generate file | Simple script |

---

## Example Workflow

### Scenario: Working on Authentication System

**1. Start work with Claude Code:**
```bash
claude
# "I need to refactor the authentication module"
```

Claude Code's hooks inject relevant context automatically. Attention state updates:
```json
{
  "modules/auth.md": 1.0,
  "integrations/oauth.md": 0.65,
  "systems/database.md": 0.45
}
```

**2. Switch to Gemini CLI:**
```bash
# Generate fresh GEMINI.md from attention state
python3 ~/.claude/scripts/generate-gemini-md.py

# Now use Gemini with same context
gemini "Review the authentication module for security issues"
```

Gemini reads GEMINI.md and sees:
- 🔥 **modules/auth.md** (full content)
- 🌡️ **integrations/oauth.md** (headers)
- 🌡️ **systems/database.md** (headers)

**3. Continue work, context stays synchronized:**
```bash
# After more work, attention state changes
# modules/session-mgmt.md becomes HOT

# Regenerate GEMINI.md
~/.claude/scripts/sync-gemini-context.sh

# Gemini now has updated context
gemini "Implement session timeout logic"
```

---

## Advanced: Custom GEMINI.md Templates

You can customize the generator to match your workflow:

```python
# Edit ~/.claude/scripts/generate-gemini-md.py

# Change thresholds
hot_threshold = 0.9  # More selective
warm_threshold = 0.3  # More inclusive

# Change max lines for WARM files
file_content = read_file_content(file_path, max_lines=50)  # Show more context

# Add project-specific sections
content.append("## Custom Section\n\n")
content.append("Your custom content here\n\n")
```

---

## Troubleshooting

**Q: Gemini doesn't seem to use GEMINI.md**
```bash
# Check if file exists
ls -lh GEMINI.md

# Check if it has content
head -50 GEMINI.md

# Try explicit prompt
gemini "Based on the GEMINI.md file, what is this project about?"
```

**Q: GEMINI.md is too large**
```bash
# Reduce max_lines for WARM files
# Edit generate-gemini-md.py line 46:
file_content = read_file_content(file_path, max_lines=15)  # Instead of 25

# Or increase thresholds to include fewer files
hot_threshold = 0.9
warm_threshold = 0.4
```

**Q: How do I know what's in my attention state?**
```bash
# Check current state
python3 ~/.claude/scripts/context-router-v2.py --status

# Or view the raw state file
cat .claude/attn_state.json | python3 -m json.tool
```

---

## Roadmap: Gemini Integration

**v1.2 (Current):**
- ✅ GEMINI.md generator
- ✅ Auto-sync script
- ✅ Documentation

**v1.3 (Planned):**
- [ ] MCP server for dynamic context injection
  - Gemini calls `@context get_files "authentication"`
  - Returns relevant files based on attention state
  - No GEMINI.md regeneration needed

- [ ] Gemini extension for automatic updates
  - Regenerates GEMINI.md on session start
  - Shows attention state in Gemini UI

- [ ] Unified pool coordination
  - Both Claude Code and Gemini CLI share pool state
  - Cross-tool coordination (what you did in Claude, Gemini knows)

**v2.0 (Future):**
- [ ] Universal AI assistant adapter
  - Support for Cursor, Copilot, Aider
  - One context system, all tools

---

## Contributing

Ideas for improving Gemini integration? Open an issue or PR!

**Especially interested in:**
- MCP server implementation
- Gemini extension development
- Better auto-sync strategies
- Cross-tool coordination patterns

---

## Links

- **Main repo:** https://github.com/GMaN1911/claude-cognitive
- **Gemini CLI docs:** https://geminicli.com/docs/
- **MCP Protocol:** https://modelcontextprotocol.io/

---

**Questions?** Open an [issue](https://github.com/GMaN1911/claude-cognitive/issues) or [discussion](https://github.com/GMaN1911/claude-cognitive/discussions)
