---
name: motion-system-engineering
description: Motion system engineering for naming, composition, timing tokens, JavaScript coordination, custom CSS builds, and regression verification. Use when a product needs a reusable animation system rather than isolated effects.
version: 0.6.0
---

# Motion System Engineering

## Use when
Use when building a reusable motion system, naming animation utilities, coordinating CSS with JavaScript state, customizing an animation bundle, or reviewing motion consistency across a product.

## Do not use when
Do not use for one unshared transition with no system impact, illustration-only animation, or a library decision unrelated to motion.

## Required inputs
Require supported components and states, naming convention, motion tokens, class or data-attribute API, CSS build tool, browser matrix, JavaScript lifecycle, reduced-motion policy, and bundle/performance budget.

## Workflow
1. Define semantic motion categories such as enter, exit, attention, feedback, and ambient. Map each to allowed purposes and components.
2. Create stable names and tokens for duration, easing, delay, iteration, and reduced-motion behavior. Keep state names separate from animation names.
3. Keep the base motion layer composable and prefixable. Expose a small public API and avoid leaking internal selectors or generated implementation details.
4. Coordinate JavaScript with `animationstart`, `animationend`, cancellation, and class cleanup. Make repeated triggers idempotent and do not use animation completion as the only source of truth for application state.
5. Build only the categories used by the product when the toolchain supports it. Inspect the final unminified and minified artifacts, prefixes, fallbacks, and source maps.
6. Verify visual, accessibility, responsive, and state-transition regressions. Include a demo or reproducible fixture for new motion patterns.

## Pass/fail checks
Pass only when naming/API rules are documented, timing and reduced-motion tokens are consistent, JS cleanup handles interruption, the build artifact is inspected, and visual/state regression evidence exists.

Required commands or procedures: run the CSS build and lint; inspect bundle size and generated selectors; exercise add/remove/retrigger/cancel paths; test reduced motion; capture representative visual states.

## Hand-offs
Hand off component semantics to `ui-ux-design`, CSS implementation to `frontend-development`, asset/motion production to `media-production`, and performance evidence to `css-motion-performance`.

## Evidence to report
Report the motion taxonomy, token table, public API, build commands and exit codes, artifact sizes/hashes, JS event behavior, visual fixtures, reduced-motion evidence, and unverified browser gaps.
