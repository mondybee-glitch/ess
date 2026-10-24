---
name: agent-skill-security-intake
description: Defensive intake and release gate for AI-agent skills, MCP artifacts, archives, dependencies, permissions, and tool definitions using bounded static analysis and human review.
version: 0.6.0
---

# Agent Skill Security Intake

## Use when
Before installing, publishing, or materially updating a skill, MCP server, tool definition, archive, or dependency bundle.

## Do not use when
Do not use when the task does not match the stated domain, lacks required authorization, or is a simpler task owned by another specialist.

## Required inputs
local or approved remote artifact; declared permissions and purpose; severity thresholds, resource ceilings, and baseline policy.

## Purpose
Assess candidate agent artifacts before installation or publication, recording findings, completeness, dependencies, permissions, provenance, remediation, suppressions, and approval decisions.

## Workflow
1. Confirm scope, authorization, versions, data classification, and acceptance criteria before acting.
2. Separate planning, read-only inspection, implementation or analysis, and verification. Keep side effects behind explicit approval.
3. Record source evidence, assumptions, exact commands, artifacts, and unresolved uncertainty. Never infer success from intent, generated text, or a partial check.
4. Compose only the secondary skills that own distinct controls; hand off implementation, testing, security, and release responsibilities explicitly.

## Pass/fail checks
Pass only when the required inputs are present, boundaries are respected, outputs are reproducible enough for the stated claim, and incomplete or failed checks are reported as such.

Required outputs: risk-scored JSON/SARIF/Markdown report; completeness record; install/remediate/block recommendation; human approval evidence.

## Safety and limits
Never execute scanned content or upload sensitive inputs to external models without approval. A clean or low-risk result is not proof of safety when coverage is partial; fail closed on incomplete analysis for high-impact decisions.

## Verification
- Run benign and malicious-pattern fixtures with resource bounds.
- Test archive traversal, size/time ceilings, dependency lookup, and partial-analysis handling.
- Require narrow baseline suppressions and human approval for exceptions.

## Hand-offs
Hand off implementation, testing, security, and release responsibilities to the selected specialist owners; do not silently duplicate their work.

## Evidence to report
Report selected sources and revisions, authorization and scope, commands and exit codes, artifacts, coverage limits, risks, handoffs, and what remains Unverified.
