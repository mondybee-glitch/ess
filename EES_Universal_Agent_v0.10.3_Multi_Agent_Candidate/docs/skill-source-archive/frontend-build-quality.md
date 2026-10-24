---
name: frontend-build-quality
description: Frontend build quality for Sass/CSS and JavaScript compilation, linting, type checks, bundle budgets, source maps, dependency locks, documentation validation, and release artifacts. Use when a frontend framework or design system is built and shipped.
version: 0.6.0
---

# Frontend Build Quality

## Use when
Use when changing Sass/CSS or component JavaScript, maintaining a frontend framework, optimizing bundles, or preparing a browser release.

## Do not use when
Do not use for a one-off local style tweak with no build or release impact.

## Required inputs
Require package-manager and runtime versions, source entry points, generated artifacts, build scripts, lockfile policy, browser targets, size budgets, test commands, and release ownership.

## Workflow
1. Inspect the source-to-artifact graph. Identify generated files, source maps, public exports, compatibility builds, and files that must not be edited manually.
2. Run focused CSS/JS lint, type checks, unit or integration tests, then the production build. Keep environment and dependency versions recorded.
3. Check lockfile integrity and dependency source policy. Do not install or execute scripts from an untrusted source without authorization and review.
4. Compare artifact size and public API against budgets. Validate minified and unminified outputs, source maps, prefixes, logical properties, and compatibility targets.
5. Validate documentation examples, accessibility fixtures, visual examples, and generated metadata when the change affects them.
6. Package a reproducible release and record checksums or build identifiers. If a check cannot run, mark the release gate Unverified.

## Pass/fail checks
Pass only when source and generated artifacts agree, focused and relevant regression checks pass, dependency and lockfile policy is satisfied, budgets are measured, and release artifacts are inspectable.

Required commands or procedures: run the repository's lint/build/test scripts; inspect generated diffs; run bundle or size checks; validate docs and examples; record exit codes and artifacts.

## Hand-offs
Hand off CSS semantics to `design-system-theming-rtl`, component behavior to `accessible-component-behavior`, and deployment to `devops-and-deployment`.

## Evidence to report
Report versions, commands and exit codes, changed source and generated files, dependency/lockfile checks, artifact sizes or hashes, browser targets, and unverified gates.
