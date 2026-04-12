"""Contract: docs/PM_STAGE_MAP.md STEP 17 row + AI_PILOT doc opener (STEP 17)."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_pm_stage_map_step17_row_lists_continue_readme_and_e1():
    text = (_repo_root() / "docs" / "PM_STAGE_MAP.md").read_text(encoding="utf-8")
    rows = [ln for ln in text.splitlines() if "| **17** — AI Pilot" in ln]
    assert len(rows) == 1
    row = rows[0]
    assert "AI_PILOT_AND_CONTINUE.md" in row
    assert "PRODUCT_SPEC.md" in row
    assert "continue_workspace.py" in row
    assert "test_root_readme_ai_pilot_contract.py" in row
    assert "test_privacy_and_ai_pilot_prioritization_cargo_contract.py" in row
    assert "test_pm_stage_map_step17_contract.py" in row
    assert "STEP 17" in row


def test_ai_pilot_continue_doc_opener_step17_and_e1():
    text = (_repo_root() / "docs" / "AI_PILOT_AND_CONTINUE.md").read_text(encoding="utf-8")
    head = "\n".join(text.splitlines()[:12])
    assert "STEP 17" in head
    assert "PM_STAGE_MAP" in head
    assert "continue_workspace.py" in head
    assert "test_root_readme_ai_pilot_contract.py" in head
    assert "test_pm_stage_map_step17_contract.py" in head
