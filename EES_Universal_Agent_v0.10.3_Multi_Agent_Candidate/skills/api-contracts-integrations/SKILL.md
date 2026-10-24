---
name: api-contracts-integrations
description: "Canonical EES specialist for API contracts & integrations; merges 2 compatible source capabilities while preserving their original IDs as aliases."
---

# API contracts & integrations — Canonical Engineering Skill

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

Canonical ID: `api-contracts-integrations`  
Source capability aliases: `api-design-contracts`, `api-integrations`.

The original source documents are retained under `../../docs/skill-source-archive/` for traceability. The sections below preserve source-specific procedures; resolve overlaps by the stricter safety invariant and record material conflicts rather than silently discarding them.



---

## Preserved specialist module: `api-design-contracts`

Source capability: `api-design-contracts`.

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

---

## Preserved specialist module: `api-integrations`

Source capability: `api-integrations`.

# api-integrations

## Use when

Use when the main deliverable involves API contracts, events, queues, webhooks, compatibility, retries, idempotency, and integration observability.

## Do not use when

Do not load this skill for local function changes with no external or cross-service boundary.

## Required inputs

Require schemas, owners, versions, compatibility window, auth, timeout, retry, dedupe, ordering, replay, rollout.

## Workflow

define contract; implement validation and idempotency; test old/new clients, duplicates, delays, malformed payloads, and partial failure; instrument and roll out

## Pass/fail checks

old/new combinations and failure cases behave as declared; observability detects violations; rollback or forward-fix exists

Required commands or procedures: run schema/contract, integration, replay, duplicate, timeout, auth, and consumer-driven tests

## Hand-offs

Coordinate with backend, payments, data, security, cloud, and system-design. Assign one owner per acceptance criterion and stop when a dependency or authorization is missing.

## Evidence to report

Preserve schema versions, request/response fixtures, traces, dashboards, and rollout decision. Report exact versions, commands, expected/actual results, and what remains Unverified.

## Release references

- [Source archive index](../../docs/skill-source-archive/README.md)


## Domain-specific cognitive depth (v0.9.2)

### API contracts: blind-spot traps
- **Likely false confidence:** A successful HTTP status does not prove semantic success or durable side effects.
- **Adversarial case to simulate:** Retries after timeout can duplicate a write if the server committed before the response was lost.

### Hard invariants
- Schema compatibility, auth scope, idempotency, and error semantics must be tested independently.
- Never report a property as verified without a reproducible check or authoritative evidence.
- State trade-offs explicitly: correctness vs. latency, safety vs. convenience, and complexity vs. operability; choose based on the task's declared constraints rather than maximizing one dimension blindly.

### Required specialist self-check
Before implementation, write one domain-specific counterexample that would falsify the proposed design. Convert the invariant above into a test or reviewable evidence item. After implementation, test the counterexample and report the exact command/result; if it cannot be tested, mark it **UNVERIFIED**.
