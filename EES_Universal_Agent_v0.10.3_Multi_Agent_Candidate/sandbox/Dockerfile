# Controlled-pilot toolchain: Node + Python. GA gate: review Trivy findings, then pin an audited multi-platform image digest.
FROM node:22-bookworm-slim
ENV DEBIAN_FRONTEND=noninteractive \
    PLAYWRIGHT_BROWSERS_PATH=/ms-playwright \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1
RUN apt-get update \
 && apt-get install -y --no-install-recommends python3 python3-pip python3-venv git ca-certificates curl jq build-essential \
 && rm -rf /var/lib/apt/lists/*
RUN python3 -m pip install --break-system-packages --no-cache-dir pytest
WORKDIR /workspace
# The Playwright fixture dependencies are installed separately so the base image remains useful for Python-only checks.
# Build context must be the project root. A committed package-lock.json is mandatory.
COPY operational-fixtures/playwright-ui-state/package.json operational-fixtures/playwright-ui-state/package-lock.json /tmp/ees-playwright/
RUN cd /tmp/ees-playwright \
 && npm ci --no-audit --no-fund \
 && npx playwright install --with-deps chromium \
 && mkdir -p /ms-playwright \
 && chmod -R a+rX /ms-playwright
# Runtime invocation must pass a non-root UID, drop capabilities, use a read-only rootfs,
# disable network by default, and mount only an isolated writable task directory.
