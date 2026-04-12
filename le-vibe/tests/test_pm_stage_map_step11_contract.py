"""Contract: docs/PM_STAGE_MAP.md STEP 11 row lists H5 brand + E1 (STEP 11)."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_pm_stage_map_step11_row_lists_h5_and_e1():
    text = (_repo_root() / "docs" / "PM_STAGE_MAP.md").read_text(encoding="utf-8")
    rows = [ln for ln in text.splitlines() if ln.lstrip().startswith("| 11 — H5 brand")]
    assert len(rows) == 1
    row = rows[0]
    assert "test_brand_assets_doc_h5_contract.py" in row
    assert "H5" in row or "STEP 11" in row
