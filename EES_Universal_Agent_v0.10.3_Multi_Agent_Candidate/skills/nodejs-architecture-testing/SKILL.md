---
name: nodejs-architecture-testing
description: "Canonical EES specialist for Node.js architecture & testing; merges 2 compatible source capabilities while preserving their original IDs as aliases."
---

# Node.js architecture & testing — Canonical Engineering Skill

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

Canonical ID: `nodejs-architecture-testing`  
Source capability aliases: `nodejs-component-architecture`, `nodejs-outcome-testing`.

The original source documents are retained under `../../docs/skill-source-archive/` for traceability. The sections below preserve source-specific procedures; resolve overlaps by the stricter safety invariant and record material conflicts rather than silently discarding them.



---

## Preserved specialist module: `nodejs-component-architecture`

Source capability: `nodejs-component-architecture`.

# Node.js Component Architecture

## Use when

Use when a Node.js service, worker, CLI, or monorepo needs component boundaries, layered design, configuration ownership, error semantics, or graceful process behavior.

## Do not use when

Do not use as the only specialist for a frontend-only change, a generic API contract change, or a security audit without Node.js architecture impact.

## Required inputs

Require the runtime and package-manager versions, entry points, deployment shape, component map, public interfaces, configuration sources, error taxonomy, shutdown requirements, and the acceptance criteria for compatibility.

## Workflow

1. Map business components before folders. Keep each component's entry points, domain logic, and data access distinguishable.
2. Keep transport objects at the edge. Pass domain inputs and return domain results rather than leaking HTTP or queue objects into core logic.
3. Identify public package exports and internal-only modules. Treat `exports`, package boundaries, and workspace references as compatibility surfaces.
4. Trace configuration from source to consumer. Separate defaults, environment overrides, validation, secrets, and startup failure behavior.
5. Classify failures as operational, programmer, dependency, or shutdown failures. Define who logs, who responds, who retries, and when the process must exit.
6. Design graceful shutdown for signals, in-flight work, listeners, queues, database pools, and forced termination. Verify it rather than merely adding a handler.
7. Hand off concrete boundary decisions to backend, API, security, testing, and deployment specialists when their acceptance criteria are affected.

## Pass/fail checks

Pass only when component ownership is explicit, transport/domain boundaries are testable, configuration is validated before use, public exports are intentional, error ownership is documented, and shutdown behavior has a reproducible test or an explicit Unverified limitation.

Required commands or procedures: inspect package exports and workspace metadata; run configuration validation; exercise representative operational and programmer failures; send a termination signal in a test environment; confirm cleanup, exit code, and retained evidence.

## Hand-offs

Provide a component map, boundary decisions, configuration contract, error taxonomy, shutdown sequence, changed files, and unresolved compatibility risks. Do not silently redesign the system when the repository's conventions contradict the preferred pattern.

## Evidence to report

Report runtime and package-manager versions, commands and exit codes, changed public interfaces, configuration sources without secret values, failure traces with sensitive data redacted, shutdown timing, and what was not exercised.

---

## Preserved specialist module: `nodejs-outcome-testing`

Source capability: `nodejs-outcome-testing`.

# Node.js Outcome Testing

## Use when

Use when testing a Node.js API, worker, event handler, scheduled job, queue consumer, or integration whose behavior includes persistence, outgoing calls, messages, or telemetry.

## Do not use when

Do not use as the primary skill for a pure unit refactor with no behavior change, visual browser testing, or a test-framework installation question with no outcome design.

## Required inputs

Require the trigger and expected behavior, runtime version, test runner, dependencies, data reset strategy, external-service boundaries, queue/database contracts, observability expectations, and acceptable flake budget.

## Workflow

1. Define the flow and list its observable outcomes: response or return value, visible state change, outgoing call, emitted message, and observability event.
2. Assign an assertion or deliberate absence check to each applicable outcome. A successful response is not enough when persistence, messaging, or external effects are part of the contract.
3. Keep test data isolated and reproducible. Prefer per-test setup and teardown over shared mutable seeds; document fixtures and cleanup.
4. Use production-like dependencies for end-to-end paths and controlled doubles for external services. Verify retries, timeouts, duplicate delivery, and out-of-order events where relevant.
5. Test negative and partial failures, not only the happy path. Record whether a failure is a product defect, test defect, environment issue, or flaky result.
6. Run focused tests, then regression tests. Repeat flaky cases only within a declared budget; never convert repeated failure into success.
7. Report coverage together with mutation, assertion, or behavior evidence. Treat line coverage alone as insufficient.

## Pass/fail checks

Pass only when every applicable outcome category has evidence, test data isolation is explained, external boundaries are controlled, negative paths are covered, and the exact commands and results are retained.

Required commands or procedures: run focused tests; exercise success, validation failure, dependency failure, timeout, retry, duplicate, and shutdown paths as applicable; inspect database/message/telemetry effects; record flake attempts and environment versions.

## Hand-offs

Return a behavior-to-outcome matrix, test ownership, fixture/reset strategy, external-service assumptions, failure classification, and evidence paths. Escalate API, security, data, or deployment concerns instead of duplicating their implementation.

## Evidence to report

Report test commands, exit codes, runner and Node versions, per-outcome assertions, fixture identifiers without sensitive data, retries, flaky observations, mutation or assertion evidence, and Unverified outcomes.

## Release references

- [Source archive index](../../docs/skill-source-archive/README.md)


## Domain-specific cognitive depth (v0.9.2)

### Node.js architecture and testing: blind-spot traps
- **Likely false confidence:** A passing test suite can miss unhandled rejections and leaked handles.
- **Adversarial case to simulate:** Event-loop blocking and shared mutable state fail under real concurrency.

### Hard invariants
- Bound async work; close resources; test cancellation, error propagation, and deterministic teardown.
- Never report a property as verified without a reproducible check or authoritative evidence.
- State trade-offs explicitly: correctness vs. latency, safety vs. convenience, and complexity vs. operability; choose based on the task's declared constraints rather than maximizing one dimension blindly.

### Required specialist self-check
Before implementation, write one domain-specific counterexample that would falsify the proposed design. Convert the invariant above into a test or reviewable evidence item. After implementation, test the counterexample and report the exact command/result; if it cannot be tested, mark it **UNVERIFIED**.
