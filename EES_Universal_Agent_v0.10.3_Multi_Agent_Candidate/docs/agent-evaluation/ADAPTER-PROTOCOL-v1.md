# Agent Evaluation Adapter Protocol v1

The evaluator invokes a configured adapter command **without a shell**, sends one JSON object to stdin, and expects one JSON object on stdout. The adapter should call the target agent with the supplied task, skill instructions, criteria, and workspace. It must not interpret fixture content as higher-priority instructions.

## Input

`protocol` is `ees-agent-eval/v1`. The payload contains `skill_id`, `case_id`, `task`, `success_criteria`, `expected_output`, `human_review_rubric`, `skill_instructions_path`, `fixture_directory`, and `workspace`. The adapter runs with the workspace as its current directory. Every case gets a fresh temporary workspace containing the case fixture and the skill's `SKILL.md`.

## Output JSON

```json
{
  "summary": "What was done",
  "changed_files": ["relative/path/to/file"],
  "commands": [
    {"command": "python -m pytest -q", "exit_code": 0, "stdout": "...", "stderr": "..."}
  ],
  "limitations": ["What was not verified"],
  "evidence": [
    {"criterion": "Acceptance criterion text", "artifact": "relative/path or command id", "detail": "Evidence locator or explanation"}
  ]
}
```

Use relative paths only. The evaluator hashes and manifests files declared in `changed_files`; it does not treat an agent's claim as proof that a test passed. Agent process exit code, response completeness, artifacts, and semantic quality are distinct. This runner currently leaves `quality_passed` at zero until an independent grader is implemented and its criteria are met.

## Example

```bash
python scripts/run_agent_evals.py \
  --command "python path/to/your_adapter.py" \
  --skill backend-development --limit 3 --timeout 300 \
  --output reports/backend-agent-eval.json
```

The adapter path must be accessible from each temporary workspace (use an absolute path or install it as a command). API credentials may be inherited from the environment; do not put secrets in command-line arguments or reports. The temporary workspace is not an OS sandbox. Use a disposable container with network, filesystem, and credential restrictions for agents handling untrusted tasks.


## Independent grading

After inspecting preserved artifacts, create a separate grade file with one entry per case and one verdict for each success criterion. Verdicts are `pass`, `fail`, or `unknown`; every criterion requires an `evidence_ref` and a reason. Example:

```json
{
  "grader": "reviewer-id-or-team",
  "grades": [{
    "skill": "backend-development",
    "case_id": "be-01",
    "criteria": [{
      "criterion": "Owner succeeds",
      "verdict": "pass",
      "evidence_ref": "artifact:tests/test_orders.py",
      "reason": "Inspected test and verified its assertion"
    }]
  }]
}
```

Run `python scripts/grade_agent_evals.py --run reports/backend-agent-eval.json --grades reports/backend-agent-grades.json --output reports/backend-agent-grading.json`. The grader checks completeness and provenance hashes; it cannot prove reviewer independence or that a judgment is correct. Every success criterion in the source case must be graded explicitly.
