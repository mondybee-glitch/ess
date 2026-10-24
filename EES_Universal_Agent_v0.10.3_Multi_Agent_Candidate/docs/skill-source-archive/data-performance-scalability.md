---
name: data-performance-scalability
description: Data pipeline performance, throughput/capacity modeling, data quality, reconciliation, partitioning, and scale limits.
version: 0.7.2
---

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
