import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from export_chat_safe_skills import export

class ChatSafeExporterTests(unittest.TestCase):
    def test_exports_markdown_only_and_excludes_runtime(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "chat.zip"
            count = export(ROOT, out)
            self.assertGreater(count, 0)
            with zipfile.ZipFile(out) as zf:
                names = zf.namelist()
                self.assertTrue(all(n.endswith(".md") for n in names))
                self.assertIn("SKILL.md", names)
                self.assertFalse(any(n.startswith("scripts/") for n in names))
                self.assertFalse(any(n.startswith("tests/") for n in names))
                self.assertIsNone(zf.testzip())

if __name__ == "__main__":
    unittest.main()
