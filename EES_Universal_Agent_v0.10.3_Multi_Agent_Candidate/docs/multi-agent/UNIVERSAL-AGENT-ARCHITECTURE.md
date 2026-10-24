# EES Universal Agent Architecture

## Goal
Share the EES skill corpus, routing data, evidence contract, and quality gates across Gemini, Google Antigravity, and Claude, with a portable baseline for ChatGPT/cloud coding environments.

## Layers
1. **Core contract:** `AGENTS.md`, `SKILL.md`, `QUALITY-GATE.md`, registry, routing map, schemas, tests.
2. **Instruction adapters:** `GEMINI.md`, `.agent/rules/ees.md`, `CLAUDE.md`; each is an entry point, not an executable runtime.
3. **Provider integration:** separate scripts and credentials per provider; no assumption that model APIs or tool schemas are interchangeable.
4. **Evidence and evaluation:** common acceptance criteria and status vocabulary; per-provider smoke/evaluation results remain separate.
5. **Execution boundary:** local or cloud environment supplies actual tools, permissions, filesystem, network and sandbox. EES instructions cannot grant these capabilities.

## Adapter conformance checklist
- [ ] Instructions were actually discovered by the selected product.
- [ ] A known task resolves to a canonical route and an existing skill path.
- [ ] Tool and permission availability are reported accurately.
- [ ] A deliberately malformed or unsupported task is rejected clearly.
- [ ] Evidence references real test outputs and distinguishes static from live checks.
- [ ] No secrets appear in logs, prompts, artifacts, or source control.
- [ ] Relevant repository tests pass.
- [ ] Provider-specific smoke test passes, or is explicitly marked BLOCKED/UNVERIFIED.

## Release rule
Do not label the cross-agent release production-ready until conformance and provider smoke tests have run in each target environment. A static test that verifies files exist is not proof an agent loaded them. A shared instruction file is not an API adapter. A successful API request is not proof of end-to-end task quality.
