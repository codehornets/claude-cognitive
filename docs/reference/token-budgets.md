# Token Budget Optimization

> **Status:** Coming soon based on beta feedback

This reference will provide strategies for optimizing token usage with claude-cognitive.

## Placeholder Topics

We plan to cover:
- Token budget calculation (chars → tokens)
- Decay rate tuning for different project types
- Co-activation graph optimization
- WARM header sizing strategies
- Budget allocation (HOT vs WARM ratio)
- Measuring token savings
- Debugging token explosions
- Per-project optimization strategies

## Current Defaults

**Hard ceiling:** 25,000 characters (~6.25K tokens)

**Typical savings:**
- Cold start: 79% (120K → 25K chars)
- Warm context: 70% (80K → 24K chars)
- Focused work: 75% (60K → 15K chars)

## Help Shape This Guide

**What's YOUR token usage scenario?**

- Running into budget ceiling?
- Want more aggressive savings?
- Need to balance HOT/WARM differently?
- Custom token limits?

**Share your data:** [GitHub Discussions](https://github.com/GMaN1911/claude-cognitive/discussions)

Real usage patterns will shape optimization strategies.

---

**For now, see:**
- [Context Tiers](../concepts/context-tiers.md) - How budget is enforced
- [Attention Decay](../concepts/attention-decay.md) - Tuning decay rates
