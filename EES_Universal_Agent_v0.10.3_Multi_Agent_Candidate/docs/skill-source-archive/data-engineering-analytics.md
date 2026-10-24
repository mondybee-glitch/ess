---
name: data-engineering-analytics
description: Specialist workflow for data pipelines, warehouses, events, metrics, lineage, quality, backfills, and dashboards. Use when the task materially involves this boundary.
version: 0.6.0
---

# data-engineering-analytics

## Use when

Use when the main deliverable involves data pipelines, warehouses, events, metrics, lineage, quality, backfills, and dashboards.

## Do not use when

Do not load this skill for single CRUD query with no pipeline or metric contract.

## Required inputs

Require schemas, owners, lineage, freshness, privacy, retention, volume, cost, replay policy.

## Workflow

define source and metric semantics; enforce schema/idempotency; implement pipeline; test corrupt/late/duplicate data; reconcile outputs; rehearse recovery

## Pass/fail checks

quality constraints, freshness, lineage, metric reconciliation, privacy, cost, and recovery criteria pass for declared volume

Required commands or procedures: run unit/integration pipeline tests, sample data checks, replay/backfill, schema evolution, and dashboard reconciliation

## Hand-offs

Coordinate with backend, system-design, security, cloud, ML, and documentation. Assign one owner per acceptance criterion and stop when a dependency or authorization is missing.

## Evidence to report

Preserve schema, lineage, quality report, sample outputs, cost/freshness metrics, and recovery evidence. Report exact versions, commands, expected/actual results, and what remains Unverified.
