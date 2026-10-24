---
name: debugging-and-code-repair
description: Reproduce, isolate, and fix defects; refactor safely; review code. Use for bug reports, failing tests, regressions, crashes, and performance regressions.
version: 0.6.0

---

# Debugging and Code Repair

## Use when
- Bug reports and failing tests
- Regressions and crashes
- Refactors that must preserve behavior

## Do not use when
- New features with no defect

## Required inputs
- Observed vs expected behavior
- Version or commit where it appeared
- Logs, stack traces, steps

## Workflow
1. Reproduce first: a failing test or script. If it cannot be reproduced, say so and stop short of patching blind.
2. Minimize the reproduction.
3. Rank hypotheses; test cheapest first; use `git bisect` for regressions.
4. Fix the root cause with the smallest diff.
5. Add a regression test that fails before and passes after.
6. Search for sibling occurrences of the same pattern.
7. Run the full relevant suite.

## Pass/fail checks
- Fail-before and pass-after evidence shown
- Diff contains no unrelated edits (`git diff --stat`)
- Flaky behavior: at most 5 diagnostic reruns, rate recorded
- Root cause stated in one sentence

## Hand-offs
- software-testing for coverage gaps
- security-review when the bug is a vulnerability

## Evidence to report
Commands run with results, files changed, and anything not verified. Use the status vocabulary from the core [SKILL.md](../../SKILL.md).

## Concrete commands

Reproduce first, then run the smallest failing test and the relevant regression set; preserve the failing trace and compare behavior before and after the patch.
