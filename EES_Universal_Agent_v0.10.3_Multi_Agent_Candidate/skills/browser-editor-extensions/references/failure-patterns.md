# browser-editor-extensions: Deep Failure Patterns

This reference expands the invariant-first checklist in `../SKILL.md`. Treat values as defaults only where explicitly stated; validate against the actual provider, platform, hardware, and threat model.

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


## Evidence checklist
- Record assumptions and versioned dependencies.
- Include at least one negative test per trust boundary.
- Include concurrency, timeout, restart, and recovery cases where applicable.
- Capture exact commands, exit codes, and artifact hashes.
- Separate static review from executed evidence; mark unrun checks `UNVERIFIED`.
