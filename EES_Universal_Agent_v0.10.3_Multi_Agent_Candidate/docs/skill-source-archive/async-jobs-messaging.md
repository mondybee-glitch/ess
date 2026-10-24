---
name: async-jobs-messaging
description: Asynchronous job, queue, event, scheduler, retry, ordering, idempotency, outbox, and dead-letter engineering.
version: 0.7.2
---

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
