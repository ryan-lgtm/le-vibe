"""STEP 7: ``lvibe continue-pin`` prints Open VSX semver."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

from le_vibe import launcher


def test_continue_pin_prints_version(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    pin = tmp_path / "v.txt"
    pin.write_text("3.2.1\n", encoding="utf-8")
    monkeypatch.setenv("LE_VIBE_CONTINUE_PIN_FILE", str(pin))
    monkeypatch.setattr(sys, "argv", ["launcher", "continue-pin"])
    assert launcher.main() == 0
    assert capsys.readouterr().out.strip() == "3.2.1"


def test_continue_pin_path_only(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    pin = tmp_path / "v.txt"
    pin.write_text("1.0.0\n", encoding="utf-8")
    monkeypatch.setenv("LE_VIBE_CONTINUE_PIN_FILE", str(pin))
    monkeypatch.setattr(sys, "argv", ["launcher", "continue-pin", "--path-only"])
    assert launcher.main() == 0
    assert Path(capsys.readouterr().out.strip()) == pin.resolve()
