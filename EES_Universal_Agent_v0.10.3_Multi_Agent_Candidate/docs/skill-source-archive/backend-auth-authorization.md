---
name: backend-auth-authorization
description: Server-side authentication and authorization, roles, object-level access, tenant isolation, credential lifecycle, and session security.
version: 0.7.2
---

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
