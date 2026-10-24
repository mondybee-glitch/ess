# Anthropic Agent Skills integration record

**Reviewed:** 2026-10-24  
**Upstream:** <https://github.com/anthropics/skills>  
**Integration version:** Elite Engineering Suite v0.7.2

## Decision
Use selected public skills as workflow references rather than importing the full repository or transplanting scripts. The local package keeps its own registry, runtime, safety policy, permission vocabulary, evaluation format and release gates.

## Patterns adapted

| Upstream skill | Local destination | Adaptation |
|---|---|---|
| `skill-creator` | `skills/skill-creation-and-evaluation/SKILL.md` | Narrow skill contracts, trigger positives/near-misses, progressive disclosure, varied evaluation cases, baseline comparisons when an agent runner exists, and truthful agent-status reporting. |
| `webapp-testing` | `skills/browser-e2e-and-test-diagnostics/SKILL.md` and `UPSTREAM-PATTERNS.md` | Readiness-first browser workflow, static/dynamic application split, rendered-state reconnaissance, resilient locators, evidence capture, cleanup and bounded execution. |
| `frontend-design` | `skills/ui-ux-design/SKILL.md` and `DISTINCTIVE-DESIGN-REVIEW.md` | Subject-specific design direction, deliberate typography/layout, critique against generic patterns, user-centered copy, purposeful motion and verification. |
| `mcp-builder` | `skills/mcp-server-engineering/SKILL.md` and `skills/ai-agents-rag-mcp/SKILL.md` | Workflow-first tool design, schemas, transport, per-operation authorization, untrusted-output handling, error/pagination/retry/timeout policy, and client-path integration testing. |

## Licensing and copyright handling

The upstream README describes many sample skills as Apache-2.0 and specifically identifies document-creation skills under `skills/docx`, `skills/pdf`, `skills/pptx`, and `skills/xlsx` as source-available rather than open source. This integration does **not** copy those document-skill implementations. The four selected public skills were reviewed through their upstream pages and are listed by the upstream repository as Apache-2.0; upstream per-skill license files and the repository license remain authoritative for any future verbatim reuse.

The local files above are independently written adaptations of broad workflow ideas and link to upstream locations for provenance. No upstream helper scripts, assets, templates, proprietary document skills, or full `SKILL.md` text were vendored in this release. This record is provenance documentation, not legal advice. Re-check the current upstream license before copying any source files or redistributing them.

## Verification boundary

This record establishes which patterns were considered and where they were implemented. It does not establish that the upstream implementations work in this package, that any LLM agent improves, or that all MCP clients and web browsers are compatible. Agent effectiveness remains unverified until an actual agent runner executes the local evaluation cases and attaches result artifacts.
