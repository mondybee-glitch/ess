---
name: mobile-desktop-development
description: Specialist workflow for mobile and desktop applications, lifecycle, packaging, permissions, offline behavior, and OS integration. Use when the task materially involves this boundary.
version: 0.6.0
---

# mobile-desktop-development

## Use when

Use when the main deliverable involves mobile and desktop applications, lifecycle, packaging, permissions, offline behavior, and OS integration.

## Do not use when

Do not load this skill for web-only changes with no app shell or device target.

## Required inputs

Require target OS/device matrix, SDK versions, signing, entitlements, lifecycle, update and crash policy.

## Workflow

inspect project and SDK; implement lifecycle-safe slice; test permissions, interruption, offline, packaging, signing, and supported devices

## Pass/fail checks

declared devices/OS versions pass launch, navigation, accessibility, offline, update, and crash-recovery checks

Required commands or procedures: run platform tests, build/package/sign verification, simulator/device smoke tests, and size/crash checks

## Hand-offs

Coordinate with frontend, backend, security, devops, UI/UX, and technical platforms. Assign one owner per acceptance criterion and stop when a dependency or authorization is missing.

## Evidence to report

Preserve device matrix, artifacts, logs, screenshots, signing result, and limitations. Report exact versions, commands, expected/actual results, and what remains Unverified.
