"""STEP 4 (E3): ``lvibe open-welcome`` opens PRODUCT_SPEC §4 welcome without Ollama."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

from le_vibe import launcher


def test_open_welcome_errors_without_lvibe(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("LE_VIBE_STRUCTURED_LOG", "0")
    monkeypatch.setattr(sys, "argv", ["launcher", "open-welcome", "."])
    rc = launcher.main()
    assert rc == 1
    err = capsys.readouterr().err
    assert "§5.1" in err


def test_open_welcome_runs_editor_on_welcome_md(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("LE_VIBE_STRUCTURED_LOG", "0")
    (tmp_path / ".lvibe").mkdir()
    recorded: list[list[str]] = []

    def fake_run(cmd: list[str], **_kwargs: object) -> object:
        recorded.append(list(cmd))
        return type("P", (), {"returncode": 0})()

    monkeypatch.setattr(launcher.subprocess, "run", fake_run)
    monkeypatch.setattr(sys, "argv", ["launcher", "open-welcome", str(tmp_path)])
    assert launcher.main() == 0
    assert len(recorded) == 1
    welcome = tmp_path / ".lvibe" / "WELCOME.md"
    assert welcome.is_file()
    assert recorded[0][-1] == str(welcome)
    assert recorded[0][0] == launcher._default_editor()
