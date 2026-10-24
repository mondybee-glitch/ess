#!/usr/bin/env sh
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
IMAGE=${EES_SANDBOX_IMAGE:-ees-pilot-sandbox:0.7.6}
docker build --pull -f "$ROOT/sandbox/Dockerfile" -t "$IMAGE" "$ROOT"
printf 'Built sandbox image: %s\n' "$IMAGE"
printf 'Before a production release, resolve and pin the exact image digest.\n'
