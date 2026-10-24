---
name: frontend-development
description: Build and modify web UI code (HTML, CSS, JS/TS, React, Vue, Svelte, Next.js and similar), including state, forms, routing, performance, RTL and i18n, and accessibility. Use for any browser-facing code. Not for purely visual design decisions (use ui-ux-design).
version: 0.6.0

---

# Frontend Development

## Use when
- Implementing or changing components, pages, forms, routing
- Fixing layout, responsive, or performance defects
- Adding Arabic/RTL or multilingual support

## Do not use when
- Backend-only changes
- Visual exploration with no code

## Required inputs
- Framework and version from package.json and lockfile
- Design tokens or existing patterns
- Target browsers and viewports

## Workflow
1. Detect the real stack and package manager; locate the nearest existing pattern and reuse it.
2. Trace the state's source of truth before editing; do not create a second owner.
3. Implement the smallest vertical slice with loading, empty, error, and disabled states.
4. Check keyboard operation and visible focus.
5. Check viewports 360, 768, 1280; check RTL when Arabic is supported (`dir`, logical CSS properties).
6. Run lint, typecheck, tests, build; measure with Lighthouse when performance is in scope.

## Pass/fail checks
- Semantic HTML, labelled controls
- Text contrast at least 4.5:1
- Images have width and height (no layout shift)
- LCP under 2.5 s, INP under 200 ms, CLS under 0.1 when measured
- No secrets in the client bundle
- Bundle size diff recorded

## Hand-offs
- ui-ux-design for new flows
- backend-development for contract changes
- software-testing for E2E

## Evidence to report
Commands run with results, files changed, and anything not verified. Use the status vocabulary from the core [SKILL.md](../../SKILL.md).

## Concrete commands

Run the configured lint/type/test/build commands; use Playwright or the project browser runner for keyboard, viewport, and route checks, and record screenshots for visual criteria.
