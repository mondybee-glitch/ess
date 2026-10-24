---
name: api-security
description: "Canonical EES specialist for API security; merges 2 compatible source capabilities while preserving their original IDs as aliases."
---

# API security — Canonical Engineering Skill

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

Canonical ID: `api-security`  
Source capability aliases: `api-security-testing`, `defensive-appsec-assessment`.

The original source documents are retained under `../../docs/skill-source-archive/` for traceability. The sections below preserve source-specific procedures; resolve overlaps by the stricter safety invariant and record material conflicts rather than silently discarding them.



---

## Preserved specialist module: `api-security-testing`

Source capability: `api-security-testing`.

# Api Security Testing

## Use when
Reviewing an API for broken access control, injection, validation gaps, excessive data exposure, mass assignment, rate-limit weaknesses, or unsafe error behavior.

## Do not use when
No authorization for the target exists, the target boundaries are unclear, or the task requests credential theft, persistence, destructive testing, or bypass of licensing/access controls.

## Required inputs
Written target authorization; in-scope hosts and endpoints; excluded systems; test window and rate limits; test accounts/data; stop conditions; and rules for sensitive findings.

## Workflow
1. Confirm scope before sending traffic. Use only designated test accounts and non-production data unless an explicit written authorization says otherwise.
2. Inventory API routes, methods, object IDs, roles, tenant boundaries, input types, upload paths, and state-changing actions. Build tests from trust boundaries rather than a scanner-only checklist.
3. Probe authentication and authorization with paired identities: same role/different owner, different tenant, lower-privilege role, expired token, and unauthenticated call. Verify read and write paths separately.
4. Test input boundaries using benign, bounded payloads; assess schema validation, mass assignment, injection handling, file limits, rate limits, and response differences that reveal account existence.
5. For every finding, preserve minimal reproducible evidence, the exact request conditions, response, side-effect proof, severity rationale, and safe remediation. Redact tokens and personal data.
6. Stop at the first unexpected destructive or out-of-scope effect, service instability, rate-limit breach, or sensitive-data exposure. Do not escalate beyond the approved scope.
7. Re-test fixes with the same conditions and a negative control. A clean scan does not establish complete security.

## Pass/fail checks
Scope and authorization are recorded; test rate and impact remain bounded; sensitive content is redacted; findings are reproducible; remediation is verified with direct evidence; unsupported security claims are excluded.

## Hand-offs
Coordinate with backend-auth-authorization for policy remediation, backend-integration-testing for regression tests, and defensive-automation-and-audit for allowlisted test execution and logging.

## Evidence to report
Authorization scope, test window, endpoints covered, tools/versions, safe request/response excerpts, reproducible findings, remediation evidence, stop events, and untested surfaces.

---

## Preserved specialist module: `defensive-appsec-assessment`

Source capability: `defensive-appsec-assessment`.

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

## Release references

- [Source archive index](../../docs/skill-source-archive/README.md)


## Domain-specific cognitive depth (v0.9.2)

### API security: blind-spot traps
- **Likely false confidence:** Authentication is not authorization; tenant IDs supplied by clients are untrusted.
- **Adversarial case to simulate:** Object-level authorization gaps often survive endpoint-level role checks.

### Hard invariants
- Deny by default; authorize every object/action at the server boundary.
- Never report a property as verified without a reproducible check or authoritative evidence.
- State trade-offs explicitly: correctness vs. latency, safety vs. convenience, and complexity vs. operability; choose based on the task's declared constraints rather than maximizing one dimension blindly.

### Required specialist self-check
Before implementation, write one domain-specific counterexample that would falsify the proposed design. Convert the invariant above into a test or reviewable evidence item. After implementation, test the counterexample and report the exact command/result; if it cannot be tested, mark it **UNVERIFIED**.
