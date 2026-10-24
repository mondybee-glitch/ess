---
name: backend-observability
description: Backend logs, metrics, traces, SLOs, actionable alerts, correlation, privacy-safe telemetry, and incident diagnosis.
version: 0.7.2
---

# Backend Observability

## Use when
Adding or changing service instrumentation, alerts, dashboards, SLOs, request correlation, operational runbooks, or audit telemetry.

## Do not use when
The task is purely a code change with no new operational signal or changed failure mode and existing telemetry already proves the required behavior.

## Required inputs
Service map; critical user journeys; known error modes; SLO/SLI targets; telemetry stack; on-call ownership; retention/privacy rules; and existing dashboards/runbooks.

## Workflow
1. Start from user-visible symptoms and failure modes; define signals that distinguish cause from impact. Use metrics for aggregated trends, traces for request paths, logs for contextual events, and audit records for attributable actions.
2. Propagate a stable correlation/trace context across API, queue, worker, and downstream calls. Bound cardinality; do not use raw user IDs, tokens, or arbitrary payload fields as metric labels.
3. Redact credentials, tokens, payment data, and personal data before export. Add seeded-secret tests to verify redaction on both success and exception paths.
4. Define SLI calculations and thresholds from an explicit objective or baseline. Alerts should have an owner, actionable meaning, runbook, severity, and a way to silence known benign conditions.
5. Test both signal presence and signal absence where important. Inject representative errors/timeouts in a safe environment and verify trace, metric, alert, and runbook behavior.
6. Check sampling, retention, cost, access controls, clock skew, and telemetry failure behavior. Observability must not become a synchronous availability dependency unless that is an explicit design choice.
7. Document known blind spots; a dashboard existing is not proof it detects an incident.

## Pass/fail checks
Critical paths are traceable; logs redact sensitive values; metric labels have bounded cardinality; alerts are actionable and owned; SLO math is explicit; injected failures produce expected signals.

## Hand-offs
Coordinate with backend-reliability-recovery for incident response, backend-performance for latency baselines, and backend-production-readiness for on-call handoff.

## Evidence to report
Instrumentation diff, sample trace/log/metric, redaction tests, alert-rule validation, ownership/runbook links, sampling/retention assumptions, and unobserved failure modes.
