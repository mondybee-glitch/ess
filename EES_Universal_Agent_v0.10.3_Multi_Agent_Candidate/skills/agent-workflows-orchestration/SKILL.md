---
name: agent-workflows-orchestration
description: "Canonical EES specialist for Agent workflows & orchestration; merges 3 compatible source capabilities while preserving their original IDs as aliases."
---

# Agent workflows & orchestration — Canonical Engineering Skill

## Hyper-Cognitive Engineering Kernel

Use this protocol for substantive implementation, architecture, debugging, and review tasks. Do not confuse procedural discipline with proof of correctness.

### 1. Inversion and trap hunting
Before choosing an implementation, enumerate the three most plausible production failures. Consider concurrency, partial failure, retries, state loss, malicious inputs, resource exhaustion, and unsafe trust boundaries as applicable. Identify which failure is most severe and how it will be detected.

### 2. Two-stage routing and invariants
Treat this canonical skill as the primary route when its scope matches. Select no more than two complementary guard skills unless evidence shows a real cross-domain dependency. Extract measurable invariants from the relevant specialist modules below and convert them into acceptance criteria before editing.

### 3. Zero-code dry run
For medium-or-higher risk, sketch the input → transformation → persistence → output path; simulate duplicate/concurrent requests and one partial outage; define a rollback or containment path. If rollback is not feasible, state the recovery strategy before implementation.

### 4. Principal-grade execution
Prefer explicit types/contracts, bounded retries, timeouts, cancellation, idempotency, least privilege, and redacted telemetry where applicable. Avoid toy implementations and unresolved TODOs. Do not invent numeric thresholds: use source-backed limits, derive them transparently, or mark them as tunable assumptions.

### 5. Adversarial self-trial and evidence gate
Assume at least one hidden defect remains. Review failure paths, boundaries, and regressions against `checks/catalog.json` and the relevant module constraints. Report VERIFIED only when a reproducible command actually ran against the current file state and its output supports the claim. Otherwise report NOT RUN, PARTIAL, or UNVERIFIED.

## Canonical scope and alias map

Canonical ID: `agent-workflows-orchestration`  
Source capability aliases: `agent-workflow-orchestration`, `agent-workflow-specification`, `multi-agent-orchestration`.

The original source documents are retained under `../../docs/skill-source-archive/` for traceability. The sections below preserve source-specific procedures; resolve overlaps by the stricter safety invariant and record material conflicts rather than silently discarding them.



---

## Preserved specialist module: `agent-workflow-orchestration`

Source capability: `agent-workflow-orchestration`.

# Agent Workflow Orchestration

## Use when
When converting an approved engineering objective into a multi-stage agent workflow or reviewing an agent run, gateway, queue, or integration policy.

## Do not use when
Do not use when the task does not match the stated domain, lacks required authorization, or is a simpler task owned by another specialist.

## Required inputs
approved objective and repository scope; constraints, acceptance criteria, stop conditions; allowed tools, services, identities, and data classes.

## Purpose
Turn an approved objective into a dependency-aware workflow with read-only reconnaissance, capability assignments, explicit handoffs, budgets, retry policy, approval checkpoints, and a final audit.

## Workflow
1. Confirm scope, authorization, versions, data classification, and acceptance criteria before acting.
2. Separate planning, read-only inspection, implementation or analysis, and verification. Keep side effects behind explicit approval.
3. Record source evidence, assumptions, exact commands, artifacts, and unresolved uncertainty. Never infer success from intent, generated text, or a partial check.
4. Compose only the secondary skills that own distinct controls; hand off implementation, testing, security, and release responsibilities explicitly.

## Pass/fail checks
Pass only when the required inputs are present, boundaries are respected, outputs are reproducible enough for the stated claim, and incomplete or failed checks are reported as such.

Required outputs: workflow plan and dependency graph; role assignments; approval checkpoints; run/audit summary; escalation or halt decision.

## Safety and limits
Use only on authorized systems and accounts. Default to read-only; require confirmation for irreversible, public, financial, destructive, or security-sensitive actions. Do not extend unsupported or vulnerable legacy agent paths.

## Verification
- Exercise delegation isolation, context boundaries, and capability profiles.
- Test retry, timeout, cancellation, backpressure, and budget circuit breakers.
- Require confirmation and audit evidence for destructive or external side effects.

## Hand-offs
Hand off implementation, testing, security, and release responsibilities to the selected specialist owners; do not silently duplicate their work.

## Evidence to report
Report selected sources and revisions, authorization and scope, commands and exit codes, artifacts, coverage limits, risks, handoffs, and what remains Unverified.

---

## Preserved specialist module: `agent-workflow-specification`

Source capability: `agent-workflow-specification`.

# Agent Workflow Specification

