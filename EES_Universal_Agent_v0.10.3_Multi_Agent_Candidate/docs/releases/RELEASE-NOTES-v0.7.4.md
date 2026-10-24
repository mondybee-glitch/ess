# Release notes — v0.7.4

## Purpose
Address the v0.7.1 review's most actionable operational-evidence and routing concerns without adding new skills. This release builds on v0.7.3, retains all 74 skills, and does not claim that the AI agent has executed the 222 evaluation contracts.

## Changes
- Added 11 deterministic, executable domain fixture projects under `operational-fixtures/` for tenant authorization, retry/idempotency, database migration rollback, queue backpressure/cancellation, readiness/shutdown, prompt-injection tool allowlisting, RAG ACL/tenant isolation, observability secret redaction, recovery/RPO, ML baseline regression, and keyboard accessibility.
- Added `scripts/run_operational_fixtures.py` to execute each fixture in a bounded subprocess and record exit codes, duration, stdout/stderr, and SHA-256 hashes for source and output artifacts.
- Added `scripts/audit_routing.py` and explicit `pre_flight_checks` for critical security/backend/data capabilities. Added recommended mandatory handoffs for backend integration, readiness, database, and async messaging work.
- Extended the package validator to validate pre-flight check references against the check catalog.
- Registered two additional checks in `checks/catalog.json` (9 total).
- Added reports for operational fixtures, routing audit, and selected runtime regressions.

## Verification performed
- Structural package validation: **passed** — 74 skills, 74 registry capabilities, 222 evaluation contracts, 51 central fixtures, 9 registered checks, 11 operational fixture projects.
- Operational domain fixture projects: **11/11 passed**. These validate the fixture implementations only, not the AI agent's ability to use the skills.
- Static routing/path audit: **0 errors, 0 warnings**.
- Existing runtime and repository-integrity regression tests: **12/12 passed** in separate bounded invocations.
- Existing fixture contract harness: **222/222 fixture contracts passed**; this verifies fixture linkage and metadata, not agent execution.
- Anthropic integration regression: **passed**.

## Known limitations
- Agent-run skill effectiveness remains **unverified**; all 222 evaluation contracts remain defined, not executed by an AI agent.
- The 11 operational fixture projects are small deterministic reference implementations; they are not production service deployments, full browser tests, real database migration rehearsals, or external security assessments.
- No baseline/candidate benchmark for an AI agent, cost/performance measurement, or human-reviewed scorecard was produced.
- Approval remains a local procedural gate, not external identity verification. The runtime is not an operating-system sandbox.
- The initial combined runtime pytest command exceeded its wall-clock budget; the 12 selected runtime/repository-integrity tests were then executed individually and each returned exit code 0. This is not a claim that the entire test suite passed in one invocation.

## Release decision
**Partial operational maturity; not production-ready as a comprehensive autonomous engineering system.** The package now has reproducible domain fixture execution and a clean static routing audit, but production readiness still requires actual AI-agent evaluations with per-criterion artifacts and independent baseline comparisons.
