"""Contract: docs/PM_STAGE_MAP.md STEP 7 row lists H4 Continue pin + E1 (STEP 7)."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_pm_stage_map_step7_row_lists_continue_pin_and_e1():
    text = (_repo_root() / "docs" / "PM_STAGE_MAP.md").read_text(encoding="utf-8")
    rows = [ln for ln in text.splitlines() if ln.lstrip().startswith("| 7 — H4 Continue")]
    assert len(rows) == 1
    row = rows[0]
    assert "test_continue_openvsx_pin.py" in row
    assert "test_install_continue_extension_script.py" in row
    assert "test_continue_extension_pin_doc_step14_contract.py" in row
    assert "H4" in row or "STEP 7" in row
