---
name: brand-graphic-design
description: "Canonical EES specialist for Brand & graphic design; merges 3 compatible source capabilities while preserving their original IDs as aliases."
---

# Brand & graphic design — Canonical Engineering Skill

## Hyper-Cognitive Engineering Kernel

Use this protocol for substantive implementation, architecture, debugging, and review tasks. Do not confuse procedural discipline with proof of correctness.

### 1. Inversion and trap hunting
Before choosing an implementation, enumerate the three most plausible production failures. Consider concurrency, partial failure, retries, state loss, malicious inputs, resource exhaustion, and unsafe trust boundaries as applicable. Identify which failure is most severe and how it will be detected.

### 2. Two-stage routing and invariants
Treat this canonical skill as the primary route when its scope matches. Select no more than two complementary guard skills unless evidence shows a real cross-domain dependency. Extract measurable invariants from the relevant specialist modules below and convert them into acceptance criteria before editing.

### 3. Zero-code dry run
For medium-or-higher risk, sketch the input → transformation → persistence → output path; simulate duplicate/concurrent requests and one partial outage; define a rollback or containment path. If rollback is not feasible, state the recovery strategy before implementation.

### 4. Principal-grade execution
Prefer explicit types/contracts, bounded retries, timeouts, cancellation, idempotency, least privilege, and redacted telemetry where applicable. Avoid toy implementations and unresolved TODOs. Do not invent numeric thresholds: use source-backed limits, derive them transparently, or mark them as tunable assumptions.

### 5. Adversarial self-trial and evidence gate
Assume at least one hidden defect remains. Review failure paths, boundaries, and regressions against `checks/catalog.json` and the relevant module constraints. Report VERIFIED only when a reproducible command actually ran against the current file state and its output supports the claim. Otherwise report NOT RUN, PARTIAL, or UNVERIFIED.

## Canonical scope and alias map

Canonical ID: `brand-graphic-design`  
Source capability aliases: `brand-guidelines`, `graphic-design`, `web-artifacts-builder`.

The original source documents are retained under `../../docs/skill-source-archive/` for traceability. The sections below preserve source-specific procedures; resolve overlaps by the stricter safety invariant and record material conflicts rather than silently discarding them.



---

## Preserved specialist module: `brand-guidelines`

Source capability: `brand-guidelines`.

# Brand Guidelines

## Scope and priority
The supplied brand system is the source of truth. Inspect brand guidelines, logo files, design tokens, existing assets, and prior approved work before making stylistic decisions. Never replace a user's brand with Anthropic styling merely because this skill originated from a public Anthropic skill.

## Workflow
1. Identify the brand, audience, medium, and intended outcome. Locate approved logos, colors, typography, imagery, spacing, iconography, voice, and prohibited treatments.
2. Extract tokens into a compact reference: primary/secondary colors, semantic colors, text/background roles, typography scale, spacing, borders, radii, shadows, and motion rules.
3. Check color contrast and readability for actual foreground/background combinations. Preserve hierarchy and do not use color as the only carrier of meaning.
4. Apply the system consistently to page structure, components, charts, forms, buttons, documents, and export assets. Keep logo proportions and clear space; do not recolor or redraw marks without authorization.
5. If guidelines conflict with accessibility, flag the conflict and choose an accessible treatment that preserves brand intent. Do not silently invent official values.
6. For a new brand without a supplied system, propose a clearly labeled draft system and mark it as proposed, not official. Keep tokens semantic and reusable.
7. Verify responsive layouts, light/dark backgrounds where applicable, export fidelity, typography fallbacks, and contrast. Record any unavailable fonts or assets.

## Anthropic-specific styling
Use this subsection only when Anthropic brand styling is explicitly requested. The public `brand-guidelines` reference lists these colors:
- Dark: `#141413`
- Light: `#faf9f5`
- Mid gray: `#b0aea5`
- Light gray: `#e8e6dc`
- Orange accent: `#d97757`
- Blue accent: `#6a9bcc`
- Green accent: `#788c5d`

