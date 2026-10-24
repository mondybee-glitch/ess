#!/usr/bin/env python3
"""Sign and verify EES task evidence manifests with Ed25519.

The signer signs canonical manifest bytes. A valid signature proves possession of
an approved private key and integrity of the signed bytes; it does not prove that
claims in the manifest are true. The independent policy check is therefore
performed separately by `verify-policy`.
"""
from __future__ import annotations
import argparse
import base64
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

try:
    from cryptography.exceptions import InvalidSignature
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
except ImportError as exc:  # fail closed; never silently downgrade to a weaker scheme
    raise SystemExit("Missing dependency: install cryptography from requirements-gemini.txt") from exc

SCHEMA_VERSION = 1
VALID_STATUSES = {"PASS", "FAIL", "BLOCKED", "NOT_RUN"}
MANDATORY_CLAIM_FIELDS = {"check_id", "status", "evidence", "subject_sha256"}


def canonical(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_json(path: Path) -> dict:
    obj = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(obj, dict):
        raise ValueError("top-level JSON value must be an object")
    return obj


def validate_manifest(manifest: dict) -> None:
    required = {"schema_version", "run_id", "package_version", "subject", "claims"}
    missing = required - set(manifest)
    if missing:
        raise ValueError(f"manifest missing required fields: {', '.join(sorted(missing))}")
    if manifest["schema_version"] != SCHEMA_VERSION:
        raise ValueError(f"unsupported schema_version: {manifest['schema_version']!r}")
    if not isinstance(manifest["run_id"], str) or not manifest["run_id"].strip():
        raise ValueError("run_id must be a non-empty string")
    if not isinstance(manifest["package_version"], str) or not manifest["package_version"].strip():
        raise ValueError("package_version must be a non-empty string")
    if not isinstance(manifest["subject"], dict) or not isinstance(manifest["subject"].get("sha256"), str):
        raise ValueError("subject.sha256 is required")
    subject_hash = manifest["subject"]["sha256"]
    if len(subject_hash) != 64:
        raise ValueError("subject.sha256 must be a SHA-256 hex digest")
    try:
        int(subject_hash, 16)
    except ValueError as exc:
        raise ValueError("subject.sha256 is not hexadecimal") from exc
    if not isinstance(manifest["claims"], list) or not manifest["claims"]:
        raise ValueError("claims must be a non-empty array")
    seen = set()
    for i, claim in enumerate(manifest["claims"]):
        if not isinstance(claim, dict):
            raise ValueError(f"claim {i} must be an object")
        missing_claim = MANDATORY_CLAIM_FIELDS - set(claim)
        if missing_claim:
            raise ValueError(f"claim {i} missing fields: {', '.join(sorted(missing_claim))}")
        check_id = claim["check_id"]
        if not isinstance(check_id, str) or not check_id.strip() or check_id in seen:
            raise ValueError(f"claim {i} has empty or duplicate check_id")
        seen.add(check_id)
        if claim["status"] not in VALID_STATUSES:
            raise ValueError(f"claim {check_id} has invalid status")
        if not isinstance(claim["evidence"], list):
            raise ValueError(f"claim {check_id} evidence must be an array")
        if not isinstance(claim["subject_sha256"], str) or len(claim["subject_sha256"]) != 64:
            raise ValueError(f"claim {check_id} subject_sha256 must be a SHA-256 hex digest")
        try:
            int(claim["subject_sha256"], 16)
        except ValueError as exc:
            raise ValueError(f"claim {check_id} subject_sha256 is not hexadecimal") from exc
        if claim["subject_sha256"].lower() != subject_hash.lower():
            raise ValueError(f"claim {check_id} subject hash does not match manifest subject")
        if claim["status"] == "PASS" and not claim["evidence"]:
            raise ValueError(f"claim {check_id} cannot PASS without evidence")


def load_private(path: Path) -> Ed25519PrivateKey:
    key = serialization.load_pem_private_key(path.read_bytes(), password=None)
    if not isinstance(key, Ed25519PrivateKey):
        raise ValueError("private key must be an Ed25519 PEM key")
    return key


def load_public(path: Path) -> Ed25519PublicKey:
    key = serialization.load_pem_public_key(path.read_bytes())
    if not isinstance(key, Ed25519PublicKey):
        raise ValueError("public key must be an Ed25519 PEM key")
    return key


def cmd_keygen(args) -> None:
    if args.private.resolve() == args.public.resolve():
        raise ValueError("private and public key paths must be different")
    if args.private.exists() or args.public.exists():
        raise ValueError("refusing to overwrite an existing key file")
    private = Ed25519PrivateKey.generate()
    public = private.public_key()
    args.private.parent.mkdir(parents=True, exist_ok=True)
    args.public.parent.mkdir(parents=True, exist_ok=True)
    args.private.write_bytes(private.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8, serialization.NoEncryption()))
    args.public.write_bytes(public.public_bytes(serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo))
    try:
        args.private.chmod(0o600)
        args.public.chmod(0o644)
    except OSError:
        pass
    print(json.dumps({"status": "KEYPAIR_CREATED", "private_key": str(args.private), "public_key": str(args.public), "algorithm": "Ed25519", "private_key_storage_warning": "Keep the private key outside the repository and execution sandbox."}, indent=2))


