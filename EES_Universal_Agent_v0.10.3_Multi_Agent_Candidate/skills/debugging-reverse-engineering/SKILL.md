---
name: debugging-reverse-engineering
description: "Canonical EES specialist for Debugging & reverse engineering; merges 2 compatible source capabilities while preserving their original IDs as aliases."
---

# Debugging & reverse engineering — Canonical Engineering Skill

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

Canonical ID: `debugging-reverse-engineering`  
Source capability aliases: `debugging-and-code-repair`, `reverse-engineering`.

The original source documents are retained under `../../docs/skill-source-archive/` for traceability. The sections below preserve source-specific procedures; resolve overlaps by the stricter safety invariant and record material conflicts rather than silently discarding them.



---

## Preserved specialist module: `debugging-and-code-repair`

Source capability: `debugging-and-code-repair`.

# Debugging and Code Repair

## Use when
- Bug reports and failing tests
- Regressions and crashes
- Refactors that must preserve behavior

## Do not use when
- New features with no defect

## Required inputs
- Observed vs expected behavior
- Version or commit where it appeared
- Logs, stack traces, steps

## Workflow
1. Reproduce first: a failing test or script. If it cannot be reproduced, say so and stop short of patching blind.
2. Minimize the reproduction.
3. Rank hypotheses; test cheapest first; use `git bisect` for regressions.
4. Fix the root cause with the smallest diff.
5. Add a regression test that fails before and passes after.
6. Search for sibling occurrences of the same pattern.
7. Run the full relevant suite.

## Pass/fail checks
- Fail-before and pass-after evidence shown
- Diff contains no unrelated edits (`git diff --stat`)
- Flaky behavior: at most 5 diagnostic reruns, rate recorded
- Root cause stated in one sentence

## Hand-offs
- software-testing for coverage gaps
- security-review when the bug is a vulnerability

## Evidence to report
Commands run with results, files changed, and anything not verified. Use the status vocabulary from the core [SKILL.md](../../docs/skill-source-archive/debugging-and-code-repair.md).

## Concrete commands

Reproduce first, then run the smallest failing test and the relevant regression set; preserve the failing trace and compare behavior before and after the patch.

---

## Preserved specialist module: `reverse-engineering`

Source capability: `reverse-engineering`.

# Reverse Engineering

## Use when
Use for binary triage, compatibility, undocumented formats/protocols, crash analysis, and behavior reconstruction.

## Do not use when
Prefer source-level debugging when source code is available and answers the question more directly.
Do not use for third-party protection changes or targets outside the approved scope.

## Required inputs
Sample or target artifact, expected question, known platform/format, available environment, and output format. Record provenance and hash where useful.

## Workflow
1. Record SHA-256, file type, size, architecture, tool versions, OS image, and date. Preserve the original; work on a copy.
2. Start with non-executing inspection: `sha256sum sample.bin`, `file sample.bin`, `strings -a -n 6 sample.bin | head -200`, `readelf -h -S -s sample.bin`, `objdump -d -M intel sample.bin`.
3. Use format-specific tools as appropriate: Ghidra, Cutter/radare2, IDA, gdb/lldb, Frida, jadx, apktool, binwalk, Wireshark.
4. Form hypotheses from multiple signals; treat decompiler output as a hypothesis, not ground truth.
5. For dynamic work, use a disposable isolated VM/container with snapshots, controlled networking, no production credentials, and resource limits. Record files, syscalls/API calls, network events, state changes, and crashes.
6. For formats/protocols, document offsets, lengths, endianness, encoding, checksums, state transitions, unknown fields, and confidence.
7. Minimize crashing inputs and retain exact hashes and reproduction commands.

## Pass/fail checks
- Sample hash and tool versions are recorded.
- Static evidence is separated from dynamic observations.
- Findings can be reproduced with the same input/environment.
- Unknown fields and confidence are explicit.
- Dynamic execution is isolated from production assets.

## Hand-offs
Hand off to `software-testing` for differential/fuzz regression cases; `defensive-security-ops` for incident indicators and containment; `technical-documentation` for a format/protocol specification.

## Evidence to report
Environment and hashes, tools/versions, methods, observed behavior, reconstructed logic/format, confidence, limitations, and reproducible next steps.

## Concrete commands

Use isolated copies and authorized samples; record hashes, static observations, dynamic traces, and scope. Use `file`, `strings`, `objdump`, or a sandboxed debugger only within authorization.

## Release references

- [Source archive index](../../docs/skill-source-archive/README.md)


## Domain-specific cognitive depth (v0.9.2)

### Debugging and reverse engineering: blind-spot traps
- **Likely false confidence:** The first visible exception may be downstream of the true cause.
- **Adversarial case to simulate:** A fix that suppresses symptoms can corrupt state or conceal a race.

### Hard invariants
- Reproduce, isolate, and preserve a failing test; distinguish observation from hypothesis.
- Never report a property as verified without a reproducible check or authoritative evidence.
- State trade-offs explicitly: correctness vs. latency, safety vs. convenience, and complexity vs. operability; choose based on the task's declared constraints rather than maximizing one dimension blindly.

### Required specialist self-check
Before implementation, write one domain-specific counterexample that would falsify the proposed design. Convert the invariant above into a test or reviewable evidence item. After implementation, test the counterexample and report the exact command/result; if it cannot be tested, mark it **UNVERIFIED**.
