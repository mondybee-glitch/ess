---
name: defensive-appsec-assessment
description: Authorized, bounded web/API security assessment planning and evidence triage using reviewed scanners or AI-assisted tools without weaponized exploitation procedures.
version: 0.6.0
---

# Defensive Appsec Assessment

## Use when
Only for a written-authorized asset, repository, or staging environment with scope, rate limits, stop conditions, and data handling rules.

## Do not use when
Do not use when the task does not match the stated domain, lacks required authorization, or is a simpler task owned by another specialist.

## Required inputs
owner-approved target and source snapshot; rules of engagement; approved identity; reviewed templates/config; impact limits and reporting destination.

## Purpose
Convert written scope, source context, test identities, rules of engagement, and impact limits into a defensive assessment with evidence, severity, remediation, retest, and explicit incomplete/error states.

## Workflow
1. Confirm scope, authorization, versions, data classification, and acceptance criteria before acting.
2. Separate planning, read-only inspection, implementation or analysis, and verification. Keep side effects behind explicit approval.
3. Record source evidence, assumptions, exact commands, artifacts, and unresolved uncertainty. Never infer success from intent, generated text, or a partial check.
4. Compose only the secondary skills that own distinct controls; hand off implementation, testing, security, and release responsibilities explicitly.

## Pass/fail checks
Pass only when the required inputs are present, boundaries are respected, outputs are reproducible enough for the stated claim, and incomplete or failed checks are reported as such.

Required outputs: scope-checked plan; evidence-backed findings or incomplete/error status; SARIF/JSON/Markdown report; remediation and retest plan.

## Safety and limits
Defensive-only and written-authorized. Exclude exploit chains, credential attacks, persistence, evasion, broad scanning, exfiltration, destructive testing, and unauthorized interception. Prefer synthetic or staging traffic and human-reviewed reports.

## Verification
- Enforce allowlists, authorization records, rate limits, and stop conditions.
- Run only low-impact synthetic fixtures and validate evidence reproducibility.
- Redact secrets and reject untrusted templates/code or partial scans as clean.

## Hand-offs
Hand off implementation, testing, security, and release responsibilities to the selected specialist owners; do not silently duplicate their work.

## Evidence to report
Report selected sources and revisions, authorization and scope, commands and exit codes, artifacts, coverage limits, risks, handoffs, and what remains Unverified.
