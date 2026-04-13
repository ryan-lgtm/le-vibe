"""STEP 10: ``lvibe ci-smoke`` / ``lvibe ci-editor-gate``."""

from __future__ import annotations

import sys

import pytest

from le_vibe import launcher


def test_ci_smoke_errors_when_no_monorepo(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.setattr("le_vibe.qa_scripts.find_monorepo_root", lambda: None)
    monkeypatch.setattr(sys, "argv", ["launcher", "ci-smoke"])
    assert launcher.main() == 1
    assert "ci-qa-hardening.md" in capsys.readouterr().err


def test_ci_editor_gate_help_when_monorepo_present(monkeypatch: pytest.MonkeyPatch) -> None:
    from le_vibe.qa_scripts import find_monorepo_root

    if find_monorepo_root() is None:
        pytest.skip("not in a monorepo checkout")
    monkeypatch.setattr(sys, "argv", ["launcher", "ci-editor-gate", "--help"])
    assert launcher.main() == 0
