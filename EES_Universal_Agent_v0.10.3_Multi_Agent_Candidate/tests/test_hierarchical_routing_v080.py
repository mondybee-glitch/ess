"""Regression tests for hierarchical routing configuration and security floor."""
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import task_runtime

class HierarchicalRoutingTests(unittest.TestCase):
    def test_route_ids_are_unique_and_all_capabilities_routed_once(self):
        doc = json.loads((ROOT / "hierarchical-routing.json").read_text(encoding="utf-8"))
        route_ids = [r["id"] for r in doc["stage1_routes"]]
        routed = [sid for r in doc["stage1_routes"] for sid in r["skills"]]
        self.assertEqual(len(route_ids), len(set(route_ids)))
        self.assertEqual(len(routed), len(set(routed)))
        self.assertEqual(set(routed), set(task_runtime.SKILLS))
        self.assertEqual(len(doc["stage1_routes"]), 32)

    def test_every_route_has_a_nonempty_skill_set(self):
        doc = json.loads((ROOT / "hierarchical-routing.json").read_text(encoding="utf-8"))
        self.assertTrue(all(r.get("name") and r.get("skills") for r in doc["stage1_routes"]))

    def test_high_risk_task_applies_security_floor(self):
        result = task_runtime.route("Perform a security review of production API authentication and injection risks")
        self.assertIn(result["task_risk"], {"high", "critical"})
        self.assertTrue(result["security_floor_applied"])
        selected = set(result["selected_skills"])
        self.assertTrue({"security-review", "defensive-appsec-assessment", "prompt-provenance-and-safety"}.issubset(selected))

    def test_route_skill_mapping_is_unique(self):
        self.assertEqual(len(task_runtime.ROUTE_BY_SKILL), len(task_runtime.SKILLS))

if __name__ == "__main__":
    unittest.main()
