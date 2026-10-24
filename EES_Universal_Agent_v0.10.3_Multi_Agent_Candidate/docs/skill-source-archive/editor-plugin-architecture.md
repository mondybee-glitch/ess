---
name: editor-plugin-architecture
description: Editor plugin architecture for schema-driven nodes, registries, render systems, undo/redo, package boundaries, and safe extension contracts. Use for 2D/3D editors, visual builders, CAD-like tools, or extensible authoring applications.
version: 0.6.0
---

# Editor Plugin Architecture

## Use when
Use when designing or extending an editor, visual builder, CAD/3D tool, scene graph, node registry, or plugin ecosystem.

## Do not use when
Do not use for a static canvas or an ordinary CRUD screen with no editor state, rendering systems, or extension contract.

## Required inputs
Require the domain schema, hierarchy rules, persistence format, renderer/system ownership, selection and tool model, undo/redo policy, plugin lifecycle, package boundaries, and compatibility policy.

## Workflow
1. Define stable data primitives and discriminators. Keep persisted domain state separate from transient selection, hover, camera, and render caches.
2. Choose an explicit hierarchy or relational representation and document parent/child invariants, deletion rules, references, and migration behavior.
3. Separate schema, state store, registry, renderer, systems, tools, and UI. A renderer should not silently own domain mutations or persistence.
4. Make plugin registration explicit: version, capabilities, schemas, renderers, migrations, cleanup, permissions, and failure isolation.
5. Design undo/redo and persistence around transactions or meaningful commands. Test partial failure, reload, duplicate registration, and incompatible plugin versions.
6. If agents or MCP tools are exposed, define bounded commands, validation, idempotency, authorization, and a local-first data boundary.

## Pass/fail checks
Pass only when state ownership and extension contracts are explicit, persisted data is versioned, transient state is not accidentally serialized, and plugin failure cannot silently corrupt the document.

Required commands or procedures: validate schemas; run store and renderer tests; exercise create/update/delete, undo/redo, reload, migration, duplicate plugin, and malformed command paths; record evidence.

## Hand-offs
Hand off 3D rendering to `game-development`, agent tools to `ai-agents-rag-mcp`, and frontend interaction to `frontend-development`.

## Evidence to report
Report schemas, invariants, package ownership, plugin contract, migration results, command validation, persistence/reload evidence, and unverified rendering or device limits.
