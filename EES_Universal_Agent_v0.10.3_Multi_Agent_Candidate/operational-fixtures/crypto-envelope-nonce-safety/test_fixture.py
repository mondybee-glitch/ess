import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location('crypto_pattern_guard', ROOT / 'scripts' / 'crypto_pattern_guard.py')
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

class CryptoPatternGuardTests(unittest.TestCase):
    def test_detects_ecb_weak_hash_and_insecure_rng(self):
        source = 'cipher = AES.MODE_ECB\ndigest = hashlib.md5(payload)\nnonce = Math.random()'
        rules = {item['rule'] for item in MODULE.scan(source)}
        self.assertTrue({'ecb-mode', 'weak-hash', 'insecure-rng'} <= rules)

    def test_detects_password_hash_and_secret_comparison(self):
        source = 'password_hash = sha256(password)\nif token == expected_token: pass'
        rules = {item['rule'] for item in MODULE.scan(source)}
        self.assertIn('raw-password-hash', rules)
        self.assertIn('ordinary-secret-compare', rules)

    def test_ignores_comment_and_vetted_api_names(self):
        source = '# hashlib.md5(payload)\ncipher = AESGCM(key)\nnonce = secrets.token_bytes(12)\nhmac.compare_digest(actual, expected)'
        self.assertEqual([], MODULE.scan(source))

if __name__ == '__main__':
    unittest.main()
