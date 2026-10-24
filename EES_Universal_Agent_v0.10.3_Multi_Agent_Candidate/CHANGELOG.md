## v0.10.2 — Packaging and Chat-Safe Export Hardening

- Added Markdown-only chat-safe exporter and regression test.
- Corrected the candidate version metadata to v0.10.2.
- Renamed release archive root to match the release version.
- Playwright lockfile generation remains blocked by unavailable package-registry access; no fabricated lockfile is included.
- Runtime Docker, cloud CI, and live Gemini checks remain pending.

# v0.10.1 — Security Fix Candidate

## Security fixes
- Enforce read-only workspace bind mounts for high-risk tasks.
- Require immutable Docker image digests via `EES_SANDBOX_IMAGE=name@sha256:...`; refuse mutable tags.
- Require HMAC-authenticated learning evaluation reports bound to candidate ID, rule hash, dataset, runner, and scores; revalidate before promotion. Set `EES_LEARNING_REPORT_HMAC_KEY` through a secret manager (minimum 32 characters), never commit it.
- Treat route-cache data as untrusted, validate cached routes against the current authoritative routing table, and write cache files atomically.
- Add regression tests for unsigned learning reports, cache tampering, and high-risk read-only policy.

Status remains `BLOCKED_NOT_GA`: Docker runtime isolation, live Gemini integration, complete test suite, dependency/SBOM/CVE scans, and independent review remain required.

---

# v0.10.0 — Adaptive Runtime & Evidence Governance Candidate

- Added temporary-instinct learning lifecycle with holdout and regression gates; candidates do not become active automatically.
- Added risk-tiered sandbox policy generation and fail-closed Docker invocation wrapper.
- Added hierarchical routing cache with content-addressed keys, TTL, and explicit invalidation; cache entries never contain signed evidence or release decisions.
- Added unified architecture and acceptance tests for the four agreed engineering requirements.
- Existing signed evidence gate remains required by default.
- Status: engineering candidate only; not production approved. Docker isolation, live Gemini cache integration, external signing-key custody, full security audit, and full test suite remain pending.

# v0.9.3 — Signed Runtime Verification Gate (engineering candidate)

- Bumped candidate package/runtime version to 0.9.3.
- Integrated the Ed25519 evidence verifier with the task runtime's final verification path.
- Signed evidence is required by default before `PASSED`; missing/invalid attestations fail closed to `BLOCKED`.
- Attestations are bound to task ID, runtime version, repository tree hash, required check IDs, signed-manifest digest, and trusted public-key file digest.
- Release decisions revalidate the attestation against the current repository tree.
- Added strict-mode integration tests for missing and valid signed attestations.
- Candidate remains BLOCKED_NOT_GA: full suite did not complete, and Docker/CI/live Gemini/dependency audit/SBOM/image scan/independent review are not fully verified.

# v0.9.2 Release Assurance Remediation — 2026-10-24

- Fixed a stale operational-fixture test that assumed 13 fixtures when the current suite has 14; expected totals are now discovered from fixture directories.
- Added real npm lockfile bootstrap/validation that delegates registry resolution and integrity generation to npm; no synthetic lockfile is supplied while registry DNS is unavailable.
- Updated direct Playwright test tooling to the current stable pins and made Docker fail closed using `npm ci` with a committed lockfile.
- Added a secret-pattern/entropy heuristic scanner that does not emit secret values, plus a CycloneDX-shaped manifest BOM explicitly labeled partial.
- Added CI workflows for lockfile-candidate resolution and release assurance, including pytest, operational fixtures, Playwright, dependency audit, SBOMs, Docker build, secret scanning, and an opt-in-by-secret live Gemini smoke gate.
- Hardened runtime tree hashing to exclude volatile test/tool caches that can change during local validation.
- Full local pytest suite passed after test-runner hardening: 67 tests plus 9 subtests. Operational fixtures pass 14/14 and JavaScript unit tests pass 2/2. Local npm lock resolution still times out, so no fake lockfile was fabricated; Playwright browser execution, clean Docker build, dependency audits/full SBOM, full-history Gitleaks scan, live Gemini call, and independent review remain unverified locally.

# v0.9.2 Contract Fix Review — 2026-10-24

