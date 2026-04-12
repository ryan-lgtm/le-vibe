"""Contract: docs/PM_STAGE_MAP.md STEP 6 row lists structured_log + E1 (STEP 6)."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_pm_stage_map_step6_row_lists_structured_log_and_e1():
    text = (_repo_root() / "docs" / "PM_STAGE_MAP.md").read_text(encoding="utf-8")
    rows = [ln for ln in text.splitlines() if ln.lstrip().startswith("| 6 — Observability")]
    assert len(rows) == 1
    row = rows[0]
    assert "structured_log.py" in row
    assert "test_structured_log.py" in row
    assert "STEP 6" in row or "E6" in row
    assert "le-vibe.log.jsonl" in row
    assert "LE_VIBE_STRUCTURED_LOG" in row
