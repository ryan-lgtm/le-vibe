"""STEP 3 (E2): ``lvibe continue-rules``."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

from le_vibe import launcher
from le_vibe.continue_workspace import LVIBE_CONTINUE_RULE_NAME


def test_continue_rules_creates_rules(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr(sys, "argv", ["launcher", "continue-rules", str(tmp_path)])
    assert launcher.main() == 0
    out = capsys.readouterr().out
    assert "NEW" in out
    assert LVIBE_CONTINUE_RULE_NAME in out
    assert (tmp_path / ".continue" / "rules" / LVIBE_CONTINUE_RULE_NAME).is_file()


def test_continue_rules_idempotent(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr(sys, "argv", ["launcher", "continue-rules", str(tmp_path)])
    assert launcher.main() == 0
    assert launcher.main() == 0
    out = capsys.readouterr().out
    assert out.count("OK") >= 2
