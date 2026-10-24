# Release notes — v0.7.6

## Focus: operational Pilot readiness, not a production claim

### Added
- `scripts/generate_baseline.py` generates authoritative counts from actual skill/evaluation files and detects metadata drift.
- Repaired 51 evaluation contracts missing `success_criteria`, grounding new criteria in existing `expected_output` and `automated_checks`; report at `reports/eval-contract-repair-v076.json`.
- `scripts/openai_compatible_agent_adapter.py` provides a provider adapter for Chat Completions-compatible APIs; provider credentials remain in the host process.
- `sandbox/Dockerfile` and `scripts/build_pilot_sandbox.sh` select Docker for the Pilot command-execution boundary. Commands run without network, with a read-only root filesystem, read-only fixtures/skill, resource limits and no privileged capabilities.
- `scripts/pilot_preflight.py` checks local readiness without calling the provider.
- Frozen 15-case Pilot manifest across five skills.
- Ownership metadata and an explicit policy clarifying that `conflicts_with` means hard exclusion; overlap candidates do not automatically become conflicts.
- Runtime response-contract validation, unsafe artifact-path rejection, manifest-based case selection, and optional estimated-cost budget guard in the runner.

### Corrected
- README evaluation total is synchronized to the actual count: 222, not 216.
- Package, capability registry, fixture catalog and validator versions are aligned to 0.7.6.

### Verified locally
- Static source-of-truth baseline and package validator (results are in `reports/`).
- Unit tests for adapter path controls, output validation, evaluator timeout/invalid-output behavior, and manifest loading (where listed by test results).
- Existing deterministic fixture suites continue to validate only the reference fixtures themselves.

### Not yet verified
- No live provider call or real AI-agent quality evaluation was executed during packaging.
- Docker/Podman is not installed in the current build environment; the sandbox image and its runtime restrictions could not be exercised here.
- No semantic quality pass rate, route-accuracy score, production readiness, or performance claim is established.