The reference describes Poppins for larger headings and Lora for body text, with Arial/Georgia fallbacks. Verify current upstream guidance and available font licenses before shipping. These are Anthropic brand values, not default values for unrelated projects.

## Quality gates
- Every brand value is sourced from approved guidance or explicitly marked proposed.
- Correct logo asset and proportions are preserved.
- Contrast and hierarchy are checked; color is not the sole signal.
- Components and exported formats remain visually consistent.
- Deviations and missing assets/fonts are reported.

## Hand-offs
- `ui-ux-design`: layout, usability, and visual hierarchy.
- `design-system-theming-rtl`: token implementation, theming, and RTL concerns.
- `graphic-design`: logo/brand collateral and visual asset production.
- `web-artifacts-builder` or `frontend-development`: apply the brand system to interactive web work.

## Upstream reference
Based on the purpose and publicly documented brand tokens of Anthropic's `skills/brand-guidelines`. This local version is adapted for multi-brand use and does not reproduce upstream assets. Source: https://github.com/anthropics/skills/tree/main/skills/brand-guidelines. See `THIRD_PARTY_NOTICES.md`.

---

## Preserved specialist module: `graphic-design`

Source capability: `graphic-design`.

# Graphic Design and Visual Assets

## Use when
- Original logos, brand guides, flyers, posters, infographics
- Print and web export specifications
- Image cleanup and asset preparation

## Do not use when
- Interface screens (use ui-ux-design)
- Requests to copy a known brand mark or character

## Required inputs
- Audience, channel, and size
- Deliverable formats
- Brand colors and fonts if any
- Licensing status of supplied images and fonts

## Workflow
1. Write a short brief: audience, message, channel, sizes, formats.
2. Produce 2 or 3 distinct concepts.
3. Build a type and color system; prefer vector (SVG).
4. Test at small size and in one color.
5. Export per channel: print 300 dpi, CMYK, 3 mm bleed; web sRGB in SVG, WebP, or AVIF; social at platform sizes.
6. Check font and image licenses; for Arabic use fonts with proper joining and test shaping.

## Pass/fail checks
- Logo legible at 32 px and in one color
- Bleed and safe margins present for print
- No unlicensed fonts or images
- Nothing derived from an identifiable existing mark

## Hand-offs
- ui-ux-design for UI use of the brand
- technical-documentation for brand guideline docs

## Evidence to report
Commands run with results, files changed, and anything not verified. Use the status vocabulary from the core [SKILL.md](../../docs/skill-source-archive/graphic-design.md).

## Concrete commands

Validate dimensions, color profile, font licensing, export format, transparency, and print/web resolution; compare the exported artifact with the acceptance reference.

---

## Preserved specialist module: `web-artifacts-builder`

Source capability: `web-artifacts-builder`.

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

## Release references

- [Source archive index](../../docs/skill-source-archive/README.md)


## Domain-specific cognitive depth (v0.9.2)

### Brand and graphic design: blind-spot traps
- **Likely false confidence:** Visual polish can conflict with brand consistency, legibility, and production constraints.
- **Adversarial case to simulate:** Color contrast and type scale fail across real assets, languages, and small screens.

### Hard invariants
- Use approved tokens and source assets; verify contrast, export dimensions, and usage rights.
- Never report a property as verified without a reproducible check or authoritative evidence.
- State trade-offs explicitly: correctness vs. latency, safety vs. convenience, and complexity vs. operability; choose based on the task's declared constraints rather than maximizing one dimension blindly.

### Required specialist self-check
Before implementation, write one domain-specific counterexample that would falsify the proposed design. Convert the invariant above into a test or reviewable evidence item. After implementation, test the counterexample and report the exact command/result; if it cannot be tested, mark it **UNVERIFIED**.
