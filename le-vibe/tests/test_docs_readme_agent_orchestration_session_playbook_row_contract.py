"""Contract: docs/README.md keeps AGENT_ORCHESTRATION_SESSION_PLAYBOOK row shape."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_docs_readme_agent_orchestration_session_playbook_row_lists_70_session_backlog():
    text = (_repo_root() / "docs" / "README.md").read_text(encoding="utf-8")
    assert "AGENT_ORCHESTRATION_SESSION_PLAYBOOK.md" in text
    assert "70 session backlog" in text
    assert "operator/subagent communication" in text
    assert "structured debate" in text
    assert "final milestone stop-conditions" in text
    assert "copy/paste engineering prompt" in text
