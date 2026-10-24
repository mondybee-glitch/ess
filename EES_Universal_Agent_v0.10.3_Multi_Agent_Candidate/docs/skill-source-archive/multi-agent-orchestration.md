---
name: multi-agent-orchestration
description: Coordinate several specialist agents on one task: decompose, assign roles, run in parallel or in sequence, run independent critic review, merge results, and resolve conflicts. Use when a task spans two or more independent specialties, is High or Critical risk, or needs independent verification.
version: 0.6.0

---

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
Commands run with results, files changed, and anything not verified. Use the status vocabulary from the core [SKILL.md](../../SKILL.md).

## Concrete commands

Record each handoff, owner, dependency, tool budget, and returned evidence; run the critic on the merged output and do not accept a narrative without artifacts.