- Fixed `scripts/check_all.py` to derive `package_version` from `package-manifest.json` instead of emitting the stale `0.7.7` value.
- Added a regression test guarding release-report version consistency.
- Exact-pinned the Playwright fixture's direct npm dependencies to reduce semver drift.
- Clarified in the Dockerfile that this candidate is not lockfile-reproducible and remains blocked from production approval until a lockfile and clean-container verification are available.
- No claim is made that the full test suite, Docker build, Playwright browser run, or live Gemini integration passed in this review.

# v0.9.1 — Controlled Internal Pilot Approval (2026-10-24)

- Scoped authorization granted for controlled internal pilot only.
- Production certification explicitly withheld pending full test-suite completion, live Gemini integration, semantic review, and independent security review.
- Added machine-readable approval evidence at `reports/v0.9.1-controlled-pilot-approval.json`.

# Changelog

## 0.9.0-Candidate
- Added a mandatory five-stage, evidence-gated engineering kernel.
- Added focused hierarchical-routing regression tests.
- Expanded four critical skills with domain-specific failure traps, invariants, decision matrices, and adversarial kill-switches.
- Added two deterministic operational contract fixtures and moved stale release artifacts out of active paths.
- Candidate only: physical 74-to-32 consolidation and full-skill cognitive rewrite remain pending and are explicitly not claimed complete.

## v0.8.0 Clean Candidate — 2026-10-24

- Enforced two-stage hierarchical routing in the task runtime.
- Added JSON Schema and validator checks for routing completeness and uniqueness.
- Added mandatory security routing floor for high/critical risk tasks.
- Added `.gitignore` and `.dockerignore` protections for secrets, bytecode, and local environments.
- Removed duplicated Node.js skill-local fixture copies; central fixtures are canonical.
- Moved v0.7.0 archive and legacy validation scripts under `docs/releases/`.
- Updated runtime/config version identifiers consistently.
- Original 74 specialist skill bodies preserved; semantic merge to fewer physical skills is not performed in this candidate.

# Changelog

## 0.7.7 — Universal Skill Contract and Cross-Agent Readiness
- Added tool-neutral machine-readable skill contract and example.
- Added conservative capability detector with explicit `not_tested` states.
- Added cross-agent evaluation and compatibility protocols.
- Added standard-library regression tests.
- No new domain skills; live cross-agent quality remains unverified.

## 0.7.5
- Added an adapter-based agent evaluation runner with per-case temporary workspaces, process timeouts, captured stdout/stderr, artifact manifests and SHA-256 hashes.
- Explicitly separates process execution from task quality; the runner never self-awards quality passes.
- Added an independent criterion-level grading record validator and artifact preservation for reviewer inspection.
- Added adapter protocol documentation and tests for execution evidence, timeouts, and grading completeness.
- Real agent effectiveness remains unverified until a real adapter is connected and results are independently graded.

# Changelog

## 0.7.4
- Added 11 executable deterministic domain fixture projects and a bounded runner that captures exit codes, durations, stdout/stderr, and SHA-256 hashes.
- Added a static routing audit and explicit pre-flight checks / handoffs for critical backend, security, data, and orchestration capabilities.
- Added two catalog checks, bringing the catalog to 9 checks; structural validation covered 74 source skill files, 74 capabilities, and 222 evaluation contracts at that release point.
- Verified 11/11 domain fixture projects, 0 routing audit errors/warnings, 12 selected runtime/repository regression tests, and 222/222 fixture contracts.
- Agent-run skill effectiveness remains unverified (0/222 agent-run eval contracts).

## 0.7.3
- Added `web-artifacts-builder` for multi-component interactive web artifacts, state, navigation, accessibility, and verification workflows.
- Added `brand-guidelines` for applying supplied brand systems, with Anthropic styling only on explicit request.
- Updated capability registry, package manifest, core version, and third-party provenance notes.
- Agent-run effectiveness remains unverified.

## 0.7.2
- Reviewed Anthropic's public Agent Skills repository and recorded source/usage boundaries.
- Added `skill-creation-and-evaluation` and `mcp-server-engineering` with domain-specific evaluation contracts.
- Adapted and documented webapp-testing patterns in `browser-e2e-and-test-diagnostics` and distinctive design critique in `ui-ux-design`.
- Strengthened tool-server design and integration-testing guidance in `ai-agents-rag-mcp`.
- Updated registry, package manifest, schema/runtime versions, validation commands, and release documentation to v0.7.2.
- Agent-run effectiveness remains unverified.

## 0.7.1
See `archive/v0.7.0/` and prior release notes for historical material. Older reports are preserved for traceability and do not represent the current release.


