---
name: nodejs-production-performance
description: Node.js production readiness for observability, event-loop safety, graceful shutdown, Docker runtime, resource limits, and measurable performance. Use when preparing or reviewing a Node.js service for deployment or load.
version: 0.6.0
---

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
