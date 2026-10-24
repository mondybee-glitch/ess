---
name: frontend-quality-and-cross-platform-ui
description: Evidence-backed frontend quality review plus Ionic-specific cross-platform UI, accessibility, responsive, performance, privacy, SEO, and platform-mode validation.
version: 0.6.0
---

# Frontend Quality And Cross Platform Ui

## Use when
For frontend pull requests, launch reviews, or Ionic applications targeting browser, PWA, iOS, or Android presentation modes.

## Do not use when
Do not use when the task does not match the stated domain, lacks required authorization, or is a simpler task owned by another specialist.

## Required inputs
changed components/pages and target platforms; review priorities and budgets; accessibility/privacy requirements; Ionic and binding versions.

## Purpose
Turn frontend changes into a prioritized checklist with measurable findings and verification across keyboard, screen reader, responsive, iOS/Material, PWA, performance, and metadata concerns.

## Workflow
1. Confirm scope, authorization, versions, data classification, and acceptance criteria before acting.
2. Separate planning, read-only inspection, implementation or analysis, and verification. Keep side effects behind explicit approval.
3. Record source evidence, assumptions, exact commands, artifacts, and unresolved uncertainty. Never infer success from intent, generated text, or a partial check.
4. Compose only the secondary skills that own distinct controls; hand off implementation, testing, security, and release responsibilities explicitly.

## Pass/fail checks
Pass only when the required inputs are present, boundaries are respected, outputs are reproducible enough for the stated claim, and incomplete or failed checks are reported as such.

Required outputs: prioritized findings; accessibility/performance evidence; theme/platform compatibility; remediation and verification steps.

## Safety and limits
Use only on authorized code and pages. Security and privacy checks remain defensive engineering checks, not legal advice; do not infer native permissions or plugin guarantees from UI documentation.

## Verification
- Validate rule metadata, sources, exceptions, and verification paths.
- Run keyboard/focus/reflow/contrast and responsive checks.
- Test Ionic lifecycle, form/event behavior, iOS/Material modes, and bundle/performance budgets.

## Hand-offs
Hand off implementation, testing, security, and release responsibilities to the selected specialist owners; do not silently duplicate their work.

## Evidence to report
Report selected sources and revisions, authorization and scope, commands and exit codes, artifacts, coverage limits, risks, handoffs, and what remains Unverified.
