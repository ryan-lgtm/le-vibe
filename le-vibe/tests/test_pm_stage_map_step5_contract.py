"""Contract: docs/PM_STAGE_MAP.md STEP 5 row lists hygiene.py + E1 (STEP 5)."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_pm_stage_map_step5_row_lists_hygiene_and_e1():
    text = (_repo_root() / "docs" / "PM_STAGE_MAP.md").read_text(encoding="utf-8")
    rows = [ln for ln in text.splitlines() if ln.lstrip().startswith("| 5 — Maintainer")]
    assert len(rows) == 1
    row = rows[0]
    assert "hygiene.py" in row
    assert "test_hygiene.py" in row
    assert "STEP 5" in row or "E5" in row
