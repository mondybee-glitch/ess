# EES v0.7.8 — Adaptive Agent Integration

## Added
- Embedded `adaptive-engineering-agent v0.1.0` source under `integrations/adaptive-engineering-agent/`.
- Arabic integration guide and EES-side presence/credential-guard tests.
- Original source archive retained in `HISTORY/release_archives/`.

## Preserved
- Existing EES v0.7.7 current-release files, 74-skill library, schemas, fixtures, reports, and prior release archives remain present in the package.
- Adaptive agent source files are included without intentional code changes.

## Validation boundaries
- ZIP integrity is checked during packaging.
- The integration test and the adaptive agent's own unit tests are executed during the build process; results are recorded in `reports/adaptive-agent-merge-verification.json`.
- This integration does not imply a live provider call, production security approval, or automatic feedback-to-skill promotion.
