import pathlib, unittest
ROOT = pathlib.Path(__file__).resolve().parents[1]
AGENT = ROOT / "integrations" / "adaptive-engineering-agent"
class AdaptiveAgentIntegrationTests(unittest.TestCase):
    def test_expected_components_present(self):
        for rel in ["SKILL.md", "README_AR.md", "scripts/agent_runtime.py", "scripts/feedback_store.py", "references/protocol.md", "references/promotion.md", "tests/test_package.py", ".env.example", "Dockerfile"]:
            with self.subTest(path=rel): self.assertTrue((AGENT / rel).is_file(), rel)
    def test_runtime_has_credential_guard(self):
        text = (AGENT / "scripts/agent_runtime.py").read_text(encoding="utf-8")
        self.assertIn("EES_API_KEY", text)
        self.assertIn("EES_MODEL", text)
        self.assertIn("required", text)
if __name__ == "__main__": unittest.main()
