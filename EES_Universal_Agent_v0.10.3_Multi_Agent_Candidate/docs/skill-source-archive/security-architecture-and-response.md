---
name: security-architecture-and-response
description: Evidence-traceable defensive security architecture, threat modeling, control mapping, incident triage, forensic provenance, detection gaps, and executive reporting.
version: 0.6.0
---

# Security Architecture And Response

## Use when
When reviewing an authorized architecture, artifact set, alert, incident, control baseline, or residual-risk decision.

## Do not use when
Do not use when the task does not match the stated domain, lacks required authorization, or is a simpler task owned by another specialist.

## Required inputs
authorized scope; architecture/code/telemetry/forensic artifacts; applicable framework identifiers; evidence and confidence policy.

## Purpose
Map trust boundaries, threats, controls, evidence, residual risk, detections, and remediation owners while keeping security work authorized, defensive, and auditable.

## Workflow
1. Confirm scope, authorization, versions, data classification, and acceptance criteria before acting.
2. Separate planning, read-only inspection, implementation or analysis, and verification. Keep side effects behind explicit approval.
3. Record source evidence, assumptions, exact commands, artifacts, and unresolved uncertainty. Never infer success from intent, generated text, or a partial check.
4. Compose only the secondary skills that own distinct controls; hand off implementation, testing, security, and release responsibilities explicitly.

## Pass/fail checks
Pass only when the required inputs are present, boundaries are respected, outputs are reproducible enough for the stated claim, and incomplete or failed checks are reported as such.

Required outputs: trust-boundary model; risk register; defensive findings/detections; chain-of-custody or incident summary; cited report.

## Safety and limits
No exploitation, credential theft, persistence, evasion, malware, phishing, unauthorized access, or offensive intrusion. Use read-only collection and isolated labs; preserve chain of custody and minimize sensitive data.

## Verification
- Check framework identifiers, evidence citations, confidence, and unresolved questions.
- Hash and preserve read-only artifacts with provenance.
- Test false positives, missing evidence, and no-weaponization output boundaries.

## Hand-offs
Hand off implementation, testing, security, and release responsibilities to the selected specialist owners; do not silently duplicate their work.

## Evidence to report
Report selected sources and revisions, authorization and scope, commands and exit codes, artifacts, coverage limits, risks, handoffs, and what remains Unverified.