def cmd_sign(args) -> None:
    manifest = read_json(args.manifest)
    validate_manifest(manifest)
    payload = canonical(manifest)
    private = load_private(args.private_key)
    signature = private.sign(payload)
    envelope = {
        "signature_schema_version": 1,
        "algorithm": "Ed25519",
        "payload": manifest,
        "payload_sha256": sha256(payload),
        "signature_base64": base64.b64encode(signature).decode("ascii"),
        "key_id": sha256(private.public_key().public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)),
        "signing_note": "Signature authenticates the canonical payload bytes only; policy verification is separate."
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(envelope, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": "SIGNED", "output": str(args.output), "payload_sha256": envelope["payload_sha256"], "key_id": envelope["key_id"]}, indent=2))


def verify_signature(envelope: dict, public: Ed25519PublicKey) -> dict:
    if envelope.get("signature_schema_version") != 1 or envelope.get("algorithm") != "Ed25519":
        raise ValueError("unsupported signature envelope or algorithm")
    manifest = envelope.get("payload")
    if not isinstance(manifest, dict):
        raise ValueError("signed payload must be an object")
    validate_manifest(manifest)
    payload = canonical(manifest)
    if sha256(payload) != envelope.get("payload_sha256"):
        raise ValueError("payload digest mismatch")
    raw_pub = public.public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)
    if sha256(raw_pub) != envelope.get("key_id"):
        raise ValueError("public key does not match envelope key_id")
    try:
        public.verify(base64.b64decode(envelope["signature_base64"], validate=True), payload)
    except (InvalidSignature, ValueError, KeyError) as exc:
        raise ValueError("signature verification failed") from exc
    return manifest


def cmd_verify(args) -> None:
    envelope = read_json(args.signed)
    manifest = verify_signature(envelope, load_public(args.public_key))
    print(json.dumps({"status": "SIGNATURE_VALID", "run_id": manifest["run_id"], "payload_sha256": envelope["payload_sha256"], "claim_count": len(manifest["claims"]), "note": "Signature validity does not mean claims passed independent policy checks."}, indent=2))


def cmd_policy(args) -> None:
    if not args.required_check:
        raise ValueError("at least one --required-check must be specified; empty policy cannot pass")
    envelope = read_json(args.signed)
    manifest = verify_signature(envelope, load_public(args.public_key))
    required = set(args.required_check)
    claims = {c["check_id"]: c for c in manifest["claims"]}
    missing = sorted(required - set(claims))
    failed = sorted(cid for cid in required & set(claims) if claims[cid]["status"] != "PASS")
    no_evidence = sorted(cid for cid in required & set(claims) if not claims[cid]["evidence"])
    decision = "PASS" if not missing and not failed and not no_evidence else "BLOCKED"
    result = {"decision": decision, "run_id": manifest["run_id"], "required_checks": sorted(required), "missing_checks": missing, "non_passing_checks": failed, "checks_without_evidence": no_evidence, "signature_valid": True, "policy_version": 1}
    print(json.dumps(result, indent=2))
    if decision != "PASS":
        raise SystemExit(2)


def parser():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="command", required=True)
    k = sub.add_parser("keygen", help="generate an Ed25519 keypair")
    k.add_argument("--private", type=Path, required=True)
    k.add_argument("--public", type=Path, required=True)
    k.set_defaults(func=cmd_keygen)
    s = sub.add_parser("sign", help="sign a validated evidence manifest")
    s.add_argument("--manifest", type=Path, required=True)
    s.add_argument("--private-key", type=Path, required=True)
    s.add_argument("--output", type=Path, required=True)
    s.set_defaults(func=cmd_sign)
    v = sub.add_parser("verify", help="verify signature and manifest structure")
    v.add_argument("--signed", type=Path, required=True)
    v.add_argument("--public-key", type=Path, required=True)
    v.set_defaults(func=cmd_verify)
    q = sub.add_parser("verify-policy", help="verify signature and require named checks to PASS")
    q.add_argument("--signed", type=Path, required=True)
    q.add_argument("--public-key", type=Path, required=True)
    q.add_argument("--required-check", action="append", default=[])
    q.set_defaults(func=cmd_policy)
    return p

if __name__ == "__main__":
    try:
        args = parser().parse_args()
        args.func(args)
    except (OSError, json.JSONDecodeError, ValueError, KeyError) as exc:
        print(json.dumps({"status": "REJECTED", "reason": str(exc)}, ensure_ascii=False), file=sys.stderr)
        raise SystemExit(1)
