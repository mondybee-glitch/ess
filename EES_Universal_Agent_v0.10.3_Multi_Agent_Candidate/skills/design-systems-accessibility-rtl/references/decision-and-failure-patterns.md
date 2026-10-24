# Decision & Failure Patterns — Design systems, accessibility, and RTL

## Scope
This reference is the production-failure companion for the `design-systems-accessibility-rtl` skill. Apply it during planning, implementation, code review, incident response, and release approval. These are testable engineering controls, not guarantees.

## High-cost blind spots
- **Trap 1:** Color alone communicates status.
- **Trap 2:** Focus indicator removed without replacement.
- **Trap 3:** RTL layout mirrors icons whose meaning should not flip.
- **Trap 4:** Contrast checked only on default background.

## Hard invariants
- Text contrast >= 4.5:1 for normal text and >= 3:1 for large text under WCAG AA.
- Interactive controls are keyboard operable with visible focus.
- Test both RTL/LTR, zoom, narrow viewport, and reduced motion.

## Failure-mode matrix

| Failure mode | Detection signal | Required response |
|---|---|---|
| Partial dependency outage | Elevated timeout/error rate with otherwise healthy process | Bound retries, preserve deadlines, expose degraded state; do not amplify load |
| Concurrent duplicate request | Duplicate event, row, message, or external action | Apply idempotency key or transactional uniqueness; test simultaneous callers |
| Stale or conflicting state | Version mismatch, stale UI response, divergent replica | Use version/ETag/sequence checks; reject stale writes and reconcile explicitly |
| Resource exhaustion | Queue growth, memory slope, event-loop lag, connection pool saturation | Apply backpressure and hard bounds; shed optional work before core work |
| Invalid or hostile input | Schema failure, unexpected source/origin, policy mismatch | Validate at the trust boundary; fail closed for authorization and integrity |
| Rollback after partial deployment | Mixed schema/app versions or partially migrated data | Keep expand/contract compatibility; rehearse rollback with new writes present |
| Observability leak | Secret/PII appears in traces, logs, exception or test artifacts | Redact before emission; add automated canary tests and restrict artifact access |

## Required decision protocol
1. Name the authoritative data source, trust boundary, state owner, and external side effects.
2. Write the failure cases before selecting the implementation. Include timeout, cancellation, duplicate delivery, stale state, partial commit, and rollback.
3. Prefer established platform primitives over custom coordination or security mechanisms.
4. Add a negative test for each high-impact failure. Include concurrency where two operations can overlap.
5. Verify the observable behavior at the actual boundary (browser, API, database, queue, or provider); do not accept a code-only claim.
6. Record assumptions, evidence, residual risk, and the exact command/environment used to validate.

## Release gate
Block release if an invariant is untested, security-sensitive fallback fails open, rollback is destructive, or the evidence does not match the claimed runtime environment. If requirements conflict or the architecture owner is unclear, stop and report the ambiguity instead of guessing.
