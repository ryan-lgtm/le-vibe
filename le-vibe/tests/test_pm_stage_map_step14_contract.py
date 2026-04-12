"""Contract: docs/PM_STAGE_MAP.md STEP 14 row keeps H6 IDE CI + build-linux alias (E1 roster)."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _step14_table_row(text: str) -> str:
    rows = [ln for ln in text.splitlines() if ln.lstrip().startswith("| **14 — H6 IDE**")]
    assert len(rows) == 1, f"expected single STEP 14 table row, got {len(rows)}"
    return rows[0]


def test_pm_stage_map_step14_lists_ide_workflows_smoke_and_e1_test_build():
    text = (_repo_root() / "docs" / "PM_STAGE_MAP.md").read_text(encoding="utf-8")
    row = _step14_table_row(text)
    assert "build-le-vibe-ide.yml" in row
    assert "build-linux.yml" in row
    assert "test_build_le_vibe_ide_workflow_contract.py" in row
    assert "le_vibe_editor_docs" in row
    assert "LE_VIBE_EDITOR" in row
    assert "ide-ci-metadata" in row
    assert "./editor/smoke.sh" in row
