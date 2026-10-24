---
name: nodejs-outcome-testing
description: Node.js outcome-oriented testing for APIs, workers, queues, persistence, external calls, and observability. Use when tests must verify more than an HTTP response or when integration and end-to-end reliability is at issue.
version: 0.6.0
---

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
