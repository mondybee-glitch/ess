---
name: backend-reliability-recovery
description: Backend resilience, timeout/retry budgets, circuit breakers, graceful degradation, backups, restore drills, rollback, and recovery objectives.
version: 0.7.2
---

# Backend Reliability Recovery

## Use when
A change affects availability, retries, circuit breakers, queue recovery, fault isolation, backup/restore, failover, rollback, or disaster recovery.

## Do not use when
The work is purely editorial and does not change operational behavior or recovery claims.

## Required inputs
Dependency graph; critical paths; error budgets; retry/deadline policy; persistence model; backup/restore design; RTO/RPO; failure ownership; and safe test environment.

## Workflow
1. Identify failure modes using a short pre-mortem: dependency outage, slow response, partial write, duplicate request, resource exhaustion, corrupted data, and failed rollback.
2. Propagate end-to-end deadlines. Use bounded retries only for classified transient errors and idempotent operations; add jitter, retry budgets, and cancellation to avoid retry storms.
3. Add circuit breaking/bulkheads/backpressure only with explicit open/half-open behavior, capacity limits, recovery signals, and user-visible degraded behavior.
4. Inject one fault at a time in isolation: timeout, connection reset, queue backlog, dependency 5xx, process restart, and stale/corrupt derived data. Assert invariants and side effects.
5. Separate backups from proven recovery. Restore or rebuild into an isolated target, reconcile integrity, measure elapsed recovery, and compare to explicit RTO/RPO. Keep the original source untouched.
6. For release rollback, test code and data compatibility in both directions. If a migration is irreversible, define forward-recovery and stop conditions instead of claiming simple rollback.
7. Make incident signals, owners, runbook, decision triggers, and communication paths operationally specific.

## Pass/fail checks
Retries and timeouts are bounded; critical invariants survive faults; degraded behavior is safe and visible; restore/rollback evidence matches the claim; RTO/RPO are measured or explicitly unknown.

## Hand-offs
Coordinate with database-engineering for restore integrity, backend-observability for failure signals, backend-production-readiness for deployment gates, and async-jobs-messaging for replay/backlog handling.

## Evidence to report
Fault-injection matrix, deadlines/retry settings, failure traces, state reconciliation, restore/rollback results, RTO/RPO measurement, and recovery gaps.
