"""Contract: root README keeps AGENT_ORCHESTRATION_SESSION_PLAYBOOK index link."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_root_readme_lists_agent_orchestration_session_playbook_link():
    text = (_repo_root() / "README.md").read_text(encoding="utf-8")
    assert "AGENT_ORCHESTRATION_SESSION_PLAYBOOK.md" in text
    assert "70-session hardening backlog" in text
    assert "one session per task" in text
