---
name: ui-design-system-accessibility
description: Reusable design-system components, tokens, themes, RTL, semantic accessibility, keyboard behavior, visual regression, and motion preferences.
version: 0.7.2
---

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
