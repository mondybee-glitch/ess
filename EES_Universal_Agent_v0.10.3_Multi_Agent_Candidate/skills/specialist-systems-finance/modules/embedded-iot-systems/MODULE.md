---
name: embedded-iot-systems
type: governed-specialist-module
canonical_route: specialist-systems-finance
---

# Embedded & IoT Systems

## Domain boundary
Own device firmware, constrained resources, sensor/actuator interfaces, boot/update lifecycle, device identity, and intermittent connectivity. Do not route financial ledger or payment settlement decisions here.

## Hard invariants
- Safety-relevant outputs fail to a defined safe state when inputs are invalid, stale, or unavailable.
- Firmware updates are authenticated, integrity-checked, versioned, recoverable, and protected against downgrade where required.
- Device identity and credentials are unique per device; fleet-wide shared secrets are a last-resort documented risk.
- Watchdogs, retries, and queues are bounded; watchdog reset loops are observable and rate-limited.
- Time is not trusted as monotonic across reboot; distinguish monotonic timers from wall-clock timestamps.
- Design for power loss at every persistent write boundary and test recovery.

## Blind-spot traps
- Assuming packets arrive once, in order, and within a bounded delay.
- Persisting partially written configuration or firmware metadata.
- Reusing device credentials across manufacturing batches.
- Failing open when secure boot, certificate validation, or update signature checks fail.
- Ignoring clock drift, sensor calibration, brownouts, and resource exhaustion.
- Treating a successful cloud publish as proof the device acted on a command.

## Required tests
Power interruption during update; invalid signature and downgrade attempts; replayed commands; offline queue overflow; clock drift; watchdog reset; corrupted persistent state; device identity rotation; safe-state transition; constrained-memory stress.
