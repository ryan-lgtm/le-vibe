"""STEP 7: ``lvibe continue-pin`` prints Open VSX semver."""

from __future__ import annotations

import json
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


def test_continue_pin_json(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    pin = tmp_path / "v.txt"
    pin.write_text("2.3.4\n", encoding="utf-8")
    monkeypatch.setenv("LE_VIBE_CONTINUE_PIN_FILE", str(pin))
    monkeypatch.setattr(sys, "argv", ["launcher", "continue-pin", "--json"])
    assert launcher.main() == 0
    data = json.loads(capsys.readouterr().out)
    assert data["semver"] == "2.3.4"
    assert data["openvsx_id"] == "continue.continue@2.3.4"
    assert Path(data["pin_file"]) == pin.resolve()


def test_continue_pin_json_mutex_path_only(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr(sys, "argv", ["launcher", "continue-pin", "--json", "--path-only"])
    assert launcher.main() == 2
    assert "cannot" in capsys.readouterr().err.lower()
