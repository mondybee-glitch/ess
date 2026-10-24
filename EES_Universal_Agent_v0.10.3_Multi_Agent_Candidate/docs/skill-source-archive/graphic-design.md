---
name: graphic-design
description: Visual identity and graphics: logos, brand guidelines, ads, posters, infographics, image editing, print-ready and social/web exports, and preparation of video, motion, and 3D assets. Use for non-UI visual assets. Never reproduces an existing logo, character, or copyrighted artwork.
version: 0.6.0

---

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
Commands run with results, files changed, and anything not verified. Use the status vocabulary from the core [SKILL.md](../../SKILL.md).

## Concrete commands

Validate dimensions, color profile, font licensing, export format, transparency, and print/web resolution; compare the exported artifact with the acceptance reference.
