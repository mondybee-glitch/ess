---
name: cloud-architecture-cost
description: Specialist workflow for cloud architecture, IAM, infrastructure as code, resilience, observability, and cost. Use when the task materially involves this boundary.
version: 0.6.0
---

# cloud-architecture-cost

## Use when

Use when the main deliverable involves cloud architecture, IAM, infrastructure as code, resilience, observability, and cost.

## Do not use when

Do not load this skill for local-only changes with no cloud/infrastructure boundary.

## Required inputs

Require provider/version, account/project, IAM, topology, SLOs, data class, budget, regions, recovery.

## Workflow

map architecture and trust boundaries; least-privilege IAM; define IaC; test plan/apply safely; measure SLO/cost; rehearse recovery

## Pass/fail checks

deployment is reproducible; IAM is bounded; SLO, cost, monitoring, and recovery criteria pass

Required commands or procedures: run IaC plan, policy scan, integration, load/failure injection in authorized environment, cost estimate, and restore checks

## Hand-offs

Coordinate with devops, security, backend, data, system-design, and payments. Assign one owner per acceptance criterion and stop when a dependency or authorization is missing.

## Evidence to report

Preserve plan diff, policy evidence, SLO/cost baseline, logs, recovery result, and approval. Report exact versions, commands, expected/actual results, and what remains Unverified.
