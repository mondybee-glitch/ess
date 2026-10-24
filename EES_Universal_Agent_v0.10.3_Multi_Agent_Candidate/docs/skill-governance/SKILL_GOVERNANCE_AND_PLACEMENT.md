# EES Skill Governance & Placement Standard (v1.0)

## 1. Non-negotiable rule
A new skill is a candidate, not an automatic addition. Never install a second active skill that substantially duplicates an existing capability merely because its source (including GitHub) appears stronger. Compare it against the current canonical skill, retain provenance, merge only evidence-supported improvements, and run regression checks before promotion.

## 2. Intake pipeline — required order
1. **Capture**: record source URL/repository, exact commit or release, retrieval date, license, author, original path, and content hash. Do not execute imported code during intake.
2. **Safety & license gate**: inspect instructions, scripts, dependencies, network behavior, secret handling, prompt-injection risks, license compatibility, and suspicious obfuscation. Reject or quarantine if unclear or unsafe.
3. **Normalize**: extract triggers, intended outcomes, inputs/outputs, workflow steps, tools/dependencies, constraints, examples, tests, and known failure modes into a standard comparison record.
4. **Find overlaps**: search capability registry, aliases, routing map, canonical skill descriptions, and neighboring skills. Compare by task intent and behavior, not just folder/name similarity.
5. **Benchmark**: score candidate and incumbent on the same representative tasks using the rubric below. Record evidence and confidence for each score. No claims such as “stronger” without comparative evidence.
6. **Decide**: choose exactly one disposition: `MERGE_UPGRADE`, `ADD_DISTINCT_SKILL`, `KEEP_EXISTING`, `QUARANTINE`, or `REJECT`.
7. **Integrate**: update the canonical skill in place when overlapping; retain the imported source in the provenance archive; preserve old capability IDs as aliases; update routing, registry, eval contracts, and documentation.
8. **Test**: run format/schema validation, routing audit, skill-specific evals, regression evals for adjacent skills, security checks, and operational fixtures. Compare results with the last known baseline.
9. **Promote**: promote only if hard gates pass and there is measurable net benefit. Otherwise keep the candidate quarantined or revert.
10. **Record**: add decision record, scorecard, test outputs, changed files, rollback pointer, and reviewer/approval status.

## 3. Comparative scorecard (0–5 each)
Score both incumbent and candidate against the same evidence and tasks:
- Task success and correctness — 25%
- Coverage of required cases and edge cases — 15%
- Safety, security, and policy compliance — 20%
- Operational reliability and recoverability — 10%
- Trigger precision and routing fit — 10%
- Test quality and reproducibility — 10%
- Maintainability, clarity, and tool compatibility — 5%
- Provenance, license clarity, and update quality — 5%

Weighted score = sum(score / 5 × weight). Safety, license, and provenance are **hard gates**, not compensable by a high total. Missing evidence is `UNKNOWN`, never silently scored as 5. A candidate is not accepted as “stronger” unless it beats the incumbent on comparable tasks without a material regression in safety, routing precision, or adjacent capabilities.

Suggested decision thresholds (after hard gates):
- `MERGE_UPGRADE`: candidate has clear, test-backed improvements; merge the best parts into the canonical skill and keep one active route.
- `ADD_DISTINCT_SKILL`: capability is materially different, has a unique trigger and output contract, and cannot be cleanly expressed as an extension of an existing skill.
- `KEEP_EXISTING`: no measurable net improvement or candidate is mostly duplicate.
- `QUARANTINE`: license, security, source integrity, or evaluation evidence is unresolved.
- `REJECT`: unsafe, incompatible, malicious, or clearly inferior.

## 4. Placement algorithm — one primary home
Assign each skill one canonical primary home using these steps:
1. Identify the skill's **primary user intent** and the artifact/outcome it owns.
2. Match the intent to the existing canonical taxonomy and route; prefer extending an existing skill if the outcome and lifecycle are the same.
3. Create a new canonical skill only if it has a distinct intent, distinct acceptance criteria, independent value, and a non-ambiguous trigger.
4. Put reusable cross-cutting rules in the shared kernel/reference layer rather than copying large blocks into many skills. Put domain-specific procedures and failure modes in the relevant canonical skill.
5. Keep cross-skill dependencies explicit as references/hand-offs; do not create circular routing or make one skill the dumping ground for unrelated work.
6. Add positive trigger examples, negative trigger examples, boundary cases, required inputs, expected outputs, and escalation rules.
7. Add a route test proving the new or changed skill is selected for its intended tasks and not selected for near-neighbor tasks.
8. Update registry, routing, alias map, eval contracts, manifest, changelog, and source archive atomically.

## 5. Required quality bar for every new or upgraded skill
Every canonical `SKILL.md` must contain:
- Purpose and explicit non-goals
- Activation triggers and exclusion/negative triggers
- Required inputs, assumptions, and missing-information behavior
- Ordered workflow with decision points
- Output contract and completion criteria
- Domain invariants and safety/security constraints
- Common failure modes and recovery/rollback behavior
- At least 3 representative examples, including one boundary or adversarial case where appropriate
- Deterministic evaluation contract with success criteria
- Dependencies, source provenance, version, and owner/reviewer status

No vague “be smart / be thorough” statements as a substitute for executable procedures. Keep skill scope narrow enough to route accurately and detailed enough to act reliably.

## 6. Regression and release gates
- Preserve all existing passing evaluations unless a change is intentionally approved and documented.
- Run the new skill's evaluations and adjacent-skill negative routing tests.
- Check alias integrity: every legacy capability ID maps to exactly one active canonical skill and a valid eval contract.
- Check no duplicate active skill route, no broken references, no secrets, and no unsafe imported executable content.
- Require a human review for security-sensitive, destructive, credential-handling, external-network, or production-deployment behavior.
- If evaluation quality drops, revert the canonical skill and routing changes together. Never delete source provenance or evaluation history.
- Release status must reflect actual evidence: `DRAFT`, `QUARANTINED`, `INTERNAL_PILOT`, or `PRODUCTION_APPROVED`. Approval labels must never be inferred from a passing structural validator alone.

## 7. Example: GitHub skill overlaps with an existing EES skill
If the GitHub skill is better, do **not** simply add a second copy. Benchmark it against the incumbent; inspect its license and code; extract its genuinely superior workflow, examples, tests, and failure handling; merge those improvements into the existing canonical skill; archive the source and record commit/hash; retain existing aliases; then run old and new evals plus routing regressions. Add a separate skill only if it owns a distinct task intent and a clear route. If evidence is inconclusive, quarantine the candidate and keep the stable incumbent.
