# Evaluation fixture: Test MCP authorization and failures

**Case ID:** mcpse-02
**Target skill:** `mcp-server-engineering`
**Agent execution status:** not run

## Request

Build a test plan for an MCP tool that retrieves customer orders from a staging system, including cross-user access, timeouts, malformed upstream responses, retries, and redaction.

## Acceptance properties

- Authorization is enforced server-side for each object access
- Denied and cross-boundary requests have explicit assertions
- Timeout, retry, pagination, malformed-data, and idempotency behavior are covered where applicable
- Logs and artifacts redact credentials and personal data

## Required reporting

- Record exact commands and exit codes.
- Attach evidence for every claimed result.
- State limitations and unverified outcomes.
