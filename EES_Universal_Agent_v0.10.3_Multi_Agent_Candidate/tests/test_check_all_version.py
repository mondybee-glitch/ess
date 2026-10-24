"""Regression test: generated release reports must use the canonical package version."""
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

class CheckAllVersionTests(unittest.TestCase):
    def test_version_is_read_from_manifest(self):
        spec = importlib.util.spec_from_file_location("ees_check_all", ROOT / "scripts" / "check_all.py")
        module = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(module)
        self.assertEqual(module.package_version(), "0.10.3")

if __name__ == "__main__":
    unittest.main()
