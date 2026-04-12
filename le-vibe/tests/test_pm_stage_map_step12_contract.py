"""Contract: docs/PM_STAGE_MAP.md STEP 12 row lists H8 product surface + E1 (STEP 12)."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_pm_stage_map_step12_row_lists_h8_and_e1():
    text = (_repo_root() / "docs" / "PM_STAGE_MAP.md").read_text(encoding="utf-8")
    rows = [ln for ln in text.splitlines() if ln.lstrip().startswith("| 12 — H8 product")]
    assert len(rows) == 1
    row = rows[0]
    assert "test_issue_template_h8_contract.py" in row
    assert "test_pm_stage_map_step12_contract.py" in row
    assert "ci.yml" in row
    assert "dependabot.yml" in row
    assert "ISSUE_TEMPLATE" in row or "config.yml" in row
    assert "privacy-and-telemetry.md" in row
    assert "docs/README.md" in row or "README.md" in row
    assert "H8" in row or "STEP 12" in row


def test_docs_readme_opener_lists_step12_h8_and_e1():
    text = (_repo_root() / "docs" / "README.md").read_text(encoding="utf-8")
    head = "\n".join(text.splitlines()[:8])
    assert "STEP 12" in head
    assert "PM_STAGE_MAP" in head
    assert "test_issue_template_h8_contract.py" in head
    assert "test_pm_stage_map_step12_contract.py" in head
    assert "dependabot.yml" in head
