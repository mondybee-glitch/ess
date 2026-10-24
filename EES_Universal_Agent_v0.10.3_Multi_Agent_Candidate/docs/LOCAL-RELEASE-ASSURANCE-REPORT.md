# EES Gemini v0.9.2 — Local Release Assurance Report

**Generated:** 2026-10-24T15:36:36Z  
**Decision:** **BLOCKED — not approved for `v1.0.0-GA` or production**

## Passed locally

- `python scripts/validate.py --full`: PASS; 32 skills, 74 capabilities, 222 evaluation contracts, 51 central fixtures, 9 checks, 16 operational fixture projects, zero warnings.
- `python -m pytest -q tests`: **67 passed, 9 subtests passed in 80.59 seconds**. This was a local run, not a clean-container/CI run.
- `python scripts/run_operational_fixtures.py`: **14/14 passed**, with no failures or timeouts. These fixture results do not evaluate live-agent effectiveness.
- Node.js fixture: **2/2 tests passed**.
- Heuristic secret scan: **0 findings across 612 text files**. It can miss secrets and is not a substitute for full-history scanning.

## Still blocked or not run

| Gate | Evidence and next action |
|---|---|
| Real Node lockfile | npm lock resolution timed out (exit 124); `package-lock.json` was not created. Run the manual `Resolve Node Lockfile Candidate` GitHub Actions workflow on a connected runner, inspect its artifact, then commit the real lockfile. |
| Playwright | Skipped locally because dependencies/browser are not installed. Re-run from the committed lockfile in CI; the release gate fails if the lockfile is absent. |
| Clean Docker build | Docker is not installed locally. Run the no-cache Docker build in `.github/workflows/release-assurance.yml`; verify runtime flags separately. |
| Container image CVEs | Trivy CI scan is configured to fail on unresolved CRITICAL/HIGH OS or library vulnerabilities. It has not run locally; review its JSON artifact and remediate findings before release. |
| Immutable Docker base | `sandbox/Dockerfile` still references mutable `node:22-bookworm-slim`. After CVE triage, resolve and commit a reviewed multi-platform digest pin; do not infer image immutability from a tag. |
| npm and Python vulnerability audits | Not run locally due registry/tool availability. Release workflow runs `npm audit` and `pip-audit`. Triage every finding and preserve evidence. |
| Complete SBOM | `candidate-manifest-sbom.cdx.json` includes 4 direct manifest components only and is `PARTIAL_NOT_RELEASE_GRADE`. CI is configured to emit resolved Node and Python environment SBOMs. |
| Full-history secrets | Gitleaks did not run locally. Release workflow scans full Git history and pins version `8.30.0`; review findings, false positives, and repository history before approval. |
| Live Gemini | Blocked: `GEMINI_API_KEY` was not supplied. Configure it as a repository secret, then run the live smoke gate with controlled cost and data. |
| Independent review | Not performed. An independent reviewer must inspect sandbox isolation, dependency and secret reports, cryptographic/key handling, telemetry/evidence, data egress, and the final release artifacts. |

## Why no fake lockfile was added

The lock bootstrap delegates resolution and `integrity` generation to npm. Inventing transitive package entries or checksums would create false reproducibility and a misleading security signal. The CI lock-resolution workflow preserves the artifact for human review immediately after resolution, even if a later browser/install step fails.

## Required release sequence

1. Run `.github/workflows/resolve-node-lock-candidate.yml` on a network-connected GitHub runner.
2. Review and commit the generated `operational-fixtures/playwright-ui-state/package-lock.json`.
3. Run `.github/workflows/release-assurance.yml`; require green pytest, fixture, Playwright, npm/pip audits, resolved SBOMs, full-history Gitleaks, Trivy container CVE scan, a reviewed immutable base-image digest, and clean Docker build gates.
4. Configure `GEMINI_API_KEY` as a GitHub secret and require a successful live smoke test.
5. Complete independent security review and attach signed approval plus triage evidence.
6. Only then consider changing the package manifest to a GA release. A green CI run alone does not replace independent review or an agent-quality evaluation.

Machine-readable counterpart: `reports/release-assurance-local-latest.json`.
