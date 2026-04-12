"""Package README must list the same E1 contract highlights as the repository README (Track D)."""

from __future__ import annotations

from pathlib import Path


def _le_vibe_dir() -> Path:
    # le-vibe/tests/this_file.py -> parents[1] == le-vibe package root
    return Path(__file__).resolve().parents[1]


def test_le_vibe_readme_lists_core_e1_contract_modules():
    text = (_le_vibe_dir() / "README.md").read_text(encoding="utf-8")
    assert "PRODUCT_SPEC_SECTION8_EVIDENCE.md" in text
    assert "test_session_orchestrator.py" in text
    assert "test_issue_template_h8_contract.py" in text
    assert "test_root_readme_ai_pilot_contract.py" in text
