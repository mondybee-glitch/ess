---
name: backend-production-readiness
description: "Canonical EES specialist for Backend production readiness; merges 2 compatible source capabilities while preserving their original IDs as aliases."
---

# Backend production readiness — Canonical Engineering Skill

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

Canonical ID: `backend-production-readiness`  
Source capability aliases: `backend-production-readiness`, `backend-reliability-recovery`.

The original source documents are retained under `../../docs/skill-source-archive/` for traceability. The sections below preserve source-specific procedures; resolve overlaps by the stricter safety invariant and record material conflicts rather than silently discarding them.



---

## Preserved specialist module: `backend-production-readiness`

Source capability: `backend-production-readiness`.

# Backend Production Readiness

## Use when
Preparing a service or backend change for release, deployment, production migration, launch, operational handoff, or readiness review.

## Do not use when
The task is a local prototype with no deployment intent, unless the user explicitly requests a production-readiness assessment.

## Required inputs
Release scope and owner; build artifact/version; test evidence; deployment strategy; data/schema changes; monitoring and SLOs; security/privacy review; rollback or forward-fix plan; and approval boundaries.

## Workflow
1. Freeze the change scope and establish source revision, build identity, environment, feature flags, dependencies, and acceptance criteria. Do not substitute branch name for immutable revision.
2. Collect test results for unit, integration, contract, migration, security, performance, and smoke checks that apply to the change. Record not-run checks explicitly and block if a required check lacks evidence.
3. Review data migrations, backward compatibility, feature-flag defaults, secrets/configuration, permissions, external side effects, and deployment ordering.
4. Confirm dashboards, alerts, runbook, service owner, on-call route, SLO/SLI, and known failure modes. A running process without actionable telemetry is not operational readiness.
5. Define rollout stages and objective stop/rollback triggers. Rehearse rollback or forward recovery where impact warrants it; account for irreversible data changes and old/new version compatibility.
6. Verify artifact provenance and expected runtime/configuration. Run post-deploy smoke checks against a scoped environment and compare actual results to acceptance criteria.
7. Produce a Go/No-Go/Partial decision with missing requirements, approval record scope/expiry, and the exact next safe action. Do not use a weighted score to override a hard blocker.

## Pass/fail checks
Required checks have direct evidence; owner and runbook exist; data and security implications are reviewed; monitoring can detect key failure modes; rollback/recovery is credible; approvals are scoped; no unresolved critical blocker remains.

## Hand-offs
Coordinate with backend-reliability-recovery for recovery testing, backend-observability for telemetry, api-design-contracts for compatibility, and release owner for the final decision.

## Evidence to report
Release revision/artifact, check matrix with exit codes, migration plan, approval record, dashboards/runbook, rollback test, smoke-test results, blockers, and decision rationale.

---

## Preserved specialist module: `backend-reliability-recovery`

Source capability: `backend-reliability-recovery`.

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

## Release references

- [Source archive index](../../docs/skill-source-archive/README.md)


## Domain-specific cognitive depth (v0.9.2)

### Production readiness: blind-spot traps
- **Likely false confidence:** A green build is not production readiness; rollback, observability, and operator actions matter.
- **Adversarial case to simulate:** Configuration drift and missing secrets often appear only after deployment.

### Hard invariants
- Readiness, liveness, startup, graceful shutdown, rollback, and alert paths are independently verified.
- Never report a property as verified without a reproducible check or authoritative evidence.
- State trade-offs explicitly: correctness vs. latency, safety vs. convenience, and complexity vs. operability; choose based on the task's declared constraints rather than maximizing one dimension blindly.

### Required specialist self-check
Before implementation, write one domain-specific counterexample that would falsify the proposed design. Convert the invariant above into a test or reviewable evidence item. After implementation, test the counterexample and report the exact command/result; if it cannot be tested, mark it **UNVERIFIED**.
