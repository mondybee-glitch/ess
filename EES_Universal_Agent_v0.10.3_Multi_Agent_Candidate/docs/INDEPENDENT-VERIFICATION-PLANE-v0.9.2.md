# Independent Verification Plane — v0.9.2 candidate design

Status: implemented prototype; not production-approved.

## Separation of duties

1. The task-producing agent creates outputs and an evidence manifest.
2. The Ed25519 signer authenticates the exact canonical manifest bytes. Private keys must be held outside the repository and outside untrusted task containers.
3. `scripts/contract_verifier.py verify` validates envelope structure, manifest structure, payload digest, key identity, and signature.
4. `scripts/contract_verifier.py verify-policy` independently checks that every named mandatory check exists, is `PASS`, and has evidence. Missing, failed, blocked, or not-run required checks yield `BLOCKED`.
5. A valid signature alone is never represented as proof that the claims are true. Evidence-producing checks and the policy decision must be independently trusted.

## Manifest shape

Required top-level fields: `schema_version`, `run_id`, `package_version`, `subject`, and `claims`. Each claim includes `check_id`, `status`, `evidence`, and `subject_sha256`. A `PASS` claim without evidence is rejected before signing. Production integration must enforce that the subject and claim hashes refer to the same immutable artifact; the current prototype validates hash syntax but does not hash arbitrary build outputs automatically.

## CLI example

```sh
python scripts/contract_verifier.py keygen --private /secure/ees-signing-key.pem --public ./trusted-ees-public-key.pem
python scripts/contract_verifier.py sign --manifest evidence-manifest.json --private-key /secure/ees-signing-key.pem --output signed-evidence.json
python scripts/contract_verifier.py verify --signed signed-evidence.json --public-key ./trusted-ees-public-key.pem
python scripts/contract_verifier.py verify-policy --signed signed-evidence.json --public-key ./trusted-ees-public-key.pem --required-check unit-tests --required-check security-scan
```

Do not commit private keys. Key generation writes an unencrypted PEM file for explicit local setup; production use must place keys in an approved secret manager/HSM and enforce key rotation and revocation outside this utility.

## Runtime isolation

`scripts/run_sandbox_task.sh` applies a non-root UID, read-only root filesystem, no network, dropped Linux capabilities, no-new-privileges, PID/memory/CPU limits, a temporary `/tmp`, and a single task-directory bind mount. This requires Docker and GNU `timeout`; it is a defense-in-depth wrapper, not a claim that containers provide a perfect security boundary. Do not pass Docker daemon access or signing keys to untrusted code.

## Remaining integration work

- Connect signed manifests to the existing task runtime's final `PASSED` / release decision transition.
- Use an immutable build artifact digest as `subject.sha256` and enforce equality with claim subject hashes.
- Add key identity allowlisting, rotation/revocation, and protected key storage.
- Run sandbox escape tests and verify the exact host runtime configuration.
- Complete clean CI, lockfile, SBOM, dependency audit, Docker/Trivy, live Gemini smoke, and independent security review.
- The adaptive-agent promotion guidance remains the policy for candidate rules: frozen regression suite, independent review for medium/high-risk changes, owner approval, and rollback.

The release remains `BLOCKED_NOT_GA` until all mandatory release gates have verifiable PASS evidence.
