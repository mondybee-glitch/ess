---
name: gitea-platform-operations
description: Authorized Gitea administration and repository operations covering organizations, permissions, reviews, Actions runners, packages, APIs, backups, releases, and migrations.
version: 0.6.0
---

# Gitea Platform Operations

## Use when
When Gitea-specific administration, APIs, Actions runners, package registries, migration, backup, or organization permissions matter.

## Do not use when
Do not use when the task does not match the stated domain, lacks required authorization, or is a simpler task owned by another specialist.

## Required inputs
authorized instance/repository identifiers; scoped token; requested operation; version, runner, branch, package, or backup configuration.

## Purpose
Provide a Gitea-specific operational adapter while keeping repository, organization, runner, package, token, and backup operations least-privileged and version-aware.

## Workflow
1. Confirm scope, authorization, versions, data classification, and acceptance criteria before acting.
2. Separate planning, read-only inspection, implementation or analysis, and verification. Keep side effects behind explicit approval.
3. Record source evidence, assumptions, exact commands, artifacts, and unresolved uncertainty. Never infer success from intent, generated text, or a partial check.
4. Compose only the secondary skills that own distinct controls; hand off implementation, testing, security, and release responsibilities explicitly.

## Pass/fail checks
Pass only when the required inputs are present, boundaries are respected, outputs are reproducible enough for the stated claim, and incomplete or failed checks are reported as such.

Required outputs: validated operation plan; result; runner/permission assessment; audit and rollback notes.

## Safety and limits
Use only on authorized instances and repositories. Protect tokens, isolate trusted runners, confirm permission/destructive changes, and preserve rollback and backup evidence.

## Verification
- Run least-privilege API fixtures and reject out-of-scope identifiers.
- Require confirmation for permission, deletion, migration, and runner changes.
- Rehearse backup/restore and package provenance without production mutation.

## Hand-offs
Hand off implementation, testing, security, and release responsibilities to the selected specialist owners; do not silently duplicate their work.

## Evidence to report
Report selected sources and revisions, authorization and scope, commands and exit codes, artifacts, coverage limits, risks, handoffs, and what remains Unverified.
