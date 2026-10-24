# Protocol `adaptive-agent/v1`

Input JSON:

```json
{
  "task_id": "string",
  "request": "string",
  "workspace": "absolute workspace path",
  "acceptance_criteria": ["observable criterion"],
  "skill_ids": ["selected skill"],
  "risk_class": "low|medium|high",
  "budget": {"max_steps": 12, "timeout_seconds": 30}
}
```

Output JSON must distinguish execution from quality:

```json
{
  "status": "completed|failed|timeout|blocked|invalid_output",
  "summary": "string",
  "changed_files": ["relative path"],
  "commands": [{"command":"...","exit_code":0,"stdout":"...","stderr":"..."}],
  "evidence": [{"criterion":"...","artifact":"...","detail":"..."}],
  "limitations": ["..."],
  "trace": [{"step":0,"tool":"read_file","ok":true}]
}
```

A grader adds criterion-level `pass`, `fail`, or `unknown`; the runtime never converts execution completion into a quality pass.
