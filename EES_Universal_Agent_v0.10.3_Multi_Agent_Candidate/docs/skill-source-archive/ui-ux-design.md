---
name: ui-ux-design
description: Product and interface design: user flows, wireframes, design systems, component specs, responsive layouts, accessibility, usability critique, and Figma work. Use for screens, flows, redesigns, and design review.
version: 0.6.0

---

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
Commands run with results, files changed, and anything not verified. Use the status vocabulary from the core [SKILL.md](../../SKILL.md).

## Concrete commands

Capture named viewport states, keyboard/focus behavior, zoom/reflow, contrast, RTL/LTR and reduced-motion cases; classify visual differences as intentional, approved, or defect.
