# EES Gemini v0.9.1 — Controlled Internal Pilot Approval

**Decision: APPROVED FOR CONTROLLED INTERNAL PILOT ONLY. NOT CERTIFIED FOR PRODUCTION.**

## Authorized scope
Use only by authorized internal testers in an isolated, non-production environment with least-privilege permissions. Do not expose this build to external users, use sensitive production data, or grant unrestricted command/file access. Require human approval for destructive or high-impact actions.

## Evidence
- Structural validator: PASS (32 canonical skills, 74 capability IDs, 222 evaluation contracts, 51 central fixtures, 13 operational fixture projects, zero warnings).
- Routing audit: PASS (zero errors and zero warnings).
- Operational fixtures: existing recorded result 13/13 passed; this does not measure agent effectiveness.
- Focused regression suites: previously recorded focused suites passed.

## Outstanding blockers
The complete pytest suite timed out in the available environment; live Gemini CLI/API integration was not run; human semantic review of all canonical skills and independent security review are outstanding. These gaps prevent production certification.

## Pilot operating controls
1. Use a disposable or isolated test environment.
2. Apply least-privilege credentials and filesystem permissions.
3. Require human confirmation for destructive actions, external sends, deployments, and permission changes.
4. Keep logs and preserve test evidence. Stop the pilot if unexpected access or command execution occurs.
5. Do not represent this internal approval as third-party, regulatory, or production certification.

## Exit criteria for production approval
- Full pytest suite completes successfully in clean CI, including resolution of timeouts.
- Live provider integration tests pass.
- Human review and sign-off for all 32 canonical skills.
- Independent security review and sandbox validation complete.
- Updated evidence report and explicit production decision are recorded.

See `reports/v0.9.1-controlled-pilot-approval.json` for machine-readable evidence and decision scope.
