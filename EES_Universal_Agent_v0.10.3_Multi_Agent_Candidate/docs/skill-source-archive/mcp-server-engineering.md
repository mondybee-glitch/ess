---
name: mcp-server-engineering
description: Design, implement, secure, and evaluate Model Context Protocol (MCP) servers and tool interfaces in Python or TypeScript, including tool schemas, transport, errors, authorization, pagination, and real workflow testing.
version: 0.7.2
---

# MCP Server Engineering

## Use when
Use for implementing or reviewing an MCP server, registering MCP tools/resources/prompts, designing tool input/output schemas, integrating an external API through MCP, or testing a tool server in a real client workflow.

## Do not use when
Do not load for ordinary REST endpoints that do not expose MCP protocol surfaces; route those to `api-design-contracts` or `api-integrations`. Do not connect to external systems or publish a server without authorization.

## Required inputs
Identify language/runtime and SDK versions, target MCP client(s), intended transport (stdio or supported HTTP transport), tools/resources/prompts to expose, upstream API contract, identity and authorization model, data sensitivity, error and retry behavior, deployment target, and test environment.

## Workflow
1. **Research the protocol and SDK version.** Use version-matched official MCP documentation and SDK references. Record the exact versions; do not infer current APIs from old examples.
2. **Model user workflows before mirroring endpoints.** Decide which operations should be focused workflow tools and which need generic endpoint coverage. Each tool must have a clear purpose, stable name, concise description, well-bounded input schema, explicit output shape, and documented side effects.
3. **Define contracts.** Validate required fields, types, ranges, enums, sizes, identifiers, and pagination cursors. Separate protocol errors from expected business errors. Return concise, actionable error messages without secrets, stack traces, or internal identifiers that should not be exposed.
4. **Enforce authorization server-side.** Do not trust a model's claims about the user or resource ownership. Derive identity from the authenticated client/session; authorize each operation and each object access; scope credentials to minimum privilege; keep secrets out of prompts, logs, and tool results.
5. **Handle untrusted content and side effects.** Treat tool arguments, fetched documents, resource contents, and upstream responses as untrusted data rather than instructions. Require explicit confirmation/approval for consequential writes when the host policy demands it. Design idempotency, retries, timeout, cancellation, and partial-failure behavior.
6. **Select transport deliberately.** Use stdio for local process integrations where suitable and the currently supported HTTP transport for remote deployments. Specify lifecycle, authentication, origin/network exposure, session behavior, and connection failure recovery. Do not expose unauthenticated administrative or write operations by default.
7. **Implement observability and bounded responses.** Log operation identifiers and durations with sensitive data redacted; report pagination metadata and truncation; bound response size, concurrency, and upstream timeouts. Keep tool descriptions distinctive and avoid overlapping tools with ambiguous semantics.
8. **Test the protocol and the user's workflow.** Test initialization/capability negotiation, tool discovery, valid and invalid schemas, authorization denial, cross-user/object isolation, pagination, empty results, upstream timeouts, retries, malformed upstream data, cancellation, redaction, and writes/idempotency. At least one test must call the server through the same client or SDK surface intended for use.
9. **Review and hand off.** Validate SDK compatibility, dependency lockfile, documented setup, environment variables, permission scopes, output contracts, monitoring, and rollback. Do not state that a server is production-ready based only on unit tests or a successful local handshake.

## Pass/fail checks
- Every tool has a narrow purpose, validated schema, documented output, and declared side effects.
- Authorization is enforced per operation/resource and tests cover denied and cross-boundary requests.
- Errors, pagination, rate limits, retries, timeouts, cancellation, and partial failures are explicit.
- Untrusted tool output cannot be silently reinterpreted as privileged instructions.
- Secrets and sensitive payloads are absent from test reports and logs.
- Integration tests use the actual MCP protocol/client path planned for deployment.

## Required outputs
Architecture and transport decision; tool contract table; implementation/configuration; automated tests and results; security/authorization notes; setup and operations guide; limitations and deployment checklist.

## Safety and limitations
A functioning local server does not prove protocol compatibility across all clients. Authentication, network exposure, SDK versions, hosting, and upstream API permissions must be reviewed in the deployment environment. Use only authorized integrations and test systems.

## Hand-offs
Use `api-integrations` for upstream API specifics, `backend-auth-authorization` for identity and access control, `security-review` for threat analysis, and `software-testing` for integration-test review.

## Evidence to report
Record protocol/SDK versions, transport, test command and exit code, client workflow exercised, schema and denial cases, redaction evidence, upstream test environment, and all unverified deployment assumptions.
