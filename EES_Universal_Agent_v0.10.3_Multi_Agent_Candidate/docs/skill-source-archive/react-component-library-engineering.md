---
name: react-component-library-engineering
description: React component library engineering for installable variants, JS/TS and CSS/Tailwind parity, prop contracts, live demos, registries, generated docs, and safe customization. Use when building a reusable React component catalog or distributing UI components.
version: 0.6.0
---

# React Component Library Engineering

## Use when
Use when creating or distributing reusable React components, a component registry, installable templates, live examples, or an agent-facing UI catalog.

## Do not use when
Do not use for one page-local component with no public API or distribution concern.

## Required inputs
Require supported React/runtime versions, component API, styling flavors, installation mechanism, peer dependencies, accessibility contract, demo/data policy, license provenance, and versioning strategy.

## Workflow
1. Define a small public component API with controlled variants, stable defaults, ref and event behavior, and explicit peer dependencies.
2. Keep JS/TS and CSS/Tailwind implementations behaviorally equivalent where both are promised. Do not let a styling flavor change semantics or accessibility.
3. Build a live example for every public component with controls for meaningful states, not only the attractive default.
4. Generate registry metadata, install instructions, prop documentation, route metadata, and search content from a source of truth. Validate generated files.
5. Test keyboard, reduced motion, loading, empty, error, long-content, responsive, and theme states. Keep visual identity separate from functional state.
6. Audit third-party code and license restrictions before redistributing or adapting components. Never copy a component catalog into a new package without permission.

## Pass/fail checks
Pass only when API, demo, docs, registry, and implementation agree; variants are accessible; generated metadata is reproducible; and license/provenance is recorded.

Required commands or procedures: run typecheck, lint, component tests, docs/registry generation, and representative visual checks; inspect package exports and dependency boundaries.

## Hand-offs
Hand off visual direction to `ui-ux-design`, motion to `motion-system-engineering`, and release evidence to `frontend-build-quality`.

## Evidence to report
Report API/variant matrix, supported flavors, commands and exit codes, generated artifact diff, accessibility/visual evidence, dependency/license findings, and unverified browsers.
