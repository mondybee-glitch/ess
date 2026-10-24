---
name: browser-e2e-and-test-diagnostics
description: Authorized Playwright-based cross-browser end-to-end testing, browser isolation, deterministic mocks, authentication-state hygiene, traces, screenshots, and failure diagnostics.
version: 0.6.0
---

# Browser E2E And Test Diagnostics

## Use when
When testing an authorized web application or API journey across supported browsers or approved device profiles.

## Do not use when
Do not use when the task does not match the stated domain, lacks required authorization, or is a simpler task owned by another specialist.

## Required inputs
allowlisted test target and journey; dedicated identity or sanitized storage state; browser matrix; assertions, fixtures, and artifact policy.

## Purpose
Design reproducible browser tests across Chromium, Firefox, and WebKit using semantic locators, isolated contexts, web-first assertions, controlled fixtures, and secret-safe diagnostics.

## Workflow
1. Confirm scope, authorization, versions, data classification, and acceptance criteria before acting.
2. Separate planning, read-only inspection, implementation or analysis, and verification. Keep side effects behind explicit approval.
3. Record source evidence, assumptions, exact commands, artifacts, and unresolved uncertainty. Never infer success from intent, generated text, or a partial check.
4. Compose only the secondary skills that own distinct controls; hand off implementation, testing, security, and release responsibilities explicitly.

## Pass/fail checks
Pass only when the required inputs are present, boundaries are respected, outputs are reproducible enough for the stated claim, and incomplete or failed checks are reported as such.

Required outputs: deterministic tests; reports and traces; mock/observability records; reproduction and remediation evidence.

## Safety and limits
Use only owned or explicitly authorized targets. Prefer staging and dedicated identities; protect cookies, tokens, traces, screenshots, videos, and network bodies. Limit interception to test mocks and observability.

## Verification
- Run locator/assertion and cross-browser matrix fixtures.
- Test context isolation, cleanup, retries, and failure-only trace capture.
- Verify trace, screenshot, storage-state, and network artifact redaction.

## Hand-offs
Hand off implementation, testing, security, and release responsibilities to the selected specialist owners; do not silently duplicate their work.

## Evidence to report
Report selected sources and revisions, authorization and scope, commands and exit codes, artifacts, coverage limits, risks, handoffs, and what remains Unverified.
