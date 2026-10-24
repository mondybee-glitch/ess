---
name: machine-learning-evaluation
description: Specialist workflow for dataset/versioned model evaluation, reproducibility, safety, drift, and promotion decisions. Use when the task materially involves this boundary.
version: 0.6.0
---

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
