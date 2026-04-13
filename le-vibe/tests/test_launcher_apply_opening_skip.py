"""STEP 2: ``lvibe apply-opening-skip``."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

from le_vibe import launcher
from le_vibe.session_orchestrator import ensure_pm_session_artifacts


def test_apply_opening_skip_cli_advances(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    (tmp_path / "x.txt").write_text("hi", encoding="utf-8")
    ensure_pm_session_artifacts(tmp_path)
    monkeypatch.setattr(sys, "argv", ["launcher", "apply-opening-skip", str(tmp_path)])
    assert launcher.main() == 0
    assert capsys.readouterr().out.strip() == "workspace_scan"


def test_apply_opening_skip_cli_no_lvibe(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr(sys, "argv", ["launcher", "apply-opening-skip", str(tmp_path)])
    assert launcher.main() == 1
    assert "missing" in capsys.readouterr().err
