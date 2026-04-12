"""Contract: docs/PM_STAGE_MAP.md STEP 3 row lists continue_workspace + E2 test (STEP 3)."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_pm_stage_map_step3_row_lists_continue_workspace_and_e1():
    text = (_repo_root() / "docs" / "PM_STAGE_MAP.md").read_text(encoding="utf-8")
    rows = [ln for ln in text.splitlines() if ln.lstrip().startswith("| 3 — Continue")]
    assert len(rows) == 1
    row = rows[0]
    assert "continue_workspace.py" in row
    assert "test_continue_workspace.py" in row
    assert "STEP 3" in row or "E2" in row
