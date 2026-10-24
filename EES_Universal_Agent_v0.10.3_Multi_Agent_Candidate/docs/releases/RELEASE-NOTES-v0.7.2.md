# Release Notes — Elite Engineering Suite v0.7.2

## Purpose

This release selectively integrates workflow patterns reviewed in Anthropic's public `anthropics/skills` repository without replacing the suite or importing upstream helper scripts. The package preserves its local runtime, safety model, registry, and evidence requirements.

## Changes

1. Added `skill-creation-and-evaluation` for skill contracts, distinctive trigger design, progressive disclosure, varied eval cases, paired baseline plans, failure categorization, and truthful evaluation-status reporting.
2. Added `mcp-server-engineering` for MCP tool contracts, SDK/version checks, transport, per-operation authorization, untrusted tool outputs, error/pagination/retry/timeout behavior, and client-path integration tests.
3. Expanded `browser-e2e-and-test-diagnostics` with a locally authored `UPSTREAM-PATTERNS.md` covering readiness, static-vs-dynamic testing, rendered DOM inspection, resilient locators, web-first assertions, redacted artifacts, and cleanup.
4. Expanded `ui-ux-design` with a locally authored distinctive design critique reference focused on subject-specific direction and avoiding unsupported generic visual defaults.
5. Added targeted MCP implementation guidance to `ai-agents-rag-mcp` and skill-quality release gates to `skill-package-governance`.
6. Added two new skills and six domain-specific fixture/evaluation contracts. Total: **72 registered skills; 216 evaluation contracts**.
7. Added source attribution and license-scope records. The source-available document skills (`docx`, `pdf`, `pptx`, `xlsx`) and upstream helper scripts/assets were not copied.
8. Bumped active package/runtime/schema/catalog version to 0.7.2 and refreshed active release documentation.

## Required tests

```bash
python scripts/validate.py --full
python tests/test_validate.py
python tests/test_runtime_v072.py
python tests/test_timeout_handling_v072.py
python tests/test_event_ledger_v072.py
python tests/test_risk_classification_v072.py
python tests/test_repository_integrity_v072.py
python tests/test_anthropic_integration_v072.py
python tests/test_eval_harness.py
python -m compileall -q scripts tests
```

## Limitations

- The tests validate package consistency and local runtime behavior; they do not execute an independent AI agent over all 216 evaluation cases.
- Agent effectiveness, universal compatibility across MCP clients, production readiness, and comprehensive security assurance remain unverified.
- Upstream source pages and license notices can change. Review current per-skill license terms before copying any upstream source or assets in a future version.
- Runtime approval records remain local/self-attested; this package is not an OS sandbox or externally signed audit service.
