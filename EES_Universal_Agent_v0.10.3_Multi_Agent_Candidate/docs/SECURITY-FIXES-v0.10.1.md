# EES_Gemini v0.10.1 — Security Fixes

## Fixed in this candidate

1. High-risk sandbox tasks mount `/workspace/task` read-only. Low/medium tiers remain read-write by profile. Network access remains disabled, root filesystem remains read-only, capabilities are dropped, `no-new-privileges` is enabled, and resource limits remain explicit.
2. Sandbox launch now refuses mutable image tags. `EES_SANDBOX_IMAGE` must be set to an immutable image reference such as `registry.example/image@sha256:<64-hex-digest>`. The deployment owner must obtain and verify the digest from a trusted registry/build pipeline.
3. Learning evaluation reports require HMAC authentication using `EES_LEARNING_REPORT_HMAC_KEY` (at least 32 characters), and bind candidate ID, candidate rule hash, dataset ID, runner ID, status, holdout result, and scores. Promotion revalidates this report. Store the key in a secret manager or protected CI secret; never commit it or put it in the task workspace.
4. Route-cache entries are treated as untrusted data. A cached route must exactly match a currently configured route, malformed caches are discarded, cache writes are atomic, and task text is not persisted.
5. Regression tests cover unsigned reports, tampered cached routes, high-risk read-only policy, and immutable-image configuration.

## Limitations / release gates

- HMAC proves possession of the configured shared key; it does not independently prove that the named runner actually executed the evaluation. Only the trusted evaluation service should hold the key and issue reports.
- Docker isolation behavior must still be verified on a real Docker daemon with adversarial tests; string-level tests are not a substitute.
- A valid image digest must be supplied at deployment; no image is bundled or assumed trusted by this package.
- Live Gemini provider-side context caching is not implemented by the local route cache.
- Full test suite timed out in this environment; selected tests and structural validation passed, but no claim of full-suite success is made.
- Dependency/SBOM/CVE scans, Playwright E2E, and independent security review remain pending.

Release decision: `BLOCKED_NOT_GA`.

## Follow-up in v0.10.2

A separate Markdown-only exporter is available at `scripts/export_chat_safe_skills.py`. It produces a knowledge-only archive and intentionally excludes executable code and runtime security controls. The legacy adaptive-engineering-agent integration is explicitly documented as compatibility-only pending a migration audit. The Playwright fixture lockfile is not included until npm registry resolution can produce and validate a complete lockfile; a hand-written or partial lockfile would falsely imply deterministic dependency resolution.
