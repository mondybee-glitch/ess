---
name: search-retrieval
description: Specialist workflow for search indexing, retrieval, ranking, relevance, freshness, facets, and zero-result behavior. Use when the task materially involves this boundary.
version: 0.6.0
---

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
