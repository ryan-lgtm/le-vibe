"""STEP 10: ``lvibe ci-smoke`` / ``lvibe ci-editor-gate``."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

from le_vibe import launcher


def test_ci_smoke_errors_when_no_monorepo(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.setattr("le_vibe.qa_scripts.find_monorepo_root", lambda: None)
    monkeypatch.setattr(sys, "argv", ["launcher", "ci-smoke"])
    assert launcher.main() == 1
    assert "ci-qa-hardening.md" in capsys.readouterr().err


def test_ci_smoke_json_errors_when_no_monorepo(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.setattr("le_vibe.qa_scripts.find_monorepo_root", lambda: None)
    monkeypatch.setattr(sys, "argv", ["launcher", "ci-smoke", "--json"])
    assert launcher.main() == 1
    data = json.loads(capsys.readouterr().out)
    assert data["error"] == "monorepo_not_found"
    assert data["script"] == "packaging/scripts/ci-smoke.sh"


def test_ci_smoke_json_ok(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    root = Path("/tmp/fake-le-vibe-root")
    monkeypatch.setattr("le_vibe.qa_scripts.find_monorepo_root", lambda: root)
    monkeypatch.setattr(
        "le_vibe.qa_scripts.run_ci_smoke_captured",
        lambda argv: (0, "out\n", "err\n"),
    )
    monkeypatch.setattr(sys, "argv", ["launcher", "ci-smoke", "--json", "--help"])
    assert launcher.main() == 0
    data = json.loads(capsys.readouterr().out)
    assert data["ok"] is True
    assert data["exit_code"] == 0
    assert data["script_args"] == ["--help"]
    assert data["monorepo_root"] == str(root)


def test_ci_editor_gate_json_errors_when_no_monorepo(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.setattr("le_vibe.qa_scripts.find_monorepo_root", lambda: None)
    monkeypatch.setattr(sys, "argv", ["launcher", "ci-editor-gate", "--json"])
    assert launcher.main() == 1
    data = json.loads(capsys.readouterr().out)
    assert data["error"] == "monorepo_not_found"
    assert data["script"] == "packaging/scripts/ci-editor-gate.sh"


def test_ci_editor_gate_help_when_monorepo_present(monkeypatch: pytest.MonkeyPatch) -> None:
    from le_vibe.qa_scripts import find_monorepo_root

    if find_monorepo_root() is None:
        pytest.skip("not in a monorepo checkout")
    monkeypatch.setattr(sys, "argv", ["launcher", "ci-editor-gate", "--help"])
    assert launcher.main() == 0
