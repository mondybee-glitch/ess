from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_universal_instruction_entrypoints_exist():
    for relative in (
        "AGENTS.md",
        "GEMINI.md",
        "CLAUDE.md",
        ".agent/rules/ees.md",
        "adapters/gemini/README.md",
        "adapters/antigravity/README.md",
        "adapters/claude/README.md",
        "adapters/chatgpt-cloud/README.md",
        "docs/multi-agent/UNIVERSAL-AGENT-ARCHITECTURE.md",
    ):
        assert (ROOT / relative).is_file(), relative


def test_adapter_docs_do_not_claim_automatic_universal_compatibility():
    for relative in (
        "adapters/antigravity/README.md",
        "adapters/claude/README.md",
        "adapters/chatgpt-cloud/README.md",
    ):
        content = (ROOT / relative).read_text(encoding="utf-8").lower()
        assert "does not" in content or "must not" in content or "not prove" in content
