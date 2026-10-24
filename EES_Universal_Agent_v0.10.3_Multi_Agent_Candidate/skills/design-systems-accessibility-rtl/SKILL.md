---
name: design-systems-accessibility-rtl
description: "Canonical EES specialist for UX, design systems & RTL; merges 4 compatible source capabilities while preserving their original IDs as aliases."
---

# UX, design systems & RTL — Canonical Engineering Skill

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

Canonical ID: `design-systems-accessibility-rtl`  
Source capability aliases: `design-intelligence-recommendation`, `design-system-theming-rtl`, `ui-design-system-accessibility`, `ui-ux-design`.

The original source documents are retained under `../../docs/skill-source-archive/` for traceability. The sections below preserve source-specific procedures; resolve overlaps by the stricter safety invariant and record material conflicts rather than silently discarding them.



---

## Preserved specialist module: `design-intelligence-recommendation`

Source capability: `design-intelligence-recommendation`.

# Design Intelligence Recommendation

## Use when
Use when turning product requirements into a design system, page map, visual direction, component states, responsive rules, or an evidence-backed UI recommendation.

## Do not use when
Do not use as a substitute for user research, brand approval, accessibility testing, or implementation verification.

## Required inputs
Require product type, audience, primary task, conversion or success goal, content density, brand constraints, platform/stack, locales and direction, device targets, accessibility requirements, and reference examples.

## Workflow
1. Translate requirements into user journeys, page hierarchy, content priorities, and component states before selecting a visual style.
2. Select a coherent visual direction with reasons tied to audience and task. Record rejected alternatives and anti-patterns; do not choose style by trend alone.
3. Define color roles, typography roles, spacing, shape, elevation, icon policy, motion policy, and data-visualization rules as tokens.
4. Design resilient content behavior: long headings, labels, chips, URLs, localization, zoom, text scaling, empty/error states, and RTL/LTR.
5. Specify responsive checkpoints and interaction accessibility: semantic controls, focus, contrast, keyboard, touch targets, reduced motion, and non-color meaning.
6. Produce a compact acceptance checklist and validate representative screens against it. Treat generated recommendations as hypotheses until rendered and tested.

## Pass/fail checks
Pass only when recommendations are traceable to requirements, tokens and anti-patterns are explicit, content resilience and accessibility are covered, and visual acceptance is tested on representative screens.

Required commands or procedures: render key screens; inspect contrast and focus; test 375/768/1024/1440 or project-specific widths; test long/localized content and RTL when applicable; retain comparison evidence.

## Hand-offs
Hand off implementation to `ui-ux-design`, responsive behavior to `responsive-utility-engineering`, and accessibility to `accessible-component-behavior`.

## Evidence to report
Report requirement-to-decision links, rejected alternatives, token choices, page/state map, responsive/accessibility checks, screenshots, and unresolved brand or user-research assumptions.

---

## Preserved specialist module: `design-system-theming-rtl`

Source capability: `design-system-theming-rtl`.

# Design System, Theming, and RTL

## Use when
Use when building or extending a reusable web UI system, theme layer, responsive grid, utility API, or RTL/LTR implementation.

## Do not use when
Do not use for a single isolated component with no shared tokens or for backend-only work.

## Required inputs
Require design tokens, component inventory, supported themes, breakpoints, direction requirements, browser matrix, public class/API conventions, and bundle or compatibility budgets.

## Workflow
1. Establish tokens for color, type, spacing, elevation, radius, motion, and state rather than scattering literals.
2. Define component and utility naming, ownership, and override order. Separate public customization points from generated internals.
3. Model responsive behavior from content constraints, not device names. Record what changes, collapses, wraps, or becomes scrollable at each breakpoint.
4. Use logical properties and direction-aware values where possible. Test mixed-direction content, icons, alignment, forms, tables, and scroll behavior in both LTR and RTL.
5. Keep theme and direction changes independent from component semantics. Preserve contrast, focus, and state colors in every theme.
6. Build a representative visual matrix and inspect compiled CSS, size, specificity, and source maps before release.

## Pass/fail checks
Pass only when token ownership is clear, responsive rules are explicit, RTL and LTR are both checked, theme states preserve contrast and focus, and generated artifacts match the source of truth.

Required commands or procedures: run style lint and CSS build; compare representative screenshots in themes and directions; inspect computed styles and bundle size; record unsupported browsers.

## Hand-offs
Hand off interaction semantics to `accessible-component-behavior`, implementation to `frontend-development`, and visual review to `ui-ux-design`.

## Evidence to report
Report token and breakpoint decisions, direction matrix, theme states, commands and exit codes, screenshots or computed-style evidence, artifact size, and limitations.

---

