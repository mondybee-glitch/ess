---
name: defensive-automation-and-audit
description: Defensive automation control planes, allowlisted command execution, authorization records, evidence ledgers, auditability, and safe recovery.
version: 0.7.2
---

# Defensive Automation And Audit

## Use when
Building or auditing automation that can alter files, systems, accounts, deployments, security configurations, or other consequential state.

## Do not use when
The task requires unauthorized intrusion, credential theft, destructive payloads, license/DRM circumvention, or hiding activity from legitimate operators.

## Required inputs
Action catalog, request/task identity, target scope, approval owner, permission model, execution environment, timeout/budget limits, expected artifacts, and recovery plan.

## Workflow
1. Separate planning from execution. Define explicit allowlisted action IDs with fixed runner paths, arguments, runtime, timeout, expected exit code, and artifact expectations.
2. Never pass arbitrary user text to a shell. Validate IDs against the catalog, execute an argument array without shell interpretation, restrict filesystem paths, bound time, and retain stdout/stderr.
3. Require task-scoped, non-expired approval for high-impact/external/destructive actions. A text field naming an approver is not identity authentication; state that limitation.
4. Record task ID, selected action, command/runner hash, start/end time, exit code, expected result, output paths, artifact hashes, and previous ledger hash. Detect mismatched state/ledger files.
5. Verify artifacts exist and their hashes remain unchanged before accepting claims. An action being present in a log does not prove it succeeded; an exit code without an artifact does not prove acceptance criteria.
6. Test missing/expired approval, out-of-scope approval, unknown action IDs, shell metacharacters, path traversal, timeout, nonzero exit, missing artifact, altered artifact, budget exhaustion, and interrupted writes.
7. Document audit limits: a local hash chain is tamper-evident but not tamper-proof if an attacker can rewrite the entire chain; signed/external anchoring requires a separate trust service.

## Pass/fail checks
Unknown actions are rejected; commands never use a shell; scope and approval requirements are enforced by code; failures cannot become PASSED; artifact tampering is detected; and logs do not claim externally verified identity unless it is.

## Hand-offs
Coordinate with agent-workflow-specification for acceptance criteria, backend-production-readiness for release gates, and security-review for threat modeling.

## Evidence to report
Action catalog entry, approval scope/status, command hash, exit code, artifact hashes, ledger verification result, negative-test outcomes, and trust-boundary limitations.