## v0.9.0 Candidate — canonical consolidation

- Consolidated 74 active skill folders into 32 canonical skill folders, one per hierarchical route.
- Preserved all 74 capability IDs as aliases to canonical skill paths.
- Archived original source SKILL.md documents for provenance.
- Added the Hyper-Cognitive Engineering Kernel and per-skill decision/failure-pattern reference to all 32 canonical skills.
- Updated validator and manifest to enforce canonical folder count and alias mapping.
- Added regression tests for alias resolution, physical skill count, and canonical skill completeness.

## v0.9.2 — Skill Governance and Intelligent Placement
- Added mandatory GitHub/external skill intake, license and security gates, evidence-based incumbent comparison, merge-versus-add decisions, and source provenance requirements.
- Added a weighted comparative scorecard with non-compensable security/license gates.
- Added canonical placement rules, positive/negative trigger boundaries, regression and rollback requirements.
- Added intake decision-record template, JSON Schema, and focused governance policy tests.
- This policy addition does not change production certification status; release remains approved for controlled internal pilot only.

## v0.9.2 engineering completion candidate
- Deepened all 32 canonical skills with domain-specific failure traps and hard invariants.
- Added native Google GenAI adapter, Node.js/Playwright fixtures, multi-language fixture runner, and E2E runtime tests.
- Archived prior reports and consolidated the current validation report.
- Release remains a candidate pending full tests and live Gemini verification.


## v0.9.2 — Engineering Completion Candidate (not production-approved)
- Expanded all 32 canonical skill failure-pattern references with domain-specific traps, invariants, and production failure matrices.
- Added governed applied-cryptography, payments-ledger, and embedded/IoT specialist modules without changing canonical routing IDs.
- Added heuristic crypto pattern guard and regression fixture; added WCAG contrast ratio checker and Playwright accessibility/viewport smoke tests.
- Updated pilot Dockerfile and ignore rules for Node/Python/Playwright workflows.
- Structural validation and crypto/contrast checks passed. Full pytest, Playwright in Docker, npm lockfile, SBOM/CVE scanning, signed telemetry, and independent security review remain blockers.
## v0.9.2 candidate — engineering hardening delta (2026-10-24)

- Added an Ed25519 evidence-manifest signer/verifier with strict manifest checks and a separate fail-closed mandatory-check policy decision.
- Added regression tests for payload tampering, missing/non-passing checks, missing evidence, subject-hash mismatch, and empty policies.
- Added a constrained Docker task launcher with non-root UID, read-only root filesystem, network disabled, capabilities dropped, no-new-privileges, temporary `/tmp`, and resource limits.
- Corrected the pilot sandbox build script to use the project root as Docker build context, matching the Dockerfile COPY paths.
- Documented evolution-promotion and routing-cache guardrails; provider-side Gemini context caching and automatic rule promotion are explicitly not implemented in this delta.
- Release status remains BLOCKED_NOT_GA. The full test suite did not complete within the available execution window; Docker, live Gemini, dependency audits/SBOM, and independent security review remain unverified.



## v0.10.0 — Adaptive Runtime Evidence Candidate (not production-approved)
- Added governed temporary instincts with bounded scores/TTL and tamper-evident event-ledger verification.
- Hardened route cache writes with atomic replacement and validated routing policy shape; tests assert raw task text is not persisted.
- Fixed sandbox wrapper tmpfs flag conformance and retained defense-in-depth Docker settings.
- Added candidate SBOM and local heuristic secret-scan report (zero findings in 632 scanned files; not a full-history scan).
- Validation batches passed: 17 focused tests, 38 broad regression tests plus 9 subtests, and 21 adapter/repository/timeout tests.
- Full pytest and runtime/E2E batch timed out; Docker, live Gemini context caching, Trivy, Playwright and independent security review remain unverified. Release remains BLOCKED_NOT_GA.


## v0.10.3 — Multi-agent compatibility candidate
- Added a portable `AGENTS.md` contract and Claude-specific `CLAUDE.md`.
- Added Antigravity-oriented `.agent/rules/ees.md` and platform adapter notes for Gemini, Antigravity, Claude, and ChatGPT/cloud environments.
- Documented the universal adapter architecture and cross-agent conformance checklist.
- Added packaging tests for adapter entry points.
- This release does not claim live compatibility until tests run in each actual platform.
