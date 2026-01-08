# Customizing claude-cognitive for Your Project

The context router loads keywords from a project-local config file, making it easy to customize for any codebase.

---

## Quick Start (Skip Customization)

**The scripts will work immediately with minimal setup:**
- They'll detect file mentions from your actual messages
- Co-activation will happen based on file proximity in `.claude/` structure
- Token savings will still be 50-70% without customization

**But for 80-95% savings:** Customize keywords to match your domain.

---

## Configuration File

Create `.claude/keywords.json` in your project root:

```json
{
  "keywords": {
    "systems/production.md": [
      "prod", "production", "deploy", "kubernetes", "k8s"
    ],
    "systems/staging.md": [
      "staging", "test env", "qa", "integration tests"
    ],
    "modules/auth.md": [
      "auth", "authentication", "login", "oauth", "jwt", "session"
    ],
    "modules/database.md": [
      "database", "postgres", "sql", "migrations", "schema"
    ],
    "integrations/stripe.md": [
      "stripe", "payment", "billing", "subscription"
    ]
  },
  "co_activation": {
    "modules/auth.md": [
      "modules/api.md",
      "modules/database.md"
    ],
    "integrations/stripe.md": [
      "modules/api.md"
    ]
  },
  "pinned": [
    "systems/network.md"
  ]
}
```

The router checks for config in this order:
1. `.claude/keywords.json` (project-local)
2. `~/.claude/keywords.json` (global fallback)
3. Empty defaults (no activation)

---

## Step-by-Step Customization

### 1. Copy the Template

```bash
cp ~/.claude-cognitive/templates/keywords.json.example .claude/keywords.json
```

### 2. Map Your `.claude/` Structure

First, list what you have:

```bash
ls .claude/systems/
ls .claude/modules/
ls .claude/integrations/
```

**Example output:**
```
systems/production.md
systems/staging.md
modules/auth.md
modules/api.md
modules/database.md
integrations/stripe.md
```

### 3. Identify Keywords for Each File

For each file, ask: **"What words would make me want to see this file?"**

**Example: `modules/auth.md`**
- Direct mentions: "auth", "authentication", "login"
- Related concepts: "oauth", "jwt", "session", "token"
- Technical terms: "passport.js", "bcrypt", "password reset"
- Common questions: "how do users log in", "session management"

### 4. Edit `.claude/keywords.json`

```json
{
  "keywords": {
    "systems/production.md": [
      "prod", "production", "deploy", "kubernetes", "k8s", "live"
    ],
    "systems/staging.md": [
      "staging", "test", "qa", "integration", "pre-prod"
    ],
    "modules/auth.md": [
      "auth", "authentication", "login", "oauth", "jwt", "session",
      "passport", "bcrypt", "password", "reset", "signup", "signin"
    ],
    "modules/api.md": [
      "api", "endpoint", "route", "express", "fastapi", "rest",
      "graphql", "controller", "handler"
    ],
    "modules/database.md": [
      "database", "db", "postgres", "sql", "orm", "sequelize",
      "migration", "schema", "query", "models"
    ],
    "integrations/stripe.md": [
      "stripe", "payment", "billing", "subscription", "checkout",
      "webhook", "invoice", "customer"
    ]
  },
  "co_activation": {
    "modules/auth.md": [
      "modules/api.md",
      "modules/database.md"
    ],
    "integrations/stripe.md": [
      "modules/api.md",
      "modules/webhooks.md"
    ]
  },
  "pinned": ["systems/network.md"]
}
```

### 5. Update Co-Activation Graph

The `co_activation` section defines which files boost each other when one activates:

```json
{
  "co_activation": {
    "modules/auth.md": [
      "modules/api.md",
      "modules/database.md"
    ],
    "integrations/stripe.md": [
      "modules/api.md",
      "modules/webhooks.md"
    ]
  }
}
```

When `auth.md` activates (score = 1.0), `api.md` and `database.md` get a +0.35 boost.

### 6. Configure Pinned Files

Files in the `pinned` array never decay below WARM:

```json
{
  "pinned": [
    "systems/network.md",
    "systems/architecture.md"
  ]
}
```

**Use for:**
- System architecture overview
- Critical topology diagrams
- Shared infrastructure everyone needs

**Don't overuse:** 2-3 files max recommended

---

## Adjusting Decay Rates (Optional)

Decay rates are still configured in the script itself. Edit `~/.claude/scripts/context-router-v2.py`:

