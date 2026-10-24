import json, unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
class UniversalContractTests(unittest.TestCase):
    def test_example_contract_has_required_sections(self):
        c=json.loads((ROOT/"templates/universal-skill-contract.example.json").read_text())
        required={"contract_version","skill_id","purpose","use_when","do_not_use_when","inputs","capabilities","workflow","outputs","success_criteria","failure_modes","evidence_contract","handoff_rules","evaluation_cases"}
        self.assertTrue(required.issubset(c))
        self.assertGreaterEqual(len(c["evaluation_cases"]),3)
        self.assertTrue(c["success_criteria"])
    def test_detector_does_not_claim_unprobeable_capabilities(self):
        s=(ROOT/"scripts/detect_capabilities.py").read_text()
        self.assertIn('"not_tested"',s)
        self.assertIn("PATH lookup only",s)
    def test_cross_agent_protocol_disclaims_quality_from_fixtures(self):
        s=(ROOT/"docs/CROSS-AGENT-EVALUATION-v1.md").read_text()
        self.assertIn("does not establish agent capability",s)
if __name__ == "__main__": unittest.main()
