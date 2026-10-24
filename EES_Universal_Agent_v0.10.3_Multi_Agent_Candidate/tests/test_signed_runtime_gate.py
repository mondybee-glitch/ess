import json, os, subprocess, sys
from pathlib import Path
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

ROOT = Path(__file__).resolve().parents[1]
RT = ROOT / "scripts" / "task_runtime.py"
SIGNER = ROOT / "scripts" / "contract_verifier.py"

def run(env, *args):
    return subprocess.run([sys.executable, str(RT), *map(str, args)], cwd=ROOT,
                          capture_output=True, text=True, timeout=20, env=env)

def setup_task(tmp_path, task_id, env):
    out = tmp_path / task_id
    common = ["--out-dir", str(out)]
    steps = [
        ["route", "--task-id", task_id, "--request", "read-only documentation audit",
         "--out-dir", str(out), "--repo", str(ROOT), "--acceptance", "validation result is evidenced"],
        ["plan", *common],
        ["start", *common],
        ["run-check", *common, "--check-id", "event-ledger-v072"],
        ["record-criterion", *common, "--index", "1", "--status", "pass",
         "--evidence", "out:runs/event-ledger-v072.stdout.txt", "--note", "evidence-backed test"],
    ]
    for step in steps:
        p = run(env, *step)
        assert p.returncode == 0, (step, p.stdout, p.stderr)
    return out, common

def tree_digest(path):
    import hashlib
    h = hashlib.sha256()
    volatile = {".git", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", ".tox", ".venv", "venv", "node_modules"}
    for f in sorted(x for x in path.rglob("*") if x.is_file() and not any(part in volatile for part in x.parts) and x.suffix != ".pyc" and not x.name.endswith(".tmp")):
        rel = f.relative_to(path)
        h.update(rel.as_posix().encode()); h.update(b"\0")
        h.update(bytes.fromhex(hashlib.sha256(f.read_bytes()).hexdigest()))
    return h.hexdigest()

def test_runtime_blocks_success_without_signed_attestation(tmp_path):
    env = {**os.environ}
    env.pop("EES_REQUIRE_SIGNED_EVIDENCE", None)
    out, common = setup_task(tmp_path, "strict-missing-attestation", env)
    p = run(env, "verify", *common)
    assert p.returncode == 0, p.stdout + p.stderr
    state = json.loads((out / "task-state.json").read_text())
    assert state["state"] == "BLOCKED"
    assert "contract attestation gate" in " ".join(state["failures"])

def test_runtime_pass_requires_signed_attestation_bound_to_task_and_tree(tmp_path):
    env = {**os.environ}
    env.pop("EES_REQUIRE_SIGNED_EVIDENCE", None)
    task_id = "strict-signed-attestation"
    out, common = setup_task(tmp_path, task_id, env)
    digest = tree_digest(ROOT)
    private = Ed25519PrivateKey.generate()
    priv = tmp_path / "signing-private.pem"
    pub = tmp_path / "trusted-public.pem"
    priv.write_bytes(private.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8, serialization.NoEncryption()))
    pub.write_bytes(private.public_key().public_bytes(serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo))
    manifest = {
        "schema_version": 1, "run_id": task_id, "package_version": "0.10.0",
        "subject": {"name": "repository-tree", "sha256": digest},
        "claims": [{"check_id": "unit-tests", "status": "PASS", "evidence": ["test runner completed; artifact is repository-bound"], "subject_sha256": digest}],
    }
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(json.dumps(manifest))
    signed_path = tmp_path / "signed-evidence.json"
    signed = subprocess.run([sys.executable, str(SIGNER), "sign", "--manifest", str(manifest_path),
                             "--private-key", str(priv), "--output", str(signed_path)],
                            cwd=ROOT, capture_output=True, text=True, timeout=10)
    assert signed.returncode == 0, signed.stdout + signed.stderr
    p = run(env, "verify", *common, "--signed-evidence", str(signed_path),
            "--public-key", str(pub), "--required-check", "unit-tests")
    assert p.returncode == 0, p.stdout + p.stderr
    state = json.loads((out / "task-state.json").read_text())
    assert state["state"] == "PASSED"
    assert state["contract_attestation"]["status"] == "PASS"
    release = run(env, "release-decision", "--out-dir", str(out))
    assert release.returncode == 0, release.stdout + release.stderr
    assert json.loads((out / "release-decision.json").read_text())["decision"] == "Go"
