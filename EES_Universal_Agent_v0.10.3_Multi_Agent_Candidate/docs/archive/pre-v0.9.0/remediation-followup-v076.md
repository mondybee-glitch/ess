# Remediation Follow-up — v0.7.6

## Implemented in this follow-up
- Added `requirements-test.txt` with the optional pytest dependency.
- Added `scripts/check_all.py`, a single standard-library orchestrator for validation, eval-fixture checks, routing audit, operational fixtures, and optional pytest. It writes `reports/check-all-latest.json` and reports missing pytest as skipped rather than pretending it ran.
- Added `reports/overlap-review-protocol-v1.json` defining two independent reviewers, at least six discriminating cases per each of the 12 candidate pairs, evidence fields, allowed outcomes, and a third-adjudicator rule. It does not approve any conflict or claim that overlap has been resolved.

## Checks actually run for this follow-up
- `python scripts/validate.py --full`: passed; 74 skills, 74 capabilities, 222 eval contracts, zero warnings.
- `python scripts/run_eval.py --output reports/check-all-eval-fixtures.json`: 222/222 fixture contracts passed; no agent was run.
- `python scripts/audit_routing.py --output reports/check-all-routing-audit.json`: passed; zero errors and warnings.
- `python scripts/run_operational_fixtures.py --output reports/check-all-operational-fixtures.json`: 11/11 passed; this is a deterministic fixture suite, not agent-quality evidence.
- A single combined `scripts/check_all.py` invocation exceeded the environment's command timeout before it emitted its final report. Its individual core checks were rerun successfully as listed above. Do not claim the combined runner itself completed end-to-end in this environment.
- pytest is not installed in this runtime; the runner reports it as skipped and gives the installation command. No pytest tests are claimed as run in this follow-up.
- Docker is unavailable in this runtime. No Docker image build, network isolation, mount policy, resource limits, or real-provider task execution was verified.

## Still unresolved
- Semantic review of the 51 repaired evaluation criteria.
- Six discriminating pilot cases for each of 12 overlap pairs, independently reviewed by two reviewers; no `conflicts_with` edges are approved.
- Real provider + model + pricing configuration and one real agent run in a disposable Docker host.
- Independent grading, repeated-run variance, token/cost/time measurement, and artifact inspection.

## Decision
GO for preparation and limited pilot setup. NO-GO for production or claims of exceptional skill performance.
