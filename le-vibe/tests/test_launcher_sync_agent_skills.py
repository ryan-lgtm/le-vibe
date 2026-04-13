"""STEP 3 (E2): ``lvibe sync-agent-skills`` copies agent templates without launching the editor."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

from le_vibe import launcher


def test_sync_agent_skills_errors_when_no_lvibe(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(sys, "argv", ["launcher", "sync-agent-skills", "."])
    rc = launcher.main()
    assert rc == 1
    assert ".lvibe" in capsys.readouterr().err


def test_sync_agent_skills_writes_missing_skills(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.chdir(tmp_path)
    (tmp_path / ".lvibe").mkdir()
    monkeypatch.setattr(sys, "argv", ["launcher", "sync-agent-skills", str(tmp_path)])
    rc = launcher.main()
    assert rc == 0
    agents = tmp_path / ".lvibe" / "agents"
    assert agents.is_dir()
    assert len(list(agents.glob("*/skill.md"))) >= 8
    out = capsys.readouterr().out
    assert "wrote" in out


def test_sync_agent_skills_noop_when_skills_present(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.chdir(tmp_path)
    (tmp_path / ".lvibe").mkdir()
    monkeypatch.setattr(sys, "argv", ["launcher", "sync-agent-skills", "."])
    assert launcher.main() == 0
    capsys.readouterr()
    monkeypatch.setattr(sys, "argv", ["launcher", "sync-agent-skills", "."])
    assert launcher.main() == 0
    out = capsys.readouterr().out
    assert "no missing skill.md" in out
