# EES Gemini v0.9.2 — Release Gates and Evidence

Status: **engineering completion candidate; not production-approved**.

## Completed in this candidate (repository-level evidence)
- Added a heuristic cryptography source-pattern scanner and a dedicated operational fixture.
- Added WCAG relative-luminance contrast checker.
- Added unit tests for both guard scripts in `project/tests/`.
- Added specialist modules for payment-ledger engineering and embedded/IoT systems under the existing specialist route.
- Expanded the 32 `decision-and-failure-patterns.md` reference files.
- Updated the sandbox Dockerfile to use Node.js 22 with Python and Playwright installation steps.

## Required before GA
1. Run the full pytest suite and all operational fixtures in a clean environment; archive command output and exit codes.
2. Build the sandbox image from a clean context, run Playwright Chromium tests, and verify non-root/read-only/no-network runtime restrictions.
3. Generate and commit a lockfile using a real package-manager resolution; use `npm ci` rather than `npm install` in release builds. Do not fabricate lockfile integrity metadata.
4. Run secret scanning, dependency vulnerability scanning, and SBOM generation; preserve reports and triage findings.
5. Add and run visual regression tests across representative viewport sizes.
6. Add distributed-systems fixtures for fencing tokens, transactional outbox, clock skew, partial failure, and migration rollback.
7. Test cryptographic behavior with vetted libraries: authenticated-encryption tamper rejection, nonce uniqueness policy, password-hash configuration, key rotation, and envelope-encryption integration. Static source scanning is heuristic and is not a security certification.
8. Implement signed telemetry/PQC only if explicitly included in the product threat model and release scope; document algorithm choices, key lifecycle, verification, and migration plan.

## Evidence policy
A file existing is not evidence that its behavior works. Record each gate as PASS, FAIL, BLOCKED, or NOT RUN, with command, environment, exit code, and artifact. Do not claim 100% completeness or GA readiness while any mandatory gate is not PASS.


## Remediation runbook

See [`RELEASE-ASSURANCE-REMEDIATION.md`](RELEASE-ASSURANCE-REMEDIATION.md) for copy/pasteable lockfile, test, security, SBOM, Docker, and live Gemini steps. The candidate remains blocked from GA until every mandatory gate has retained PASS evidence.

For the most recent local evidence and exact blockers, see [`LOCAL-RELEASE-ASSURANCE-REPORT.md`](LOCAL-RELEASE-ASSURANCE-REPORT.md) and [`../reports/release-assurance-local-latest.json`](../reports/release-assurance-local-latest.json).
