# Release notes — v0.7.5

## Purpose
Adds the first real-agent execution evidence path to the existing 74-skill suite. This is a runner/instrumentation release, not a claim that agent quality is now proven.

## Added
- `scripts/run_agent_evals.py`: adapter-driven execution of selected skill evaluation cases.
- Fresh temporary workspace per case, copied fixture and skill instructions, bounded timeout, captured stdout/stderr, output hashes, changed-file manifest and artifact hashes.
- `scripts/grade_agent_evals.py`: separate criterion-level grading record validator with evidence references, reasons, unknown verdicts, and source hashes.
- Preserved declared changed artifacts under a run-specific artifact directory for independent review.
- `docs/agent-evaluation/ADAPTER-PROTOCOL-v1.md`: JSON input/output protocol, grading format, and integration example.
- Tests for successful adapter execution and timeout behavior.

## Quality and security boundaries
- Process completion is distinct from task correctness.
- `quality_passed` remains zero by design until an independent grader is implemented and used.
- Agent output is untrusted and self-reported evidence is not independently validated by this runner.
- Temporary workspaces are not OS-level sandboxes. Run untrusted agents in a disposable container with restricted filesystem, network, and credentials.
- No real model/provider adapter was connected as part of this release; therefore no claim is made that 222 cases have been executed by an AI agent.

## Verification
To be filled with the final release verification run; see `reports/v0.7.5-verification-summary.md`.
