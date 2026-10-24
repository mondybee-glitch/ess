---
name: responsive-cross-platform
description: "Canonical EES specialist for Responsive UI & cross-platform; merges 2 compatible source capabilities while preserving their original IDs as aliases."
---

# Responsive UI & cross-platform — Canonical Engineering Skill

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

Canonical ID: `responsive-cross-platform`  
Source capability aliases: `mobile-desktop-development`, `responsive-utility-engineering`.

The original source documents are retained under `../../docs/skill-source-archive/` for traceability. The sections below preserve source-specific procedures; resolve overlaps by the stricter safety invariant and record material conflicts rather than silently discarding them.



---

## Preserved specialist module: `mobile-desktop-development`

Source capability: `mobile-desktop-development`.

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

---

## Preserved specialist module: `responsive-utility-engineering`

Source capability: `responsive-utility-engineering`.

# Responsive Utility Engineering

## Use when
Use when designing a mobile-first layout system, grid, spacing utilities, visibility helpers, responsive components, or cross-viewport behavior.

## Do not use when
Do not use for a single fixed-size artifact or for backend APIs.

## Required inputs
Require content priorities, minimum and maximum widths, breakpoints, grid/container rules, overflow policy, direction support, target devices, and visual acceptance references.

## Workflow
1. Start from the smallest useful layout and progressively add columns, navigation, density, and affordances as space allows.
2. Define container, gutter, grid, and utility behavior as constraints. Avoid breakpoint-specific patches that contradict the component's content model.
3. Test long text, localization, zoom, touch targets, empty states, errors, tables, images, and nested components at each relevant width.
4. Prefer logical properties for direction-sensitive spacing and alignment. Check scrollbars and overflow in LTR, RTL, and mixed content.
5. Keep utilities composable but bounded. Document precedence and avoid a class combination that creates invalid or inaccessible states.
6. Capture representative screenshots and compare them against the acceptance reference; investigate differences instead of hiding them with arbitrary overrides.

## Pass/fail checks
Pass only when content remains usable at target widths and zoom, overflow is intentional, direction behavior is correct, utility precedence is predictable, and visual evidence covers states rather than only the happy path.

Required commands or procedures: run responsive browser checks; test zoom and long content; inspect computed layout and overflow; capture screenshots at agreed viewports; run accessibility checks.

## Hand-offs
Hand off semantic interaction to `accessible-component-behavior`, tokens to `design-system-theming-rtl`, and implementation regression to `frontend-development` and `software-testing`.

## Evidence to report
Report viewport matrix, zoom/localization cases, overflow findings, screenshots, commands, and unresolved browser differences.

## Release references

- [Source archive index](../../docs/skill-source-archive/README.md)


## Domain-specific cognitive depth (v0.9.2)

### Responsive cross-platform UI: blind-spot traps
- **Likely false confidence:** A layout that fits one viewport may fail at text zoom, localization, or touch input.
- **Adversarial case to simulate:** Fixed widths and hover-only interactions break on mobile and assistive devices.

### Hard invariants
- Test narrow/wide breakpoints, zoom, long content, touch targets, and keyboard parity.
- Never report a property as verified without a reproducible check or authoritative evidence.
- State trade-offs explicitly: correctness vs. latency, safety vs. convenience, and complexity vs. operability; choose based on the task's declared constraints rather than maximizing one dimension blindly.

### Required specialist self-check
Before implementation, write one domain-specific counterexample that would falsify the proposed design. Convert the invariant above into a test or reviewable evidence item. After implementation, test the counterexample and report the exact command/result; if it cannot be tested, mark it **UNVERIFIED**.
