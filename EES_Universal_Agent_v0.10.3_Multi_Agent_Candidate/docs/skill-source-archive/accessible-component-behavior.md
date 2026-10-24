---
name: accessible-component-behavior
description: Accessible component behavior for keyboard interaction, focus management, ARIA state, progressive enhancement, dismissal, and reusable JavaScript UI components. Use when implementing or reviewing interactive web components.
version: 0.6.0
---

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
