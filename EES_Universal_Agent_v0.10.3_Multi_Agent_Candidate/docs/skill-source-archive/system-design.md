---
name: system-design
description: Specialist workflow for system architecture, distributed systems, boundaries, data flows, and ADRs. Use when the task materially involves this boundary.
version: 0.6.0
---

# system-design

## Use when

Use when the main deliverable involves system architecture, distributed systems, boundaries, data flows, and ADRs.

## Do not use when

Do not load this skill for single-file fixes with no architectural impact.

## Required inputs

Require requirements, constraints, NFRs, traffic, data, failure domains, ownership.

## Workflow

map context and containers; define contracts; choose a reversible design; model failure and capacity; write ADR; validate with a thin vertical slice

## Pass/fail checks

all NFRs have measurable budgets; every boundary has owner, contract, failure mode, and rollback

Required commands or procedures: run architecture checks, contract tests, dependency graph checks, and capacity assumptions; use ADRs and diagrams

## Hand-offs

Coordinate with frontend, backend, data, security, devops, and documentation owners. Assign one owner per acceptance criterion and stop when a dependency or authorization is missing.

## Evidence to report

Preserve requirements map, ADR, diagrams, contracts, risks, commands, and review decision. Report exact versions, commands, expected/actual results, and what remains Unverified.

## AI blind-spot traps
1. **Premature service decomposition:** microservices can multiply failure modes and operational cost before independent scaling or ownership exists. Start with the simplest reversible boundary.
2. **Average-load sizing:** averages hide burst concurrency, queue growth, tail latency, and downstream saturation. Model peak and failure load, not only mean traffic.
3. **Unstated consistency:** designs say “eventually consistent” without defining lag bounds, read-your-writes, duplicate events, or reconciliation. Specify observable semantics.
4. **Retry amplification:** retries at multiple layers multiply load. Assign one retry owner per boundary, cap attempts, add jitter, and enforce a total deadline.
5. **No degraded mode:** architecture diagrams omit dependency loss, stale data, backpressure, and recovery ownership. Model partial outage explicitly.

## Hard invariants
- Every critical path has an owner, contract, SLO/latency budget, capacity assumption, failure mode, and recovery procedure.
- End-to-end deadlines must be budgeted across hops; child timeouts are strictly less than remaining parent deadline.
- Queue stability requires sustained arrival rate below sustainable service rate; if utilization approaches 1, queue delay rises sharply. Load shedding/backpressure is required when bounded queues fill.
- Every cross-service write/event defines idempotency, ordering expectations, replay behavior, and reconciliation.
- Architecture decisions name trade-offs and a migration/rollback path; no “exactly once” claim without defining its scope and mechanism.

## Decision matrix
| Constraint | Default decision | Escalate when |
|---|---|---|
| One team, one release cadence, moderate load | Modular monolith with explicit boundaries | Independent scaling, isolation, or ownership is proven necessary |
| External dependency timeout | Deadline propagation, bounded retry with jitter, circuit/bulkhead as appropriate | Retry budget or degraded behavior is undefined |
| Event-driven consistency | Explicit event schema, idempotent consumer, DLQ/replay and reconciliation | Ordering or duplicate semantics are unspecified |
| Capacity estimate | Peak RPS × resource cost, concurrency, burst and dependency limits | No measured baseline or workload distribution |
| Risky migration | Expand/contract, dual-read/write only with reconciliation, rollback/forward-fix plan | Irreversible schema or data transformation lacks restore test |

## Adversarial kill-switch
Reject if any critical dependency has no timeout or failure behavior, retries can multiply without a budget, queue growth is unbounded, data consistency is hand-waved, or rollback has no owner and tested steps.

