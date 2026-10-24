---
name: motion-animation
description: "Canonical EES specialist for Motion & animation; merges 3 compatible source capabilities while preserving their original IDs as aliases."
---

# Motion & animation — Canonical Engineering Skill

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

Canonical ID: `motion-animation`  
Source capability aliases: `css-motion-performance`, `motion-system-engineering`, `web-motion-accessibility`.

The original source documents are retained under `../../docs/skill-source-archive/` for traceability. The sections below preserve source-specific procedures; resolve overlaps by the stricter safety invariant and record material conflicts rather than silently discarding them.



---

## Preserved specialist module: `css-motion-performance`

Source capability: `css-motion-performance`.

# CSS Motion Performance

## Use when
Use when CSS animation or transitions cause jank, layout shifts, input delay, excess paint, battery cost, large bundles, or unstable visual performance.

## Do not use when
Do not use for motion aesthetics with no performance concern, server performance, or video rendering.

## Required inputs
Require target devices and viewports, motion property list, frame-rate or latency budget, interaction path, baseline trace, browser versions, and acceptable visual trade-offs.

## Workflow
1. Capture a baseline on representative hardware. Record frame timing, long tasks, input delay, layout shifts, paint/composite behavior, and memory where available.
2. Prefer properties that can be animated without repeated layout when the design allows it. Treat `transform` and `opacity` as hypotheses, not guarantees; verify with a trace.
3. Inspect large elements, root-level motion, expensive filters, box-shadow and layout changes, excessive simultaneous animations, and infinite loops.
4. Bound duration, delay, iteration count, and concurrent animated elements. Avoid solving jank by blindly adding `will-change`; remove hints that do not produce measured benefit.
5. Check overflow, responsive geometry, reduced-motion mode, low-power/mobile behavior, and interruption or cancellation.
6. Re-run the same trace after the change. Keep the change only when the required experience improves without violating accessibility or layout budgets.

## Pass/fail checks
Pass only with comparable before/after evidence, no unacceptable layout or input regression, bounded motion, and a stated device/browser scope. A visual claim without a trace or repeatable observation remains Unverified.

Required commands or procedures: run the project's browser performance tooling; collect a trace for the same flow; inspect long tasks, frame timing, layout shifts, and paint/composite behavior; test reduced motion and a constrained device profile.

## Hand-offs
Hand off design trade-offs to `ui-ux-design`, implementation to `frontend-development`, and release budgets to `devops-and-deployment` or `webdev-seo` when page metrics are affected.

## Evidence to report
Report device/browser, workload, baseline and after measurements, trace locations, animated properties, concurrency and timing budgets, reduced-motion result, and limitations of the measurement.

---

## Preserved specialist module: `motion-system-engineering`

Source capability: `motion-system-engineering`.

# Motion System Engineering

## Use when
Use when building a reusable motion system, naming animation utilities, coordinating CSS with JavaScript state, customizing an animation bundle, or reviewing motion consistency across a product.

## Do not use when
Do not use for one unshared transition with no system impact, illustration-only animation, or a library decision unrelated to motion.

## Required inputs
Require supported components and states, naming convention, motion tokens, class or data-attribute API, CSS build tool, browser matrix, JavaScript lifecycle, reduced-motion policy, and bundle/performance budget.

## Workflow
1. Define semantic motion categories such as enter, exit, attention, feedback, and ambient. Map each to allowed purposes and components.
2. Create stable names and tokens for duration, easing, delay, iteration, and reduced-motion behavior. Keep state names separate from animation names.
3. Keep the base motion layer composable and prefixable. Expose a small public API and avoid leaking internal selectors or generated implementation details.
4. Coordinate JavaScript with `animationstart`, `animationend`, cancellation, and class cleanup. Make repeated triggers idempotent and do not use animation completion as the only source of truth for application state.
5. Build only the categories used by the product when the toolchain supports it. Inspect the final unminified and minified artifacts, prefixes, fallbacks, and source maps.
6. Verify visual, accessibility, responsive, and state-transition regressions. Include a demo or reproducible fixture for new motion patterns.

