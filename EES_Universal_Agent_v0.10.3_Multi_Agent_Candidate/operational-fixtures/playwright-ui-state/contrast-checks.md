# Visual/accessibility checks

Run `python scripts/wcag_contrast_check.py '#000000' '#FFFFFF'` for a known WCAG AA pass.
Run `python scripts/wcag_contrast_check.py '#777777' '#FFFFFF'` for a known normal-text fail.
The Playwright suite checks keyboard focus, a narrow viewport, and live-region exposure. It is not pixel-diff visual regression and does not replace axe-core or manual screen-reader testing.
