---
name: api-integrations
description: Specialist workflow for API contracts, events, queues, webhooks, compatibility, retries, idempotency, and integration observability. Use when the task materially involves this boundary.
version: 0.6.0
---

# api-integrations

## Use when

Use when the main deliverable involves API contracts, events, queues, webhooks, compatibility, retries, idempotency, and integration observability.

## Do not use when

Do not load this skill for local function changes with no external or cross-service boundary.

## Required inputs

Require schemas, owners, versions, compatibility window, auth, timeout, retry, dedupe, ordering, replay, rollout.

## Workflow

define contract; implement validation and idempotency; test old/new clients, duplicates, delays, malformed payloads, and partial failure; instrument and roll out

## Pass/fail checks

old/new combinations and failure cases behave as declared; observability detects violations; rollback or forward-fix exists

Required commands or procedures: run schema/contract, integration, replay, duplicate, timeout, auth, and consumer-driven tests

## Hand-offs

Coordinate with backend, payments, data, security, cloud, and system-design. Assign one owner per acceptance criterion and stop when a dependency or authorization is missing.

## Evidence to report

Preserve schema versions, request/response fixtures, traces, dashboards, and rollout decision. Report exact versions, commands, expected/actual results, and what remains Unverified.
