---
name: documentation-seo
description: "Canonical EES specialist for Documentation & SEO; merges 2 compatible source capabilities while preserving their original IDs as aliases."
---

# Documentation & SEO — Canonical Engineering Skill

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

Canonical ID: `documentation-seo`  
Source capability aliases: `seo-digital-content`, `technical-documentation`.

The original source documents are retained under `../../docs/skill-source-archive/` for traceability. The sections below preserve source-specific procedures; resolve overlaps by the stricter safety invariant and record material conflicts rather than silently discarding them.



---

## Preserved specialist module: `seo-digital-content`

Source capability: `seo-digital-content`.

# seo-digital-content

## Use when

Use when the main deliverable involves SEO, content systems, crawlability, metadata, structured data, localization, and editorial quality.

## Do not use when

Do not load this skill for private non-indexed tools with no content discovery requirement.

## Required inputs

Require route map, content owner, language/direction, canonical policy, sitemap/robots, privacy, freshness.

## Workflow

map public routes/content; render crawler-visible output; set metadata/canonical/schema; test links and languages; record editorial approval

## Pass/fail checks

intended routes are reachable; metadata/schema/links/localization/robots/sitemap match policy; no private leakage

Required commands or procedures: run build, route, HTML, link, structured-data, sitemap/robots, accessibility, and localization checks

## Hand-offs

Coordinate with websites, UI/UX, technical docs, security, analytics, and owner. Assign one owner per acceptance criterion and stop when a dependency or authorization is missing.

## Evidence to report

Preserve route inventory, rendered HTML, reports, screenshots, owner approval, and unverified indexing limits. Report exact versions, commands, expected/actual results, and what remains Unverified.

---

## Preserved specialist module: `technical-documentation`

Source capability: `technical-documentation`.

# Technical Documentation

## Use when
- READMEs, API references, runbooks, ADRs
- Bilingual (Arabic/English) documents
- Converting content into office or PDF formats

## Do not use when
- Inline code comments only

## Required inputs
- Audience and task they must complete
- Source of truth (code, spec)
- Languages and formats required

## Workflow
1. Name the audience and the task the document must enable.
2. Structure: overview, quickstart, reference, troubleshooting.
3. Run every command you document; paste real output.
4. Generate API reference from the contract (OpenAPI) rather than by hand where possible.
5. For bilingual docs write both versions from the same outline and keep a glossary of fixed terms.
6. Check links; version the document.

## Pass/fail checks
- Every quickstart command executed in this run
- OpenAPI validates and matches handlers
- Arabic version has correct RTL rendering
- Both languages have identical step numbering

## Hand-offs
- domain skill that owns the subject
- devops-and-deployment for docs-site builds

## Evidence to report
Commands run with results, files changed, and anything not verified. Use the status vocabulary from the core [SKILL.md](../../docs/skill-source-archive/technical-documentation.md).

## Concrete commands

Build the docs, check links and examples, validate OpenAPI/schema output, and test commands in a clean environment; mark version-specific claims.

## Release references

- [Source archive index](../../docs/skill-source-archive/README.md)


## Domain-specific cognitive depth (v0.9.2)

### Documentation and SEO: blind-spot traps
- **Likely false confidence:** Keyword density is not search quality; misleading structured data harms trust.
- **Adversarial case to simulate:** Canonical, locale, redirect, and sitemap conflicts can deindex correct pages.

### Hard invariants
- Claims must match visible content; canonical/robots/status/structured-data behavior must agree.
- Never report a property as verified without a reproducible check or authoritative evidence.
- State trade-offs explicitly: correctness vs. latency, safety vs. convenience, and complexity vs. operability; choose based on the task's declared constraints rather than maximizing one dimension blindly.

### Required specialist self-check
Before implementation, write one domain-specific counterexample that would falsify the proposed design. Convert the invariant above into a test or reviewable evidence item. After implementation, test the counterexample and report the exact command/result; if it cannot be tested, mark it **UNVERIFIED**.