## Preserved specialist module: `ui-design-system-accessibility`

Source capability: `ui-design-system-accessibility`.

# Ui Design System Accessibility

## Use when
Creating or changing reusable UI components, design tokens, themes, RTL layouts, component APIs, accessibility behavior, or cross-product visual consistency.

## Do not use when
The task is not a UI surface or when a local one-off style change is explicitly preferred over reusable system behavior.

## Required inputs
Design system and code conventions; target viewports; supported languages/directions; browser/device matrix; interaction states; accessibility requirements; and reference screenshots where available.

## Workflow
1. Inspect existing tokens, component primitives, variants, spacing, type scale, and theme conventions before adding new styles. Prefer shared tokens over duplicated constants.
2. Define component API and states: default, hover, focus, active, disabled, loading, error, empty, and responsive/overflow behavior. Separate content from presentation.
3. Use semantic HTML and accessible names. Test keyboard order, focus visibility, focus return in dialogs, screen-reader announcements, label/error association, contrast, and reduced motion.
4. Verify RTL and localization explicitly: logical CSS properties, mirrored directional icons when appropriate, number/date formatting, text expansion, and mixed-direction strings.
5. Capture visual baselines at agreed viewports and compare rendered output after font and asset loading. Review diffs rather than assuming a DOM test catches layout regressions.
6. Ensure tokens produce consistent themes and that contrast is maintained in hover/disabled/error states. Avoid color-only indicators and AI-generated visual effects that conflict with supplied brand direction.
7. Check bundle impact and motion/performance; provide a non-animated or reduced-motion path.

## Pass/fail checks
Keyboard and focus behavior work; semantic/accessibility tests pass; contrast and RTL checks pass; no unintended visual regressions; tokens and variants are reused; responsive overflow and reduced motion are addressed.

## Hand-offs
Coordinate with responsive-utility-engineering for layout behavior, css-motion-performance for motion budget, frontend-quality-and-cross-platform-ui for browser/device coverage, and graphic-design for art assets.

## Evidence to report
Component API/states, token diff, viewport screenshots, accessibility/keyboard checks, contrast results, RTL review, bundle/performance impact, and known deviations.

---

## Preserved specialist module: `ui-ux-design`

Source capability: `ui-ux-design`.

# UI/UX Product Design

## Use when
- New screens, flows, or redesigns
- Design tokens and component libraries
- Heuristic or accessibility critique

## Do not use when
- Backend-only work
- Brand marks and print assets (use graphic-design)

## Required inputs
- Users and their main tasks
- Constraints (brand, platform, languages)
- Existing design system or screenshots

## Workflow
1. Define users, jobs to be done, and success measures.
2. Map the flow before drawing screens.
3. Wireframe, then high fidelity.
4. Define tokens: color roles, type scale, spacing on a 4 or 8 point grid.
5. Specify every state: default, hover, focus, empty, loading, error, disabled.
6. Specify breakpoints and RTL behavior.
7. Check WCAG 2.2 AA; critique against Nielsen heuristics.
8. Deliver a handoff spec developers can implement.

## Pass/fail checks
- Text contrast ratios computed and at least 4.5:1
- Touch targets at least 24 CSS px (WCAG 2.2) and preferably 44
- All states specified
- Findings in critiques have heuristic, severity, and fix

## Hand-offs
- frontend-development for implementation
- graphic-design for brand assets

## Evidence to report
Commands run with results, files changed, and anything not verified. Use the status vocabulary from the core [SKILL.md](../../docs/skill-source-archive/ui-ux-design.md).

## Concrete commands

Capture named viewport states, keyboard/focus behavior, zoom/reflow, contrast, RTL/LTR and reduced-motion cases; classify visual differences as intentional, approved, or defect.

## Release references

- [Source archive index](../../docs/skill-source-archive/README.md)


## Domain-specific cognitive depth (v0.9.2)

### Design systems, accessibility, RTL: blind-spot traps
- **Likely false confidence:** Mirroring layout mechanically can invert semantic direction or icon meaning.
- **Adversarial case to simulate:** Keyboard focus, zoom, screen readers, and mixed-direction text expose hidden failures.

### Hard invariants
- Semantic HTML, visible focus, logical CSS properties, and keyboard parity are required.
- Never report a property as verified without a reproducible check or authoritative evidence.
- State trade-offs explicitly: correctness vs. latency, safety vs. convenience, and complexity vs. operability; choose based on the task's declared constraints rather than maximizing one dimension blindly.

### Required specialist self-check
Before implementation, write one domain-specific counterexample that would falsify the proposed design. Convert the invariant above into a test or reviewable evidence item. After implementation, test the counterexample and report the exact command/result; if it cannot be tested, mark it **UNVERIFIED**.
