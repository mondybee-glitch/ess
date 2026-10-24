---
name: devops-and-deployment
description: Git workflows, Docker, CI/CD, Linux administration, cloud and hosting, monitoring, logging, backups, and rollback. Use for building pipelines, deploying, infrastructure configuration, and operational triage.
version: 0.6.0

---

# DevOps and Deployment

## Use when
- Dockerfiles, CI pipelines, deploy scripts
- Monitoring, logging, backup and rollback design
- Operational incidents that are not security incidents

## Do not use when
- Writing application logic

## Required inputs
- Hosting target and access method
- Environments and their owners
- Deploy and rollback approvals

## Workflow
1. Detect environments, runtimes, and existing pipeline.
2. Make builds reproducible: lockfiles, pinned base image tag or digest.
3. Pipeline order: lint, test, build, scan, deploy.
4. Deploy in stages or behind a flag; add health checks.
5. Test rollback before relying on it; prove backups by a restore test.
6. Keep secrets in a secret manager; grant least privilege.
7. Monitor latency, traffic, errors, saturation.

## Pass/fail checks
- Container runs as non-root; `.dockerignore` present
- Images and Actions pinned
- No secrets in images, logs, or CI output
- Restore test executed, or backup marked `unverified`
- Production deploy has explicit human approval

## Hand-offs
- security-review for pipeline and image review
- backend-development for migration coordination

## Evidence to report
Commands run with results, files changed, and anything not verified. Use the status vocabulary from the core [SKILL.md](../../SKILL.md).

## Concrete commands

Run `docker build`, `docker run` smoke checks, CI locally where supported, IaC plan rather than apply first, health checks, and a documented rollback command.
