---
name: database-engineering
description: "Canonical EES specialist for Databases & migrations; merges 1 compatible source capabilities while preserving their original IDs as aliases."
---

# Databases & migrations — Canonical Engineering Skill

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

Canonical ID: `database-engineering`  
Source capability aliases: `database-engineering`.

The original source documents are retained under `../../docs/skill-source-archive/` for traceability. The sections below preserve source-specific procedures; resolve overlaps by the stricter safety invariant and record material conflicts rather than silently discarding them.



---

## Preserved specialist module: `database-engineering`

Source capability: `database-engineering`.

# Database Engineering

## Use when
Changing relational or document schemas, indexes, transactions, migrations, backfills, tenant isolation, backup/restore procedures, or data integrity checks.

## Do not use when
The request only changes presentation and does not affect persistence, data contracts, query cost, or database operations.

## Required inputs
Database engine/version; schema and migration history; approximate row sizes and cardinalities; traffic and locking constraints; consistency requirements; backup and recovery objectives; sample data policy; and acceptance criteria.

## Workflow
1. Inspect the live source schema, migration conventions, indexes, query plans, and data ownership. Confirm the target environment and never infer that a local database is safe to modify.
2. Establish invariants: uniqueness, referential integrity, nullability, tenant scope, monetary precision, timestamp semantics, and acceptable data loss (normally none).
3. Review migration locking and table-rewrite behavior for the actual engine/version. Prefer expand-migrate-contract changes for large or shared tables; backfill in bounded, resumable batches.
4. Define transaction boundaries and idempotent retry behavior. Avoid assuming a sequence of statements is atomic unless the engine and transaction context guarantee it.
5. Test against representative data, including empty, existing, duplicate, malformed, and high-cardinality cases. Record duration, locks, row counts, constraints, and query plans.
6. Treat backup completion and successful restore as separate claims. Rehearse restore or rebuild in isolation, reconcile row counts/checksums, and measure recovery time before claiming recoverability.
7. Write an explicit rollback or forward-recovery plan, including compatibility of application versions with both old and new schema states.

## Pass/fail checks
Migrations are repeatable or safely guarded; data invariants reconcile; application/schema rollout order is safe; query changes are measured; restore evidence exists for recovery claims; destructive changes require scoped authorization.

## Hand-offs
Coordinate with api-design-contracts for persisted public contracts, backend-reliability-recovery for restore drills, backend-performance for query baselines, and backend-production-readiness for production migration gates.

## Evidence to report
Schema and migration diff, engine/version, representative dataset description, commands and exit codes, row/constraint reconciliation, query-plan or timing evidence, restore result, and recovery limitations.

## Release references

- [Source archive index](../../docs/skill-source-archive/README.md)


## Domain-specific cognitive depth (v0.9.2)

### Database engineering: blind-spot traps
- **Likely false confidence:** Application-level checks do not replace database constraints under concurrency.
- **Adversarial case to simulate:** Migration success on an empty database says little about a large live dataset.

### Hard invariants
- Preserve referential integrity; migration is reversible or has a documented forward-recovery plan.
- Never report a property as verified without a reproducible check or authoritative evidence.
- State trade-offs explicitly: correctness vs. latency, safety vs. convenience, and complexity vs. operability; choose based on the task's declared constraints rather than maximizing one dimension blindly.

### Required specialist self-check
Before implementation, write one domain-specific counterexample that would falsify the proposed design. Convert the invariant above into a test or reviewable evidence item. After implementation, test the counterexample and report the exact command/result; if it cannot be tested, mark it **UNVERIFIED**.
