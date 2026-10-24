# Elite Engineering Suite v0.7.6 — Pilot Execution Plan

**Decision:** GO for a bounded Pilot; NO-GO for production release.  
**Pilot:** 5 skills / 15 cases / one OpenAI-compatible Chat Completions adapter / one Docker sandbox image.  
**Current state:** Prepared in the repository; live provider runs remain blocked until credentials, Docker, and the image are available.

## 1. Scope and intentional deferrals

### In scope
- Generate counts from source files instead of hand-maintained numbers.
- Repair the 51 contracts that lacked explicit `success_criteria` using their existing `expected_output` and `automated_checks`.
- Execute the 15 cases listed in `reports/pilot-manifest-v076.json`.
- Use one host-side provider adapter and one no-network Docker sandbox image.
- Record actual tool commands, run status, changed-file hashes, duration, token usage, and estimated cost where model pricing is configured.
- Independently grade all 15 case runs with two reviewers.
- Produce a Pilot report and only then decide whether to expand to 15–20 skills.

### Deferred until the Pilot gate passes
- Running all 222 contracts.
- Refactoring or deleting skills across all 74 skills.
- Browser/Playwright end-to-end execution requiring a live browser service.
- Any production readiness claim, service deployment, or automatic promotion based only on agent self-reports.
- Fixed universal thresholds such as 95% routing or 85% semantic pass rate before the Pilot produces representative results.

## 2. Work packages, owners, time, resources, exit criteria

Durations below are estimates in working days, not promises. Owners are roles; a small team may combine roles but the independent reviewers must not author the task output they grade.

| Work package | Accountable owner | Estimate | Needed resources | Entry criteria | Exit criteria |
|---|---|---:|---|---|---|
| P0 — Source baseline and contract repair | Package Maintainer | 0.5–1 day | Python 3.11+, repo checkout | v0.7.5 source available | Actual counts generated; 51 missing criteria fixed; validation is clean |
| P1 — Provider configuration and connectivity | Agent Infrastructure Engineer | 0.5–1 day | Provider API key stored as host env var; selected model; API pricing | P0 passes | One real provider call succeeds; key absent from reports and container env |
| P2 — Build and verify sandbox | DevSecOps Owner | 0.5–1.5 days | Docker daemon; image build access; 2 CPU / 2 GB RAM per case | Docker host is available | Image builds; `--network=none`, readonly rootfs, non-root UID, no-new-privileges, dropped capabilities, PID/CPU/RAM limits verified |
| P3 — Run Pilot-1 | Evaluation Lead | 0.5–1 day | 15 case runs, output/artifact storage, provider budget | P1 and P2 pass | 15 records or explicit blocked statuses; failures/timeouts preserved; no quality auto-pass |
| P4 — Independent grading | Two independent reviewers; Evaluation Lead arbitrates | 1–2 days | Rubrics, artifacts, reviewer log | P3 artifacts frozen and hashed | Every criterion is pass/fail/unknown from both reviewers; disagreements reconciled and reported |
| P5 — Routing and overlap review | Routing Owner + domain reviewers | 1 day | Registry, routing audit, overlap candidates, Pilot results | At least one run per selected skill | Primary owner, handoffs, and hard-conflict semantics recorded; no unverified auto-merge |
| P6 — Pilot release decision | Release Owner | 0.5 day | P0–P5 reports | Evidence package complete | Written GO/NO-GO with reasons, residual risks, revised budget, and next sample |

**Expected elapsed time:** approximately 4–7 working days with provider credentials and Docker available; longer if access, image build, or reviewer capacity is blocked. This is a planning estimate only.

## 3. Pilot skill selection

The immutable selection is in `reports/pilot-manifest-v076.json`:
- `api-design-contracts` — backward compatibility, webhook idempotency, invalid contract path.
- `database-engineering` — safe migration, concurrency integrity, backup restore.
- `frontend-development` — filter behavior, RTL, CLS measurement.
- `software-testing` — boundary tests/mutation, E2E test quality, assertions vs coverage.
- `devops-and-deployment` — production Dockerfile, CI stages/scanning, restore evidence.

The selection deliberately spans API, data, UI, testing, and delivery. Some criteria inherently depend on tooling/services not bundled into the workspace. The agent must mark them `unverified` rather than claim they passed. Add missing dependencies as prebuilt image layers only after documenting and pinning them; do not enable arbitrary network from the case container to make a failing check pass.

