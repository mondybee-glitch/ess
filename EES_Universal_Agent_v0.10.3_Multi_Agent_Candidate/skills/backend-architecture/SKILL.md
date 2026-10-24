---
name: backend-architecture
description: "Canonical EES specialist for Backend architecture; merges 3 compatible source capabilities while preserving their original IDs as aliases."
---

# Backend architecture — Canonical Engineering Skill

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

Canonical ID: `backend-architecture`  
Source capability aliases: `backend-development`, `fullstack-platform-boundaries`, `system-design`.

The original source documents are retained under `../../docs/skill-source-archive/` for traceability. The sections below preserve source-specific procedures; resolve overlaps by the stricter safety invariant and record material conflicts rather than silently discarding them.



---

## Preserved specialist module: `backend-development`

Source capability: `backend-development`.

# Backend Development

## Use when
- Adding or changing endpoints, schemas, migrations, jobs
- Auth, permissions, multi-tenant data access
- Performance of queries and background work

## Do not use when
- Static copy or styling changes

## Required inputs
- API contract and its owner
- Database engine and version
- Auth model and roles
- Data volume and traffic estimates

## Workflow
1. Map the contract: schema owner, versions, consumers.
2. Keep authorization server-side and resource-level; validate input at the boundary.
3. Use parameterized queries only.
4. Write migrations as expand then contract; avoid long locks on large tables.
5. Make retried writes idempotent (idempotency key or natural key).
6. Set timeouts; log structured events without personal data.
7. Test authorization negatives, duplicates, and partial failures.

## Pass/fail checks
- Another user's resource returns 403 or 404 (test exists)
- Query count per request stable (no N+1)
- `EXPLAIN` shows an index for each new filter or join column
- Migration is reversible or has a forward-fix plan
- Pagination and rate limits on list endpoints

## Hand-offs
- security-review for High changes
- devops-and-deployment for rollout
- software-testing for contract tests

## Evidence to report
Commands run with results, files changed, and anything not verified. Use the status vocabulary from the core [SKILL.md](../../docs/skill-source-archive/backend-development.md).

## Concrete commands

Run the repository test command; for Python use `pytest -q`, inspect queries with `EXPLAIN (ANALYZE, BUFFERS)`, and run the migration tool in a disposable database before approval.

---

## Preserved specialist module: `fullstack-platform-boundaries`

Source capability: `fullstack-platform-boundaries`.

# Fullstack Platform Boundaries

## Use when
A feature spans UI and server, public/private API boundaries, client configuration, SSR, authentication, background services, or deployment environments.

## Do not use when
The change is isolated to a component or service and the existing boundary contracts are clear and unaffected.

## Required inputs
Application architecture; runtime boundaries; data flow; identity model; configuration sources; network/service dependencies; error contract; and relevant deployment constraints.

## Workflow
1. Draw a simple trust/data-flow inventory in prose or tables: browser, server, API, database, worker, third-party service, and secret/config source. Treat client input as untrusted.
2. Assign ownership of validation, authorization, business rules, data fetching, caching, errors, and retries. The server remains authoritative for secrets and protected data.
3. Validate API contracts at both ends when appropriate. Version environment variables, define required/optional values, fail fast on missing configuration, and prevent server secrets from entering bundles or HTML.
4. Review SSR/client boundaries, hydration, caching, tenant isolation, CSRF/CORS, serialization, and error leakage based on the actual framework and deployment mode.
5. Test success, denial, timeout, malformed response, empty state, stale cache, and dependency failure end-to-end without relying only on UI visibility.
6. Ensure accessible error/loading states and useful correlation IDs across client and server. Redact private internals from user-facing messages.
7. Document deployment-specific assumptions and avoid adding cross-boundary abstractions until a concrete need is demonstrated.

## Pass/fail checks
Boundary ownership is explicit; secrets stay server-side; authorization is server-enforced; contracts and configuration are validated; errors are consistent; failure paths are tested across the relevant layers.

## Hand-offs
Coordinate with api-design-contracts for external contracts, backend-auth-authorization for policy, ui-design-system-accessibility for user interaction, and devops-and-deployment for environment configuration.

## Evidence to report
Boundary/data-flow summary, configuration schema, relevant integration tests, bundle/secret checks, error-state screenshots/logs, deployment assumptions, and remaining risks.

---

## Preserved specialist module: `system-design`

Source capability: `system-design`.

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

## Release references

- [Source archive index](../../docs/skill-source-archive/README.md)


## Domain-specific cognitive depth (v0.9.2)

### Backend architecture: blind-spot traps
- **Likely false confidence:** A clean module diagram does not prove runtime boundaries or transaction correctness.
- **Adversarial case to simulate:** Shared database access can silently bypass service ownership and invariants.

### Hard invariants
- One authoritative owner per invariant; external side effects use explicit boundaries and compensation.
- Never report a property as verified without a reproducible check or authoritative evidence.
- State trade-offs explicitly: correctness vs. latency, safety vs. convenience, and complexity vs. operability; choose based on the task's declared constraints rather than maximizing one dimension blindly.

### Required specialist self-check
Before implementation, write one domain-specific counterexample that would falsify the proposed design. Convert the invariant above into a test or reviewable evidence item. After implementation, test the counterexample and report the exact command/result; if it cannot be tested, mark it **UNVERIFIED**.
