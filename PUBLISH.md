# Publishing claude-cognitive to GitHub

## 1. Create GitHub Repository

1. Go to https://github.com/new
2. **Repository name:** `claude-cognitive`
3. **Description:** `Working memory for Claude Code - persistent context and multi-instance coordination`
4. **Visibility:** ✅ Public
5. **Initialize:** ❌ Do NOT add README, .gitignore, or license (we already have them)
6. Click "Create repository"

## 2. Push to GitHub

GitHub will show you commands. Use these instead (we already have a commit):

```bash
cd /home/garret-sutherland/claude-cognitive-package

# Add GitHub as remote (replace GMaN1911)
git remote add origin git@github.com:GMaN1911/claude-cognitive.git

# Or if using HTTPS:
git remote add origin https://github.com/GMaN1911/claude-cognitive.git

# Push to GitHub
git branch -M main  # Rename master → main
git push -u origin main
```

## 3. Configure Repository

On GitHub repository page:

**Settings → General:**
- Website: `https://mirrorethic.com` (or leave blank)
- Topics: `claude-code`, `claude-ai`, `context-management`, `ai-tools`, `developer-tools`

**Settings → Features:**
- ✅ Issues (for bug reports)
- ✅ Discussions (for community questions)
- ❌ Wiki (not needed yet)
- ❌ Projects (not needed yet)

**Create Discussion Categories:**
1. Go to Discussions tab
2. Enable Discussions
3. Create categories:
   - **Beta Feedback** (for early users)
   - **Show & Tell** (for success stories)
   - **Q&A** (for questions)

## 4. Add Topics/Tags

In repository main page, click ⚙️ next to "About" and add:
- `claude-code`
- `claude-ai`
- `context-management`
- `token-optimization`
- `developer-tools`
- `productivity`

## 5. Pin Important Issues/Discussions

Create a pinned discussion:
- Title: "Welcome Beta Testers! 🎉"
- Content: See BETA_WELCOME.md

## Done!

Your repo is now live at: `https://github.com/GMaN1911/claude-cognitive`

Next steps:
1. Test installation on a fresh machine
2. Post to communities (see COMMUNITY_POSTS.md)
3. Monitor GitHub Discussions for feedback
