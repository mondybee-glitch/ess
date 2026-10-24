> Runtime routing is two-stage and enforced by `scripts/task_runtime.py` using `hierarchical-routing.json`; this table remains the specialist-level signal reference. Validate route coverage with `python scripts/validate.py`.

# Routing matrix v0.8.0 Clean Candidate

The registry is authoritative. This file is explanatory and must not diverge from it. Scores are independent from risk. The router chooses the smallest dependency-closed set that covers positive signals and the risk floor.

| Skill | Positive signals | Risk | Dependencies |
|---|---|---|---|
| `api-design-contracts` | api, endpoint, openapi, graphql, grpc, webhook, schema, pagination, idempotency, versioning, event | critical | none |
| `database-engineering` | database, schema, migration, sql, index, transaction, backup, restore, backfill, tenancy | critical | backend-reliability-recovery |
| `backend-auth-authorization` | auth, authentication, authorization, rbac, abac, tenant, session, token, permission, identity | critical | none |
| `api-security-testing` | api security, idor, bola, injection, cors, rate limit, secret leakage, upload, webhook verification | critical | backend-auth-authorization |
| `backend-integration-testing` | integration test, contract test, end to end, provider, payment, storage, queue, webhook, service | critical | api-design-contracts |
| `async-jobs-messaging` | queue, worker, job, stream, message, dlq, retry, outbox, inbox, poison, deduplication | high | backend-observability, backend-reliability-recovery |
| `backend-observability` | observability, logging, metrics, tracing, trace, slo, sli, alert, dashboard, correlation | high | none |
| `backend-performance` | performance, latency, p95, p99, throughput, load, capacity, query plan, cache, memory | high | backend-observability |
| `backend-reliability-recovery` | reliability, recovery, rto, rpo, outage, timeout, circuit breaker, degradation, restore, incident | high | none |
| `backend-production-readiness` | production readiness, release, go no-go, canary, rollout, rollback, feature flag, readiness, launch | critical | api-design-contracts, database-engineering, backend-auth-authorization, api-security-testing, backend-integration-testing, async-jobs-messaging, backend-observability, backend-performance, backend-reliability-recovery |
| `web-artifacts-builder` | interactive artifact, multi-step interface, state management, web prototype, single-file HTML | high | frontend-development; component and browser-test co-activation as needed |
| `brand-guidelines` | brand guidelines, brand colors, brand identity, typography system, design tokens | medium | ui-ux-design; design-system-theming-rtl as needed |


## v0.9.0 canonical skill mapping

There are 32 active canonical skill folders. The 74 source capability IDs remain routable as aliases; resolve their active instructions using `capability-registry.json` fields `canonical_skill_id` and `skill_path`. The source texts are retained under `docs/skill-source-archive/` and are not separate runtime skills.
