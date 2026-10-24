# Evolution and Routing Guardrails — v0.9.2 candidate

## Continuous evolution: promotion protocol

The current adaptive-agent promotion guidance remains authoritative. A new rule is a candidate, not an active policy, until it passes all of these gates:

1. Capture the original failure, expected behavior, environment, and reproducible regression fixture.
2. Preserve the baseline skill/rule and freeze the baseline evaluation set before changing the candidate.
3. Run candidate and baseline against the same frozen regression suite, plus adversarial tests and a separate holdout set.
4. Do not repeatedly tune against the holdout. If holdout results influence a candidate revision, rotate to a fresh holdout.
5. Reject candidates that cause a critical regression or modify trust, release, authorization, or sandbox policies without independent approval.
6. Record the change, evidence, measured benefit, known limitations, reviewer/owner decision, and rollback target.
7. Promote only through an explicit versioned change; preserve rejected candidates and their reasons.

A model-generated rationale, confidence score, or self-assessment is not evidence. Passing one fixture does not establish general agent effectiveness.

## Hierarchical routing and context caching

The existing hierarchical router is the authoritative route selector. A cache is a performance optimization and must never become a source of policy or authority.

Cache only stable, versioned context such as capability descriptions or routing metadata. Do not cache live task state, approvals, credentials, evidence, or decisions that depend on mutable authorization.

Every cache entry should be keyed by at least the normalized context digest, capability-registry digest, routing-policy version, model identifier, and provider cache mode. Invalidate entries on any relevant version/policy change. Expired, missing, or unsupported cache entries must fall back to uncached routing.

Before enabling a provider-side context cache, benchmark representative tasks and record:

- route selection accuracy against a frozen labeled set;
- p50/p95 routing latency;
- token usage and measured cost;
- cache hit rate and invalidation correctness;
- behavior when cache creation, lookup, or expiry fails.

Provider features differ by model and may change. Capability detection must be explicit and versioned; do not assume that all Gemini models support the same explicit or implicit caching behavior. Do not report a latency or cost improvement until measured in the target environment.

## Current implementation boundary

This candidate adds signed evidence verification and a constrained Docker launch wrapper. It does not yet connect signed evidence to `task_runtime.py` state transitions, automatically promote learned rules, or implement Gemini provider-side context caching. Those are separate integration tasks and remain open rather than being represented as complete.
