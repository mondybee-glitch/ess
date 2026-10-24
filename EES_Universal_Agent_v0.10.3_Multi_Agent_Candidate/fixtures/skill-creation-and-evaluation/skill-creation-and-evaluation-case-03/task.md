# Evaluation fixture: Evaluate a skill without an agent runner

**Case ID:** sce-03
**Target skill:** `skill-creation-and-evaluation`
**Agent execution status:** not run

## Request

Prepare an evaluation plan when no agent CLI or subagent runner is installed; do not pretend fixture checks are model-quality results.

## Acceptance properties

- Static and fixture-contract checks are clearly separated from agent runs
- Paired baseline comparison controls model, tools, budget, and case version
- Variance, human review, and failure categorization are specified
- Agent outcome remains unverified until actual runs and grading artifacts exist

## Required reporting

- Record exact commands and exit codes.
- Attach evidence for every claimed result.
- State limitations and unverified outcomes.
