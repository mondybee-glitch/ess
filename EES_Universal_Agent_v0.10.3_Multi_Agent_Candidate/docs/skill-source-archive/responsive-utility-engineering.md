---
name: responsive-utility-engineering
description: Responsive utility engineering for mobile-first layout, grid constraints, breakpoint behavior, logical properties, component composition, and visual regression evidence. Use when implementing responsive pages or a utility layer.
version: 0.6.0
---

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
