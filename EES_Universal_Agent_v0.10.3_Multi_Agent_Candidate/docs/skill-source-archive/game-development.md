---
name: game-development
description: Specialist workflow for games and game engines, gameplay systems, scenes, saves, input, performance, and platform builds. Use when the task materially involves this boundary.
version: 0.6.0
---

# game-development

## Use when

Use when the main deliverable involves games and game engines, gameplay systems, scenes, saves, input, performance, and platform builds.

## Do not use when

Do not load this skill for ordinary web UI with no game loop or engine.

## Required inputs

Require engine/version, target platforms, input, save schema, frame/memory/thermal budgets.

## Workflow

map loop and state; implement deterministic rules; handle pause/focus/save migration; profile; export; test device inputs and recovery

## Pass/fail checks

game loop remains stable; saves migrate; target builds launch; frame/memory/load budgets meet profile; no progression/economy regression

Required commands or procedures: run engine tests, exported build smoke, save migration, input/focus, profiler, and device checks

## Hand-offs

Coordinate with system-design, graphics, mobile/desktop, backend, QA, and devops. Assign one owner per acceptance criterion and stop when a dependency or authorization is missing.

## Evidence to report

Preserve build artifacts, save fixtures, profiler traces, screenshots/video, and device results. Report exact versions, commands, expected/actual results, and what remains Unverified.
