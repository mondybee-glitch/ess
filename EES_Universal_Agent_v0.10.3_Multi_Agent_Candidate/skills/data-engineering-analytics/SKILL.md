---
name: data-engineering-analytics
description: "Canonical EES specialist for Data engineering & analytics; merges 2 compatible source capabilities while preserving their original IDs as aliases."
---

# Data engineering & analytics — Canonical Engineering Skill

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

Canonical ID: `data-engineering-analytics`  
Source capability aliases: `data-engineering-analytics`, `data-performance-scalability`.

The original source documents are retained under `../../docs/skill-source-archive/` for traceability. The sections below preserve source-specific procedures; resolve overlaps by the stricter safety invariant and record material conflicts rather than silently discarding them.



---

## Preserved specialist module: `data-engineering-analytics`

Source capability: `data-engineering-analytics`.

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

---

## Preserved specialist module: `data-performance-scalability`

Source capability: `data-performance-scalability`.

# Data Performance Scalability

## Use when
A data or storage workload grows, slows, misses freshness targets, introduces quality issues, or needs a reproducible capacity estimate.

## Do not use when
There is no defined workload, baseline, data volume, or decision to be informed; avoid speculative scale claims from repository size alone.

## Required inputs
Data source/sink, schemas, volume and growth rate, freshness SLA, workload distribution, current throughput/latency, resource limits, cost constraints, and data-quality invariants.

## Workflow
1. Characterize volume, velocity, skew, cardinality, update/delete patterns, peak-to-average ratio, and acceptable freshness/consistency. Preserve a reproducible input sample or synthetic generator.
2. Define invariants for records read, written, rejected, deduplicated, and transformed. Reconcile key counts/checksums and quarantine malformed records with explicit reasons.
3. Capture a baseline using the same hardware/runtime/workload that will be used for comparisons. Include throughput, latency percentiles, CPU/memory/IO, queue lag, and error/rejection rate.
4. Locate the measured bottleneck: source rate, serialization, repartition/shuffle, index scan, join skew, lock contention, network, or sink capacity. Hypothesize before changing architecture.
5. Evaluate partition sizing, batching, concurrency, caching, indexing, backpressure, and incremental processing one factor at a time. Track cost, correctness, and tail latency alongside throughput.
6. Model capacity with explicit assumptions, safety margin, scale trigger, and sensitivity analysis. Label extrapolations from synthetic loads as estimates, not guarantees.
7. Test replay, partial failure, late data, schema evolution, and recovery so performance optimization does not silently lose or duplicate records.

## Pass/fail checks
Data reconciliation balances; pipeline freshness and throughput targets are measured; resource/cost limits are explicit; partial failures are detected; scaling assumptions are reproducible and documented.

## Hand-offs
Coordinate with database-engineering for storage layout, backend-performance for application bottlenecks, and observability-and-ai-evaluation for monitoring freshness and quality.

## Evidence to report
Data profile, workload generator/seed, baseline and candidate metrics, quality reconciliation, resource/cost data, capacity assumptions, and limitations.

## Release references

- [Source archive index](../../docs/skill-source-archive/README.md)


## Domain-specific cognitive depth (v0.9.2)

### Data engineering: blind-spot traps
- **Likely false confidence:** A correct aggregate over incomplete or duplicated events is still wrong.
- **Adversarial case to simulate:** Late-arriving data, timezone boundaries, and schema drift bias metrics.

### Hard invariants
- Define grain, event-time semantics, deduplication key, and reconciliation rules before aggregation.
- Never report a property as verified without a reproducible check or authoritative evidence.
- State trade-offs explicitly: correctness vs. latency, safety vs. convenience, and complexity vs. operability; choose based on the task's declared constraints rather than maximizing one dimension blindly.

### Required specialist self-check
Before implementation, write one domain-specific counterexample that would falsify the proposed design. Convert the invariant above into a test or reviewable evidence item. After implementation, test the counterexample and report the exact command/result; if it cannot be tested, mark it **UNVERIFIED**.
