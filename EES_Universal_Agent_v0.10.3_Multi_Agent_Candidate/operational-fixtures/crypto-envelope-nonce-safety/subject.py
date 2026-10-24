from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("crypto_pattern_guard", ROOT / "scripts" / "crypto_pattern_guard.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

def test_flags_ecb_and_weak_hash_and_insecure_random():
    source = """
cipher = AES.new(key, AES.MODE_ECB)
digest = hashlib.md5(password.encode()).hexdigest()
nonce = Math.random()
"""
    rules = {x["rule"] for x in MODULE.scan(source)}
    assert {"ecb-mode", "weak-hash", "insecure-rng"} <= rules

def test_flags_raw_password_hash_and_secret_compare():
    source = 'password_hash = sha256(password)\nif token == expected_token: pass\n'
    rules = {x["rule"] for x in MODULE.scan(source)}
    assert "raw-password-hash" in rules
    assert "ordinary-secret-compare" in rules

def test_no_findings_for_vetted_api_names_and_nonce_invariant_documentation():
    source = """
cipher = AESGCM(key)
nonce = secrets.token_bytes(12)  # caller must guarantee uniqueness per key
hmac.compare_digest(actual, expected)
"""
    assert MODULE.scan(source) == []
