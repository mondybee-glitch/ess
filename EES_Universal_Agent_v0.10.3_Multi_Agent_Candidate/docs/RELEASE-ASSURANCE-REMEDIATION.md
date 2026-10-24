# EES Gemini v0.9.2 — Release Assurance Remediation

Status: **candidate; not production-approved**. This document converts the outstanding areas into reproducible actions and evidence. A missing tool, skipped test, network error, or external review is never counted as PASS.

## 1. Resolve and commit the Node lockfile

From the project root on a network-connected machine with Node.js 22 and npm 10+:

```bash
python scripts/bootstrap_node_lock.py
```

The script lets npm generate the real `operational-fixtures/playwright-ui-state/package-lock.json`, validates lockfile v3 plus root dependencies and registry integrity metadata, then runs `npm ci`. Do not hand-write lock entries or integrity strings. Review and commit the resulting lockfile. If generation fails because of DNS, proxy, or registry access, fix that network path and rerun it.

The sandbox Dockerfile now uses `npm ci` and requires the committed package-lock; this is deliberate fail-closed behavior, preventing Docker from silently resolving a different dependency tree on each build.

## 2. Run the full test matrix

```bash
python -m pytest -q tests
python scripts/run_operational_fixtures.py --timeout 60 --output reports/operational-fixtures-release.json
python scripts/run_multilang_fixtures.py --include-playwright --timeout 120 --output reports/multilang-fixtures-release.json
cd operational-fixtures/playwright-ui-state
npm ci
npx playwright install --with-deps chromium
npm test
cd ../..
docker build --no-cache -f sandbox/Dockerfile -t ees-gemini-sandbox:0.9.2 .
```

The matrix is PASS only when all commands return zero, the Playwright record is not skipped, and Docker builds cleanly. The container must also be run as non-root with a read-only root filesystem, dropped capabilities, network disabled by default, and a narrowly scoped writable mount.

## 3. Security and SBOM gates

Local heuristic scanning and a manifest-level BOM can be started with:

```bash
python scripts/secret_entropy_scan.py
python scripts/generate_candidate_sbom.py
```

The entropy scanner does not print candidate secret values. It is only a heuristic. The release workflow also runs Gitleaks over full Git history; review the generated CI result and triage findings before release. The workflow pins Gitleaks 8.30.0 rather than 8.30.1 because an upstream issue reports a detection regression in 8.30.1. For repositories owned by a GitHub organization, configure the required `GITLEAKS_LICENSE` repository/organization secret; personal accounts do not require it. `candidate-manifest-sbom.cdx.json` is explicitly PARTIAL: a direct-manifest list without resolved transitive dependencies is not a release-grade SBOM.

On a network-connected clean environment, run at minimum:

```bash
npm audit --audit-level=high
npm sbom --sbom-format=cyclonedx > reports/node-sbom.cdx.json
python -m pip install pip-audit cyclonedx-bom
python -m pip_audit -r requirements-test.txt -r requirements-gemini.txt --format=json > reports/pip-audit.json
cat requirements-test.txt requirements-gemini.txt | cyclonedx-py requirements - --output-file reports/python-manifest-sbom.cdx.json --output-reproducible
```

For a complete environment SBOM, create an isolated virtual environment, install only the release-relevant dependencies, then generate an environment BOM with `cyclonedx-py environment`. Preserve tool versions, timestamps, raw reports, and vulnerability triage. A clean command is not by itself sufficient if a vulnerability remains unresolved.

## 4. Gemini and independent security review

Live Gemini verification requires a controlled test project, a least-privilege API key injected through a secret manager/environment variable, cost limits, a recorded model/version, request/response hashes with personal data redacted, timeout/retry checks, and explicit acceptance criteria. Never embed credentials in this ZIP or its reports. The final security review must be performed by a reviewer independent of the implementation author and should cover sandbox isolation, secret handling, dependency reports, cryptographic/key lifecycle, event-ledger integrity, and data egress.

## 5. Release decision rule

`v1.0.0-GA` is blocked until the real lockfile is committed; full pytest, operational Python fixtures, JavaScript and Playwright tests, clean Docker build/runtime restrictions, dependency audits, complete SBOMs, secret scanning, live Gemini verification, and independent security review are all PASS with retained evidence. Never relabel blocked or unrun gates as passed.


## Container image vulnerability and reproducibility gates

The release workflow runs Trivy against the built sandbox image and fails on CRITICAL/HIGH OS or library findings. Retain the JSON artifact, investigate each finding, and do not broadly suppress findings without a documented exception and expiry. The Dockerfile currently uses a mutable `node:22-bookworm-slim` tag; before GA, resolve the intended multi-platform image, review its vulnerability report, and commit a digest-pinned `FROM` reference. Re-run the clean Docker build and image scan after pinning.
