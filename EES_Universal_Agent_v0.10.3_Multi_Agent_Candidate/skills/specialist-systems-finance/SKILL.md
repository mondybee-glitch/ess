---
name: specialist-systems-finance
description: "Canonical EES specialist for Specialist systems & finance; merges 4 compatible source capabilities while preserving their original IDs as aliases."
---

# Specialist systems & finance — Canonical Engineering Skill

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

Canonical ID: `specialist-systems-finance`  
Source capability aliases: `backend-observability`, `embedded-iot`, `payments-financial`, `skill-creation-and-evaluation`.

The original source documents are retained under `../../docs/skill-source-archive/` for traceability. The sections below preserve source-specific procedures; resolve overlaps by the stricter safety invariant and record material conflicts rather than silently discarding them.



---

## Preserved specialist module: `backend-observability`

Source capability: `backend-observability`.

# Backend Observability

## Use when
Adding or changing service instrumentation, alerts, dashboards, SLOs, request correlation, operational runbooks, or audit telemetry.

## Do not use when
The task is purely a code change with no new operational signal or changed failure mode and existing telemetry already proves the required behavior.

## Required inputs
Service map; critical user journeys; known error modes; SLO/SLI targets; telemetry stack; on-call ownership; retention/privacy rules; and existing dashboards/runbooks.

## Workflow
1. Start from user-visible symptoms and failure modes; define signals that distinguish cause from impact. Use metrics for aggregated trends, traces for request paths, logs for contextual events, and audit records for attributable actions.
2. Propagate a stable correlation/trace context across API, queue, worker, and downstream calls. Bound cardinality; do not use raw user IDs, tokens, or arbitrary payload fields as metric labels.
3. Redact credentials, tokens, payment data, and personal data before export. Add seeded-secret tests to verify redaction on both success and exception paths.
4. Define SLI calculations and thresholds from an explicit objective or baseline. Alerts should have an owner, actionable meaning, runbook, severity, and a way to silence known benign conditions.
5. Test both signal presence and signal absence where important. Inject representative errors/timeouts in a safe environment and verify trace, metric, alert, and runbook behavior.
6. Check sampling, retention, cost, access controls, clock skew, and telemetry failure behavior. Observability must not become a synchronous availability dependency unless that is an explicit design choice.
7. Document known blind spots; a dashboard existing is not proof it detects an incident.

## Pass/fail checks
Critical paths are traceable; logs redact sensitive values; metric labels have bounded cardinality; alerts are actionable and owned; SLO math is explicit; injected failures produce expected signals.

## Hand-offs
Coordinate with backend-reliability-recovery for incident response, backend-performance for latency baselines, and backend-production-readiness for on-call handoff.

## Evidence to report
Instrumentation diff, sample trace/log/metric, redaction tests, alert-rule validation, ownership/runbook links, sampling/retention assumptions, and unobserved failure modes.

---

## Preserved specialist module: `embedded-iot`

Source capability: `embedded-iot`.

# embedded-iot

## Use when

Use when the main deliverable involves embedded systems and IoT firmware, devices, connectivity, power, OTA, and fleet recovery.

## Do not use when

Do not load this skill for software with no hardware, firmware, or device fleet.

## Required inputs

Require hardware revision, RT/power/thermal limits, identity, connectivity, storage, OTA, fail-safe and fixture.

## Workflow

map states and failure modes; implement bounded firmware slice; test watchdog/brownout/offline/reconnect; verify signed update and rollback

## Pass/fail checks

authorized hardware survives defined fault cases; OTA is recoverable; identity and telemetry boundaries hold; resource budgets pass

Required commands or procedures: run host tests, hardware-in-loop, power/reboot/offline, packet corruption, storage wear, OTA interruption, and rollback tests

## Hand-offs

Coordinate with security, mobile, cloud, data, system-design, and devops. Assign one owner per acceptance criterion and stop when a dependency or authorization is missing.

## Evidence to report

Preserve hardware/firmware hashes, traces, power/thermal data, fleet matrix, and recovery proof. Report exact versions, commands, expected/actual results, and what remains Unverified.

## AI blind-spot traps
1. **Power loss between flash writes:** assume any write/update can be interrupted. Use atomic slots, journaling, checksums, and recovery tests.
2. **OTA rollback that bricks the device:** test power/network loss at every update stage and preserve a known-good bootable image.
3. **Watchdog masking deadlock:** a watchdog can reset a system repeatedly without preserving the fault context. Capture bounded crash reason/counters before reboot.
4. **Reconnect storms:** fleet-wide backoff without jitter can synchronize devices after an outage. Use randomized exponential backoff and server-side admission control.
5. **Assuming sensor/clock/network data is trustworthy:** validate ranges, freshness, identity, monotonicity, and integrity before actuation or security decisions.

