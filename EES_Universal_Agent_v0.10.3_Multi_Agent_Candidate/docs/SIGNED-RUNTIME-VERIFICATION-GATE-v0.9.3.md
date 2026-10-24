# EES Gemini v0.9.3 — Signed Runtime Verification Gate

Status: engineering hardening candidate; **not production-approved**.

## What changed

The task runtime now treats signed evidence as required by default before a task can transition to `PASSED`. The verification command accepts:

- `--signed-evidence PATH`
- `--public-key PATH`
- one or more `--required-check CHECK_ID`

The signed envelope is checked by `scripts/contract_verifier.py`. The runtime additionally binds the manifest to the current task ID, runtime version, and verified repository-tree SHA-256. A missing or invalid attestation moves verification to `BLOCKED`. The release-decision command revalidates the signed envelope, key file, manifest digest, required checks, task ID, version, and current repository tree.

The compatibility override `EES_REQUIRE_SIGNED_EVIDENCE=0` disables this gate and is intended only for legacy regression tests or controlled migration. It must not be set in release or production environments.

## Create an evidence manifest

Create a JSON manifest with:
- `schema_version: 1`
- `run_id` equal to the runtime task ID
- `package_version: "0.9.3"`
- `subject.sha256` equal to the repository tree hash recorded for the task
- non-empty `claims`, each with `check_id`, `status`, `evidence`, and `subject_sha256`
- every required claim set to `PASS`, with evidence, and bound to the same subject hash

Generate a keypair with `python scripts/contract_verifier.py keygen --private /secure/path/private.pem --public /secure/path/public.pem`. Keep the private key outside the repository and outside the task sandbox. Sign the manifest with `sign`, then run `task_runtime.py verify --out-dir ... --signed-evidence ... --public-key ... --required-check ...`.

## Security limits

A valid signature proves integrity and possession of a trusted signing key; it does not prove that evidence statements are truthful. The runtime binds the attestation to a repository tree and requires named checks, but independent provenance of each check result remains dependent on how the evidence is produced and who controls the signing key. Production use should keep the private key in a managed signing service or protected CI secret store, not on the same untrusted agent that generates code.

## Verification performed for this candidate

- `python scripts/validate.py --full`: PASS; 32 skills, 74 capabilities, 222 evaluation contracts, 51 central fixtures, 9 checks, 16 operational fixture projects, zero warnings.
- `tests/test_signed_runtime_gate.py`: 2 passed.
- `tests/test_contract_verifier.py` and `tests/test_check_all_version.py`: 8 passed.
- `tests/test_runtime_v072.py` with explicit compatibility override: 9 passed.
- `tests/test_repository_integrity_v072.py` with explicit compatibility override: 3 passed.
- Python compilation checks passed for changed runtime and test files.
- A combined broader test invocation did not complete within the execution window; the full suite is not claimed as passed.
- Docker runtime enforcement, CI, live Gemini smoke, dependency audit/SBOM, image CVE scan, and independent security review remain unverified or blocked.

## Release decision

`BLOCKED_NOT_GA`. Do not describe this candidate as production-ready or GA until all mandatory release gates have fresh, retained PASS evidence and independent review signs off.
