#!/usr/bin/env sh
# Fail-closed risk-tiered Docker sandbox. Requires Docker and GNU timeout.
set -eu
if [ "$#" -lt 3 ]; then echo "Usage: $0 TASK_DIRECTORY RISK_TIER -- COMMAND [ARG ...]" >&2; exit 64; fi
TASK_DIR=$1; RISK=$2; shift 2
if [ "$1" != "--" ]; then echo "Expected -- before command" >&2; exit 64; fi
shift
if [ "$#" -lt 1 ]; then echo "Missing command" >&2; exit 64; fi
TASK_DIR=$(CDPATH= cd -- "$TASK_DIR" && pwd)
SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
POLICY=$(python3 "$SCRIPT_DIR/sandbox_policy.py" --risk "$RISK") || { echo "Sandbox policy rejected task" >&2; exit 77; }
# Keep runtime options fixed by reviewed profiles; do not eval policy output.
case "$RISK" in
 low) MEMORY=512m; CPUS=1; PIDS=64; TIMEOUT=120; TMPFS=32m; WORKSPACE_MODE=rw ;;
 medium) MEMORY=1g; CPUS=2; PIDS=128; TIMEOUT=300; TMPFS=64m; WORKSPACE_MODE=rw ;;
 high) MEMORY=2g; CPUS=2; PIDS=128; TIMEOUT=180; TMPFS=64m; WORKSPACE_MODE=ro ;;
 *) echo "Unknown risk tier" >&2; exit 64 ;;
esac
IMAGE=${EES_SANDBOX_IMAGE:-}
if ! printf '%s\n' "$IMAGE" | grep -Eq '^.+@sha256:[a-fA-F0-9]{64}$'; then
  echo "EES_SANDBOX_IMAGE must be set to an immutable image digest (name@sha256:<64 hex characters>)" >&2
  exit 78
fi
exec timeout --signal=TERM --kill-after=5s "$TIMEOUT" docker run --rm \
  --user 10001:10001 --read-only \
  --tmpfs /tmp:rw,noexec,nosuid,nodev,size="$TMPFS" \
  --network none --cap-drop ALL --security-opt no-new-privileges:true \
  --pids-limit "$PIDS" --memory "$MEMORY" --cpus "$CPUS" \
  --mount "type=bind,src=$TASK_DIR,dst=/workspace/task,$WORKSPACE_MODE" \
  --workdir /workspace/task "$IMAGE" "$@"
