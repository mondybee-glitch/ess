---
name: media-production
description: Specialist workflow for video, audio, animation, motion, 3D assets, codecs, exports, playback, and rights. Use when the task materially involves this boundary.
version: 0.6.0
---

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
