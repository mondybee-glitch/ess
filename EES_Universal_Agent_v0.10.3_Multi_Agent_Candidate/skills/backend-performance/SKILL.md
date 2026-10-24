---
name: backend-performance
description: "Canonical EES specialist for Backend performance; merges 2 compatible source capabilities while preserving their original IDs as aliases."
---

# Backend performance — Canonical Engineering Skill

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

Canonical ID: `backend-performance`  
Source capability aliases: `backend-performance`, `nodejs-production-performance`.

The original source documents are retained under `../../docs/skill-source-archive/` for traceability. The sections below preserve source-specific procedures; resolve overlaps by the stricter safety invariant and record material conflicts rather than silently discarding them.



---

## Preserved specialist module: `backend-performance`

Source capability: `backend-performance`.

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

---

## Preserved specialist module: `nodejs-production-performance`

Source capability: `nodejs-production-performance`.

# Node.js Production Performance

## Use when

Use when a Node.js service is being deployed, containerized, load-tested, monitored, or investigated for latency, memory, event-loop, shutdown, or runtime reliability problems.

## Do not use when

Do not use for application feature logic with no production, runtime, deployment, or measurable performance concern.

## Required inputs

Require service topology, Node.js and base-image versions, startup command, resource limits, traffic profile, latency and throughput budgets, shutdown policy, health/readiness semantics, logging and metrics destinations, and rollback authority.

## Workflow

1. Establish a baseline with representative traffic and record runtime, image, dependency, CPU, memory, latency, throughput, error, and event-loop measurements.
2. Inspect CPU-heavy synchronous work, unbounded payloads, blocking filesystem or crypto operations, accidental serial awaits, and excessive allocations. Move work only when measurement and ownership justify it.
3. Define observability around user-facing symptoms and technical signals: uptime, request or job errors, latency, event-loop lag, memory, saturation, logs, and distributed correlation.
4. Verify process lifecycle: direct runtime entry point, signal propagation, readiness versus liveness, draining, queue behavior, connection cleanup, timeout, and forced-stop path.
5. Review container construction for minimal runtime artifacts, non-root execution, lockfile-aware production installation, ignored files, build-time secret avoidance, image scanning, and reproducible tags.
6. Load-test the stated budget, compare before and after, and inspect tail latency and resource saturation. Do not infer scalability from one local run.
7. Prepare release, monitoring, abort, and rollback evidence. Stop before deployment when ownership, access, or rollback is missing.

## Pass/fail checks

Pass only when budgets are explicit, baseline and post-change measurements are comparable, event-loop and resource risks are assessed, lifecycle behavior is exercised, container artifacts are inspectable, and rollback/monitoring criteria are owned.

Required commands or procedures: run the repository's build and production-like start command; inspect the final image; run health/readiness and signal tests; measure latency, errors, memory, CPU, and event-loop behavior; run dependency/image checks available in the environment; record limitations.

## Hand-offs

Provide a measurement plan, runtime/container findings, observability contract, shutdown sequence, release gates, rollback trigger, and exact evidence. Hand off cloud/IAM/cost decisions to cloud and deployment specialists.

## Evidence to report

Report versions, image digest or build identifier, commands and exit codes, workload and sample size, p50/p95/p99 where relevant, CPU/memory/event-loop results, logs/metrics without secrets, monitoring links or absence, and Unverified production assumptions.

## Release references

- [Source archive index](../../docs/skill-source-archive/README.md)


## Domain-specific cognitive depth (v0.9.2)

### Backend performance: blind-spot traps
- **Likely false confidence:** Optimizing average latency can worsen p95/p99 and overload behavior.
- **Adversarial case to simulate:** Unbounded concurrency converts a slow dependency into a system-wide outage.

### Hard invariants
- Measure p50/p95/p99 and resource saturation; concurrency and queues must be bounded.
- Never report a property as verified without a reproducible check or authoritative evidence.
- State trade-offs explicitly: correctness vs. latency, safety vs. convenience, and complexity vs. operability; choose based on the task's declared constraints rather than maximizing one dimension blindly.

### Required specialist self-check
Before implementation, write one domain-specific counterexample that would falsify the proposed design. Convert the invariant above into a test or reviewable evidence item. After implementation, test the counterexample and report the exact command/result; if it cannot be tested, mark it **UNVERIFIED**.
