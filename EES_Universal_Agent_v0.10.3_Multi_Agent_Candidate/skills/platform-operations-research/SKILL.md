---
name: platform-operations-research
description: "Canonical EES specialist for Platform operations & research; merges 2 compatible source capabilities while preserving their original IDs as aliases."
---

# Platform operations & research — Canonical Engineering Skill

## Hyper-Cognitive Engineering Kernel

Use this protocol for substantive implementation, architecture, debugging, and review tasks. Do not confuse procedural discipline with proof of correctness.

### 1. Inversion and trap hunting
Before choosing an implementation, enumerate the three most plausible production failures. Consider concurrency, partial failure, retries, state loss, malicious inputs, resource exhaustion, and unsafe trust boundaries as applicable. Identify which failure is most severe and how it will be detected.

### 2. Two-stage routing and invariants
Treat this canonical skill as the primary route when its scope matches. Select no more than two complementary guard skills unless evidence shows a real cross-domain dependency. Extract measurable invariants from the relevant specialist modules below and convert them into acceptance criteria before editing.

### 3. Zero-code dry run
For medium-or-higher risk, sketch the input → transformation → persistence → output path; simulate duplicate/concurrent requests and one partial outage; define a rollback or containment path. If rollback is not feasible, state the recovery strategy before implementation.

### 4. Principal-grade execution
Prefer explicit types/contracts, bounded retries, timeouts, cancellation, idempotency, least privilege, and redacted telemetry where applicable. Avoid toy implementations and unresolved TODOs. Do not invent numeric thresholds: use source-backed limits, derive them transparently, or mark them as tunable assumptions.

### 5. Adversarial self-trial and evidence gate
Assume at least one hidden defect remains. Review failure paths, boundaries, and regressions against `checks/catalog.json` and the relevant module constraints. Report VERIFIED only when a reproducible command actually ran against the current file state and its output supports the claim. Otherwise report NOT RUN, PARTIAL, or UNVERIFIED.

## Canonical scope and alias map

Canonical ID: `platform-operations-research`  
Source capability aliases: `gitea-platform-operations`, `github-research`.

The original source documents are retained under `../../docs/skill-source-archive/` for traceability. The sections below preserve source-specific procedures; resolve overlaps by the stricter safety invariant and record material conflicts rather than silently discarding them.



---

## Preserved specialist module: `gitea-platform-operations`

Source capability: `gitea-platform-operations`.

# Gitea Platform Operations

## Use when
When Gitea-specific administration, APIs, Actions runners, package registries, migration, backup, or organization permissions matter.

## Do not use when
Do not use when the task does not match the stated domain, lacks required authorization, or is a simpler task owned by another specialist.

## Required inputs
authorized instance/repository identifiers; scoped token; requested operation; version, runner, branch, package, or backup configuration.

## Purpose
Provide a Gitea-specific operational adapter while keeping repository, organization, runner, package, token, and backup operations least-privileged and version-aware.

## Workflow
1. Confirm scope, authorization, versions, data classification, and acceptance criteria before acting.
2. Separate planning, read-only inspection, implementation or analysis, and verification. Keep side effects behind explicit approval.
3. Record source evidence, assumptions, exact commands, artifacts, and unresolved uncertainty. Never infer success from intent, generated text, or a partial check.
4. Compose only the secondary skills that own distinct controls; hand off implementation, testing, security, and release responsibilities explicitly.

## Pass/fail checks
Pass only when the required inputs are present, boundaries are respected, outputs are reproducible enough for the stated claim, and incomplete or failed checks are reported as such.

Required outputs: validated operation plan; result; runner/permission assessment; audit and rollback notes.

## Safety and limits
Use only on authorized instances and repositories. Protect tokens, isolate trusted runners, confirm permission/destructive changes, and preserve rollback and backup evidence.

## Verification
- Run least-privilege API fixtures and reject out-of-scope identifiers.
- Require confirmation for permission, deletion, migration, and runner changes.
- Rehearse backup/restore and package provenance without production mutation.

## Hand-offs
Hand off implementation, testing, security, and release responsibilities to the selected specialist owners; do not silently duplicate their work.

## Evidence to report
Report selected sources and revisions, authorization and scope, commands and exit codes, artifacts, coverage limits, risks, handoffs, and what remains Unverified.

---

## Preserved specialist module: `github-research`

Source capability: `github-research`.

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
Commands run with results, files changed, and anything not verified. Use the status vocabulary from the core [SKILL.md](../../docs/skill-source-archive/github-research.md).

## Concrete commands

Record repository URL, exact release/commit, license files, lockfile, install scripts, advisories, and supported runtime; never pipe an unreviewed remote installer to a shell.

## Release references

- [Source archive index](../../docs/skill-source-archive/README.md)


## Domain-specific cognitive depth (v0.9.2)

### Platform operations and research: blind-spot traps
- **Likely false confidence:** Search snippets and copied directories are not primary evidence.
- **Adversarial case to simulate:** Stale docs, spoofed repositories, and package-name confusion poison research.

### Hard invariants
- Trace claims to primary sources; record dates, versions, provenance, and confidence.
- Never report a property as verified without a reproducible check or authoritative evidence.
- State trade-offs explicitly: correctness vs. latency, safety vs. convenience, and complexity vs. operability; choose based on the task's declared constraints rather than maximizing one dimension blindly.

### Required specialist self-check
Before implementation, write one domain-specific counterexample that would falsify the proposed design. Convert the invariant above into a test or reviewable evidence item. After implementation, test the counterexample and report the exact command/result; if it cannot be tested, mark it **UNVERIFIED**.
