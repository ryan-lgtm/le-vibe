"""Launcher runtime writes goal_alignment_check start/end records."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

from le_vibe import launcher


class _FakeProc:
    def __init__(self, _cmd: list[str]) -> None:
        self._rc = 0

    def wait(self) -> int:
        return self._rc


def test_launcher_records_goal_alignment_start_and_end(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    ws = tmp_path / "workspace"
    ws.mkdir()
    monkeypatch.setenv("LE_VIBE_LVIBE_CONSENT", "accept")
    monkeypatch.setattr("le_vibe.launcher.ensure_managed_ollama", lambda **_: (True, "ok", None))
    monkeypatch.setattr("le_vibe.launcher.stop_managed_ollama", lambda: None)
    monkeypatch.setattr("le_vibe.launcher.subprocess.Popen", lambda cmd: _FakeProc(cmd))
    monkeypatch.setattr(sys, "argv", ["launcher", "--skip-first-run", "--editor", "fake-editor", str(ws)])

    assert launcher.main() == 0

    manifest = ws / ".lvibe" / "session-manifest.json"
    data = json.loads(manifest.read_text(encoding="utf-8"))
    checks = data["meta"]["goal_alignment_check"]
    assert checks["start"]["current_milestone"] == "Launcher session start"
    assert checks["start"]["status"] == "aligned"
    assert checks["start"]["evidence"] == ["launcher.session_start", "editor=fake-editor"]
    assert checks["end"]["current_milestone"] == "Launcher session end"
    assert checks["end"]["status"] == "aligned"
    assert checks["end"]["evidence"] == ["launcher.editor_exit", "editor_exit_code=0"]
    stop = data["meta"]["stop_condition_check"]
    assert stop["completion_allowed"] is False
    assert stop["product_goals_satisfied"] is False
    assert stop["final_milestone_achieved"] is False
    summary = data["meta"]["release_readiness_summary"]
    assert summary["ready"] is False
    assert summary["source"] == "launcher_session_end"
    assert "stop_condition_not_met" in summary["blockers"]


def test_launcher_appends_wait_flag_when_missing(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    captured: list[str] = []

    class _CaptureProc:
        def __init__(self, cmd: list[str]) -> None:
            captured.extend(cmd)
            self._rc = 0

        def wait(self) -> int:
            return self._rc

    ws = tmp_path / "workspace"
    ws.mkdir()
    monkeypatch.setenv("LE_VIBE_LVIBE_CONSENT", "accept")
    monkeypatch.setattr("le_vibe.launcher.ensure_managed_ollama", lambda **_: (True, "ok", None))
    monkeypatch.setattr("le_vibe.launcher.stop_managed_ollama", lambda: None)
    monkeypatch.setattr("le_vibe.launcher.subprocess.Popen", lambda cmd: _CaptureProc(cmd))
    monkeypatch.setattr(sys, "argv", ["launcher", "--skip-first-run", "--editor", "fake-editor", str(ws)])

    assert launcher.main() == 0
    assert "--wait" in captured


def test_launcher_does_not_duplicate_wait_flag(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    captured: list[str] = []

    class _CaptureProc:
        def __init__(self, cmd: list[str]) -> None:
            captured.extend(cmd)
            self._rc = 0

        def wait(self) -> int:
            return self._rc

    ws = tmp_path / "workspace"
    ws.mkdir()
    monkeypatch.setenv("LE_VIBE_LVIBE_CONSENT", "accept")
    monkeypatch.setattr("le_vibe.launcher.ensure_managed_ollama", lambda **_: (True, "ok", None))
    monkeypatch.setattr("le_vibe.launcher.stop_managed_ollama", lambda: None)
    monkeypatch.setattr("le_vibe.launcher.subprocess.Popen", lambda cmd: _CaptureProc(cmd))
    monkeypatch.setattr(
        sys,
        "argv",
        ["launcher", "--skip-first-run", "--editor", "fake-editor", "--", "--wait", str(ws)],
    )

    assert launcher.main() == 0
    assert captured.count("--wait") == 1
