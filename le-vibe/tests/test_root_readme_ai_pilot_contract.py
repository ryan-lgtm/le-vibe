"""Root README must retain §7.1 Please continue / AI Pilot UX copy (PRODUCT_SPEC, STEP 17) and E1 Tests roster (STEP 2 session orchestrator + H8 issue-template contracts)."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    # le-vibe/tests/this_file.py -> parents[2] == monorepo root
    return Path(__file__).resolve().parents[2]


def test_root_readme_documents_ai_pilot_and_user_gate():
    text = (_repo_root() / "README.md").read_text(encoding="utf-8")
    assert "Lé Vibe" in text
    assert "Please continue" in text
    assert "AI Pilot" in text
    assert "USER RESPONSE REQUIRED" in text
    assert "AI_PILOT_AND_CONTINUE.md" in text
    assert "PM_STAGE_MAP.md" in text


def test_root_readme_tests_section_cites_issue_template_h8_contract():
    """E1 / §10: *Tests* / **E1 mapping** must keep **H8** **`test_issue_template_h8_contract.py`** (STEP 12)."""
    text = (_repo_root() / "README.md").read_text(encoding="utf-8")
    assert "test_issue_template_h8_contract.py" in text
    assert "PRODUCT_SPEC_SECTION8_EVIDENCE.md" in text


def test_root_readme_tests_section_cites_session_orchestrator_contract():
    """E1 / STEP 2: *E1 mapping* must cite **`test_session_orchestrator.py`** (bundled example ↔ schema; PM manifests)."""
    text = (_repo_root() / "README.md").read_text(encoding="utf-8")
    assert "test_session_orchestrator.py" in text


def test_root_readme_e1_mapping_cites_le_vibe_readme_contract():
    """*Tests* / **E1 mapping** must cite **`test_le_vibe_readme_e1_contract.py`** (package README roster alignment)."""
    text = (_repo_root() / "README.md").read_text(encoding="utf-8")
    assert "test_le_vibe_readme_e1_contract.py" in text
