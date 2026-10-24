---
name: database-engineering
description: Database schema, query, transaction, migration, backup/restore, data backfill, and tenancy-boundary engineering.
version: 0.7.2
---

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
