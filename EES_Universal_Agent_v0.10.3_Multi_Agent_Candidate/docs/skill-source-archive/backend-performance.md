---
name: backend-performance
description: Measured backend latency, throughput, resource use, database behavior, profiling, load testing, and regression analysis.
version: 0.7.2
---

# Backend Performance

## Use when
Investigating slow endpoints, high CPU/memory, query bottlenecks, throughput ceilings, queue lag, or performance regressions.

## Do not use when
There is no measurable symptom or baseline and the proposed optimization is based only on intuition.

## Required inputs
Representative workload, environment/build version, latency/throughput/error baseline, resource metrics, dataset scale, performance target, and constraints on load generation.

## Workflow
1. Define the performance question before changing code: metric, percentile, workload, concurrency, sample size, and pass threshold. Preserve an unmodified baseline.
2. Reproduce the issue in a controlled environment and record warm-up, hardware/runtime, dataset, cache state, and competing load. Never compare materially different test conditions as a valid speedup.
3. Profile before optimizing. Inspect CPU, allocations, memory, query plans, lock contention, network calls, queue waits, and serialization to identify the dominant measured cost.
4. Form a falsifiable hypothesis and change one major factor at a time. Prefer algorithmic and query fixes over speculative caching or parallelism that changes semantics.
5. Re-run the same workload and include p50/p95/p99, throughput, error rate, resource use, confidence/variability, and sample count. Check worst-case and tail behavior, not only averages.
6. Test regressions, saturation behavior, timeouts, backpressure, and recovery after load. Validate that optimizations do not weaken authorization, consistency, observability, or resource caps.
7. State limits: a microbenchmark does not imply production capacity, and a synthetic load test does not prove real-user experience.

## Pass/fail checks
Baseline and after measurements are reproducible; the bottleneck is evidence-backed; required percentile/throughput targets pass; errors and resources do not regress beyond policy; limitations and test conditions are reported.

## Hand-offs
Coordinate with database-engineering for query/schema tuning, backend-observability for metrics, and backend-reliability-recovery for saturation/backpressure.

## Evidence to report
Workload and environment, profiler/query plan, exact commands, p50/p95/p99, throughput/error/resource data, sample size, baseline comparison, and trade-offs.
