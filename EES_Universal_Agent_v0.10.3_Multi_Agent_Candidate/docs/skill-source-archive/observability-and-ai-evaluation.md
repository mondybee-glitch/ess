---
name: observability-and-ai-evaluation
description: Privacy-conscious infrastructure and AI observability covering metrics, traces, alerts, prompts, datasets, experiments, cost, latency, quality, and operational evidence.
version: 0.6.0
---

# Observability And Ai Evaluation

## Use when
When establishing AI tracing/evaluation or authorized infrastructure metrics, alerts, anomaly, replication, and read-only MCP workflows.

## Do not use when
Do not use when the task does not match the stated domain, lacks required authorization, or is a simpler task owned by another specialist.

## Required inputs
telemetry schema and minimization policy; authorized metrics/logs/traces; evaluation datasets and retention policy; deployment topology and access controls.

## Purpose
Instrument and evaluate AI and infrastructure systems with data minimization, masking, trace/metric contracts, reproducible experiments, alert triage, and clear limits on what telemetry can prove.

## Workflow
1. Confirm scope, authorization, versions, data classification, and acceptance criteria before acting.
2. Separate planning, read-only inspection, implementation or analysis, and verification. Keep side effects behind explicit approval.
3. Record source evidence, assumptions, exact commands, artifacts, and unresolved uncertainty. Never infer success from intent, generated text, or a partial check.
4. Compose only the secondary skills that own distinct controls; hand off implementation, testing, security, and release responsibilities explicitly.

## Pass/fail checks
Pass only when the required inputs are present, boundaries are respected, outputs are reproducible enough for the stated claim, and incomplete or failed checks are reported as such.

Required outputs: dashboards and alert triage; evaluation report; latency/cost/quality trends; retention/masking/escalation recommendations.

## Safety and limits
Do not collect sensitive telemetry without authorization. Redact secrets and personal data; keep runtime enforcement in appropriate guardrail layers. Do not claim telemetry alone proves root cause or safety.

## Verification
- Run PII/secret masking and trace/metric schema tests.
- Test alert deduplication, retention, backup/restore, and read-only authorization.
- Reproduce evaluation results with model/dataset/version metadata and human review.

## Hand-offs
Hand off implementation, testing, security, and release responsibilities to the selected specialist owners; do not silently duplicate their work.

## Evidence to report
Report selected sources and revisions, authorization and scope, commands and exit codes, artifacts, coverage limits, risks, handoffs, and what remains Unverified.
