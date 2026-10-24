---
name: ml-lifecycle-and-synthetic-media-governance
description: Reproducible TensorFlow/Keras ML lifecycle and defensive synthetic-media governance covering data, models, hardware, deployment, consent, provenance, disclosure, and detection.
version: 0.6.0
---

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
