---
name: api-security-testing
description: Authorized, scoped API security testing covering authentication, object/property/function authorization, validation, abuse controls, and data exposure.
version: 0.7.2
---

# Api Security Testing

## Use when
Reviewing an API for broken access control, injection, validation gaps, excessive data exposure, mass assignment, rate-limit weaknesses, or unsafe error behavior.

## Do not use when
No authorization for the target exists, the target boundaries are unclear, or the task requests credential theft, persistence, destructive testing, or bypass of licensing/access controls.

## Required inputs
Written target authorization; in-scope hosts and endpoints; excluded systems; test window and rate limits; test accounts/data; stop conditions; and rules for sensitive findings.

## Workflow
1. Confirm scope before sending traffic. Use only designated test accounts and non-production data unless an explicit written authorization says otherwise.
2. Inventory API routes, methods, object IDs, roles, tenant boundaries, input types, upload paths, and state-changing actions. Build tests from trust boundaries rather than a scanner-only checklist.
3. Probe authentication and authorization with paired identities: same role/different owner, different tenant, lower-privilege role, expired token, and unauthenticated call. Verify read and write paths separately.
4. Test input boundaries using benign, bounded payloads; assess schema validation, mass assignment, injection handling, file limits, rate limits, and response differences that reveal account existence.
5. For every finding, preserve minimal reproducible evidence, the exact request conditions, response, side-effect proof, severity rationale, and safe remediation. Redact tokens and personal data.
6. Stop at the first unexpected destructive or out-of-scope effect, service instability, rate-limit breach, or sensitive-data exposure. Do not escalate beyond the approved scope.
7. Re-test fixes with the same conditions and a negative control. A clean scan does not establish complete security.

## Pass/fail checks
Scope and authorization are recorded; test rate and impact remain bounded; sensitive content is redacted; findings are reproducible; remediation is verified with direct evidence; unsupported security claims are excluded.

## Hand-offs
Coordinate with backend-auth-authorization for policy remediation, backend-integration-testing for regression tests, and defensive-automation-and-audit for allowlisted test execution and logging.

## Evidence to report
Authorization scope, test window, endpoints covered, tools/versions, safe request/response excerpts, reproducible findings, remediation evidence, stop events, and untested surfaces.