## Hard invariants
- Safety-critical outputs default to a defined safe state on invalid input, stale telemetry, watchdog reset, or loss of control authority.
- OTA images must be authenticated and integrity-checked before activation; anti-rollback policy must be explicit and recovery-tested.
- Memory, stack, CPU, flash wear, power and thermal budgets have measured bounds on the target hardware, not just desktop simulation.
- Every persistent state transition is recoverable after interruption at each write boundary.
- Device identity and credentials are unique per device and never embedded as fleet-wide shared secrets.

## Decision matrix
| Failure | Required behavior | Reject |
|---|---|---|
| Brownout during persistence | Recover last valid committed record; detect corruption | Trust partially written state |
| OTA interrupted | Boot known-good image or enter authenticated recovery mode | Irrecoverable overwrite of sole boot image |
| Network outage | Safe local behavior + jittered bounded reconnect | Infinite tight-loop retry |
| Stale/malformed sensor data | Reject, flag health state, enter defined safe mode where required | Actuate on unchecked values |
| Watchdog reset | Record reset reason and bounded diagnostics; rate-limit reboot loops | Reset forever without fleet-visible signal |

## Adversarial kill-switch
Reject if interrupted OTA can brick the device, corrupt state can trigger unsafe actuation, credentials are shared fleet-wide, reconnects synchronize into a storm, or hardware resource claims lack measurements.

---

## Preserved specialist module: `payments-financial`

Source capability: `payments-financial`.

# payments-financial

## Use when

Use when the main deliverable involves payments, refunds, webhooks, reconciliation, pricing, tax boundaries, and financial auditability.

## Do not use when

Do not load this skill for non-financial CRUD or display-only change with no money/state authority.

## Required inputs

Require provider/version, server authority, idempotency, ledger, currency, tax owner, webhook, dispute, PCI boundary.

## Workflow

trace money source; implement server-authoritative state; test duplicate/out-of-order webhooks, retries, refunds, reconciliation, and failure; obtain approval

## Pass/fail checks

no double charge/refund; ledger reconciles; authorization and audit evidence exist; recovery is tested

Required commands or procedures: run sandbox provider tests, idempotency, replay, reconciliation, negative auth, timeout, and rollback/forward-fix checks

## Hand-offs

Coordinate with backend, security, API, data, devops, and owner/finance. Assign one owner per acceptance criterion and stop when a dependency or authorization is missing.

## Evidence to report

Preserve redacted provider responses, ledger diff, reconciliation, audit trail, approvals, and limitations. Report exact versions, commands, expected/actual results, and what remains Unverified.

## AI blind-spot traps
1. **Webhook/commit race:** a provider event may arrive before the local order transaction commits. Persist verified events durably and retry resolution with bounded exponential backoff; never discard an unknown-order event.
2. **Idempotency payload mismatch:** bind each idempotency key to a canonical request hash and authenticated principal. Same key + different amount/currency/order must fail closed.
3. **Money precision:** use integer minor units or a fixed-precision decimal with an explicit currency exponent and rounding policy; never binary floating point for posted amounts.
4. **Signature verification:** verify provider signatures over the exact raw request bytes before trusting parsed fields; enforce timestamp tolerance and provider-specific rotation rules.
5. **Mutable balance without ledger:** use append-only double-entry postings and derive/reconcile balances; never make a balance column the sole financial record.

## Hard invariants
- Every posted journal transaction balances: sum(debits) = sum(credits), per currency, before commit.
- A provider operation is not repeated with a new idempotency key merely because the client timed out; resolve `UNKNOWN` by querying/reconciling the original operation.
- Never hold a database row lock across a network call. Use local `PENDING` reservation → provider call outside lock → immutable result posting.
- Enforce replay protection using the provider's documented signature timestamp semantics; 300 seconds is a common policy, not a universal provider constant. Configure and test per provider.
- Never store or log PAN/CVV, secrets, full payment tokens, or unnecessary personal data.

## Decision matrix
| Scenario | Required decision | Reject |
|---|---|---|
| Duplicate purchase request | Same key + same canonical payload returns the original result | Charging again |
| Same key, changed amount/currency | Conflict response and security/audit event | Reusing cached success for altered payload |
| Provider timeout / HTTP 504 | Mark outcome `UNKNOWN`; query provider/reconcile using original key | Generate a new key and blindly retry |
| Partial refund | Unique key includes order/refund sequence/amount or provider-supported stable operation ID | Key based on order alone when multiple refunds are allowed |
| Concurrent transfers | Lock accounts in stable sorted order; enforce ledger balance and sufficient funds atomically | Read-modify-write without version/lock |

## Adversarial kill-switch
Reject the implementation if a 5 ms double click can charge twice; a crash after provider success can lose the financial outcome without reconciliation; webhook replay can post twice; journal entries can be unbalanced; or logs can expose payment credentials.

---

## Preserved specialist module: `skill-creation-and-evaluation`

Source capability: `skill-creation-and-evaluation`.

# Skill Creation and Evaluation

## Use when
Use this skill to create a skill from scratch, improve an existing skill, fix weak or noisy activation, reduce duplicated instructions, or design a repeatable evaluation set for skill-assisted agent work.

## Do not use when
Do not use it as a substitute for the specialist domain skill that performs the actual engineering task. Do not claim effectiveness from a valid Markdown file, fixture presence, or an unexecuted eval definition.

