---
name: ai-evaluation-observability
description: "Canonical EES specialist for LLM evaluation & observability; merges 3 compatible source capabilities while preserving their original IDs as aliases."
---

# LLM evaluation & observability — Canonical Engineering Skill

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

Canonical ID: `ai-evaluation-observability`  
Source capability aliases: `llm-evaluation-observability`, `machine-learning-evaluation`, `observability-and-ai-evaluation`.

The original source documents are retained under `../../docs/skill-source-archive/` for traceability. The sections below preserve source-specific procedures; resolve overlaps by the stricter safety invariant and record material conflicts rather than silently discarding them.



---

## Preserved specialist module: `llm-evaluation-observability`

Source capability: `llm-evaluation-observability`.

# LLM Evaluation and Observability

## Use when
Use when evaluating agents, chains, RAG, tool use, structured output, model changes, prompts, or production LLM behavior.

## Do not use when
Do not use for a one-off prompt experiment with no acceptance claim or for ordinary deterministic unit tests.

## Required inputs
Require task set, ground-truth or rubric, representative and adversarial cases, model/provider versions, dataset privacy rules, trace fields, latency/cost budgets, baseline, and promotion threshold.

## Workflow
1. Define task-level success and failure dimensions before choosing a model or prompt. Include correctness, refusal/safety, groundedness, tool behavior, latency, cost, and regressions as applicable.
2. Build a fixed evaluation set with normal, boundary, multilingual, adversarial, and failure-recovery cases. Keep fixtures versioned and privacy-minimized.
3. Capture traces that connect input, retrieval, model, tool, output, timing, tokens, cost, and error without storing secrets or unnecessary personal data.
4. Compare candidates under the same dataset, settings, budgets, and evaluator. Separate automated scores from human review and report uncertainty.
5. Test retrieval separately from generation. Inspect citation support, missing context, stale documents, prompt injection, and context-window failures.
6. Gate release on stated thresholds and rollback triggers. A high aggregate score cannot hide a critical failure slice.

## Pass/fail checks
Pass only when results are reproducible enough for the stated claim, critical slices are reviewed, traces support diagnosis, privacy is respected, and promotion/rollback criteria are explicit.

Required commands or procedures: run the fixed suite; compare baseline/candidate; inspect representative traces; measure latency/cost; review critical failures; retain report and environment metadata.

## Hand-offs
Hand off tool safety to `llm-tool-contracts`, retrieval implementation to `search-retrieval`, and deployment gates to `devops-and-deployment`.

## Evidence to report
Report dataset version, evaluator method, model/provider settings, slice results, traces, cost/latency, human-review sample, privacy controls, and unverified generalization.

---

## Preserved specialist module: `machine-learning-evaluation`

Source capability: `machine-learning-evaluation`.

# machine-learning-evaluation

## Use when

Use when the main deliverable involves dataset/versioned model evaluation, reproducibility, safety, drift, and promotion decisions.

## Do not use when

Do not load this skill for ordinary deterministic feature with no learned model.

## Required inputs

Require dataset/model/code versions, split policy, baseline, metrics, slices, seeds, thresholds, approval, rollback.

## Workflow

freeze data and baseline; test leakage; evaluate slices and uncertainty; probe edge/adversarial cases; measure latency/cost; define promotion and rollback

## Pass/fail checks

reproducible metrics beat baseline under declared uncertainty; no leakage; critical slices and safety tests pass; fallback exists

Required commands or procedures: run training/eval with pinned environment, leakage checks, slice metrics, calibration/drift probes, and regression suite

## Hand-offs

Coordinate with data, backend, security, AI automation, system-design, and product owner. Assign one owner per acceptance criterion and stop when a dependency or authorization is missing.

## Evidence to report

Preserve dataset/model hashes, metrics, confidence, slice report, cost/latency, and promotion decision. Report exact versions, commands, expected/actual results, and what remains Unverified.

---

## Preserved specialist module: `observability-and-ai-evaluation`

Source capability: `observability-and-ai-evaluation`.

# Observability And Ai Evaluation

## Use when
When establishing AI tracing/evaluation or authorized infrastructure metrics, alerts, anomaly, replication, and read-only MCP workflows.

## Do not use when
Do not use when the task does not match the stated domain, lacks required authorization, or is a simpler task owned by another specialist.

## Required inputs
telemetry schema and minimization policy; authorized metrics/logs/traces; evaluation datasets and retention policy; deployment topology and access controls.

## Purpose
Instrument and evaluate AI and infrastructure systems with data minimization, masking, trace/metric contracts, reproducible experiments, alert triage, and clear limits on what telemetry can prove.

## Workflow
1. Confirm scope, authorization, versions, data classification, and acceptance criteria before acting.
2. Separate planning, read-only inspection, implementation or analysis, and verification. Keep side effects behind explicit approval.
3. Record source evidence, assumptions, exact commands, artifacts, and unresolved uncertainty. Never infer success from intent, generated text, or a partial check.
4. Compose only the secondary skills that own distinct controls; hand off implementation, testing, security, and release responsibilities explicitly.

## Pass/fail checks
Pass only when the required inputs are present, boundaries are respected, outputs are reproducible enough for the stated claim, and incomplete or failed checks are reported as such.

Required outputs: dashboards and alert triage; evaluation report; latency/cost/quality trends; retention/masking/escalation recommendations.

## Safety and limits
Do not collect sensitive telemetry without authorization. Redact secrets and personal data; keep runtime enforcement in appropriate guardrail layers. Do not claim telemetry alone proves root cause or safety.

## Verification
- Run PII/secret masking and trace/metric schema tests.
- Test alert deduplication, retention, backup/restore, and read-only authorization.
- Reproduce evaluation results with model/dataset/version metadata and human review.

## Hand-offs
Hand off implementation, testing, security, and release responsibilities to the selected specialist owners; do not silently duplicate their work.

## Evidence to report
Report selected sources and revisions, authorization and scope, commands and exit codes, artifacts, coverage limits, risks, handoffs, and what remains Unverified.

## Release references

- [Source archive index](../../docs/skill-source-archive/README.md)


## Domain-specific cognitive depth (v0.9.2)

### AI evaluation: blind-spot traps
- **Likely false confidence:** Aggregate scores can hide catastrophic failures; segment by task class and severity.
- **Adversarial case to simulate:** Dataset leakage and evaluator contamination can inflate scores without improving capability.

### Hard invariants
- Every claim links to immutable case/version evidence; compare on the same frozen evaluation set.
- Never report a property as verified without a reproducible check or authoritative evidence.
- State trade-offs explicitly: correctness vs. latency, safety vs. convenience, and complexity vs. operability; choose based on the task's declared constraints rather than maximizing one dimension blindly.

### Required specialist self-check
Before implementation, write one domain-specific counterexample that would falsify the proposed design. Convert the invariant above into a test or reviewable evidence item. After implementation, test the counterexample and report the exact command/result; if it cannot be tested, mark it **UNVERIFIED**.
