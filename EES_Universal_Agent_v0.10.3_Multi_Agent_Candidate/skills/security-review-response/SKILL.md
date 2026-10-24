---
name: security-review-response
description: "Canonical EES specialist for Security review & response; merges 3 compatible source capabilities while preserving their original IDs as aliases."
---

# Security review & response — Canonical Engineering Skill

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

Canonical ID: `security-review-response`  
Source capability aliases: `defensive-security-ops`, `security-architecture-and-response`, `security-review`.

The original source documents are retained under `../../docs/skill-source-archive/` for traceability. The sections below preserve source-specific procedures; resolve overlaps by the stricter safety invariant and record material conflicts rather than silently discarding them.



---

## Preserved specialist module: `defensive-security-ops`

Source capability: `defensive-security-ops`.

# Defensive Security Ops

## Use when
Use for hardening, logs/alerts, incident triage, dependency and supply-chain posture, backup assurance, and security operations.

## Do not use when
Do not route ordinary feature development here unless operational security or resilience is a substantive requirement.

## Required inputs
System/service inventory, log sources, environment/provider, incident window if relevant, critical assets, and current recovery/monitoring capabilities.

## Workflow
1. Inventory critical assets, privileged identities, internet-facing services, sensitive data, and recovery dependencies.
2. Prioritize patching by exposure and exploitability; assign owner and deadline.
3. Review MFA, least privilege, managed secrets, access reviews, and recovery account separation.
4. Centralize identity, endpoint, DNS, cloud control-plane, and application logs; document signal, threshold, false-positive path, and response owner.
5. Preserve timestamps, sources, hashes, and chain-of-custody notes during triage. Scope affected systems/accounts and first/last observed activity.
6. Contain proportionately and record side effects. Eradicate root cause, rotate affected credentials, patch, validate clean state, restore from trusted sources, and monitor for recurrence.
7. Verify backups through restore drills; review lockfiles, advisories, integrity, build provenance, and unexpected install scripts.

## Pass/fail checks
- Findings have a priority, owner, deadline, and evidence.
- Incident timelines distinguish observed facts from hypotheses.
- Containment and recovery steps include side effects and verification.
- Metrics state window and denominator.
- Restore capability is proven by a drill, not merely by backup existence.

## Hand-offs
Hand off to `security-review` for application flaws; `reverse-engineering` for isolated artifact analysis; `devops-and-deployment` for infrastructure changes and rollout/rollback.

## Evidence to report
Useful diagnostics include `ss -tulpn`, `journalctl --since '1 hour ago'`, `systemctl --failed`, `docker ps --no-trunc`, and `docker inspect CONTAINER` where applicable. Cloud commands depend on provider/context. Track time to detect/contain/recover, log coverage, restore-test success, patch SLA, and recurrence.

## Concrete commands

Use authorized, bounded checks such as `ss -tulpn`, configuration diff, dependency/secret scans, and log timeline analysis; never scan an unapproved target.

---

## Preserved specialist module: `security-architecture-and-response`

Source capability: `security-architecture-and-response`.

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

---

## Preserved specialist module: `security-review`

Source capability: `security-review`.

# Security Review

## Use when
Use for source/config/API review, threat modeling, auth/session/access-control checks, dependency exposure, and remediation validation.

## Do not use when
Do not route a purely visual change here unless it affects sensitive behavior, data, or trust boundaries.

## Required inputs
Repository/configuration, deployment context if relevant, assets and trust boundaries, expected behavior, and any known constraints.

## Workflow
1. Map assets, identities, trust boundaries, entry points, sensitive data, and dependencies.
2. Separate authentication (who) from authorization (what an identity may do).
3. Trace untrusted input to sensitive sinks: SQL, shell, HTML, file paths, deserializers, outbound requests, and logs.
4. Check object-level access on every read/write, session rotation/expiry, CSRF model, upload/parser limits, secrets, error disclosure, and dependency advisories.
5. Run available tools only in the relevant repository: `npm audit --omit=dev`, `pip-audit`, `bandit -r .`, `semgrep --config auto .`, `gitleaks detect --source .`. Confirm scope and installation first.
6. Tie each finding to code/config evidence and a realistic precondition. Distinguish confirmed vulnerabilities from hypotheses.
7. Add regression tests for fixes, rerun relevant checks, and inspect the final diff.

## Pass/fail checks
- Findings include evidence/location, preconditions, impact, remediation, and verification.
- Access control is tested server-side, including object-level boundaries.
- Scan results are reported only when actually executed.
- Secrets are redacted from reports.
- Fixes have regression tests or an explicit reason why not.

## Hand-offs
Hand off to `backend-development` or `frontend-development` for fixes; `software-testing` for independent regression coverage; `defensive-security-ops` for telemetry and incident response.

## Evidence to report
Use `ID | severity | component/location | evidence | preconditions | impact | remediation | verification`. Rank by impact and exploitability; avoid unsupported severity precision.

## Concrete commands

Run the project lint/tests plus authorized SAST, dependency, secret, and negative authorization checks; distinguish confirmed findings from hypotheses and redact evidence.

## Release references

- [Source archive index](../../docs/skill-source-archive/README.md)


## Domain-specific cognitive depth (v0.9.2)

### Security review and response: blind-spot traps
- **Likely false confidence:** Severity labels without exploitability and asset context produce bad prioritization.
- **Adversarial case to simulate:** Logs may expose secrets or incident response may destroy forensic evidence.

### Hard invariants
- Contain first, preserve evidence, rotate exposed credentials, and verify remediation independently.
- Never report a property as verified without a reproducible check or authoritative evidence.
- State trade-offs explicitly: correctness vs. latency, safety vs. convenience, and complexity vs. operability; choose based on the task's declared constraints rather than maximizing one dimension blindly.

### Required specialist self-check
Before implementation, write one domain-specific counterexample that would falsify the proposed design. Convert the invariant above into a test or reviewable evidence item. After implementation, test the counterexample and report the exact command/result; if it cannot be tested, mark it **UNVERIFIED**.
