---
name: api-design-contracts
description: API, event, webhook, and streaming contract design, compatibility, versioning, and consumer-safe change verification.
version: 0.7.2
---

# Api Design Contracts

## Use when
Designing or changing REST, GraphQL, gRPC, event, webhook, or streaming contracts, including schema evolution, pagination, errors, idempotency, and deprecation.

## Do not use when
The task is purely visual, has no API/event boundary, or asks for an implementation before the owning contract and consumers are understood.

## Required inputs
Current contract/schema; consumer inventory; compatibility policy; auth and tenancy assumptions; payload examples; acceptance criteria; rollout constraints; and test tools.

## Workflow
1. Find the source of truth for the contract and enumerate producers, consumers, versions, generated clients, webhooks, and stored events.
2. Capture a before-state schema and representative valid/invalid payloads. Classify the change as additive, behavior-changing, or breaking; field names alone do not determine compatibility.
3. Define request/response semantics, required versus optional fields, nullability, error codes, pagination, ordering, idempotency scope, retries, and timeout expectations.
4. Compare old and new schemas against existing consumers. Prefer additive rollout: tolerant readers first, producer change second, removal only after usage evidence and an announced deprecation window.
5. Add contract tests for old-client compatibility, invalid inputs, auth failures, duplicate requests/events, and partial downstream failure. Test generated artifacts where they are part of delivery.
6. Document versioning, ownership, migration steps, telemetry, and rollback/forward-fix limits. Do not claim backward compatibility from a successful build alone.

## Pass/fail checks
All supported consumers remain compatible or have an approved migration; schema diff is reviewed; negative paths have stable error contracts; duplicate operations are safe where promised; examples and generated clients agree; evidence is attached.

## Hand-offs
Coordinate with backend-auth-authorization for access semantics, backend-integration-testing for consumer contracts, database-engineering for persisted schema changes, and backend-production-readiness for release planning.

## Evidence to report
Before/after schema diff, consumer matrix, contract test command and exit code, generated-client status, compatibility exceptions, rollout/deprecation plan, and unresolved assumptions.
