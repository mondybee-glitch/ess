---
name: web-artifacts-builder
description: Build rich, multi-component interactive web interfaces and shareable browser artifacts with React, TypeScript, Tailwind CSS, reusable UI components, state, and routing. Use for interactive prototypes or complete frontend experiences that need composed components; use frontend-development for routine edits or established production app implementation.
version: 0.7.4
---

# Web Artifacts Builder

## Purpose and routing boundary
Use this skill when the request calls for a multi-component interactive artifact, prototype, dashboard, configurator, multi-step flow, or frontend experience that benefits from shared state, navigation, and a reusable component system. It complements `frontend-development` and `react-component-library-engineering`; it does not replace either. For an existing production application, preserve its stack and conventions instead of forcing an artifact scaffold.

## Required discovery
1. Inspect the repository, framework, package manager, lockfile, build scripts, and existing design tokens before creating files.
2. Clarify the artifact's users, primary tasks, important states, responsive targets, data sources, and delivery format from the request. Ask only if a missing detail materially changes the implementation.
3. Choose the smallest architecture that fits: existing app conventions first; otherwise React + TypeScript + Vite is a reasonable default, with Tailwind and an established component library only when they add value.
4. Distinguish a standalone, self-contained HTML artifact from a deployable app. Do not promise that routing, server-side rendering, APIs, persistence, or external assets will work in a single-file export unless verified.

## Build workflow
1. Translate the request into a short acceptance checklist and map the main user flow.
2. Define component boundaries and a single source of truth for shared state. Avoid duplicate state and unnecessary global state.
3. Implement the complete happy path and meaningful loading, empty, error, disabled, success, and validation states.
4. Use semantic HTML and accessible controls; provide labels, keyboard operation, visible focus, sensible heading order, and reduced-motion support.
5. Make layouts responsive; verify at narrow, medium, and wide viewports. Support RTL and localization when required using `dir`, logical CSS properties, and locale-aware formatting.
6. Use realistic content and a deliberate visual hierarchy. Avoid generic template appearance, excessive centered layouts, gratuitous gradients, identical rounded cards, and arbitrary animation. Respect supplied brand assets and design tokens.
7. Keep secrets and privileged operations out of client code. Treat user content and external data as untrusted; do not add network calls, telemetry, or dependencies without a clear need.
8. Run available lint, typecheck, unit/component tests, and build. Use browser/E2E checks for critical interactions when the tooling is available.
9. If a single-file artifact is requested, verify the produced HTML opens offline or document external dependencies and limitations; do not confuse bundling with security isolation.
10. Report the files changed, commands and outcomes, what was manually exercised, and any remaining gaps.

## Completion gates
- Primary task can be completed without dead controls or placeholder handlers.
- Navigation, forms, dialogs, filters, and state transitions behave as requested.
- Responsive, keyboard, focus, contrast, and RTL checks are recorded when relevant.
- Build output exists and build command passes, or the blocker is clearly stated.
- No invented verification claims; distinguish automated checks from visual/manual review.

## Hand-offs
- `frontend-development`: production application changes and established framework conventions.
- `react-component-library-engineering`: reusable primitives, API design, composition, and package boundaries.
- `ui-ux-design`: unresolved flows, visual direction, and usability critique.
- `browser-e2e-and-test-diagnostics`: browser interaction and regression verification.

## Upstream reference
Inspired by the public Anthropic Agent Skills project, especially `skills/web-artifacts-builder`. This local skill is adapted to the Elite Engineering Suite and is not a promise of compatibility with Claude-specific artifact hosting or upstream scripts. See `references/anthropic-agent-skills-integration.md` and `THIRD_PARTY_NOTICES.md` for provenance and scope.
