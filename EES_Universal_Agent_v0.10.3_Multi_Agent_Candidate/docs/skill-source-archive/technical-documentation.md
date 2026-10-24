---
name: technical-documentation
description: Write and maintain READMEs, API documentation, runbooks, decision records, user guides, and bilingual Arabic/English technical content, and produce PDF, DOCX, XLSX, or PPTX deliverables. Use for any documentation deliverable.
version: 0.6.0

---

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
Commands run with results, files changed, and anything not verified. Use the status vocabulary from the core [SKILL.md](../../SKILL.md).

## Concrete commands

Build the docs, check links and examples, validate OpenAPI/schema output, and test commands in a clean environment; mark version-specific claims.
