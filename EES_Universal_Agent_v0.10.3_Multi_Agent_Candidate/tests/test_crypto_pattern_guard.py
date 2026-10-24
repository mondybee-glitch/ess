import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('crypto_pattern_guard', ROOT / 'scripts' / 'crypto_pattern_guard.py')
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_detects_ecb_and_weak_hash():
    findings = MODULE.scan('cipher = AES.MODE_ECB\ndigest = hashlib.md5(payload)')
    assert {item['rule'] for item in findings} >= {'ecb-mode', 'weak-hash'}


def test_detects_non_crypto_random_and_password_hash():
    findings = MODULE.scan('nonce = random.random()\npassword_hash = hashlib.sha256(password)')
    assert {item['rule'] for item in findings} >= {'insecure-rng', 'raw-password-hash'}


def test_ignores_comment_lines_and_clean_source():
    assert MODULE.scan('# hashlib.md5(payload)\nvalue = secrets.token_bytes(32)') == []


def test_secret_comparison_is_flagged_for_review():
    findings = MODULE.scan('if token == expected_token:')
    assert any(item['rule'] == 'ordinary-secret-compare' for item in findings)
