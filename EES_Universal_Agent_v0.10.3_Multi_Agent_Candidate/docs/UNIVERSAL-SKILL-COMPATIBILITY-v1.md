# Universal Skill Compatibility Layer v1

## Portability principle
The portable unit is a domain workflow contract, not a promise that all agents interpret it identically. Keep the core instructions plain Markdown and tool-neutral. Put machine-readable contracts, scripts, schemas, fixtures, and provider-specific adapters alongside it.

## Three layers
- **Skill pack:** scope, workflow, examples, schemas, evaluation cases, acceptance criteria.
- **Agent runtime:** model/provider adapter, tool loop, workspace, permissions, timeout and retry policy.
- **Verification:** deterministic checks, independent grader, evidence ledger, human review for high-impact decisions.

## Capability statuses
`available`, `unavailable`, `failed_probe`, `not_tested`, `permission_denied`, and `degraded` are distinct states. Do not infer browser, network, credentials, tool calling, or workspace write access from a tool's name or executable presence.

## Fallback policy
A fallback is allowed only when it preserves the meaning and safety of the task. Otherwise stop with `NOT_RUN` or `UNKNOWN`, explain the missing prerequisite, and return a plan or handoff. Never silently substitute a weaker check while retaining the stronger check's success label.

## Runtime adapter interface
Adapters should expose task input, capability inventory, tool invocation, timeout/cancellation, result/error normalization, artifact collection, and telemetry. Provider-specific implementations must declare supported features and limitations. This repository's OpenAI-compatible adapter does not imply universal provider compatibility.

## Suggested skill folder
```text
skill-id/
  SKILL.md
  contract.json
  schemas/
  examples/
  fixtures/
  evals/evals.json
  checks/
  scripts/
  README.md
```

## Evidence labels
- `PASS`: required verification completed and passed.
- `FAIL`: verification completed and failed.
- `UNKNOWN`: evidence is insufficient to decide.
- `NOT_RUN`: verification was not executed.
- `BLOCKED`: prerequisite or authorization prevented execution.
