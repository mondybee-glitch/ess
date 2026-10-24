# Evaluation fixture: Design a narrowly scoped MCP server

**Case ID:** mcpse-01
**Target skill:** `mcp-server-engineering`
**Agent execution status:** not run

## Request

Design a TypeScript MCP server for a read-only inventory API. Define the tool surface, validated schemas, transport, output shape, pagination, and error behavior.

## Acceptance properties

- Workflow tools and generic endpoint coverage are explicitly balanced
- Schemas bound types, size, pagination, and invalid inputs
- Transport and SDK versions are recorded as assumptions or verified facts
- Errors reveal no secrets or stack traces

## Required reporting

- Record exact commands and exit codes.
- Attach evidence for every claimed result.
- State limitations and unverified outcomes.