## 4. Docker Pilot sandbox decision

**Selected implementation:** Docker CLI, one container per `run_command` call, with the case workspace as the only writable bind mount. The fixture directory and `SKILL.md` are separate read-only bind mounts.

Required runtime restrictions:
- `--network=none`
- `--read-only`
- `--cap-drop=ALL`
- `--security-opt=no-new-privileges:true`
- `--pids-limit=128`
- `--memory=2g`
- `--cpus=2`
- non-root container UID/GID
- bounded `/tmp` tmpfs; no host socket, home directory, credentials, or provider key mounted
- command timeout no greater than 300 seconds

Build with `scripts/build_pilot_sandbox.sh`. `sandbox/Dockerfile` supplies Node.js and Python toolchains for this Pilot. The adapter invokes the provider from the host and sends only code/test commands into the no-network container; the provider key is not passed into Docker.

**Residual risk:** Docker shares the host kernel. This is an appropriate first Pilot boundary, not a high-assurance hostile-code sandbox. Use a disposable host. Pin the resolved image digest before production deployment. Runtime package installation from the public network is intentionally unavailable; pre-seed verified dependencies in the image or report the check as unverified.

## 5. Provider API and budgets

Adapter: `scripts/openai_compatible_agent_adapter.py`. It expects a Chat Completions-compatible endpoint and environment variables:
- `EES_API_BASE_URL` (default `https://api.openai.com/v1`)
- `EES_API_KEY` (host only)
- `EES_MODEL`
- `EES_SANDBOX_IMAGE` (default `ees-pilot-sandbox:0.7.6`)
- `EES_MAX_TOOL_STEPS` (default 16) and `EES_MAX_COMPLETION_TOKENS` (default 2048)
- optional provider-specific `EES_INPUT_PRICE_PER_1M` and `EES_OUTPUT_PRICE_PER_1M`

Run budget is set using `--budget-usd`. The runner requires price values when budget control is enabled. Adapter cost estimates are estimates, not billing records; provider tokenization/pricing may vary. Choose a cap before starting, leave contingency, inspect actual billing after the run, and stop the run if provider usage or cost reporting is absent. Do not store API keys in the package or report.

Recommended Pilot cap policy: one named owner approves a fixed maximum before execution; set the dollar cap based on selected model pricing and expected context/output. A numerical dollar figure is intentionally not guessed in this plan because no provider/model/price has been supplied.

## 6. Objective quality gates for Pilot-1

These are Pilot safety/measurement gates, not global skill-quality thresholds:
1. 100% of selected records are accounted for as completed, failed, timed out, or blocked.
2. 0 path traversal artifacts accepted; 0 fixture/SKILL write attempts accepted by adapter file tools.
3. 0 API credentials present in container environment or artifacts.
4. 100% of run reports preserve hashes, exact command exit codes, timing, and explicit limitations for executed cases.
5. 100% of 15 case outputs are independently graded; unknown is permitted and must not count as pass.
6. Any suspected sandbox escape, credential leak, corruption of read-only inputs, or unbounded command is an automatic NO-GO.
7. Report per-skill and per-case outcome, criterion pass/fail/unknown, failure mode, routing decision, duration, tokens, estimated cost, and variance if repeated runs are performed.

Do not adopt 95% routing / 85% semantic success / 90% critical-case success as permanent policy until the Pilot distribution, confidence limitations, unknown rate, reviewer agreement, and costs are reviewed. Initial sample thresholds guide investigation, not product claims.

## 7. Human review governance

- Two reviewers independently grade each case against the frozen source criteria and artifact hashes.
- Reviewers must have relevant engineering experience for the domain; record role/competence and conflicts of interest.
- Both reviewers provide a criterion-level `pass`, `fail`, or `unknown`, evidence reference, and rationale.
- Report raw agreement and Cohen's kappa at criterion level; because the sample is small, treat kappa as descriptive and include prevalence/unknown counts.
- Target agreement for the Pilot is at least 0.70 Cohen's kappa and 80% raw agreement; below either target requires rubric calibration and adjudication before interpreting pass rate.
- The Evaluation Lead arbitrates disagreements after preserving both original judgments. Only the Release Owner can make the Pilot GO/NO-GO decision.
- Self-reported agent confidence or declared “success” never substitutes for grader evidence.

## 8. Skill ownership / overlap decision matrix

