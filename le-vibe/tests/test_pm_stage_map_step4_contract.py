"""Contract: docs/PM_STAGE_MAP.md STEP 4 row lists editor_welcome + E1 (STEP 4)."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_pm_stage_map_step4_row_lists_editor_welcome_and_e1():
    text = (_repo_root() / "docs" / "PM_STAGE_MAP.md").read_text(encoding="utf-8")
    rows = [ln for ln in text.splitlines() if ln.lstrip().startswith("| 4 — In-editor")]
    assert len(rows) == 1
    row = rows[0]
    assert "editor_welcome.py" in row
    assert "test_editor_welcome.py" in row
    assert "test_continue_workspace.py" in row
    assert "test_product_spec_section8.py" in row
    assert "STEP 4" in row
    assert "PRODUCT_SPEC" in row and "§4" in row
