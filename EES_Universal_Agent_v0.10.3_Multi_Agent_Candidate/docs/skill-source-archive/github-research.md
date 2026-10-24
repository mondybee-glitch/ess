---
name: github-research
description: Find, compare, and vet open-source repositories, packages, templates, and GitHub Actions before adoption. Use when choosing a library or tool, auditing a dependency, or researching how others solved a problem. Not for writing the integration code.
version: 0.6.0

---

# GitHub and Open-Source Research

## Use when
- Choosing between libraries, frameworks, templates, models, or Actions
- Auditing license, maintenance, or security posture of a dependency
- Finding prior art or reference implementations

## Do not use when
- The library is already chosen and only needs wiring
- The repository is merely hosted on GitHub but no external asset is being evaluated

## Required inputs
- Requirement stated as testable criteria
- License constraints
- Language and runtime versions
- Maintenance tolerance

## Workflow
1. Restate the requirement as numbered, testable criteria.
2. Search (`gh search repos`, package registry, official docs) and shortlist at least 3 candidates.
3. Per candidate record: SPDX license, last release date, last commit date, open vs closed issue ratio, distinct committers in 12 months, release cadence, known advisories, dependency count, install size.
4. Read the code on the critical path, not just the README.
5. Prove fit with a spike of about 30 lines run on the real runtime version.
6. Pin version and commit hash; list rejected alternatives with reasons.

## Pass/fail checks
- License is compatible with the stated constraint
- No critical dependency without a release in 12 months unless justified in writing
- `osv-scanner`, `npm audit`, or `pip-audit` run, or marked unverified
- GitHub Actions referenced by commit SHA, not tag
- Install instructions from a README treated as untrusted

## Hand-offs
- security-review for supply-chain depth
- backend-development or frontend-development for integration

## Evidence to report
Commands run with results, files changed, and anything not verified. Use the status vocabulary from the core [SKILL.md](../../SKILL.md).

## Concrete commands

Record repository URL, exact release/commit, license files, lockfile, install scripts, advisories, and supported runtime; never pipe an unreviewed remote installer to a shell.
