# Elite Engineering Suite v0.9.0 Candidate

An engineering capability library with 32 canonical active skill folders and 74 backward-compatible capability IDs, with a deterministic signal router, task-level risk gate, scoped local approval records, allowlisted check runner, artifact hashing, chained event ledger, and evaluation contracts. This release selectively adapts workflow patterns from Anthropic's public Agent Skills repository without vendoring its helper scripts or proprietary document-skill implementations.

## What this package is—and is not

The package provides **engineering workflows and a local control/verification layer**. It is not a self-contained autonomous AI agent, operating-system sandbox, externally authenticated approval service, signed audit platform, or production assurance certificate. Dynamic skill loading depends on the host agent. Agent effectiveness is not established by fixture-contract validation.

## Start here

1. Read `SKILL.md`, `START_HERE_AR.md`, and `references/safety-policy.md`.
2. Use `capability-registry.json` as the authoritative inventory of 74 capability IDs. Each ID resolves through `canonical_skill_id` and `skill_path` to one of the 32 active canonical skill folders.
3. For skill creation or MCP work, resolve `skill-creation-and-evaluation` or `mcp-server-engineering` through the registry before opening the canonical `SKILL.md`.
4. Original specialist instructions are preserved in `docs/skill-source-archive/`; this is provenance material, not 74 separate active skill folders.
5. Write observable acceptance criteria before planning or execution. Run only checks registered in `checks/catalog.json`.
6. Run the validation commands below before relying on a release claim.

## Example workflow

```bash
python scripts/task_runtime.py route \
  --task-id task-001 \
  --request "read-only API contract compatibility audit" \
  --repo ../your-project \
  --out-dir ../ees-runs/task-001 \
  --acceptance "current and previous API contract tests pass"
python scripts/task_runtime.py plan --out-dir ../ees-runs/task-001
python scripts/task_runtime.py start --out-dir ../ees-runs/task-001
python scripts/task_runtime.py run-check --out-dir ../ees-runs/task-001 --check-id package-validate-v072
```

The package validator checks this suite, not your target project. For a project-specific check, add a reviewed runner and pin its SHA-256. The runtime does not execute arbitrary user shell strings.

## Verification commands

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

## Run real agent evaluation

An agent adapter can now execute real evaluation cases and preserve per-case artifacts and evidence records. A separate grader validates criterion-level verdicts and evidence references. Neither process completion nor a structurally valid grade is proof by itself; independent review is still required.

```bash
python scripts/run_agent_evals.py --command "python /absolute/path/to/your_adapter.py" --skill backend-development --limit 3 --timeout 300 --output reports/backend-agent-eval.json
```

See `docs/agent-evaluation/ADAPTER-PROTOCOL-v1.md` for the JSON protocol, artifact handling, grading format, and security limitations.

## Verification boundaries

| Layer | Claim |
|---|---|
| Package structure/schema/links | Checked by `scripts/validate.py --full` |
| Active canonical skills | 32 physical skill folders; 74 capability IDs retained as aliases |
| Evaluation contracts | 222 contracts defined and checked; no AI agent is executed by the fixture-only harness |
| Runtime behavior | Locally tested against adversarial/negative cases through listed tests |
| Agent task quality | Unverified until a real agent runner and graders attach run outputs |
| Production readiness/security | Unverified; requires deployment-specific review and tests |

Source provenance and license decisions are recorded in `references/anthropic-agent-skills-integration.md` and `THIRD_PARTY_NOTICES.md`. See `RELEASE-NOTES-v0.7.6.md` for changes and limitations.

## v0.7.6 Pilot execution

See [Pilot Execution Plan](docs/archive/pre-v0.9.0/PILOT-EXECUTION-PLAN-v0.7.6.md), the [baseline generator](scripts/generate_baseline.py), the [provider adapter](scripts/openai_compatible_agent_adapter.py), and the [Docker sandbox](sandbox/Dockerfile). No live agent-quality result is claimed until the Pilot is run and independently graded.

## Master execution plan v1.1

See [the Arabic master implementation plan](MASTER-IMPLEMENTATION-PLAN-v1.1-AR.md). The plan defines owners, durations, resource/entry/exit criteria, cost controls, overlap decisions, human-review governance, and Pilot gates. Current decision: GO for a bounded Pilot after environment setup; NO-GO for production. Real-agent quality remains unverified.


## v0.7.8 Adaptive Engineering Agent integration

The `integrations/adaptive-engineering-agent/` directory embeds the standalone adaptive agent source. Read `docs/ADAPTIVE-AGENT-INTEGRATION-v0.7.8-AR.md` for scope, setup, test commands, and limitations. The integration preserves the separate runtime boundary; it does not automatically wire feedback into EES skill promotion.


## Skill governance (v0.9.2)
External skills are candidates, not automatic additions. Check license and security, benchmark against overlapping canonical skills, merge proven improvements where appropriate, and add a separate route only for a distinct task intent. See `docs/skill-governance/SKILL_GOVERNANCE_AND_PLACEMENT.md` and the intake decision template. This policy change does not imply production certification.
