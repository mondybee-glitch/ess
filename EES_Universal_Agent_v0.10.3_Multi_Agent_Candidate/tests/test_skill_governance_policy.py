from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]


def test_skill_governance_policy_covers_required_controls():
    text = (ROOT / "docs/skill-governance/SKILL_GOVERNANCE_AND_PLACEMENT.md").read_text(encoding="utf-8")
    for required in [
        "MERGE_UPGRADE", "ADD_DISTINCT_SKILL", "KEEP_EXISTING", "QUARANTINE", "REJECT",
        "Safety, security, and policy compliance", "negative routing tests", "rollback", "license",
        "simply add a second copy"
    ]:
        assert required.lower() in text.lower(), required


def test_candidate_schema_has_hard_gates_and_dispositions():
    schema = json.loads((ROOT / "templates/skill-ingestion/skill-candidate.schema.json").read_text(encoding="utf-8"))
    assert "license_status" in schema["required"]
    assert "security_review" in schema["required"]
    assert "evaluation_status" in schema["required"]
    assert set(schema["properties"]["disposition"]["enum"]) == {
        "MERGE_UPGRADE", "ADD_DISTINCT_SKILL", "KEEP_EXISTING", "QUARANTINE", "REJECT"
    }
