# Quality Gate — v0.7.2

A release must satisfy all of the following:

1. Registry, manifest, and actual skill directories agree exactly.
2. JSON Schemas and local Markdown links validate.
3. Every skill contains specialist procedures and has an evaluation contract.
4. The fixed check catalog has valid runner paths, timeouts, expected exit codes, and current SHA-256 pins.
5. Runtime tests prove that unsuccessful or tampered evidence cannot result in `PASSED`.
6. New upstream-derived workflow adaptations include provenance and license decisions.
7. All fixture-only results are labeled as contract checks; they are not reported as successful agent runs.
8. No production-ready or effectiveness claim is made without environment-specific evidence.

## Mandatory checks

See the exact commands in `README.md` and `RELEASE-NOTES-v0.7.2.md`. A failed, skipped, timed-out, or unavailable check is not a pass.
