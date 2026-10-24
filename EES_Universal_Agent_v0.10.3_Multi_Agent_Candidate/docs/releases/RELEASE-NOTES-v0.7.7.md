# Release Notes — v0.7.7

## Focus
Portability contracts, capability discovery, and evidence-based cross-agent evaluation. No new domain skills were added.

## Added
- `schemas/universal-skill-contract.schema.json`: machine-readable contract for portable skill metadata.
- `templates/universal-skill-contract.example.json`: complete example contract with capability fallbacks, evidence policy, and evaluation cases.
- `scripts/detect_capabilities.py`: conservative PATH/import capability inventory; explicitly labels provider/browser/network/permissions as not tested.
- `docs/UNIVERSAL-SKILL-COMPATIBILITY-v1.md`: skill/runtime/verification separation and status vocabulary.
- `docs/CROSS-AGENT-EVALUATION-v1.md`: repeatable evaluation matrix, reviewer protocol, and release gates.
- `tests/test_universal_contract.py`: standard-library regression checks.

## Limitations
- This does not create a self-contained AI agent.
- The capability detector checks local executable presence and Python standard-library import only; it does not prove permissions, connectivity, or successful tool operation.
- Cross-agent evaluation protocol is prepared, but no new live provider/model executions were performed in this release.
- Existing Docker/provider limitations remain.

## Release posture
GO for local evaluation/preparation. NO-GO for claims of universal compatibility or production readiness until live multi-agent tests and independent grading are completed.
