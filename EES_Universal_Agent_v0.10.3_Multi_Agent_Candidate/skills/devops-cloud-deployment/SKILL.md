---
name: devops-cloud-deployment
description: "Canonical EES specialist for DevOps & deployment; merges 2 compatible source capabilities while preserving their original IDs as aliases."
---

# DevOps & deployment — Canonical Engineering Skill

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

Canonical ID: `devops-cloud-deployment`  
Source capability aliases: `cloud-architecture-cost`, `devops-and-deployment`.

The original source documents are retained under `../../docs/skill-source-archive/` for traceability. The sections below preserve source-specific procedures; resolve overlaps by the stricter safety invariant and record material conflicts rather than silently discarding them.



---

## Preserved specialist module: `cloud-architecture-cost`

Source capability: `cloud-architecture-cost`.

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

---

## Preserved specialist module: `devops-and-deployment`

Source capability: `devops-and-deployment`.

# DevOps and Deployment

## Use when
- Dockerfiles, CI pipelines, deploy scripts
- Monitoring, logging, backup and rollback design
- Operational incidents that are not security incidents

## Do not use when
- Writing application logic

## Required inputs
- Hosting target and access method
- Environments and their owners
- Deploy and rollback approvals

## Workflow
1. Detect environments, runtimes, and existing pipeline.
2. Make builds reproducible: lockfiles, pinned base image tag or digest.
3. Pipeline order: lint, test, build, scan, deploy.
4. Deploy in stages or behind a flag; add health checks.
5. Test rollback before relying on it; prove backups by a restore test.
6. Keep secrets in a secret manager; grant least privilege.
7. Monitor latency, traffic, errors, saturation.

## Pass/fail checks
- Container runs as non-root; `.dockerignore` present
- Images and Actions pinned
- No secrets in images, logs, or CI output
- Restore test executed, or backup marked `unverified`
- Production deploy has explicit human approval

## Hand-offs
- security-review for pipeline and image review
- backend-development for migration coordination

## Evidence to report
Commands run with results, files changed, and anything not verified. Use the status vocabulary from the core [SKILL.md](../../docs/skill-source-archive/devops-and-deployment.md).

## Concrete commands

Run `docker build`, `docker run` smoke checks, CI locally where supported, IaC plan rather than apply first, health checks, and a documented rollback command.

## Release references

- [Source archive index](../../docs/skill-source-archive/README.md)


## Domain-specific cognitive depth (v0.9.2)

### DevOps and cloud: blind-spot traps
- **Likely false confidence:** A successful deployment command does not prove healthy traffic or rollback viability.
- **Adversarial case to simulate:** Shared mutable infrastructure and unpinned dependencies make releases irreproducible.

### Hard invariants
- Immutable artifacts, least-privilege identity, health verification, and tested rollback are mandatory.
- Never report a property as verified without a reproducible check or authoritative evidence.
- State trade-offs explicitly: correctness vs. latency, safety vs. convenience, and complexity vs. operability; choose based on the task's declared constraints rather than maximizing one dimension blindly.

### Required specialist self-check
Before implementation, write one domain-specific counterexample that would falsify the proposed design. Convert the invariant above into a test or reviewable evidence item. After implementation, test the counterexample and report the exact command/result; if it cannot be tested, mark it **UNVERIFIED**.
