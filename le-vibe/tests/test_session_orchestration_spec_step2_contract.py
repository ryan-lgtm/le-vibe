"""Contract: docs/SESSION_ORCHESTRATION_SPEC.md keeps STEP 2 + session_orchestrator pointer."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_session_orchestration_spec_documents_step2_and_e1():
    text = (_repo_root() / "docs" / "SESSION_ORCHESTRATION_SPEC.md").read_text(encoding="utf-8")
    assert "STEP 2" in text
    assert "session_orchestrator" in text
    assert "test_session_orchestrator.py" in text
    assert "ensure_pm_session_artifacts" in text or "apply_opening_skip" in text
    assert "spec-phase2.md" in text and "§14" in text
