---
name: media-games-desktop
description: "Canonical EES specialist for Media, games & desktop workflows; merges 3 compatible source capabilities while preserving their original IDs as aliases."
---

# Media, games & desktop workflows — Canonical Engineering Skill

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

Canonical ID: `media-games-desktop`  
Source capability aliases: `game-development`, `local-desktop-media-lifecycle`, `media-production`.

The original source documents are retained under `../../docs/skill-source-archive/` for traceability. The sections below preserve source-specific procedures; resolve overlaps by the stricter safety invariant and record material conflicts rather than silently discarding them.



---

## Preserved specialist module: `game-development`

Source capability: `game-development`.

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

---

## Preserved specialist module: `local-desktop-media-lifecycle`

Source capability: `local-desktop-media-lifecycle`.

# Local Desktop Media Lifecycle

## Use when
Implementing desktop app file access, local media import/export, conversion/transcoding, indexing, background workers, cancellation, or cleanup.

## Do not use when
The feature is browser-only and does not interact with local files, OS permissions, child processes, or long-running media work.

## Required inputs
Target OS/framework; user-consent model; file-size range; temporary-storage policy; child-process behavior; cancellation semantics; permissions; and recovery expectations.

## Workflow
1. Identify the user-selected source, destination, temporary paths, and any child processes. Use the narrowest platform-supported permission and avoid broad filesystem access by default.
2. Define lifecycle states: selected, validating, processing, completed, cancelled, failed, cleanup-pending, and recoverable. Ensure state survives app restart only when intended.
3. Make imports and exports atomic where practical: write to a temporary file, validate completion, then rename into place. Never silently overwrite the source; ask before replacing an existing destination.
4. Handle large files with bounded memory and streaming/chunking. Respect cancellation and platform background limits. Distinguish cancel request from confirmed process termination.
5. Clean temporary files on success, cancellation, and exceptions; add startup reconciliation for leftovers. Avoid deleting files outside the app-owned temp root.
6. Validate file type/size and guard path traversal, symlink surprises, malformed metadata, and shell argument injection when invoking an external tool. Invoke child processes with argument arrays, not interpolated shell strings.
7. Test permission denied, disk full, abrupt process exit, app restart, partial output, corrupted input, and process timeout; keep the original data intact.

## Pass/fail checks
Permissions are least-privilege; source files are preserved; partial output is detectable; cancellation/cleanup works; memory/storage use is bounded; child processes terminate or are recoverable; errors are surfaced safely.

## Hand-offs
Coordinate with mobile-desktop-development for platform APIs, media-production for codec/format behavior, and defensive-automation-and-audit for process allowlisting.

## Evidence to report
Platform/version, lifecycle state table, permission tests, large-file behavior, cancellation/cleanup artifacts, child-process invocation, and recovery limitations.

---

## Preserved specialist module: `media-production`

Source capability: `media-production`.

# media-production

## Use when

Use when the main deliverable involves video, audio, animation, motion, 3D assets, codecs, exports, playback, and rights.

## Do not use when

Do not load this skill for ordinary UI asset use without creation or export.

## Required inputs

Require source/provenance, rights, spec, codec, color/audio profile, captions, target devices, size/render budget.

## Workflow

inventory sources and rights; define spec; create/export; validate sync/captions/color; test playback and fallback; archive sources

## Pass/fail checks

exports meet spec, rights, captions/accessibility, sync, playback, size, and target-device criteria

Required commands or procedures: run metadata/codec inspection, ffprobe or equivalent, playback, caption, sync, render, memory, and reduced-motion checks

## Hand-offs

Coordinate with graphic-design, UI/UX, game/WebGL, websites, accessibility, and legal owner. Assign one owner per acceptance criterion and stop when a dependency or authorization is missing.

## Evidence to report

Preserve source manifest, rights record, export logs, media probes, screenshots/recordings, and limitations. Report exact versions, commands, expected/actual results, and what remains Unverified.

## Release references

- [Source archive index](../../docs/skill-source-archive/README.md)


## Domain-specific cognitive depth (v0.9.2)

### Media, games, and desktop: blind-spot traps
- **Likely false confidence:** A playable demo may hide frame-time spikes, lifecycle leaks, or platform-specific behavior.
- **Adversarial case to simulate:** Large assets, device loss, and background/foreground transitions create resource leaks.

### Hard invariants
- Bound memory and frame work; dispose resources deterministically; test target platforms.
- Never report a property as verified without a reproducible check or authoritative evidence.
- State trade-offs explicitly: correctness vs. latency, safety vs. convenience, and complexity vs. operability; choose based on the task's declared constraints rather than maximizing one dimension blindly.

### Required specialist self-check
Before implementation, write one domain-specific counterexample that would falsify the proposed design. Convert the invariant above into a test or reviewable evidence item. After implementation, test the counterexample and report the exact command/result; if it cannot be tested, mark it **UNVERIFIED**.
