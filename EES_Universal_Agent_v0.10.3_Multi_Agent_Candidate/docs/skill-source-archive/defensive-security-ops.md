---
name: defensive-security-ops
description: Improve system hardening, detection, incident triage, dependency posture, telemetry, and recovery readiness.
version: 0.6.0
---

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
