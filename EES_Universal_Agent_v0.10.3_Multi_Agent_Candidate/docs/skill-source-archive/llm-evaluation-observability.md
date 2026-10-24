---
name: llm-evaluation-observability
description: LLM application evaluation and observability for traces, datasets, task-level metrics, regression suites, model comparisons, retrieval quality, cost, latency, and safe release gates. Use when validating an agent or LLM feature beyond anecdotal demos.
version: 0.6.0
---

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
