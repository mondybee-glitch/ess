# Evaluation fixture: Verify real client-path compatibility

**Case ID:** mcpse-03
**Target skill:** `mcp-server-engineering`
**Agent execution status:** not run

## Request

Review an MCP server that starts successfully but has not been tested through the intended client. Define the verification needed before a release recommendation.

## Acceptance properties

- Server startup is not treated as client compatibility proof
- At least one integration case uses the planned client/SDK surface
- Tool discovery, invocation, invalid arguments, and protocol errors are tested
- Release decision distinguishes tested behavior from deployment assumptions

## Required reporting

- Record exact commands and exit codes.
- Attach evidence for every claimed result.
- State limitations and unverified outcomes.
