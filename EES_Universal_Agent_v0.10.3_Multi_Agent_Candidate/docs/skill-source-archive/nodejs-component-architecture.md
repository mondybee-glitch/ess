---
name: nodejs-component-architecture
description: Node.js component and boundary engineering for modular services, layered design, configuration, and error ownership. Use when a Node.js or JavaScript backend needs architecture decisions, module boundaries, configuration, or failure semantics.
version: 0.6.0
---

# Node.js Component Architecture

## Use when

Use when a Node.js service, worker, CLI, or monorepo needs component boundaries, layered design, configuration ownership, error semantics, or graceful process behavior.

## Do not use when

Do not use as the only specialist for a frontend-only change, a generic API contract change, or a security audit without Node.js architecture impact.

## Required inputs

Require the runtime and package-manager versions, entry points, deployment shape, component map, public interfaces, configuration sources, error taxonomy, shutdown requirements, and the acceptance criteria for compatibility.

## Workflow

1. Map business components before folders. Keep each component's entry points, domain logic, and data access distinguishable.
2. Keep transport objects at the edge. Pass domain inputs and return domain results rather than leaking HTTP or queue objects into core logic.
3. Identify public package exports and internal-only modules. Treat `exports`, package boundaries, and workspace references as compatibility surfaces.
4. Trace configuration from source to consumer. Separate defaults, environment overrides, validation, secrets, and startup failure behavior.
5. Classify failures as operational, programmer, dependency, or shutdown failures. Define who logs, who responds, who retries, and when the process must exit.
6. Design graceful shutdown for signals, in-flight work, listeners, queues, database pools, and forced termination. Verify it rather than merely adding a handler.
7. Hand off concrete boundary decisions to backend, API, security, testing, and deployment specialists when their acceptance criteria are affected.

## Pass/fail checks

Pass only when component ownership is explicit, transport/domain boundaries are testable, configuration is validated before use, public exports are intentional, error ownership is documented, and shutdown behavior has a reproducible test or an explicit Unverified limitation.

Required commands or procedures: inspect package exports and workspace metadata; run configuration validation; exercise representative operational and programmer failures; send a termination signal in a test environment; confirm cleanup, exit code, and retained evidence.

## Hand-offs

Provide a component map, boundary decisions, configuration contract, error taxonomy, shutdown sequence, changed files, and unresolved compatibility risks. Do not silently redesign the system when the repository's conventions contradict the preferred pattern.

## Evidence to report

Report runtime and package-manager versions, commands and exit codes, changed public interfaces, configuration sources without secret values, failure traces with sensitive data redacted, shutdown timing, and what was not exercised.
