---
name: backend-development
description: Design and implement server-side code: REST and GraphQL APIs, authentication and authorization, databases, migrations, queues, and caching. Use for any server, API, or data-layer change.
version: 0.6.0

---

# Backend Development

## Use when
- Adding or changing endpoints, schemas, migrations, jobs
- Auth, permissions, multi-tenant data access
- Performance of queries and background work

## Do not use when
- Static copy or styling changes

## Required inputs
- API contract and its owner
- Database engine and version
- Auth model and roles
- Data volume and traffic estimates

## Workflow
1. Map the contract: schema owner, versions, consumers.
2. Keep authorization server-side and resource-level; validate input at the boundary.
3. Use parameterized queries only.
4. Write migrations as expand then contract; avoid long locks on large tables.
5. Make retried writes idempotent (idempotency key or natural key).
6. Set timeouts; log structured events without personal data.
7. Test authorization negatives, duplicates, and partial failures.

## Pass/fail checks
- Another user's resource returns 403 or 404 (test exists)
- Query count per request stable (no N+1)
- `EXPLAIN` shows an index for each new filter or join column
- Migration is reversible or has a forward-fix plan
- Pagination and rate limits on list endpoints

## Hand-offs
- security-review for High changes
- devops-and-deployment for rollout
- software-testing for contract tests

## Evidence to report
Commands run with results, files changed, and anything not verified. Use the status vocabulary from the core [SKILL.md](../../SKILL.md).

## Concrete commands

Run the repository test command; for Python use `pytest -q`, inspect queries with `EXPLAIN (ANALYZE, BUFFERS)`, and run the migration tool in a disposable database before approval.
