# Validation Report — v0.7.4

This report is regenerated from the commands executed for this release. It distinguishes structural checks, local runtime tests, evaluation contract validation, and real-agent outcomes.

## Required commands

```bash
python scripts/validate.py --full
python tests/test_validate.py
python tests/test_runtime_v072.py
python tests/test_timeout_handling_v072.py
python tests/test_event_ledger_v072.py
python tests/test_risk_classification_v072.py
python tests/test_repository_integrity_v072.py
python tests/test_anthropic_integration_v072.py
python tests/test_eval_harness.py
python -m compileall -q scripts tests
```

**Interpretation rule:** these checks establish package consistency and local control-plane behavior only. Fixture/evaluation definitions do not execute an AI agent. The real-agent effectiveness result remains `unverified` unless a runner produces and stores actual outputs and grading evidence.
