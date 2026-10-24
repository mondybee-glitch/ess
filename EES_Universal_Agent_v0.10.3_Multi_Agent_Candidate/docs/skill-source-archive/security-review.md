---
name: security-review
description: Review application code and architecture for security weaknesses, prioritized findings, practical fixes, and verification.
version: 0.6.0
---

# Security Review

## Use when
Use for source/config/API review, threat modeling, auth/session/access-control checks, dependency exposure, and remediation validation.

## Do not use when
Do not route a purely visual change here unless it affects sensitive behavior, data, or trust boundaries.

## Required inputs
Repository/configuration, deployment context if relevant, assets and trust boundaries, expected behavior, and any known constraints.

## Workflow
1. Map assets, identities, trust boundaries, entry points, sensitive data, and dependencies.
2. Separate authentication (who) from authorization (what an identity may do).
3. Trace untrusted input to sensitive sinks: SQL, shell, HTML, file paths, deserializers, outbound requests, and logs.
4. Check object-level access on every read/write, session rotation/expiry, CSRF model, upload/parser limits, secrets, error disclosure, and dependency advisories.
5. Run available tools only in the relevant repository: `npm audit --omit=dev`, `pip-audit`, `bandit -r .`, `semgrep --config auto .`, `gitleaks detect --source .`. Confirm scope and installation first.
6. Tie each finding to code/config evidence and a realistic precondition. Distinguish confirmed vulnerabilities from hypotheses.
7. Add regression tests for fixes, rerun relevant checks, and inspect the final diff.

## Pass/fail checks
- Findings include evidence/location, preconditions, impact, remediation, and verification.
- Access control is tested server-side, including object-level boundaries.
- Scan results are reported only when actually executed.
- Secrets are redacted from reports.
- Fixes have regression tests or an explicit reason why not.

## Hand-offs
Hand off to `backend-development` or `frontend-development` for fixes; `software-testing` for independent regression coverage; `defensive-security-ops` for telemetry and incident response.

## Evidence to report
Use `ID | severity | component/location | evidence | preconditions | impact | remediation | verification`. Rank by impact and exploitability; avoid unsupported severity precision.

## Concrete commands

Run the project lint/tests plus authorized SAST, dependency, secret, and negative authorization checks; distinguish confirmed findings from hypotheses and redact evidence.