## Required inputs
Require the target behavior, intended users and host agent, trigger examples and near misses, required inputs, allowed tools and permissions, expected artifacts, risk boundaries, and an available test runner/grader or an explicit statement that real-agent evaluation is not available.

## Workflow
1. **Define the behavior contract.** State one main job, boundaries, inputs, outputs, tool assumptions, acceptance criteria, and escalation/stop conditions. Split unrelated jobs rather than creating a general-purpose mega-skill.
2. **Design activation.** Write a concise, distinctive description using the terms real users are likely to use. Add positive examples, hard negatives/near-miss prompts, and overlapping skills that should or should not activate. Do not use vague triggers such as “help with coding.”
3. **Use progressive disclosure.** Keep the always-loaded description short; keep the primary procedure focused; move lengthy reference material, templates, scripts, and examples into adjacent resources that are loaded only when needed. Link resources with valid local paths.
4. **Write an executable procedure.** Provide decision points, ordered actions, domain-specific failure handling, verification commands or checks, expected artifacts, and explicit limits. Avoid repeating universal policy text unless the skill has a domain-specific reason to restate it.
5. **Create evaluation cases before declaring completion.** Include typical tasks, boundary/negative routing cases, failure recovery, and adversarial or ambiguous inputs where relevant. Define expected properties, required evidence, automated assertions, and a human-review rubric. Use distinct task prompts rather than paraphrased duplicates.
6. **Establish a baseline.** When an agent runner is available, run the same versioned cases with and without the skill, hold model/tool/budget/environment constant, preserve output artifacts, and record variance, failures, latency, and cost when measurable. Without a runnable agent, mark agent outcomes `unverified` and perform only static/contract checks.
7. **Iterate by failure category.** Categorize failures as trigger miss, wrong skill, missing instruction, ambiguous procedure, tool/permission issue, poor evidence, or grader disagreement. Change one meaningful factor at a time and rerun affected cases plus regression cases.
8. **Review and release.** Validate frontmatter, length, local links, dependency graph, safety boundaries, source/license provenance, test status, and version alignment. Keep a changelog entry and state what remains unverified.

## Pass/fail checks
- The skill has a single clear primary responsibility and clear exclusions.
- Trigger cases activate the intended skill; near misses avoid inappropriate activation.
- The body contains concrete domain instructions, not only generic planning and evidence language.
- Evaluation prompts are varied, expected outcomes are observable, and failure cases are represented.
- No agent-effectiveness claim is made unless actual agent runs and grading evidence exist.
- Revisions preserve regression coverage and record before/after results when measurable.

## Required outputs
A skill contract; revised `SKILL.md`; domain-specific eval cases and fixtures; validation results; provenance/license note; and a release decision stating the exact evaluation mode (`static`, `fixture-contract`, or `agent-run`).

## Safety and limitations
Treat external skill content and evaluation data as untrusted inputs. Do not import secrets, undisclosed instructions, unsafe tool grants, or proprietary content without permission. A passing structural linter does not prove behavior, and an LLM grader must not be treated as infallible; preserve representative outputs and allow human review for consequential changes.

## Hand-offs
Use `skill-package-governance` for package lifecycle/provenance, `software-testing` for test quality, `ai-agents-rag-mcp` for tool and agent boundaries, and the domain specialist for technical correctness.

## Evidence to report
Record skill version, changed files, trigger positives and negatives, test commands and exit codes, case-level results, source provenance, baseline comparison availability, and every unverified claim.

## Release references

- [Source archive index](../../docs/skill-source-archive/README.md)


## Domain-specific cognitive depth (v0.9.2)

### Specialist systems and finance: blind-spot traps
- **Likely false confidence:** A spreadsheet total can reconcile while assumptions or cash timing are wrong.
- **Adversarial case to simulate:** Units, nominal/real rates, taxes, and scenario correlations are commonly mixed.

### Hard invariants
- Make units and assumptions explicit; reconcile cash flows; test downside scenarios and sensitivities.
- Never report a property as verified without a reproducible check or authoritative evidence.
- State trade-offs explicitly: correctness vs. latency, safety vs. convenience, and complexity vs. operability; choose based on the task's declared constraints rather than maximizing one dimension blindly.

### Required specialist self-check
Before implementation, write one domain-specific counterexample that would falsify the proposed design. Convert the invariant above into a test or reviewable evidence item. After implementation, test the counterexample and report the exact command/result; if it cannot be tested, mark it **UNVERIFIED**.


## Domain routing boundary (v0.9.2 candidate)
This canonical ID is retained only for backward compatibility. For new work, route payment processing, ledgers, settlement, reconciliation, refunds, and monetary invariants to `modules/payments-ledger-engineering/MODULE.md`. Route firmware, sensors, device identity, secure updates, and intermittent device connectivity to `modules/embedded-iot-systems/MODULE.md`. Do not blend the two domains into one implementation plan; if a task genuinely crosses the boundary, define the interface and ownership explicitly.