## Use when
A request is ambiguous, multi-step, affects architecture, needs coordination across specialists, or requires an evaluation plan before implementation.

## Do not use when
The user asks a well-scoped factual or tiny edit task that can be completed directly without extra process overhead.

## Required inputs
Desired outcome; constraints; source of truth; stakeholders/owners; out-of-scope boundaries; risk; acceptance criteria; and the evidence needed to judge success.

## Workflow
1. Convert the request into observable outcomes. Replace vague terms like “better” or “secure” with measurable acceptance criteria and explicitly state what will not be changed.
2. Separate facts, assumptions, inferences, and unknowns. Ask for clarification only when a wrong guess would be costly; otherwise record the assumption and make a reversible choice.
3. Build a dependency-closed plan with file ownership, risk gates, verification, rollback, budget, and stop conditions. Identify tasks that can safely run independently and those that cannot.
4. Use a decision record for material architecture choices: constraints, alternatives, evidence, trade-offs, reversibility, owner, and revisit trigger.
5. Select specialists by scope, not by name familiarity; avoid loading every skill. Include an independent critic for consequential work and require it to test assumptions and counterexamples.
6. Evaluate agent work against the same reproducible task and baseline. Distinguish fixture validity, task execution, grader outcome, human review, and production evidence as separate statuses.
7. Preserve only durable project decisions and provenance. Do not turn an unverified inference into project memory or silently rewrite requirements.

## Pass/fail checks
Each acceptance criterion is testable; scope and assumptions are visible; plan dependencies and owners are clear; success/failure evidence is specified; evaluation claims reflect actual execution.

## Hand-offs
Coordinate with multi-agent-orchestration for roles and dependencies, skill-package-governance for skill contracts, and software-testing for graders and mutation tests.

## Evidence to report
Task brief, decision records, dependency plan, accepted assumptions, critic findings, test/grader evidence, unresolved questions, and handoff owner.

---

## Preserved specialist module: `multi-agent-orchestration`

Source capability: `multi-agent-orchestration`.

# Multi-Agent Orchestration

## Use when
- Features spanning UI, API, and security
- High or Critical changes needing independent review
- Large audits that split cleanly by area

## Do not use when
- One-file fixes
- Typos and formatting
- Work with tight sequential dependencies and no independent parts

## Required inputs
- Task brief with acceptance criteria
- Routing matrix
- Budget: time, tool calls, number of agents

## Workflow
1. Decompose into sub-tasks with disjoint file ownership; identify dependencies.
2. Assign a role per sub-task: Architect, Frontend, Backend, Designer, Security Reviewer, Tester, Reverse Engineer, Researcher.
3. Send each agent a handoff using the handoff template (objective, files owned, definition of done, return format).
4. Run independent sub-tasks in parallel (at most 5 concurrent); run dependent ones in order.
5. Collect results; check each against its definition of done.
6. Run an independent Critic that receives the requirements and the output, not the producer's reasoning.
7. Resolve conflicts with evidence (contract test, measurement, official docs); record the decision.
8. Merge, run the full verification, and report with statuses.

## Pass/fail checks
- No two agents own the same file
- Security review runs after implementation, on the merged result
- Critic output attached to the report
- Budget respected; stop rule triggered on unresolved conflict
- No agent output accepted as `verified` without evidence

## Hand-offs
- Any specialist skill as the assigned role
- multi-agent handoff template in templates/handoff.md

## Evidence to report
Commands run with results, files changed, and anything not verified. Use the status vocabulary from the core [SKILL.md](../../docs/skill-source-archive/multi-agent-orchestration.md).

## Concrete commands

Record each handoff, owner, dependency, tool budget, and returned evidence; run the critic on the merged output and do not accept a narrative without artifacts.

## Release references

- [Source archive index](../../docs/skill-source-archive/README.md)


## Domain-specific cognitive depth (v0.9.2)

### Orchestration: blind-spot traps
- **Likely false confidence:** A retry is not a recovery plan; preserve task identity and idempotency keys across handoffs.
- **Adversarial case to simulate:** Concurrent workers may both believe they own a task; leases need expiry and fencing tokens.

### Hard invariants
- At most one authoritative terminal decision per task; every transition must be allowed and append-only.
- Never report a property as verified without a reproducible check or authoritative evidence.
- State trade-offs explicitly: correctness vs. latency, safety vs. convenience, and complexity vs. operability; choose based on the task's declared constraints rather than maximizing one dimension blindly.

### Required specialist self-check
Before implementation, write one domain-specific counterexample that would falsify the proposed design. Convert the invariant above into a test or reviewable evidence item. After implementation, test the counterexample and report the exact command/result; if it cannot be tested, mark it **UNVERIFIED**.
