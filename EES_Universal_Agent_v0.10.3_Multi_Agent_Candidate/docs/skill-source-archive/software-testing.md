---
name: software-testing
description: Design and run unit, integration, end-to-end (Playwright), regression, contract, and performance tests, and judge whether a test result is trustworthy. Use when adding coverage, validating a change, or evaluating test quality.
version: 0.6.0

---

# Software Testing and QA

## Use when
- Adding tests to code or a fix
- Auditing the quality of an existing suite
- Performance or load measurement

## Do not use when
- Pure refactors already covered by a trusted suite

## Required inputs
- Acceptance criteria
- Test runner and CI command
- Environment and data setup

## Workflow
1. Derive test cases from acceptance criteria, including boundaries and failure paths.
2. Prefer unit and integration tests; reserve E2E for critical flows.
3. Make time, randomness, and data deterministic.
4. Use locators and auto-waiting in Playwright; no fixed sleeps.
5. Mutation spot-check: break the code on purpose; at least one test must fail.
6. For performance: baseline then after, same conditions, report percentiles and sample size.

## Pass/fail checks
- Each acceptance criterion maps to at least one test
- Tests contain assertions about behavior, not just execution
- E2E passes 3 consecutive runs
- Coverage reported for critical paths, not only line percentage

## Hand-offs
- debugging-and-code-repair for discovered defects
- devops-and-deployment for CI integration

## Evidence to report
Commands run with results, files changed, and anything not verified. Use the status vocabulary from the core [SKILL.md](../../SKILL.md).

## Concrete commands

Run the smallest relevant test first, then regression; record flaky attempts, fixture reset, environment, coverage of critical requirements, and exact failure output.
