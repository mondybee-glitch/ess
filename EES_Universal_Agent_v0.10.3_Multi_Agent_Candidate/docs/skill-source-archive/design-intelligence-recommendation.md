---
name: design-intelligence-recommendation
description: Evidence-driven design intelligence for mapping product requirements to information architecture, visual direction, typography, color, responsive behavior, accessibility, anti-patterns, and technology constraints. Use when generating or reviewing a project-specific design system.
version: 0.6.0
---

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
