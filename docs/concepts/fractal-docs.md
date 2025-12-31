# Fractal Documentation - Infinite Zoom Strategy

**Concept:** Documentation structured like a fractal - summary at every level, detail expands on demand.

---

## The Problem This Solves

**Scenario:** You have a large, complex codebase. Traditional documentation faces a dilemma:

**Option 1: Detailed from the start**
```markdown
# Authentication System

Our authentication uses JWT tokens with RS256 signing. The JwtTokenService
class (auth/services/token.py:45) implements token generation using the
pyjwt library (v2.8.0). Tokens include claims for user_id, role, and
expiration (configurable via JWT_EXPIRY_SECONDS in config.py). The
RefreshTokenHandler (auth/handlers/refresh.py:23) manages refresh tokens...

[continues for 50 pages]
```

**Problem:** Too much detail overwhelms newcomers. Token limit exhausted on single topic.

**Option 2: High-level only**
```markdown
# Authentication System

Handles user authentication and session management.
```

**Problem:** Not enough detail to actually work with the system.

---

## The Fractal Solution

**Every level has a complete summary.** Detail expands on demand.

### Level 0: Project Root
```markdown
# My Project

Modern web app with auth, payments, and real-time chat.

**Core systems:**
- [Authentication](./auth/) - JWT-based auth
- [Payments](./payments/) - Stripe integration
- [Chat](./chat/) - WebSocket real-time messaging
```

### Level 1: System Overview
```markdown
# Authentication

> **Role:** User authentication and session management
> **Tech:** JWT tokens (RS256), Redis sessions
> **Entry Point:** `auth/services/token.py:JwtTokenService`

**Quick health:** `curl /api/auth/health`

## Components
- [Token Service](./token.md) - JWT generation/validation
- [Refresh Handler](./refresh.md) - Token refresh logic
- [Session Store](./session.md) - Redis session management

---
<!-- WARM CONTEXT ENDS ABOVE THIS LINE -->

[Full architectural details below...]
```

### Level 2: Component Detail
```markdown
# JWT Token Service

> **Purpose:** Generate and validate JWT tokens
> **File:** `auth/services/token.py:45-234`
> **Dependencies:** pyjwt, cryptography

**Quick start:**
```python
from auth.services import JwtTokenService

service = JwtTokenService()
token = service.generate(user_id=123, role="admin")
```

## Key Methods
- `generate(user_id, role)` - Create new token
- `validate(token)` - Verify token signature
- `refresh(refresh_token)` - Issue new access token

---
<!-- WARM CONTEXT ENDS ABOVE THIS LINE -->

[Implementation details below...]
```

### Level 3: Implementation Details
```markdown
# Token Generation Implementation

Full implementation details of JWT token generation...

[All the details]
```

---

## Why This Works with Attention-Based Context

### WARM Tier Shows Structure

When a file is **WARM** (headers only), you see:
```markdown
# Authentication

> **Role:** User authentication and session management
> **Tech:** JWT tokens (RS256), Redis sessions

## Components
- Token Service
- Refresh Handler
- Session Store

... [WARM: Content truncated, mention to expand] ...
```

**Value:** You know the authentication system exists, what it does, and what components it has.

**Token cost:** ~500 chars (vs 50KB for full details)

### HOT Tier Shows Full Detail

Mention "token service" and it becomes **HOT** (full content):
```markdown
━━━ [🔥 HOT] auth/token.md (score: 1.00) ━━━
# JWT Token Service

> **Purpose:** Generate and validate JWT tokens
> **File:** `auth/services/token.py:45-234`

[Full implementation, code examples, edge cases...]
```

**Value:** Everything you need to work with token service.

**Token cost:** ~5KB (full content)

---

## The Fractal Pattern

```
Project
├─ System A (WARM: role, components)
│  ├─ Component A1 (WARM: purpose, interface)
│  │  └─ Implementation (HOT: full code, examples)
│  └─ Component A2 (COLD: not mentioned)
└─ System B (HOT: full architecture)
   └─ Component B1 (WARM: co-activated from B)
```

