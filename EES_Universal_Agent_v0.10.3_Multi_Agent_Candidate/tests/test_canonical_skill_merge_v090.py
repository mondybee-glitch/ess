"""Regression tests for v0.9.0 physical skill consolidation and aliases."""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

class CanonicalSkillMergeTests(unittest.TestCase):
    def setUp(self):
        self.registry = json.loads((ROOT / "capability-registry.json").read_text(encoding="utf-8"))
        self.routing = json.loads((ROOT / "hierarchical-routing.json").read_text(encoding="utf-8"))
        self.manifest = json.loads((ROOT / "package-manifest.json").read_text(encoding="utf-8"))
        self.caps = {c["id"]: c for c in self.registry["capabilities"]}

    def test_exactly_32_physical_canonical_skill_folders(self):
        folders = {p.parent.name for p in (ROOT / "skills").rglob("SKILL.md")}
        self.assertEqual(len(folders), 32)
        self.assertEqual(folders, set(self.manifest["skills"]))

    def test_all_74_legacy_capability_ids_are_preserved(self):
        self.assertEqual(len(self.caps), 74)
        routed = {sid for route in self.routing["stage1_routes"] for sid in route["skills"]}
        self.assertEqual(routed, set(self.caps))

    def test_every_alias_resolves_to_existing_canonical_skill(self):
        folders = {p.parent.name for p in (ROOT / "skills").rglob("SKILL.md")}
        for sid, cap in self.caps.items():
            canonical = cap["canonical_skill_id"]
            self.assertIn(canonical, folders, sid)
            self.assertEqual(cap["skill_path"], f"skills/{canonical}/SKILL.md")
            self.assertTrue((ROOT / cap["skill_path"]).is_file())

    def test_each_canonical_skill_has_kernel_and_reference(self):
        for skill_file in (ROOT / "skills").rglob("SKILL.md"):
            folder = skill_file.parent
            body = skill_file.read_text(encoding="utf-8")
            self.assertIn("Hyper-Cognitive Engineering Kernel", body)
            self.assertTrue((folder / "references" / "decision-and-failure-patterns.md").is_file())

    def test_original_source_documents_are_archived(self):
        archive = ROOT / "docs" / "skill-source-archive"
        files = [p for p in archive.glob("*.md") if p.name != "README.md"]
        self.assertEqual(len(files), 74)

if __name__ == "__main__":
    unittest.main()
