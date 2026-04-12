"""Contract: docs/PM_STAGE_MAP.md STEP 10 row lists H3 QA CI + E1 (STEP 10)."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_pm_stage_map_step10_row_lists_h3_and_e1():
    text = (_repo_root() / "docs" / "PM_STAGE_MAP.md").read_text(encoding="utf-8")
    rows = [ln for ln in text.splitlines() if ln.lstrip().startswith("| 10 — H3 QA")]
    assert len(rows) == 1
    row = rows[0]
    assert "test_ci_qa_hardening_doc_h3_contract.py" in row
    assert "test_ci_qa_hardening_prioritization_cargo_contract.py" in row
    assert "H3" in row or "STEP 10" in row
