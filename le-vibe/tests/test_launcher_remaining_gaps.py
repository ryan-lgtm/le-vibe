"""STEP 66: ``lvibe remaining-gaps`` output contracts."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

from le_vibe import launcher
from le_vibe.workspace_hub import ensure_lvibe_workspace


def test_remaining_gaps_json(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    ws = tmp_path / "w"
    ws.mkdir()
    ensure_lvibe_workspace(ws)
    monkeypatch.setattr(sys, "argv", ["launcher", "remaining-gaps", "-C", str(ws), "--json"])
    assert launcher.main() == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["workspace_root"] == str(ws.resolve())
    report = payload["report"]
    assert report["has_gaps"] is True
    assert "stop_condition_not_met" in report["gaps"]


def test_remaining_gaps_human(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    ws = tmp_path / "w"
    ws.mkdir()
    ensure_lvibe_workspace(ws)
    monkeypatch.setattr(sys, "argv", ["launcher", "remaining-gaps", "--workspace", str(ws)])
    assert launcher.main() == 0
    out = capsys.readouterr().out
    assert "Task 66" in out
    assert "Gap count:" in out


def test_remaining_gaps_missing_manifest(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    ws = tmp_path / "w"
    ws.mkdir()
    monkeypatch.setattr(sys, "argv", ["launcher", "remaining-gaps", "-C", str(ws), "--json"])
    assert launcher.main() == 1
    assert "missing" in capsys.readouterr().err.lower()
