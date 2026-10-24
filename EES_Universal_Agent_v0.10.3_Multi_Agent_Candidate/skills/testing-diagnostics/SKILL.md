---
name: testing-diagnostics
description: "Canonical EES specialist for Testing & diagnostics; merges 3 compatible source capabilities while preserving their original IDs as aliases."
---

# Testing & diagnostics — Canonical Engineering Skill

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

Canonical ID: `testing-diagnostics`  
Source capability aliases: `backend-integration-testing`, `browser-e2e-and-test-diagnostics`, `software-testing`.

The original source documents are retained under `../../docs/skill-source-archive/` for traceability. The sections below preserve source-specific procedures; resolve overlaps by the stricter safety invariant and record material conflicts rather than silently discarding them.



---

## Preserved specialist module: `backend-integration-testing`

Source capability: `backend-integration-testing`.

# Backend Integration Testing

## Use when
Verifying behavior across a service and its database, queue, filesystem, identity provider, or external dependency, especially around contract drift and partial failures.

## Do not use when
A focused pure-function unit test gives sufficient confidence and no boundary behavior is affected.

## Required inputs
Service graph, dependency contracts, supported runtimes, test environment, data fixtures, timeout/retry rules, acceptance criteria, and allowed external-service access.

## Workflow
1. Identify every boundary touched by the change and choose the least expensive test that still exercises the risk. Keep unit, integration, contract, and end-to-end claims distinct.
2. Use deterministic dependencies where possible. Stub time, randomness, network failures, and queue delivery explicitly instead of sleeping or relying on incidental timing.
3. Test valid behavior, schema drift, timeout, cancellation, unavailable dependency, malformed response, authentication failure, retry exhaustion, and partial completion.
4. Verify side effects in the authoritative store. A 200 response is not enough if the database state, message acknowledgement, or external request is wrong.
5. Isolate test data per run/worker. Use unique namespaces, transaction rollbacks, disposable containers, or guaranteed cleanup; fail closed if the configured target appears production-like.
6. Record environment versions, seed data, fixtures, commands, exit codes, logs, and known nondeterminism. Re-run flaky cases under controlled conditions rather than discarding failures.
7. Add regression coverage for each discovered bug and ensure the test fails when the relevant behavior is deliberately broken.

## Pass/fail checks
Failure paths are bounded and asserted; tests are repeatable; test data is isolated; external calls are controlled; state changes are verified; critical regression tests fail under a mutation of the target behavior.

## Hand-offs
Coordinate with api-design-contracts for consumer contracts, async-jobs-messaging for queue semantics, backend-observability for correlation, and software-testing for suite-wide coverage.

## Evidence to report
Boundary matrix, environment/version, fixtures and seed, exact commands/exit codes, artifact paths, flake history, mutation check, and uncovered failure cases.

---

## Preserved specialist module: `browser-e2e-and-test-diagnostics`

Source capability: `browser-e2e-and-test-diagnostics`.

# Browser E2E And Test Diagnostics

## Use when
When testing an authorized web application or API journey across supported browsers or approved device profiles.

## Do not use when
Do not use when the task does not match the stated domain, lacks required authorization, or is a simpler task owned by another specialist.

## Required inputs
allowlisted test target and journey; dedicated identity or sanitized storage state; browser matrix; assertions, fixtures, and artifact policy.

## Purpose
Design reproducible browser tests across Chromium, Firefox, and WebKit using semantic locators, isolated contexts, web-first assertions, controlled fixtures, and secret-safe diagnostics.

## Workflow
1. Confirm scope, authorization, versions, data classification, and acceptance criteria before acting.
2. Separate planning, read-only inspection, implementation or analysis, and verification. Keep side effects behind explicit approval.
3. Record source evidence, assumptions, exact commands, artifacts, and unresolved uncertainty. Never infer success from intent, generated text, or a partial check.
4. Compose only the secondary skills that own distinct controls; hand off implementation, testing, security, and release responsibilities explicitly.

## Pass/fail checks
Pass only when the required inputs are present, boundaries are respected, outputs are reproducible enough for the stated claim, and incomplete or failed checks are reported as such.

Required outputs: deterministic tests; reports and traces; mock/observability records; reproduction and remediation evidence.

## Safety and limits
Use only owned or explicitly authorized targets. Prefer staging and dedicated identities; protect cookies, tokens, traces, screenshots, videos, and network bodies. Limit interception to test mocks and observability.

## Verification
- Run locator/assertion and cross-browser matrix fixtures.
- Test context isolation, cleanup, retries, and failure-only trace capture.
- Verify trace, screenshot, storage-state, and network artifact redaction.

## Hand-offs
Hand off implementation, testing, security, and release responsibilities to the selected specialist owners; do not silently duplicate their work.

## Evidence to report
Report selected sources and revisions, authorization and scope, commands and exit codes, artifacts, coverage limits, risks, handoffs, and what remains Unverified.

---

## Preserved specialist module: `software-testing`

Source capability: `software-testing`.

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
Commands run with results, files changed, and anything not verified. Use the status vocabulary from the core [SKILL.md](../../docs/skill-source-archive/software-testing.md).

## Concrete commands

Run the smallest relevant test first, then regression; record flaky attempts, fixture reset, environment, coverage of critical requirements, and exact failure output.

## Release references

- [Source archive index](../../docs/skill-source-archive/README.md)


## Domain-specific cognitive depth (v0.9.2)

### Testing and diagnostics: blind-spot traps
- **Likely false confidence:** More tests do not help if assertions are weak or tests share the same faulty oracle.
- **Adversarial case to simulate:** Flaky tests and test-only mocks can hide integration defects.

### Hard invariants
- Assert observable outcomes; isolate tests; cover boundaries, concurrency, recovery, and negative cases.
- Never report a property as verified without a reproducible check or authoritative evidence.
- State trade-offs explicitly: correctness vs. latency, safety vs. convenience, and complexity vs. operability; choose based on the task's declared constraints rather than maximizing one dimension blindly.

### Required specialist self-check
Before implementation, write one domain-specific counterexample that would falsify the proposed design. Convert the invariant above into a test or reviewable evidence item. After implementation, test the counterexample and report the exact command/result; if it cannot be tested, mark it **UNVERIFIED**.
