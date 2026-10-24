---
name: frontend-engineering
description: "Canonical EES specialist for Frontend implementation; merges 3 compatible source capabilities while preserving their original IDs as aliases."
---

# Frontend implementation — Canonical Engineering Skill

## Hyper-Cognitive Engineering Kernel

Use this protocol for substantive implementation, architecture, debugging, and review tasks. Do not confuse procedural discipline with proof of correctness.

### 1. Inversion and trap hunting
Before choosing an implementation, enumerate the three most plausible production failures. Consider concurrency, partial failure, retries, state loss, malicious inputs, resource exhaustion, and unsafe trust boundaries as applicable. Identify which failure is most severe and how it will be detected.

### 2. Two-stage routing and invariants
Treat this canonical skill as the primary route when its scope matches. Select no more than two complementary guard skills unless evidence shows a real cross-domain dependency. Extract measurable invariants from the relevant specialist modules below and convert them into acceptance criteria before editing.

### 3. Zero-code dry run
For medium-or-higher risk, sketch the input → transformation → persistence → output path; simulate duplicate/concurrent requests and one partial outage; define a rollback or containment path. If rollback is not feasible, state the recovery strategy before implementation.

### 4. Principal-grade execution
Prefer explicit types/contracts, bounded retries, timeouts, cancellation, idempotency, least privilege, and redacted telemetry where applicable. Avoid toy implementations and unresolved TODOs. Do not invent numeric thresholds: use source-backed limits, derive them transparently, or mark them as tunable assumptions.

### 5. Adversarial self-trial and evidence gate
Assume at least one hidden defect remains. Review failure paths, boundaries, and regressions against `checks/catalog.json` and the relevant module constraints. Report VERIFIED only when a reproducible command actually ran against the current file state and its output supports the claim. Otherwise report NOT RUN, PARTIAL, or UNVERIFIED.

## Canonical scope and alias map

Canonical ID: `frontend-engineering`  
Source capability aliases: `frontend-build-quality`, `frontend-development`, `frontend-quality-and-cross-platform-ui`.

The original source documents are retained under `../../docs/skill-source-archive/` for traceability. The sections below preserve source-specific procedures; resolve overlaps by the stricter safety invariant and record material conflicts rather than silently discarding them.



---

## Preserved specialist module: `frontend-build-quality`

Source capability: `frontend-build-quality`.

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

---

## Preserved specialist module: `frontend-development`

Source capability: `frontend-development`.

# Frontend Development

## Use when
- Implementing or changing components, pages, forms, routing
- Fixing layout, responsive, or performance defects
- Adding Arabic/RTL or multilingual support

## Do not use when
- Backend-only changes
- Visual exploration with no code

## Required inputs
- Framework and version from package.json and lockfile
- Design tokens or existing patterns
- Target browsers and viewports

## Workflow
1. Detect the real stack and package manager; locate the nearest existing pattern and reuse it.
2. Trace the state's source of truth before editing; do not create a second owner.
3. Implement the smallest vertical slice with loading, empty, error, and disabled states.
4. Check keyboard operation and visible focus.
5. Check viewports 360, 768, 1280; check RTL when Arabic is supported (`dir`, logical CSS properties).
6. Run lint, typecheck, tests, build; measure with Lighthouse when performance is in scope.

## Pass/fail checks
- Semantic HTML, labelled controls
- Text contrast at least 4.5:1
- Images have width and height (no layout shift)
- LCP under 2.5 s, INP under 200 ms, CLS under 0.1 when measured
- No secrets in the client bundle
- Bundle size diff recorded

## Hand-offs
- ui-ux-design for new flows
- backend-development for contract changes
- software-testing for E2E

## Evidence to report
Commands run with results, files changed, and anything not verified. Use the status vocabulary from the core [SKILL.md](../../docs/skill-source-archive/frontend-development.md).

## Concrete commands

Run the configured lint/type/test/build commands; use Playwright or the project browser runner for keyboard, viewport, and route checks, and record screenshots for visual criteria.

---

## Preserved specialist module: `frontend-quality-and-cross-platform-ui`

Source capability: `frontend-quality-and-cross-platform-ui`.

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

## Release references

- [Source archive index](../../docs/skill-source-archive/README.md)


## Domain-specific cognitive depth (v0.9.2)

### Frontend engineering: blind-spot traps
- **Likely false confidence:** A component rendering once does not prove hydration, navigation, or async state correctness.
- **Adversarial case to simulate:** Stale requests and optimistic updates can overwrite newer user intent.

### Hard invariants
- Accessible state transitions, race-safe async handling, and production-build verification are required.
- Never report a property as verified without a reproducible check or authoritative evidence.
- State trade-offs explicitly: correctness vs. latency, safety vs. convenience, and complexity vs. operability; choose based on the task's declared constraints rather than maximizing one dimension blindly.

### Required specialist self-check
Before implementation, write one domain-specific counterexample that would falsify the proposed design. Convert the invariant above into a test or reviewable evidence item. After implementation, test the counterexample and report the exact command/result; if it cannot be tested, mark it **UNVERIFIED**.
