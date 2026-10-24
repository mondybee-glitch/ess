# EES Gemini v0.10.0 — Adaptive Runtime & Evidence Governance

## Integrated requirements

1. **Signed self-verifying evidence mesh**: the v0.9.3 runtime gate remains fail-closed and binds the signed manifest to task ID, package version, repository tree digest, trusted public key and required checks. Signatures authenticate signed bytes/key possession; they do not prove a claim is true. Keep private signing keys outside the repository and sandbox.
2. **Continuous learning with temporary instincts**: `scripts/learning_governor.py` stores candidates as `TEMPORARY`; promotion requires a passing regression report, holdout evidence, a score threshold and an unexpired candidate. Rollback is explicit and event records are hash-chained. The score/report is only as trustworthy as the independent evaluation process supplying it.
3. **Dynamic runtime sandboxing**: `scripts/sandbox_policy.py` selects reviewed resource profiles by risk and rejects network/secret requests by default. `scripts/run_sandbox_task.sh TASK_DIR RISK -- COMMAND ...` applies Docker isolation. The wrapper does not itself prove Docker daemon configuration, kernel isolation or image provenance; validate these in the target environment.
4. **Hierarchical routing and Gemini context caching**: `scripts/hierarchical_router_cache.py` caches routing decisions using a content-addressed key derived from task text, routing configuration, model label and policy version; entries expire and can be invalidated. `provider_cache` deliberately reports `NOT_CONFIGURED`: real Gemini provider-side context caching requires credentials, API integration, lifecycle management and live smoke tests, which are not claimed here. Never cache signed evidence, secrets or release decisions.

## Useful commands

```bash
python scripts/learning_governor.py propose --name "candidate-rule" --rule "Describe the proposed behavior"
python scripts/learning_governor.py list
python scripts/sandbox_policy.py --risk medium
python scripts/hierarchical_router_cache.py select --task "Build a React UI and test it"
python scripts/hierarchical_router_cache.py invalidate
python scripts/validate.py --full
python -m pytest -q tests/test_adaptive_runtime_v010.py tests/test_signed_runtime_gate.py
```

## Release gates still required

Not GA / not production-approved. Before release: run the complete pytest suite, real Docker build and adversarial isolation tests, resolved dependency audit and SBOM, Trivy/image CVE triage, full-history secret scan, immutable image digest pinning, Playwright execution, live Gemini API/cache smoke test, and independent security review. Confirm package-lock generation where Node package workflows require it.
