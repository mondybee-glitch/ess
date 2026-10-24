---
name: rag-ingestion-and-vector-retrieval
description: Durable, versioned, idempotent knowledge ingestion and lexical/semantic/hybrid retrieval with citations, permissions, plugins, vector schemas, and deployment hardening.
version: 0.6.0
---

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
