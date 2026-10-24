---
name: css-motion-performance
description: CSS motion performance engineering for transform/opacity choices, layout stability, paint/compositing cost, timing budgets, and measurable animation regressions. Use when animation affects smoothness, battery, input latency, or page performance.
version: 0.6.0
---

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
