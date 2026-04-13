"""STEP 17: ``lvibe ai-pilot-continue``."""

from __future__ import annotations

import json
import sys

import pytest

from le_vibe import launcher


def test_ai_pilot_continue_path_only_doc(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.setattr(sys, "argv", ["launcher", "ai-pilot-continue", "--path-only", "doc"])
    assert launcher.main() == 0
    out = capsys.readouterr().out.strip()
    assert out.endswith("AI_PILOT_AND_CONTINUE.md")


def test_ai_pilot_continue_json(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.setattr(sys, "argv", ["launcher", "ai-pilot-continue", "--json"])
    assert launcher.main() == 0
    data = json.loads(capsys.readouterr().out)
    assert len(data["entries"]) == 3
    assert data["all_present"] is True
    assert any("continue_workspace.py" in e["path"] for e in data["entries"])


def test_ai_pilot_continue_no_monorepo(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.setattr("le_vibe.qa_scripts.find_monorepo_root", lambda: None)
    monkeypatch.setattr(sys, "argv", ["launcher", "ai-pilot-continue", "--json"])
    assert launcher.main() == 1
    assert json.loads(capsys.readouterr().out)["error"] == "monorepo_not_found"
