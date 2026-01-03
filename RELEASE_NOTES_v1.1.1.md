# Release v1.1.1 - Patch Release

**Release Date:** January 2, 2026

## What's Fixed

### Pool Loader Hardcoded Fallback (#2)

Fixed hardcoded "MirrorBot/CVMP" fallback in SessionStart hook that showed misleading project name when no pool activity existed.

**Before:**
```
## Session Context
- **Codebase**: MirrorBot/CVMP  ❌ (wrong project)
- **Instance Pool**: No recent activity
```

**After:**
```
## Session Context
- **Codebase**: your-actual-project  ✅ (correctly detected)
- **Instance Pool**: No recent activity
```

### Technical Details

Added `get_project_name()` function that intelligently detects project name from multiple sources:

1. **Git remote URL** - Extracts repository name from origin remote
2. **Git repo root** - Uses git repository directory name
3. **Current directory** - Falls back to working directory name
4. **Generic fallback** - "Current Project" if all detection fails

This ensures users see their actual project name instead of confusing development artifacts.

## Installation

### New Users

```bash
cd ~
git clone https://github.com/GMaN1911/claude-cognitive.git .claude-cognitive
cp -r .claude-cognitive/scripts ~/.claude/scripts/
cat .claude-cognitive/hooks-config.json >> ~/.claude/settings.json
```

### Existing Users (Upgrade)

```bash
cd ~/.claude-cognitive
git pull origin main
cp -r scripts/* ~/.claude/scripts/
```

No configuration changes required - the fix is automatic.

## Credits

- **Fixed by:** Garret Sutherland
- **Reported by:** @sbozh (thank you! 🙏)
- **Issue:** #2

## Full Changelog

See [CHANGELOG.md](./CHANGELOG.md) for complete version history.

## Links

- **GitHub:** https://github.com/GMaN1911/claude-cognitive
- **Documentation:** https://github.com/GMaN1911/claude-cognitive#readme
- **Issues:** https://github.com/GMaN1911/claude-cognitive/issues
- **Discussions:** https://github.com/GMaN1911/claude-cognitive/discussions

---

**Questions?** Open an [issue](https://github.com/GMaN1911/claude-cognitive/issues) or [discussion](https://github.com/GMaN1911/claude-cognitive/discussions)

**Updates?** Watch the [repo](https://github.com/GMaN1911/claude-cognitive) for releases
