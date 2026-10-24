---
name: elite-engineering-suite
description: Route and govern software engineering work through 74 specialist capabilities, task-level risk gates, allowlisted checks, acceptance criteria, and artifact-bound evidence. Use for planning, implementation, security, testing, operations, release, and recovery work.
version: 0.8.0-clean-candidate
---

# Elite Engineering Suite v0.8.0 Clean Candidate

The package has three layers: the universal core, routed specialist skills, and the target project's own profile and checks. `capability-registry.json` is the authoritative inventory; all 72 skill folders must be represented there exactly once. Load only selected skills and their dependency closure.

## Non-negotiable truth rule

Do not claim that a command ran because an action was written to a log. Do not claim a check passed because its exit code was typed by a caller. Executed evidence is produced only by `scripts/task_runtime.py run-check` for a SHA-256-pinned runner in `checks/catalog.json`. Verify the actual exit code and hash-bound output artifact. A structurally valid fixture is not an executed agent task.

## Task lifecycle

1. Define the goal and at least one unique, observable acceptance criterion.
2. Route with `scripts/task_runtime.py route`, providing task ID, request, target repo, out directory, and each criterion using `--acceptance`.
3. Review the selected capabilities, dependency order, conflicts, and `task_risk` separately.
4. Run `plan`. Run `start`; start must block on stale package/repository tree hashes or missing high/critical task-scoped approval.
5. Execute only catalogued checks using `run-check`. This package does not allow arbitrary shell commands. `record-action` records manual/planned steps only and cannot create execution evidence.
6. Record each acceptance criterion through `record-criterion` with a status and an existing `repo:relative/path` or `out:relative/path` evidence artifact.
7. Run `verify`. It must refuse `PASSED` for a failed/nonzero check, absent evidence, changed artifact hash, unfinished criterion, or invalid event ledger.
8. Run `release-decision`; report all blockers and limitations. Keep recovery/rollback explicit for high/critical-risk work.

## Safety and audit limits

The task-risk classifier is deterministic and cue-based; it is not a complete threat model. Human review remains required for consequential work. Local approval records are self-attested, not external identity authentication. The event SHA-256 chain detects partial/accidental tampering but is not signed or externally anchored. The check runner uses `shell=False`, runner hashes, timeouts, and a fixed catalog, but it is not an OS sandbox.

## Hierarchical specialist selection

The runtime enforces `hierarchical-routing.json`: Stage 1 selects relevant engineering routes, Stage 2 activates specialists inside those routes. For high- and critical-risk requests, the runtime additionally activates the mandatory security floor (`security-review`, `defensive-appsec-assessment`, and `prompt-provenance-and-safety`) when those capabilities exist. `scripts/validate.py` checks that every registered skill is mapped exactly once and that the routing document conforms to `schemas/hierarchical-routing.schema.json`.

## Specialist selection

Use the machine-readable registry and routing output, then read only `skills/<skill-id>/SKILL.md` for the selected domain. Dependencies and co-activation are computed transitively; ordering constraints are applied to the selected set; conflicting capabilities cause routing to fail rather than proceed silently. The numeric route score is heuristic, not a calibrated probability.

## Status vocabulary

- `PASSED`: all configured checks succeeded, their evidence hashes remain stable, and every acceptance criterion is marked pass with evidence.
- `PARTIAL`: some requirements are complete but at least one remains unresolved.
- `FAILED`: a required check failed, an execution artifact changed, or an acceptance criterion failed.
- `BLOCKED`: a gate or integrity check prevents execution.
- `UNVERIFIED`: evidence is absent, incomplete, or insufficient to establish the outcome.

Passing these local tests does not prove production readiness, complete security, or AI-agent effectiveness.

## Hyper-Cognitive Engineering Kernel (mandatory for implementation tasks)

Do not treat the first plausible answer as a solution. Use this evidence-driven five-stage protocol before implementing or making a consequential recommendation. This is a work protocol, not a claim that hidden reasoning can be exposed or that the model becomes infallible.

### 1. Inversion and trap hunting
State the three most plausible production failures first. Check concurrency/races, duplicate delivery, state loss, partial network failure, untrusted inputs, authorization boundaries, and recovery. Select only those applicable; do not pad the analysis with irrelevant risks.

### 2. Two-stage routing and invariant extraction
Read `hierarchical-routing.json`, select the primary route, then at most one primary skill and two guard skills. Read the selected `SKILL.md` and its referenced material only as needed. Convert applicable hard invariants into testable acceptance criteria before coding. If route selection is ambiguous, state the ambiguity and request context only when a wrong guess would be costly.

### 3. Zero-code dry run
For MEDIUM or higher risk, record a compact state/data-flow simulation before editing: (a) input → validation → authority → persistence → output, (b) duplicate/concurrent request behavior, (c) timeout/partial failure behavior, and (d) rollback or forward-fix path. If rollback cannot safely fit in under a minute, document the longer recovery plan rather than pretending it can.

### 4. Principal-grade implementation
Avoid toy implementations and placeholder error handling. Define types/contracts, timeouts, cancellation, bounded retries, idempotency, least privilege, secret/PII redaction, observability, and migration/rollback behavior where applicable. Use exact domain constraints; never apply an invariant outside its stated assumptions.

### 5. Adversarial self-trial and evidence gate
Assume at least one hidden defect remains. Run the relevant entries in `checks/catalog.json`, regression tests, and failure-path tests. Record exact commands and outcomes. `VERIFIED` requires successful execution against the exact current artifact; static inspection, a plan, or a previous run is not proof. Otherwise use `UNVERIFIED`, `PARTIAL`, or `BLOCKED` and state what is missing.

### Output contract
For meaningful engineering work, deliver: assumptions and top failure modes; selected route/skills; acceptance invariants; implementation or decision; checks actually run with outcomes; residual risks and rollback/recovery. Keep the visible plan proportional to task risk and avoid dumping irrelevant process prose.



## Canonical Skill Consolidation (v0.9.0 Candidate)

The active skill library contains 32 canonical skill folders. The 74 legacy capability IDs remain in `capability-registry.json` and `hierarchical-routing.json` as compatibility aliases mapped through `canonical_skill_id` and `skill_path`. Original specialist SKILL.md documents are retained under `docs/skill-source-archive/` for provenance; that archive is not loaded as active skills.
