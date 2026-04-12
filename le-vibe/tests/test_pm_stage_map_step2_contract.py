"""Contract: docs/PM_STAGE_MAP.md STEP 2 row lists session_orchestrator + STEP 2 E1 tests."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_pm_stage_map_step2_row_lists_e1_and_session_orchestrator():
    text = (_repo_root() / "docs" / "PM_STAGE_MAP.md").read_text(encoding="utf-8")
    rows = [ln for ln in text.splitlines() if ln.lstrip().startswith("| 2 — PM session")]
    assert len(rows) == 1
    row = rows[0]
    assert "session_orchestrator.py" in row
    assert "test_session_orchestrator.py" in row
    assert "test_session_orchestration_spec_step2_contract.py" in row
    assert "STEP 2" in row
    assert "STEP 14" in row


def test_pm_stage_map_queue_advance_honest_step14_vs_rest():
    text = (_repo_root() / "docs" / "PM_STAGE_MAP.md").read_text(encoding="utf-8")
    assert "Queue advance (honest)" in text
    assert "14.a" in text and "14.j" in text
    assert "STEP 2" in text
    assert "spec-phase2.md" in text
