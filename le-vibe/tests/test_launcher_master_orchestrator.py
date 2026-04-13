"""STEP 16: ``lvibe master-orchestrator``."""

from __future__ import annotations

import json
import sys

import pytest

from le_vibe import launcher


def test_master_orchestrator_json(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.setattr(sys, "argv", ["launcher", "master-orchestrator", "--json"])
    assert launcher.main() == 0
    data = json.loads(capsys.readouterr().out)
    assert data["master_fence_extractable"] is True
    assert "PROMPT_BUILD_LE_VIBE.md" in data["prompt_build_le_vibe_md"]
    assert "fence_char_count" in data


def test_master_orchestrator_print(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.setattr(sys, "argv", ["launcher", "master-orchestrator", "--print"])
    assert launcher.main() == 0
    out = capsys.readouterr().out
    assert "You are the senior engineer for Lé Vibe" in out
    assert "ORDERED WORK QUEUE" in out


def test_master_orchestrator_no_monorepo(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.setattr("le_vibe.qa_scripts.find_monorepo_root", lambda: None)
    monkeypatch.setattr(sys, "argv", ["launcher", "master-orchestrator", "--json"])
    assert launcher.main() == 1
    assert json.loads(capsys.readouterr().out)["error"] == "monorepo_not_found"


def test_master_orchestrator_print_json_rejected(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.setattr(sys, "argv", ["launcher", "master-orchestrator", "--print", "--json"])
    with pytest.raises(SystemExit) as exc:
        launcher.main()
    assert exc.value.code == 2
