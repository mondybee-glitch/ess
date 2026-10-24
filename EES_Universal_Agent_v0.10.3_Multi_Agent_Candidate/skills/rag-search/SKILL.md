---
name: rag-search
description: "Canonical EES specialist for RAG & search; merges 2 compatible source capabilities while preserving their original IDs as aliases."
---

# RAG & search — Canonical Engineering Skill

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

Canonical ID: `rag-search`  
Source capability aliases: `rag-ingestion-and-vector-retrieval`, `search-retrieval`.

The original source documents are retained under `../../docs/skill-source-archive/` for traceability. The sections below preserve source-specific procedures; resolve overlaps by the stricter safety invariant and record material conflicts rather than silently discarding them.



---

## Preserved specialist module: `rag-ingestion-and-vector-retrieval`

Source capability: `rag-ingestion-and-vector-retrieval`.

# Rag Ingestion And Vector Retrieval

## Use when
When designing an authorized self-hosted knowledge or retrieval system using durable ingestion, vector search, plugins, or hybrid ranking.

## Do not use when
Do not use when the task does not match the stated domain, lacks required authorization, or is a simpler task owned by another specialist.

## Required inputs
consented content and credentials; corpus/tenant permissions; idempotency/versioning and retention policy; vector schema and relevance set.

## Purpose
Design authorized content pipelines that preserve source/version offsets, quarantine failures, isolate connectors/plugins, evaluate relevance, and secure vector storage and retrieval.

## Workflow
1. Confirm scope, authorization, versions, data classification, and acceptance criteria before acting.
2. Separate planning, read-only inspection, implementation or analysis, and verification. Keep side effects behind explicit approval.
3. Record source evidence, assumptions, exact commands, artifacts, and unresolved uncertainty. Never infer success from intent, generated text, or a partial check.
4. Compose only the secondary skills that own distinct controls; hand off implementation, testing, security, and release responsibilities explicitly.

## Pass/fail checks
Pass only when the required inputs are present, boundaries are respected, outputs are reproducible enough for the stated claim, and incomplete or failed checks are reported as such.

Required outputs: ingestion receipts/quarantine; versioned citations and results; retrieval evaluation; plugin/security review; backup/migration plan.

## Safety and limits
Ingest only authorized data. Secure vector stores, restrict tenants, verify plugin/model egress, isolate untrusted plugins, and never expose raw credentials or confidential corpus content.

## Verification
- Test idempotent retry, immutable versions, quarantine, and partial search states.
- Verify authorization re-checks, tenant isolation, and plugin manifest/egress limits.
- Run hybrid-search relevance, snapshot/restore, and schema-migration fixtures.

## Hand-offs
Hand off implementation, testing, security, and release responsibilities to the selected specialist owners; do not silently duplicate their work.

## Evidence to report
Report selected sources and revisions, authorization and scope, commands and exit codes, artifacts, coverage limits, risks, handoffs, and what remains Unverified.

---

## Preserved specialist module: `search-retrieval`

Source capability: `search-retrieval`.

# search-retrieval

## Use when

Use when the main deliverable involves search indexing, retrieval, ranking, relevance, freshness, facets, and zero-result behavior.

## Do not use when

Do not load this skill for simple database lookup with no search quality requirement.

## Required inputs

Require documents, fields, analyzer, language, relevance metric, freshness, privacy, index lifecycle, query budget.

## Workflow

define relevance and test set; build index; evaluate recall/precision/NDCG or project metric; test updates, deletes, permissions, facets, and failures

## Pass/fail checks

relevance, permission filtering, freshness, latency, cost, and zero-result behavior meet budgets

Required commands or procedures: run index/fixture tests, relevance judgments, permission negatives, freshness/delete propagation, load, and recovery tests

## Hand-offs

Coordinate with data, backend, SEO, ML, security, and UI/UX. Assign one owner per acceptance criterion and stop when a dependency or authorization is missing.

## Evidence to report

Preserve query set, judgments, metrics, index version, latency/cost, and limitations. Report exact versions, commands, expected/actual results, and what remains Unverified.

## Release references

- [Source archive index](../../docs/skill-source-archive/README.md)


## Domain-specific cognitive depth (v0.9.2)

### RAG and search: blind-spot traps
- **Likely false confidence:** High retrieval similarity does not guarantee relevance, freshness, or authorization.
- **Adversarial case to simulate:** Chunk boundaries and metadata filters can leak cross-tenant content.

### Hard invariants
- Apply ACLs before generation; evaluate recall/precision and freshness; cite retrieved evidence.
- Never report a property as verified without a reproducible check or authoritative evidence.
- State trade-offs explicitly: correctness vs. latency, safety vs. convenience, and complexity vs. operability; choose based on the task's declared constraints rather than maximizing one dimension blindly.

### Required specialist self-check
Before implementation, write one domain-specific counterexample that would falsify the proposed design. Convert the invariant above into a test or reviewable evidence item. After implementation, test the counterexample and report the exact command/result; if it cannot be tested, mark it **UNVERIFIED**.
