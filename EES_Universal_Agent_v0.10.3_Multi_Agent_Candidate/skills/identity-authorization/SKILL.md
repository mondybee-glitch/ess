---
name: identity-authorization
description: "Canonical EES specialist for Identity & authorization; merges 1 compatible source capabilities while preserving their original IDs as aliases."
---

# Identity & authorization — Canonical Engineering Skill

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

Canonical ID: `identity-authorization`  
Source capability aliases: `backend-auth-authorization`.

The original source documents are retained under `../../docs/skill-source-archive/` for traceability. The sections below preserve source-specific procedures; resolve overlaps by the stricter safety invariant and record material conflicts rather than silently discarding them.



---

## Preserved specialist module: `backend-auth-authorization`

Source capability: `backend-auth-authorization`.

# Backend Auth Authorization

## Use when
Designing or changing identity, sessions, tokens, roles, permissions, object ownership, tenant boundaries, service identities, or secret rotation.

## Do not use when
The task is merely cosmetic or changes a UI affordance without changing the server-side access policy; hiding a button is never an authorization control.

## Required inputs
Threat model; identity provider and token/session model; actors, resources, actions, tenant model, service accounts, revocation needs, and explicit positive/negative acceptance criteria.

## Workflow
1. Create an access matrix of actor × action × resource × tenant and identify trusted identity claims. Treat user-supplied owner or tenant IDs as untrusted until checked server-side.
2. Separate authentication (who is calling) from authorization (what they may do). Apply deny-by-default policy on every server entry point, background job, and administrative path.
3. Enforce object-level checks after loading the authoritative resource or through a query constrained by identity. Avoid “check one endpoint, trust all related endpoints” assumptions.
4. Check privilege escalation, role inheritance, default roles, account recovery, expired/revoked credentials, session fixation, token audience/issuer/expiry, CSRF where applicable, and service-to-service identity.
5. Test a permission matrix with allowed, denied, cross-user, cross-tenant, anonymous, stale-token, and concurrent changes. Assert response and side-effect state, not only status codes.
6. Keep secrets out of logs and fixtures. For rotation, define overlap, revocation, failure handling, and rollback without printing secret values.
7. Record policy decisions and owners; request approval for production identity or access-control changes.

## Pass/fail checks
Every protected operation has a server-side authorization check; tenant boundaries are tested; denied operations make no unauthorized side effect; secrets are not exposed; recovery and revocation paths are defined.

## Hand-offs
Coordinate with api-design-contracts for authorization errors, api-security-testing for adversarial tests, and backend-observability for safe audit events.

## Evidence to report
Access matrix, threat assumptions, denied-path test results, side-effect assertions, token/session configuration checks, redaction results, and approval scope.

## Release references

- [Source archive index](../../docs/skill-source-archive/README.md)


## Domain-specific cognitive depth (v0.9.2)

### Identity and authorization: blind-spot traps
- **Likely false confidence:** A valid token can be expired, mis-scoped, revoked, or valid for a different audience.
- **Adversarial case to simulate:** Confused-deputy and privilege-escalation paths hide in role inheritance.

### Hard invariants
- Validate issuer, audience, expiry, scope, and object-level policy; fail closed.
- Never report a property as verified without a reproducible check or authoritative evidence.
- State trade-offs explicitly: correctness vs. latency, safety vs. convenience, and complexity vs. operability; choose based on the task's declared constraints rather than maximizing one dimension blindly.

### Required specialist self-check
Before implementation, write one domain-specific counterexample that would falsify the proposed design. Convert the invariant above into a test or reviewable evidence item. After implementation, test the counterexample and report the exact command/result; if it cannot be tested, mark it **UNVERIFIED**.


## Specialized module: Applied Cryptography & Key Management
For encryption design, key lifecycle, envelope encryption, nonce safety, password hashing, signed telemetry, and PQC migration readiness, consult `modules/applied-cryptography-key-management/MODULE.md`. Do not replace this module with improvised cryptographic code.
