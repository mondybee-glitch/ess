---
name: brand-guidelines
description: Apply a supplied brand system consistently across web interfaces, documents, slides, and visual artifacts; use the Anthropic palette and typography only when the user explicitly requests Anthropic styling or the artifact is meant to represent Anthropic.
version: 0.7.4
---

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
