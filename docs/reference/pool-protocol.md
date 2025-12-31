# Pool Protocol Technical Specification

> **Status:** Coming soon based on beta feedback

This reference will provide the technical specification for the instance pool protocol.

## Placeholder Topics

We plan to document:
- JSONL entry schema (complete specification)
- Relevance scoring algorithm (exact formula)
- TTL enforcement rules
- Deduplication strategy
- Concurrency guarantees
- File format versioning
- Error handling specifications
- Hook integration contract

## Current Implementation

See working code in:
- `~/.claude/scripts/pool-loader.py`
- `~/.claude/scripts/pool-extractor.py`
- `~/.claude/scripts/pool-query.py`

## Help Shape This Spec

**What technical details do you need?**

- Writing custom pool tools?
- Integrating with other systems?
- Need formal schema validation?
- Want protocol extensions?

**Discuss in:** [GitHub Discussions](https://github.com/GMaN1911/claude-cognitive/discussions)

---

**For now, see:**
- [Pool Coordination](../concepts/pool-coordination.md) - Conceptual overview
- Source code in `scripts/` - Implementation
