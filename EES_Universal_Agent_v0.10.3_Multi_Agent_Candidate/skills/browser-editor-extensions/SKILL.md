---
name: browser-editor-extensions
description: "Canonical EES specialist for Browser & editor extensions; merges 2 compatible source capabilities while preserving their original IDs as aliases."
---

# Browser & editor extensions — Canonical Engineering Skill

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

Canonical ID: `browser-editor-extensions`  
Source capability aliases: `browser-editor-extensions`, `editor-plugin-architecture`.

The original source documents are retained under `../../docs/skill-source-archive/` for traceability. The sections below preserve source-specific procedures; resolve overlaps by the stricter safety invariant and record material conflicts rather than silently discarding them.



---

## Preserved specialist module: `browser-editor-extensions`

Source capability: `browser-editor-extensions`.

# browser-editor-extensions

## Use when

Use when the main deliverable involves browser and editor extensions, manifests, permissions, content scripts, APIs, packaging, and updates.

## Do not use when

Do not load this skill for web app code with no extension/editor runtime or permissions.

## Required inputs

Require manifest/SDK version, host permissions, trust boundary, browser/editor matrix, signing/store policy.

## Workflow

map permissions and contexts; implement least-privileged slice; test content/background isolation, messaging, packaging, update, and uninstall

## Pass/fail checks

supported hosts/editors work with minimal permissions; no data leakage; package validates and rollback/uninstall works

Required commands or procedures: run manifest/schema, permission negative, host matrix, messaging, package/signature, update/uninstall, and regression tests

## Hand-offs

Coordinate with frontend, security, technical platforms, devops, and documentation. Assign one owner per acceptance criterion and stop when a dependency or authorization is missing.

## Evidence to report

Preserve manifest diff, permission rationale, package hash, host results, screenshots, and limitations. Report exact versions, commands, expected/actual results, and what remains Unverified.

## AI blind-spot traps
1. **Permission creep:** host permissions are often broadened for convenience. Start with the narrowest host/path permissions and justify every permission in a manifest-to-feature table.
2. **Content-script trust confusion:** page DOM and `window` messages are attacker-controlled, even on a trusted site. Treat page data as untrusted and never pass privileged extension messages without schema and sender validation.
3. **Confused-deputy messaging:** validate `sender.id`, tab/frame/origin constraints, message type, payload schema, and allowed action; do not expose generic privileged RPC.
4. **Secrets in extension storage:** extension bundles and local storage are not secure secret vaults. Do not ship provider secrets or long-lived privileged credentials to clients.
5. **Update and lifecycle gaps:** test service-worker suspension/restart, duplicate listeners, migration, uninstall cleanup, and rollback/update compatibility.

## Hard invariants
- Privileged actions are allow-listed by message type and validated at the receiving boundary; reject unknown fields/actions by default.
- Content scripts assume the DOM is hostile. Never use DOM text as an instruction or authority signal.
- No remote executable code or dynamically evaluated strings; comply with the target platform's extension CSP and store policies.
- Permissions are least-privilege, documented, and covered by negative tests proving denied hosts/actions fail.
- User data collection is purpose-limited, minimized, disclosed, and deleted on the defined retention/uninstall path.

## Decision matrix
| Scenario | Required decision | Reject |
|---|---|---|
| Need one host | Restrict host permissions to required origins/paths where supported | `<all_urls>` without a documented, unavoidable need |
| Content script requests privileged action | Typed allow-listed message + sender/context checks | Arbitrary command or URL passed to background worker |
| API credential needed | Backend broker or user-authenticated flow with scoped token | Embed a server secret in the package |
| Manifest migration | Versioned migration, idempotent restart-safe logic, backup/rollback where possible | Destructive migration without recovery |
| Store release | Build reproducibly, inspect permissions, hash/sign artifacts, test upgrade and uninstall | Treat local load success as release verification |

## Adversarial kill-switch
Reject if a hostile page can trigger privileged extension actions, messages are accepted from untrusted contexts, a secret is recoverable from the package, permissions exceed the feature contract, or update/uninstall leaves sensitive state behind.

---

## Preserved specialist module: `editor-plugin-architecture`

Source capability: `editor-plugin-architecture`.

# Editor Plugin Architecture

## Use when
Use when designing or extending an editor, visual builder, CAD/3D tool, scene graph, node registry, or plugin ecosystem.

## Do not use when
Do not use for a static canvas or an ordinary CRUD screen with no editor state, rendering systems, or extension contract.

## Required inputs
Require the domain schema, hierarchy rules, persistence format, renderer/system ownership, selection and tool model, undo/redo policy, plugin lifecycle, package boundaries, and compatibility policy.

## Workflow
1. Define stable data primitives and discriminators. Keep persisted domain state separate from transient selection, hover, camera, and render caches.
2. Choose an explicit hierarchy or relational representation and document parent/child invariants, deletion rules, references, and migration behavior.
3. Separate schema, state store, registry, renderer, systems, tools, and UI. A renderer should not silently own domain mutations or persistence.
4. Make plugin registration explicit: version, capabilities, schemas, renderers, migrations, cleanup, permissions, and failure isolation.
5. Design undo/redo and persistence around transactions or meaningful commands. Test partial failure, reload, duplicate registration, and incompatible plugin versions.
6. If agents or MCP tools are exposed, define bounded commands, validation, idempotency, authorization, and a local-first data boundary.

## Pass/fail checks
Pass only when state ownership and extension contracts are explicit, persisted data is versioned, transient state is not accidentally serialized, and plugin failure cannot silently corrupt the document.

Required commands or procedures: validate schemas; run store and renderer tests; exercise create/update/delete, undo/redo, reload, migration, duplicate plugin, and malformed command paths; record evidence.

## Hand-offs
Hand off 3D rendering to `game-development`, agent tools to `ai-agents-rag-mcp`, and frontend interaction to `frontend-development`.

## Evidence to report
Report schemas, invariants, package ownership, plugin contract, migration results, command validation, persistence/reload evidence, and unverified rendering or device limits.

## Release references

- [Source archive index](../../docs/skill-source-archive/README.md)


## Domain-specific cognitive depth (v0.9.2)

### Browser/editor extensions: blind-spot traps
- **Likely false confidence:** Content scripts and background contexts have different lifecycles and permissions.
- **Adversarial case to simulate:** Message sender spoofing, stale tabs, and service-worker suspension break naive flows.

### Hard invariants
- Validate sender/origin and message schema; request least privilege; tolerate restart and duplicate delivery.
- Never report a property as verified without a reproducible check or authoritative evidence.
- State trade-offs explicitly: correctness vs. latency, safety vs. convenience, and complexity vs. operability; choose based on the task's declared constraints rather than maximizing one dimension blindly.

### Required specialist self-check
Before implementation, write one domain-specific counterexample that would falsify the proposed design. Convert the invariant above into a test or reviewable evidence item. After implementation, test the counterexample and report the exact command/result; if it cannot be tested, mark it **UNVERIFIED**.
