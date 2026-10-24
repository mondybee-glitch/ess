---
name: design-system-theming-rtl
description: Design-system theming for tokens, Sass/CSS architecture, responsive breakpoints, logical properties, RTL/LTR parity, and controlled customization. Use when extending a reusable web UI system across themes or directions.
version: 0.6.0
---

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
