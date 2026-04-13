"""Contract: docs/PM_STAGE_MAP.md STEP 16 row + intro keep the doc-locked loop (STEP 16)."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_pm_stage_map_step16_row_lists_prompt_build_print_script_and_e1():
    text = (_repo_root() / "docs" / "PM_STAGE_MAP.md").read_text(encoding="utf-8")
    rows = [ln for ln in text.splitlines() if "| **16** — PM map" in ln]
    assert len(rows) == 1
    row = rows[0]
    assert "PROMPT_BUILD_LE_VIBE.md" in row
    assert "print-master-orchestrator-prompt.py" in row
    assert "test_prompt_build_orchestrator_fence.py" in row
    assert "test_pm_stage_map_step16_contract.py" in row
    assert "STEP 16" in row
    assert "AI_PILOT_AND_CONTINUE.md" in row


def test_pm_stage_map_intro_paragraph_step16_doc_locked_loop():
    text = (_repo_root() / "docs" / "PM_STAGE_MAP.md").read_text(encoding="utf-8")
    head = "\n".join(text.splitlines()[:25])
    assert "**STEP 16" in head
    assert "print-master-orchestrator-prompt.py" in head
    assert "test_pm_stage_map_step16_contract.py" in head
    assert "Rolling iteration — prefer continuation" in head
    assert "PASTE SAME AGAIN" in head and "LÉ VIBE SESSION COMPLETE" in head


def test_root_and_docs_readme_link_pm_stage_map():
    root_readme = (_repo_root() / "README.md").read_text(encoding="utf-8")
    docs_readme = (_repo_root() / "docs" / "README.md").read_text(encoding="utf-8")
    assert "PM_STAGE_MAP.md" in root_readme
    assert "PM_STAGE_MAP.md" in docs_readme
