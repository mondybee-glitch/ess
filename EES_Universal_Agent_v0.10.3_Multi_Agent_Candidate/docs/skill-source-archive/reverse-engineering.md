---
name: reverse-engineering
description: Reconstruct program, binary, protocol, and file-format behavior using static and dynamic evidence.
version: 0.6.0
---

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
