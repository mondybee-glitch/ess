# Release notes — v0.7.3

## Scope
This release adds exactly two skills requested for this iteration:

1. `web-artifacts-builder` — multi-component interactive web artifacts/prototypes with state, navigation, responsive UI, accessibility, and build/test evidence. It complements `frontend-development` and `react-component-library-engineering` rather than replacing them.
2. `brand-guidelines` — consistent application of supplied brand systems. Anthropic colors/typography are scoped to explicit Anthropic-brand requests; unrelated projects keep their own brand.

## Integration details
- Added each skill's `SKILL.md` and `UPSTREAM-PATTERNS.md`.
- Added both capability definitions to `capability-registry.json`.
- Updated package metadata and core skill version to 0.7.3.
- No other Anthropic skills were added in this release.
- No upstream scripts, binaries, font files, or component archives were copied.

## Provenance
Public references:
- https://github.com/anthropics/skills/tree/main/skills/web-artifacts-builder
- https://github.com/anthropics/skills/tree/main/skills/brand-guidelines

This is a documented local adaptation, not a full upstream repository import. See `THIRD_PARTY_NOTICES.md` and `references/anthropic-agent-skills-integration.md`.

## Verification boundary
Package consistency and ZIP integrity are tested during packaging. These checks do not prove the agent performs successfully on real user projects; live agent-run effectiveness remains unverified.