**At any moment:**
- 2-4 files **HOT** (what you're working on)
- 6-8 files **WARM** (related systems, background awareness)
- Remaining **COLD** (irrelevant right now)

**Result:** You always see the structure, details expand where needed.

---

## Structured Header Format

**Every documentation file follows this pattern:**

```markdown
# [Title]

> **Role:** One-line description
> **Host/Location:** Where this lives
> **Key Dependencies:** What it needs

## Quick Health
[One-liner health checks]

## Topology/Components/Interface
[Connection diagram or component list]

## Key Entry Points
[Main functions/classes/files]

---
<!-- WARM CONTEXT ENDS ABOVE THIS LINE -->

## Full Documentation

[Everything below this line appears only when HOT]
```

**Why this structure?**

**First 25 lines = Header:**
- Designed to fit in WARM tier
- Answers: What is this? Where is it? How do I check it?
- Shows relationships (topology, components)
- Enough to decide if you need full content

**After marker = Details:**
- Implementation specifics
- Code examples
- Edge cases
- Historical context
- Only loaded when HOT

---

## Metadata for Navigation

**Every file also has metadata:**

```markdown
---
parent: path/to/parent.md
children: [child1.md, child2.md]
depth: 2
keywords: [keyword1, keyword2, ...]
---
```

**Enables:**
- **Zoom out:** "What's the parent system?"
- **Zoom in:** "What are the child components?"
- **Lateral:** "What are sibling systems?"
- **Discovery:** Keywords trigger attention

---

## Real Example: MirrorBot

**Level 0 (Project):**
```
systems/      - Hardware nodes (Legion, Orin, ASUS, Pi5)
modules/      - Software systems (pipeline, intelligence, T³)
integrations/ - Cross-system communication
```

**Level 1 (System):**
```
systems/orin.md - Jetson Orin node
  > Role: Layer 0 sensory cortex
  > Hardware: Hailo-8 NPU
  > Critical Path: YES (blocking)

  Components:
  - Sentiment analysis
  - Typing detection
  - Uncertainty scoring
```

**Level 2 (Component):**
```
When WARM: See "sentiment analysis" listed
When HOT:  See full sentiment algorithm, model details, edge cases
```

**Attention routing:**
- Mention "orin" → systems/orin.md becomes HOT
- Mention "sentiment" → orin.md stays HOT, sentiment component expands
- Don't mention for 10 turns → decays to WARM (still see structure)
- Don't mention for 20 turns → decays to COLD (evicted)

---

## Why "Fractal"?

**Fractal = self-similar at every scale**

```
Zoom level 1: "We have an auth system"
Zoom level 2: "Auth has token service, session store, refresh handler"
Zoom level 3: "Token service uses JWT with RS256 signing"
Zoom level 4: "JWT generation uses pyjwt library, here's the code..."
```

**At every level:**
- Complete summary
- Pointers to next level
- Consistent structure

**Just like fractals:**
- Coastline looks similar from plane, car, or on foot
- Documentation looks similar at project, system, or component level

---

## Benefits for Large Codebases

### 1. No Information Overload

**Traditional docs:**
- Load everything → Token limit exceeded
- Load nothing → No context
- Load some → Guessing which parts

**Fractal + attention:**
- Load what you're working on (HOT)
- See structure of related systems (WARM)
- Evict irrelevant details (COLD)
- Expand on demand (mention keywords)

### 2. Persistent Navigation

**Conversation example:**

```
Turn 1: "How does auth work?"
  → auth.md HOT (full details)
  → auth components WARM (can see token service, refresh handler)

Turn 5: "What about token refresh?"
  → auth.md still WARM (context maintained!)
  → refresh.md now HOT (zoomed into component)

Turn 10: "Back to the full auth system"
  → auth.md HOT again (zoom out)
  → Can see how refresh fits in bigger picture
```

**Navigation preserved across conversation.**

### 3. Onboarding at Any Level

**New developer:**
- Start at level 0: "We have auth, payments, chat"
- Zoom into auth: "JWT tokens, session management"
- Zoom into tokens: "Here's the implementation"

**Experienced developer:**
- Jump straight to "token refresh implementation"
- Still see headers for related systems (context)
- Can zoom out to architecture when needed

### 4. Token Budget Optimization

**64-95% savings:**

**Without fractal:**
```
Load auth.md (50KB) + payments.md (40KB) + chat.md (60KB) = 150KB
→ Exceeds token limit
```

**With fractal:**
```
HOT: auth.md (50KB)
WARM: payments.md header (1KB), chat.md header (1KB)
Total: 52KB (65% savings)
```

**And you still see:**
- Full auth details (HOT)
- That payments and chat exist (WARM headers)
- Can expand either by mentioning them

---

## Common Questions

### "How do I decide what goes in headers vs details?"

**Headers should answer:**
- What is this?
- Where is it?
- How does it connect to other systems?
- How do I check if it's working?

**Details should answer:**
- How does it work internally?
- What are the edge cases?
- What's the implementation history?
- What are code examples?

**Rule of thumb:** If a newcomer needs it to understand system position → header. If they need it to modify code → details.

### "How deep should the hierarchy go?"

**Depends on complexity:**

**Simple project (< 10K lines):**
```
depth 0: Project
depth 1: Systems (2-3 levels total)
```

**Medium project (10K-100K lines):**
```
depth 0: Project
depth 1: Systems
depth 2: Components (3-4 levels total)
```

**Large project (100K+ lines):**
```
depth 0: Project
depth 1: Systems
depth 2: Subsystems
depth 3: Components
depth 4: Implementation details (4-5 levels total)
```

**MirrorBot (1M+ lines):** 4-5 levels deep in some areas.

### "What if headers get too long?"

**Keep first 25 lines focused:**

**Too much in header:**
```markdown
# Auth System

We use JWT tokens with RS256 signing implemented via the pyjwt
library version 2.8.0 which we chose because of its security track
record and performance characteristics. The tokens include claims
for user_id, role, and expiration which defaults to 3600 seconds
but can be configured via JWT_EXPIRY_SECONDS in the config.py file
located at config/app/config.py line 145...

[Exceeds 25 lines before getting to structure]
```

**Better header:**
```markdown
# Auth System

> **Role:** User authentication and session management
> **Tech:** JWT tokens (RS256), Redis sessions
> **Entry:** `auth/services/token.py:JwtTokenService`

## Components
- [Token Service](./token.md) - JWT generation/validation
- [Refresh Handler](./refresh.md) - Token refresh logic
- [Session Store](./session.md) - Redis persistence

## Quick Health
```bash
curl /api/auth/health
```

---
<!-- WARM CONTEXT ENDS ABOVE THIS LINE -->

## Full Architecture

[Now explain implementation choices, version history, etc.]
```

**Keep headers scannable. Details go below the marker.**

---

## Implementation Tips

### 1. Start with Headers

**Write top-level headers first:**
- What systems exist?
- How do they connect?
- What's their role?

**Then fill in details over time:**
- As people ask questions
- As edge cases emerge
- As implementation evolves

### 2. Use Consistent Structure

**Every file:**
```markdown
# Title
> Metadata fields
## Topology/Components
## Quick Health/Interface
---
<!-- WARM CONTEXT ENDS -->
## Full Details
```

**Why:** Claude's attention router expects this pattern. Consistent structure = better WARM tier extraction.

### 3. Link Parent/Children

**In each file's metadata:**
```markdown
---
parent: ../index.md
children: [component-a.md, component-b.md]
---
```

**Enables:** Navigation queries like "zoom out" or "what are the sub-components?"

### 4. Co-Activation Graph

**Tell the router which files relate:**

```python
# In context-router-v2.py
CO_ACTIVATION = {
    "systems/auth.md": [
        "systems/database.md",  # Auth uses DB
        "systems/api.md",       # Auth protects API
    ]
}
```

**Result:** Mention auth → database and api headers become WARM automatically.

---

## Summary

**Fractal documentation = information at every zoom level**

**Benefits:**
- ✅ No information overload (headers < 25 lines)
- ✅ Full details on demand (mention keywords)
- ✅ Persistent navigation (WARM tier shows structure)
- ✅ Token budget optimization (64-95% savings)
- ✅ Works at any codebase scale

**Pattern:**
- Level 0: Project overview
- Level 1-N: Systems → Components → Details
- Every level: Complete summary in first 25 lines
- Attention routing: HOT (full), WARM (headers), COLD (evicted)

**Think of it as:**
- **Zoom out:** See the forest (project structure)
- **Zoom in:** See the trees (component details)
- **Always in focus:** What you're working on (HOT)
- **Peripheral vision:** Related systems (WARM)

---

**For your project:**
1. Create `.claude/` structure (systems/, modules/, integrations/)
2. Write headers for each system (first 25 lines)
3. Add `---\n<!-- WARM CONTEXT ENDS -->\n---` marker
4. Fill in details below marker over time
5. Update keywords in context-router-v2.py
6. Let attention routing handle the rest

**Next:** [Context Tiers](./context-tiers.md) - How HOT/WARM/COLD works

**See also:**
- [Attention Decay](./attention-decay.md) - Files fade when not mentioned
- [Getting Started](../guides/getting-started.md) - Set up your project
- [CUSTOMIZATION.md](../../CUSTOMIZATION.md) - Keyword mapping
