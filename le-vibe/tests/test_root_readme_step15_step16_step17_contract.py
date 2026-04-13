"""Contract: root README lists STEP 15–17 (governance, PM map, AI Pilot & Continue)."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_root_readme_step15_lvibe_governance_section():
    text = (_repo_root() / "README.md").read_text(encoding="utf-8")
    assert "### `.lvibe/` governance — STEP 15" in text
    assert "Master orchestrator STEP 15" in text
    assert "resolve_lvibe_creation" in text
    assert "workspace-governance" in text
    assert "test_pm_stage_map_step15_contract.py" in text


def test_root_readme_step16_pm_stage_map_section():
    text = (_repo_root() / "README.md").read_text(encoding="utf-8")
    assert "### PM stage map — STEP 16" in text
    assert "Master orchestrator STEP 16" in text
    assert "print-master-orchestrator-prompt.py" in text
    assert "test_prompt_build_orchestrator_fence.py" in text


def test_root_readme_step17_ai_pilot_continue_section():
    text = (_repo_root() / "README.md").read_text(encoding="utf-8")
    assert "### AI Pilot & Continue contracts — STEP 17" in text
    assert "Master orchestrator STEP 17" in text
    assert "AI_PILOT_AND_CONTINUE.md" in text
    assert "test_pm_stage_map_step17_contract.py" in text
