---
name: ml-lifecycle-governance
description: "Canonical EES specialist for ML lifecycle & synthetic media governance; merges 1 compatible source capabilities while preserving their original IDs as aliases."
---

# ML lifecycle & synthetic media governance — Canonical Engineering Skill

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

Canonical ID: `ml-lifecycle-governance`  
Source capability aliases: `ml-lifecycle-and-synthetic-media-governance`.

The original source documents are retained under `../../docs/skill-source-archive/` for traceability. The sections below preserve source-specific procedures; resolve overlaps by the stricter safety invariant and record material conflicts rather than silently discarding them.



---

## Preserved specialist module: `ml-lifecycle-and-synthetic-media-governance`

Source capability: `ml-lifecycle-and-synthetic-media-governance`.

# Ml Lifecycle And Synthetic Media Governance

## Use when
For authorized ML experimentation/deployment or defensive synthetic-media review with owned, synthetic, or explicitly licensed data.

## Do not use when
Do not use when the task does not match the stated domain, lacks required authorization, or is a simpler task owned by another specialist.

## Required inputs
versioned data/model manifests; shapes/dtypes/hardware/backend; consent and rights records; target runtime and resource limits.

## Purpose
Support benign model experiments and deployment handoffs while preventing non-consensual synthetic-media use through rights gates, isolated evaluation, provenance, disclosure, and defensive review.

## Workflow
1. Confirm scope, authorization, versions, data classification, and acceptance criteria before acting.
2. Separate planning, read-only inspection, implementation or analysis, and verification. Keep side effects behind explicit approval.
3. Record source evidence, assumptions, exact commands, artifacts, and unresolved uncertainty. Never infer success from intent, generated text, or a partial check.
4. Compose only the secondary skills that own distinct controls; hand off implementation, testing, security, and release responsibilities explicitly.

## Pass/fail checks
Pass only when the required inputs are present, boundaries are respected, outputs are reproducible enough for the stated claim, and incomplete or failed checks are reported as such.

Required outputs: reproducible experiment record; validated model handoff; consent/provenance decision; detection or incident report.

## Safety and limits
Use only owned, synthetic, or explicitly licensed media. Prohibit impersonation, non-consensual face changes, sexual/exploitative content, fraud, evasion, political deception, harassment, or concealment. Do not provide transformation recipes.

## Verification
- Run schema, leakage, distribution, numerical equivalence, and export compatibility checks.
- Sandbox untrusted models/checkpoints and enforce resource limits.
- Test consent, rights, disclosure, watermark/provenance, and incident-evidence gates.

## Hand-offs
Hand off implementation, testing, security, and release responsibilities to the selected specialist owners; do not silently duplicate their work.

## Evidence to report
Report selected sources and revisions, authorization and scope, commands and exit codes, artifacts, coverage limits, risks, handoffs, and what remains Unverified.

## Release references

- [Source archive index](../../docs/skill-source-archive/README.md)


## Domain-specific cognitive depth (v0.9.2)

### ML lifecycle governance: blind-spot traps
- **Likely false confidence:** Offline metric gains can mask data leakage, drift, or subgroup regressions.
- **Adversarial case to simulate:** Training-serving skew and non-reproducible datasets invalidate comparisons.

### Hard invariants
- Version data, features, code, model, and thresholds; monitor drift and subgroup outcomes.
- Never report a property as verified without a reproducible check or authoritative evidence.
- State trade-offs explicitly: correctness vs. latency, safety vs. convenience, and complexity vs. operability; choose based on the task's declared constraints rather than maximizing one dimension blindly.

### Required specialist self-check
Before implementation, write one domain-specific counterexample that would falsify the proposed design. Convert the invariant above into a test or reviewable evidence item. After implementation, test the counterexample and report the exact command/result; if it cannot be tested, mark it **UNVERIFIED**.
