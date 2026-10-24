---
name: async-jobs-messaging
description: "Canonical EES specialist for Async jobs & messaging; merges 1 compatible source capabilities while preserving their original IDs as aliases."
---

# Async jobs & messaging — Canonical Engineering Skill

## Hyper-Cognitive Engineering Kernel

Use this protocol for substantive implementation, architecture, debugging, and review tasks. Do not confuse procedural discipline with proof of correctness.

### 1. Inversion and trap hunting
Before choosing an implementation, enumerate the three most plausible production failures. Consider concurrency, partial failure, retries, state loss, malicious inputs, resource exhaustion, and unsafe trust boundaries as applicable. Identify which failure is most severe and how it will be detected.

### 2. Two-stage routing and invariants
Treat this canonical skill as the primary route when its scope matches. Select no more than two complementary guard skills unless evidence shows a real cross-domain dependency. Extract measurable invariants from the relevant specialist modules below and convert them into acceptance criteria before editing.

### 3. Zero-code dry run
For medium-or-higher risk, sketch the input → transformation → persistence → output path; simulate duplicate/concurrent requests and one partial outage; define a rollback or containment path. If rollback is not feasible, state the recovery strategy before implementation.

### 4. Principal-grade execution
Prefer explicit types/contracts, bounded retries, timeouts, cancellation, idempotency, least privilege, and redacted telemetry where applicable. Avoid toy implementations and unresolved TODOs. Do not invent numeric thresholds: use source-backed limits, derive them transparently, or mark them as tunable assumptions.

### 5. Adversarial self-trial and evidence gate
Assume at least one hidden defect remains. Review failure paths, boundaries, and regressions against `checks/catalog.json` and the relevant module constraints. Report VERIFIED only when a reproducible command actually ran against the current file state and its output supports the claim. Otherwise report NOT RUN, PARTIAL, or UNVERIFIED.

## Canonical scope and alias map

Canonical ID: `async-jobs-messaging`  
Source capability aliases: `async-jobs-messaging`.

The original source documents are retained under `../../docs/skill-source-archive/` for traceability. The sections below preserve source-specific procedures; resolve overlaps by the stricter safety invariant and record material conflicts rather than silently discarding them.



---

## Preserved specialist module: `async-jobs-messaging`

Source capability: `async-jobs-messaging`.

# Async Jobs Messaging

## Use when
Changing queues, background jobs, scheduled work, event delivery, retry policies, message schemas, or asynchronous workflows.

## Do not use when
The work is synchronous and no asynchronous boundary, event delivery, or delayed side effect is involved.

## Required inputs
Broker and version; delivery semantics; message schema; ordering and partitioning guarantees; idempotency key; retry/dead-letter policy; timeout and cancellation rules; and side-effect boundaries.

## Workflow
1. Declare the delivery model: at-most-once, at-least-once, or effectively-once under a defined idempotency boundary. Never assume a broker guarantees end-to-end exactly-once side effects.
2. Define message identity, schema compatibility, correlation ID, tenant, creation time, expiry, and poison-message behavior. Validate messages before applying side effects.
3. Make consumers idempotent using a durable dedupe/inbox record or domain-safe idempotency mechanism. Test simultaneous duplicate delivery, not just sequential replay.
4. Set bounded retries with classification of transient versus permanent errors, exponential backoff with jitter, attempt/deadline budget, and a dead-letter route containing safe diagnostics.
5. Handle ordering only where the domain needs it. Define partition key, sequence behavior, late/out-of-order events, replay, and how downstream state catches up.
6. For database-plus-message changes, evaluate transactional outbox/inbox or an explicitly documented consistency boundary. Test crash points between persistence, publish, acknowledge, and side effect.
7. Define replay authorization and dedupe retention. A replay must not create duplicate payments, notifications, exports, or irreversible actions.

## Pass/fail checks
Duplicate and concurrent delivery are safe; retry budget is bounded; poison messages become observable; ordering guarantees are explicit; crash points and replay are tested; secrets/PII are excluded from message logs.

## Hand-offs
Coordinate with database-engineering for transactional storage, backend-observability for trace propagation, backend-reliability-recovery for backlog/replay recovery, and api-design-contracts for event schemas.

## Evidence to report
Delivery semantics, message schema, retry/dead-letter configuration, duplicate/concurrency tests, crash-point results, queue lag evidence, replay policy, and unresolved consistency risks.

## Release references

- [Source archive index](../../docs/skill-source-archive/README.md)


## Domain-specific cognitive depth (v0.9.2)

### Async jobs: blind-spot traps
- **Likely false confidence:** Queue acceptance is not job completion; delivery is commonly at-least-once.
- **Adversarial case to simulate:** Poison messages and retry storms can starve healthy work.

### Hard invariants
- Handlers are idempotent; retries are bounded; dead-letter and visibility-timeout behavior is explicit.
- Never report a property as verified without a reproducible check or authoritative evidence.
- State trade-offs explicitly: correctness vs. latency, safety vs. convenience, and complexity vs. operability; choose based on the task's declared constraints rather than maximizing one dimension blindly.

### Required specialist self-check
Before implementation, write one domain-specific counterexample that would falsify the proposed design. Convert the invariant above into a test or reviewable evidence item. After implementation, test the counterexample and report the exact command/result; if it cannot be tested, mark it **UNVERIFIED**.
