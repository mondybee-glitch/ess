---
name: backend-production-readiness
description: Pre-release backend readiness: release gates, migration safety, deployment verification, monitoring, ownership, operational handoff, and rollback.
version: 0.7.2
---

# Backend Production Readiness

## Use when
Preparing a service or backend change for release, deployment, production migration, launch, operational handoff, or readiness review.

## Do not use when
The task is a local prototype with no deployment intent, unless the user explicitly requests a production-readiness assessment.

## Required inputs
Release scope and owner; build artifact/version; test evidence; deployment strategy; data/schema changes; monitoring and SLOs; security/privacy review; rollback or forward-fix plan; and approval boundaries.

## Workflow
1. Freeze the change scope and establish source revision, build identity, environment, feature flags, dependencies, and acceptance criteria. Do not substitute branch name for immutable revision.
2. Collect test results for unit, integration, contract, migration, security, performance, and smoke checks that apply to the change. Record not-run checks explicitly and block if a required check lacks evidence.
3. Review data migrations, backward compatibility, feature-flag defaults, secrets/configuration, permissions, external side effects, and deployment ordering.
4. Confirm dashboards, alerts, runbook, service owner, on-call route, SLO/SLI, and known failure modes. A running process without actionable telemetry is not operational readiness.
5. Define rollout stages and objective stop/rollback triggers. Rehearse rollback or forward recovery where impact warrants it; account for irreversible data changes and old/new version compatibility.
6. Verify artifact provenance and expected runtime/configuration. Run post-deploy smoke checks against a scoped environment and compare actual results to acceptance criteria.
7. Produce a Go/No-Go/Partial decision with missing requirements, approval record scope/expiry, and the exact next safe action. Do not use a weighted score to override a hard blocker.

## Pass/fail checks
Required checks have direct evidence; owner and runbook exist; data and security implications are reviewed; monitoring can detect key failure modes; rollback/recovery is credible; approvals are scoped; no unresolved critical blocker remains.

## Hand-offs
Coordinate with backend-reliability-recovery for recovery testing, backend-observability for telemetry, api-design-contracts for compatibility, and release owner for the final decision.

## Evidence to report
Release revision/artifact, check matrix with exit codes, migration plan, approval record, dashboards/runbook, rollback test, smoke-test results, blockers, and decision rationale.
