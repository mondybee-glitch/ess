# Evaluation fixture: Diagnose false skill activation

**Case ID:** sce-02
**Target skill:** `skill-creation-and-evaluation`
**Agent execution status:** not run

## Request

A repository has two skills whose descriptions both match “build a REST API”; refine the trigger contract and design positive and near-miss routing cases without changing unrelated skill instructions.

## Acceptance properties

- Overlapping trigger cause is identified
- Positive and near-miss prompts distinguish the intended skill
- Any proposed description is concise and domain-specific
- Routing improvement is marked unverified until the cases are actually run

## Required reporting

- Record exact commands and exit codes.
- Attach evidence for every claimed result.
- State limitations and unverified outcomes.