## Pass/fail checks
Pass only when naming/API rules are documented, timing and reduced-motion tokens are consistent, JS cleanup handles interruption, the build artifact is inspected, and visual/state regression evidence exists.

Required commands or procedures: run the CSS build and lint; inspect bundle size and generated selectors; exercise add/remove/retrigger/cancel paths; test reduced motion; capture representative visual states.

## Hand-offs
Hand off component semantics to `ui-ux-design`, CSS implementation to `frontend-development`, asset/motion production to `media-production`, and performance evidence to `css-motion-performance`.

## Evidence to report
Report the motion taxonomy, token table, public API, build commands and exit codes, artifact sizes/hashes, JS event behavior, visual fixtures, reduced-motion evidence, and unverified browser gaps.

---

## Preserved specialist module: `web-motion-accessibility`

Source capability: `web-motion-accessibility`.

# Web Motion Accessibility

## Use when
Use when adding, reviewing, or debugging web animation, transitions, loading motion, modal transitions, attention cues, or state changes.

## Do not use when
Do not use for static visual design with no motion, video production, or a browser performance issue unrelated to animation.

## Required inputs
Require the user goal for the motion, affected states, keyboard and screen-reader behavior, motion sensitivity requirements, supported browsers, duration/repeat budget, and a static or reduced-motion alternative.

## Workflow
1. Name the product meaning of the motion: orient, confirm, reveal, or direct attention. Reject decorative motion with no user benefit.
2. Preserve the functional state independently of the animation. A user must receive the same content, focus, status, and action path when motion is reduced or unavailable.
3. Implement and test `prefers-reduced-motion: reduce` without overriding the user's preference. Replace large travel or repeated motion with an instant or low-motion state change when appropriate.
4. Check focus order, keyboard operation, screen-reader announcements, loading/error states, and whether motion causes disorientation, flashing, clipping, or unexpected scrollbars.
5. Avoid animating root documents and inline-only elements without a deliberate layout strategy. Keep entrance/exit semantics understandable and reversible.
6. Verify normal, reduced-motion, keyboard, narrow viewport, and interrupted-animation states.

## Pass/fail checks
Pass only when the motion has a stated purpose, reduced-motion behavior is present and tested, functional state and focus remain correct, repeated/flashing motion is bounded, and a non-motion path is documented.

Required commands or procedures: run accessibility checks; emulate reduced motion; exercise keyboard focus and screen-reader-visible state; inspect screenshots or recordings at relevant viewports; record any unverified assistive-technology limitation.

## Hand-offs
Hand off visual timing and composition to `ui-ux-design`, implementation to `frontend-development`, and browser evidence to browser testing. Do not duplicate their ownership.

## Evidence to report
Report the purpose, state diagram, reduced-motion result, focus behavior, viewport evidence, duration/repetition values, browser versions, commands, and unresolved accessibility limits.

## Release references

- [Source archive index](../../docs/skill-source-archive/README.md)


## Domain-specific cognitive depth (v0.9.2)

### Motion and animation: blind-spot traps
- **Likely false confidence:** Animation that looks smooth in a recording may block input or harm vestibular comfort.
- **Adversarial case to simulate:** Layout-triggering animation and uncontrolled loops degrade frame rate and battery.

### Hard invariants
- Prefer transform/opacity, respect reduced motion, and measure interaction latency.
- Never report a property as verified without a reproducible check or authoritative evidence.
- State trade-offs explicitly: correctness vs. latency, safety vs. convenience, and complexity vs. operability; choose based on the task's declared constraints rather than maximizing one dimension blindly.

### Required specialist self-check
Before implementation, write one domain-specific counterexample that would falsify the proposed design. Convert the invariant above into a test or reviewable evidence item. After implementation, test the counterexample and report the exact command/result; if it cannot be tested, mark it **UNVERIFIED**.
