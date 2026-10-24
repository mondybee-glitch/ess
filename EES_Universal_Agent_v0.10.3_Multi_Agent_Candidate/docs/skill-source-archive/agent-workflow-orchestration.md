---
name: agent-workflow-orchestration
description: Bounded multi-stage agent workflow orchestration with role-scoped delegation, approvals, retries, audit records, queues, and safe external-side-effect gates.
version: 0.6.0
---

# Agent Workflow Orchestration

## Use when
When converting an approved engineering objective into a multi-stage agent workflow or reviewing an agent run, gateway, queue, or integration policy.

## Do not use when
Do not use when the task does not match the stated domain, lacks required authorization, or is a simpler task owned by another specialist.

## Required inputs
approved objective and repository scope; constraints, acceptance criteria, stop conditions; allowed tools, services, identities, and data classes.

## Purpose
Turn an approved objective into a dependency-aware workflow with read-only reconnaissance, capability assignments, explicit handoffs, budgets, retry policy, approval checkpoints, and a final audit.

## Workflow
1. Confirm scope, authorization, versions, data classification, and acceptance criteria before acting.
2. Separate planning, read-only inspection, implementation or analysis, and verification. Keep side effects behind explicit approval.
3. Record source evidence, assumptions, exact commands, artifacts, and unresolved uncertainty. Never infer success from intent, generated text, or a partial check.
4. Compose only the secondary skills that own distinct controls; hand off implementation, testing, security, and release responsibilities explicitly.

## Pass/fail checks
Pass only when the required inputs are present, boundaries are respected, outputs are reproducible enough for the stated claim, and incomplete or failed checks are reported as such.

Required outputs: workflow plan and dependency graph; role assignments; approval checkpoints; run/audit summary; escalation or halt decision.

## Safety and limits
Use only on authorized systems and accounts. Default to read-only; require confirmation for irreversible, public, financial, destructive, or security-sensitive actions. Do not extend unsupported or vulnerable legacy agent paths.

## Verification
- Exercise delegation isolation, context boundaries, and capability profiles.
- Test retry, timeout, cancellation, backpressure, and budget circuit breakers.
- Require confirmation and audit evidence for destructive or external side effects.

## Hand-offs
Hand off implementation, testing, security, and release responsibilities to the selected specialist owners; do not silently duplicate their work.

## Evidence to report
Report selected sources and revisions, authorization and scope, commands and exit codes, artifacts, coverage limits, risks, handoffs, and what remains Unverified.