`conflicts_with` is defined as a **hard exclusion**: two skills must not be co-selected for the same decision scope. Similar names or overlapping vocabulary alone do not qualify. No hard-conflict pairs are pre-populated without evidence, because incorrectly excluding complementary skills can break routing. The registry adds explicit ownership metadata and a separate overlap candidate report so humans can validate the candidates before changing hard routing rules.

| Decision | Evidence threshold | Required action |
|---|---|---|
| Keep | Clear unique scope and at least one distinct output/acceptance criterion in Pilot | Keep primary owner; document handoffs |
| Improve | Repeated actionable failures or high unknown rate, while scope remains unique | Fix instructions/fixtures; rerun affected cases |
| Split | At least two distinct task clusters with materially different outputs; each cluster has separate examples | Split only with owner approval and new evaluation contracts |
| Merge | At least 70% scope/criteria overlap **and** at least 80% of outputs/criteria judged interchangeable by two reviewers; no unique routing signal | Draft merged skill, rerun both route sets and regressions before removal |
| Add `conflicts_with` | The two skills cannot both own the same task decision; no normal task requires both simultaneously; two reviewers agree | Add reciprocal links, test routing effects, require explicit override for exceptional tasks |
| Deprecate | No unique acceptance criteria, function fully covered by a successor, and evidence from at least two review cycles | Archive, update references/manifest, run route regression, then remove only after Release Owner approval |

With only three baseline cases per skill, no skill should be deleted or merged solely from a raw pass percentage. Expand a candidate to at least six discriminating cases before irreversible catalog changes.

## 9. Required probes before Pilot acceptance

- **Success:** one provider call produces a valid response; one small artifact is created; sandbox test command returns its real code.
- **Timeout:** command reaches configured timeout; runner records `timeout`, returns non-zero for the run, and never counts a quality pass.
- **Invalid provider output:** invalid final JSON is reported as `adapter_status=invalid_final_json`; it must not become an accepted successful grade.
- **Disallowed path:** absolute paths, `../` traversal, and writes to `fixture/` or `SKILL.md` are rejected by file tools.
- **Missing Docker/image:** command run returns an explicit blocked error; no unsandboxed fallback is allowed.
- **Budget:** guard refuses a provider call when conservative token/cost estimate exceeds remaining budget; any budget ambiguity stops further runs.

## 10. Commands

```bash
# 1) Static package validation and source-of-truth counts
python scripts/generate_baseline.py --output reports/baseline-v076.json
python scripts/validate.py --full
python scripts/audit_routing.py --output reports/routing-audit-v076.json

# 2) Build sandbox on a Docker-enabled disposable host
scripts/build_pilot_sandbox.sh
python scripts/pilot_preflight.py

# 3) Run exactly the 15 frozen Pilot cases; set a positive approved cap
export EES_API_KEY='(set securely in your shell/environment manager)'
export EES_MODEL='(provider-supported model id)'
export EES_INPUT_PRICE_PER_1M='(current input USD price)'
export EES_OUTPUT_PRICE_PER_1M='(current output USD price)'
python scripts/run_agent_evals.py \
  --manifest reports/pilot-manifest-v076.json \
  --command "python $PWD/scripts/openai_compatible_agent_adapter.py" \
  --timeout 300 --budget-usd 1.00 \
  --output reports/pilot-1-run.json

# 4) Grade the preserved run artifacts independently; do not copy the example grader identity.
python scripts/grade_agent_evals.py --run reports/pilot-1-run.json \
  --grades reports/pilot-1-grades.json --output reports/pilot-1-grading.json
```

Replace `1.00` with a pre-approved cap derived from the actual model pricing and estimated tokens. The command above is an example only; it must not be executed until the real price variables, credentials, Docker image, and budget approval are in place.

## 11. Current status and next decision

| Item | State |
|---|---|
| 51 missing success-criteria entries | Repaired from existing expectations/checks; human review remains |
| README totals | Synchronized to actual scan count |
| Automatic source-of-truth baseline | Implemented |
| Real provider adapter code | Implemented; unit test / mockable protocol only until credentials are supplied |
| Docker isolation configuration | Implemented, not runnable in the current environment because Docker/Podman is unavailable |
| Pilot manifest | Frozen at 5 skills / 15 cases |
| Real agent runs | 0 in this build; blocked pending provider credentials + Docker image/daemon |
| Semantic quality pass claims | 0 |

**Release decision:** GO for running Pilot-1 on an appropriately configured disposable Docker host; NO-GO for claiming agent quality or production readiness before the run and independent review.
