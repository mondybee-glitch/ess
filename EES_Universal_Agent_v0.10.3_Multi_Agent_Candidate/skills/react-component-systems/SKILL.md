---
name: react-component-systems
description: "Canonical EES specialist for React & component systems; merges 2 compatible source capabilities while preserving their original IDs as aliases."
---

# React & component systems — Canonical Engineering Skill

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

Canonical ID: `react-component-systems`  
Source capability aliases: `accessible-component-behavior`, `react-component-library-engineering`.

The original source documents are retained under `../../docs/skill-source-archive/` for traceability. The sections below preserve source-specific procedures; resolve overlaps by the stricter safety invariant and record material conflicts rather than silently discarding them.



---

## Preserved specialist module: `accessible-component-behavior`

Source capability: `accessible-component-behavior`.

# Accessible Component Behavior

## Use when
Use when building or reviewing dialogs, menus, dropdowns, tabs, tooltips, carousels, toasts, drawers, form controls, or any JavaScript-enhanced component.

## Do not use when
Do not use for CSS-only styling with no interaction or for server-only accessibility concerns.

## Required inputs
Require component state model, trigger and target relationships, keyboard contract, focus policy, dismissal rules, screen-reader expectations, reduced-motion policy, browser matrix, and progressive-enhancement fallback.

## Workflow
1. Define states and transitions before writing handlers. Distinguish open/closed, active/inactive, valid/invalid, loading/complete, and disabled/unavailable.
2. Use native HTML semantics first. Add ARIA only when it expresses a real state or relationship and keep attributes synchronized with behavior.
3. Specify keyboard behavior, focus entry, focus return, escape handling, outside-click behavior, and nested-component ownership.
4. Make initialization, disposal, repeated activation, and dynamic DOM changes idempotent. Avoid duplicate listeners and stale state.
5. Keep content available without JavaScript where feasible. Do not make hover or animation the only way to discover or complete an action.
6. Test screen-reader-visible names, focus order, contrast, reduced motion, touch targets, errors, and interrupted transitions.

## Pass/fail checks
Pass only when every state has a semantic representation, keyboard and focus behavior are verified, ARIA reflects actual state, cleanup is safe, and the non-JavaScript or failure path is documented.

Required commands or procedures: run accessibility tooling; exercise keyboard-only and touch paths; inspect accessibility tree; test repeated open/close and dynamic insertion; record browser and assistive-technology limits.

## Hand-offs
Hand off token and visual decisions to `design-system-theming-rtl` and `ui-ux-design`; hand off regression ownership to `software-testing`.

## Evidence to report
Report the state machine, keyboard table, focus traces, accessibility results, browser versions, commands, and unverified assistive-technology cases.

---

## Preserved specialist module: `react-component-library-engineering`

Source capability: `react-component-library-engineering`.

# React Component Library Engineering

## Use when
Use when creating or distributing reusable React components, a component registry, installable templates, live examples, or an agent-facing UI catalog.

## Do not use when
Do not use for one page-local component with no public API or distribution concern.

## Required inputs
Require supported React/runtime versions, component API, styling flavors, installation mechanism, peer dependencies, accessibility contract, demo/data policy, license provenance, and versioning strategy.

## Workflow
1. Define a small public component API with controlled variants, stable defaults, ref and event behavior, and explicit peer dependencies.
2. Keep JS/TS and CSS/Tailwind implementations behaviorally equivalent where both are promised. Do not let a styling flavor change semantics or accessibility.
3. Build a live example for every public component with controls for meaningful states, not only the attractive default.
4. Generate registry metadata, install instructions, prop documentation, route metadata, and search content from a source of truth. Validate generated files.
5. Test keyboard, reduced motion, loading, empty, error, long-content, responsive, and theme states. Keep visual identity separate from functional state.
6. Audit third-party code and license restrictions before redistributing or adapting components. Never copy a component catalog into a new package without permission.

## Pass/fail checks
Pass only when API, demo, docs, registry, and implementation agree; variants are accessible; generated metadata is reproducible; and license/provenance is recorded.

Required commands or procedures: run typecheck, lint, component tests, docs/registry generation, and representative visual checks; inspect package exports and dependency boundaries.

## Hand-offs
Hand off visual direction to `ui-ux-design`, motion to `motion-system-engineering`, and release evidence to `frontend-build-quality`.

## Evidence to report
Report API/variant matrix, supported flavors, commands and exit codes, generated artifact diff, accessibility/visual evidence, dependency/license findings, and unverified browsers.

## Release references

- [Source archive index](../../docs/skill-source-archive/README.md)


## Domain-specific cognitive depth (v0.9.2)

### React component systems: blind-spot traps
- **Likely false confidence:** Memoization is not correctness and can preserve stale closures.
- **Adversarial case to simulate:** Unstable keys, duplicated state, and effect races cause subtle UI corruption.

### Hard invariants
- Single source of truth; stable identity; effect cleanup; test keyboard and async states.
- Never report a property as verified without a reproducible check or authoritative evidence.
- State trade-offs explicitly: correctness vs. latency, safety vs. convenience, and complexity vs. operability; choose based on the task's declared constraints rather than maximizing one dimension blindly.

### Required specialist self-check
Before implementation, write one domain-specific counterexample that would falsify the proposed design. Convert the invariant above into a test or reviewable evidence item. After implementation, test the counterexample and report the exact command/result; if it cannot be tested, mark it **UNVERIFIED**.
