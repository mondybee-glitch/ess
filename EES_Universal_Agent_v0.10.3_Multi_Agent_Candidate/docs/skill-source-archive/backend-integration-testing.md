---
name: backend-integration-testing
description: Integration, contract, dependency-failure, environment, and test-data-isolation verification for backend services.
version: 0.7.2
---

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
