"""STEP 16: ``master_orchestrator.extract_master_orchestrator_fence``."""

from __future__ import annotations

from pathlib import Path

from le_vibe.master_orchestrator import extract_master_orchestrator_fence


def test_extract_fence_matches_prompt_build_contract():
    root = Path(__file__).resolve().parents[2]
    fence = extract_master_orchestrator_fence(root)
    assert fence is not None
    assert "ORDERED WORK QUEUE" in fence
    assert "STEP 0" in fence and "STEP 17" in fence
