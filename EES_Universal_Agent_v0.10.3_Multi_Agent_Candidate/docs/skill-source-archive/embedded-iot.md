---
name: embedded-iot
description: Specialist workflow for embedded systems and IoT firmware, devices, connectivity, power, OTA, and fleet recovery. Use when the task materially involves this boundary.
version: 0.6.0
---

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

