# Cross-Agent Evaluation Protocol v1

## Purpose
Measure portability and outcome quality across actual agent/model/runtime combinations. Repository validation alone is not an agent-quality result.

## Required test matrix
For each run record: provider, model ID/version, agent runtime/version, skill-pack digest, tool set, permission profile, operating system, temperature/sampling settings when exposed, case ID, run number, timestamp, latency, token/cost telemetry if available, tool calls, exit states, artifacts, and reviewer decisions. Never store API secrets.

## Minimum case classes
1. Normal success path.
2. Missing optional capability with fallback.
3. Missing required capability, requiring plan-only or handoff.
4. Invalid or incomplete input.
5. Tool failure/nonzero exit.
6. Timeout or interrupted run.
7. Conflicting or ambiguous requirements.
8. Output format/schema violation.
9. Recovery/rollback path where applicable.
10. Unsupported request where the skill should stop or hand off.

## Scoring
Grade each criterion as PASS, FAIL, UNKNOWN, or NOT_RUN. Do not collapse UNKNOWN/NOT_RUN into PASS. Keep automated and human grades separate. High-impact cases require two independent reviewers; record disagreements and adjudication. Report exact denominator, pass rate, failure categories, inter-reviewer agreement, latency distribution, cost when measurable, and run-to-run variance.

## Comparison design
Run the same case set across each supported agent combination. Preserve prompts, skill pack, configuration, and fixtures by digest. Use repeated runs for nondeterministic systems. Do not compare models under materially different tools or permissions without labeling the confounder.

## Release gates
- Structural validation: package and schema checks pass.
- Runtime integration: at least one live, authorized agent execution with captured evidence.
- Portability: at least two materially different agent integrations run the same representative case set; unsupported combinations are explicitly labeled.
- Quality: predefined minimum criteria pass and independent review is complete.
- Production: security, isolation, cost controls, observability, failure recovery, and operational ownership are separately verified.

## Prohibited inference
Passing fixtures, routing audits, or schema validation does not establish agent capability, reasoning quality, universal compatibility, or production readiness.
