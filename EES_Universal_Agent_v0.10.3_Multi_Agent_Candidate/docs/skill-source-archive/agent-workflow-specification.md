---
name: agent-workflow-specification
description: Specification-driven task framing, acceptance criteria, architecture decisions, bounded project memory, handoffs, and reproducible agent evaluation.
version: 0.7.2
---

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