```python
DECAY_RATES = {
    "systems/": 0.85,       # Infrastructure is stable
    "modules/": 0.70,       # Code changes frequently
    "integrations/": 0.80,  # APIs semi-stable
    "docs/": 0.75,          # Documentation medium
    "default": 0.70
}
```

**Higher number = slower decay** (file stays relevant longer)

---

## Testing Your Customization

### 1. Check Keyword Activation

Start Claude Code and say:
```
I need to debug the authentication flow
```

Then check if `modules/auth.md` activated:
```bash
tail -20 ~/.claude/context_injection.log
```

Should see:
```
[HOT] modules/auth.md (score: 1.00)
```

### 2. Verify Co-Activation

If you mention auth, related files should warm up:
```
Show me how authentication works
```

Check log:
```
[HOT] modules/auth.md (score: 1.00)
[WARM] modules/api.md (score: 0.35)
[WARM] modules/database.md (score: 0.35)
```

### 3. Test Decay

In subsequent messages without mentioning auth:
```
How does the frontend work?
```

Auth should decay:
```
[WARM] modules/auth.md (score: 0.70)  # 1.0 * 0.70 decay
```

---

## Common Patterns

### Web Application

```json
{
  "keywords": {
    "systems/frontend.md": [
      "frontend", "react", "vue", "ui", "component", "css"
    ],
    "systems/backend.md": [
      "backend", "api", "server", "node", "express", "django"
    ],
    "modules/auth.md": [
      "auth", "login", "jwt", "session"
    ],
    "modules/database.md": [
      "database", "postgres", "sql", "orm"
    ]
  }
}
```

### Microservices

```json
{
  "keywords": {
    "systems/user-service.md": [
      "user service", "users", "accounts", "profiles"
    ],
    "systems/payment-service.md": [
      "payment", "billing", "stripe", "transactions"
    ],
    "integrations/kafka.md": [
      "kafka", "event bus", "messaging", "queue"
    ]
  }
}
```

### Data Pipeline

```json
{
  "keywords": {
    "modules/ingestion.md": [
      "ingestion", "data collection", "sources", "extract"
    ],
    "modules/transformation.md": [
      "transform", "etl", "clean", "normalize"
    ],
    "modules/storage.md": [
      "storage", "s3", "data lake", "warehouse"
    ]
  }
}
```

---

## Tips for Good Keywords

### DO:
- **Include common variations**: "auth", "authentication", "login"
- **Add technical terms**: "jwt", "oauth", "bcrypt"
- **Include error messages**: "401", "unauthorized", "invalid token"
- **Think like your questions**: "how do users log in"

### DON'T:
- Use overly generic words ("the", "system", "code")
- Duplicate keywords across unrelated files
- Add keywords just to have more (quality > quantity)

---

## Validation Script

Check your keyword mapping:

```bash
# From project root
python3 -c "
import json
from pathlib import Path

config_path = Path('.claude/keywords.json')
if config_path.exists():
    config = json.load(open(config_path))
    keywords = config.get('keywords', {})
    co_activation = config.get('co_activation', {})
    pinned = config.get('pinned', [])

    print('Files mapped:', len(keywords))
    print('\nKeywords per file:')
    for file, kws in sorted(keywords.items()):
        print(f'  {file}: {len(kws)} keywords')

    print('\nCo-activations:')
    for file, related in sorted(co_activation.items()):
        print(f'  {file} -> {len(related)} related files')

    print('\nPinned files:', pinned)
else:
    print('No .claude/keywords.json found')
"
```

---

## When to Recustomize

**Recustomize when:**
- Adding new files to `.claude/`
- Files aren't activating when you expect
- Frequently typing the same thing without file activation
- Token usage higher than expected

**Don't customize if:**
- It's working well
- You just set it up (give it time)
- Making it perfect (good enough is fine)

---

## Getting Help

**If keywords aren't working:**
1. Check logs: `tail -f ~/.claude/context_injection.log`
2. Verify file paths match `.claude/` structure
3. Try more specific keywords
4. Post in GitHub Discussions with example

**If co-activation isn't working:**
1. Check `co_activation` in your `keywords.json`
2. Verify file names match exactly
3. Start with direct mentions first

---

## Remember

**Project-local config makes customization easy.**

You'll still get 50-70% token savings without customization. Customization gets you to 80-95%.

Start simple. Iterate based on actual usage. Perfection isn't required.
