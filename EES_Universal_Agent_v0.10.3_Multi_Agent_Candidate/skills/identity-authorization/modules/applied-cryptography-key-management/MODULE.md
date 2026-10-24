---
name: applied-cryptography-key-management
description: "Applied cryptography, key lifecycle, privacy boundaries, and cryptographic protocol review."
---

# Applied Cryptography & Key Management

## Mission and decision boundary
Use established, maintained cryptographic libraries and managed KMS/HSM services. Do not design new primitives, protocols, ciphers, padding schemes, random generators, or home-grown key wrapping. If requirements do not identify the threat model, data lifetime, regulatory boundary, key owner, and recovery model, stop and ask.

## Hard invariants
- Prefer authenticated encryption: AES-256-GCM or ChaCha20-Poly1305 through a reputable library. Never use ECB; do not use unauthenticated encryption without a separately reviewed integrity construction.
- A nonce/IV must never repeat under the same key for AES-GCM or ChaCha20-Poly1305. Use a library-approved CSPRNG or a rigorously designed counter allocation scheme; document uniqueness across processes, replicas, restores, and failover.
- Never use `Math.random`, `random.random`, timestamps, UUIDs without a reviewed construction, or application identifiers as cryptographic randomness.
- Passwords are not encrypted. Store password verifiers with Argon2id using parameters calibrated to the deployment; use a vetted password-hashing library and unique salts. Do not substitute raw SHA-256, MD5, SHA-1, or a fast general-purpose hash.
- Compare secret MACs and authentication tokens using constant-time comparison APIs where available; do not rely on ordinary string equality for secret-dependent comparisons.
- Use envelope encryption for data keys at scale: generate a DEK with a CSPRNG, encrypt data with an AEAD, and wrap the DEK using a KMS/HSM-managed KEK. Persist algorithm/version, key identifier, nonce, tag, and required AAD alongside ciphertext; never persist plaintext keys in logs or source.
- Rotation must support key versioning and staged migration: new writes use the active key, old key versions remain decrypt-capable until rewrapped or expired, and rollback/recovery is tested before retiring keys.
- Bind ciphertext to context using authenticated additional data (AAD), such as tenant, record ID, schema/version, and purpose, where appropriate. Validate that context before decrypting to prevent cross-tenant substitution.
- Avoid logging plaintext, keys, DEKs, credentials, full tokens, or decrypted sensitive payloads. Redaction must be tested, not assumed.
- Cryptographic hashes detect changes only when the expected digest is trusted. For tamper-evident event provenance, use signed checkpoints or a signature chain with protected private keys, key IDs, rotation/revocation rules, and verification tooling. Hash chains alone do not authenticate the writer.
- PQC readiness is a migration plan, not an instruction to invent a hybrid protocol. Track standardized algorithms and vetted provider support; define crypto-agility, versioned envelopes, and migration inventory. Do not deploy experimental algorithms without explicit approval.

## Blind-spot traps
1. Reusing a nonce after a process restart, snapshot restore, or replica failover.
2. Treating Base64, hashing, obfuscation, or TLS as application-level encryption at rest.
3. Reusing one key across tenants, purposes, environments, or encryption and signing.
4. Omitting AAD and accepting ciphertext copied from another tenant or record.
5. Rotating the KEK but forgetting wrapped DEKs, backups, replicas, and disaster-recovery copies.
6. Destroying an old key before verifying that all live data and backups have migrated.
7. Reporting a SHA-256 event chain as “signed” or “immutable” without a protected signing key and verifier.
8. Catching authentication/decryption errors and returning success or partial plaintext.
9. Adding custom crypto fallbacks when the KMS or secure random source is unavailable.
10. Selecting cryptographic parameters by a universal hard-coded rule without checking library support, threat model, latency, compliance, and recovery needs.

## Required workflow
1. State assets, threat model, attacker capabilities, retention, tenant boundaries, and recovery requirements.
2. Identify the maintained library/KMS and supported algorithms; verify versions and provider documentation.
3. Design envelope metadata, AAD, key ownership, rotation, revocation, backup, and incident procedures.
4. Implement using library APIs only; fail closed when keys, authentication tags, or randomness are unavailable.
5. Add negative tests for tampering, wrong key, wrong AAD, nonce uniqueness assumptions, rotation, restore, and redaction.
6. Run static scans and dependency/SBOM checks; manually review findings to avoid treating regex matches as proof of exploitability.
7. Document limitations and obtain a security review before production.

## Trade-offs
- AEAD provides confidentiality and integrity but does not hide access patterns, record sizes, or necessarily metadata.
- Frequent rotation reduces exposure duration but increases operational complexity and recovery risk.
- KMS/HSM improves key custody but introduces availability, quota, latency, and provider-dependency concerns.
- PQC migration improves future agility but can increase payload sizes and interoperability complexity.
- Constant-time primitives should come from vetted libraries; application-level timing behavior also depends on surrounding code and infrastructure.

## Exit criteria
Do not approve until the design has explicit key ownership, nonce strategy, envelope format, rotation/recovery tests, negative authentication tests, dependency review, and a documented residual-risk decision.
