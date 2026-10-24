# Consolidated Release — v0.7.4

## Summary

This release builds on v0.7.3 with operational fixture execution and routing-audit improvements, while retaining the selective, independently authored adaptations of four workflows reviewed in Anthropic's public Agent Skills repository. It adds two focused specialists and strengthens three existing specialist workflows.

## Inventory

- 74 skills registered in both the package manifest and capability registry.
- 222 evaluation contracts defined; fixture-only validation does not represent agent execution.
- Source provenance and licensing decisions documented in `references/anthropic-agent-skills-integration.md` and `THIRD_PARTY_NOTICES.md`.
- 11/11 deterministic operational fixture projects passed; static routing audit returned 0 errors and 0 warnings. See `RELEASE-NOTES-v0.7.4.md` and `reports/v0.7.4-verification-summary.md`.

## Limitations

This is not a standalone AI agent or OS sandbox. Local approvals do not authenticate identities. An unsigned hash chain is tamper-evident rather than tamper-proof. Agent effectiveness and production readiness remain unverified.
