---
name: fullstack-platform-boundaries
description: Full-stack system boundary design across browser, server, APIs, databases, identity, configuration, and deployment environments.
version: 0.7.2
---

# Fullstack Platform Boundaries

## Use when
A feature spans UI and server, public/private API boundaries, client configuration, SSR, authentication, background services, or deployment environments.

## Do not use when
The change is isolated to a component or service and the existing boundary contracts are clear and unaffected.

## Required inputs
Application architecture; runtime boundaries; data flow; identity model; configuration sources; network/service dependencies; error contract; and relevant deployment constraints.

## Workflow
1. Draw a simple trust/data-flow inventory in prose or tables: browser, server, API, database, worker, third-party service, and secret/config source. Treat client input as untrusted.
2. Assign ownership of validation, authorization, business rules, data fetching, caching, errors, and retries. The server remains authoritative for secrets and protected data.
3. Validate API contracts at both ends when appropriate. Version environment variables, define required/optional values, fail fast on missing configuration, and prevent server secrets from entering bundles or HTML.
4. Review SSR/client boundaries, hydration, caching, tenant isolation, CSRF/CORS, serialization, and error leakage based on the actual framework and deployment mode.
5. Test success, denial, timeout, malformed response, empty state, stale cache, and dependency failure end-to-end without relying only on UI visibility.
6. Ensure accessible error/loading states and useful correlation IDs across client and server. Redact private internals from user-facing messages.
7. Document deployment-specific assumptions and avoid adding cross-boundary abstractions until a concrete need is demonstrated.

## Pass/fail checks
Boundary ownership is explicit; secrets stay server-side; authorization is server-enforced; contracts and configuration are validated; errors are consistent; failure paths are tested across the relevant layers.

## Hand-offs
Coordinate with api-design-contracts for external contracts, backend-auth-authorization for policy, ui-design-system-accessibility for user interaction, and devops-and-deployment for environment configuration.

## Evidence to report
Boundary/data-flow summary, configuration schema, relevant integration tests, bundle/secret checks, error-state screenshots/logs, deployment assumptions, and remaining risks.
