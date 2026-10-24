---
name: local-desktop-media-lifecycle
description: Local desktop and media workflows covering file permissions, import/export, long-running jobs, cancellation, temporary storage, process lifecycle, and recovery.
version: 0.7.2
---

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
