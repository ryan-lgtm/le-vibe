"""``le_vibe.continue_pin`` — STEP 7 / H4 pin resolution."""

from __future__ import annotations

from pathlib import Path

import pytest

from le_vibe.continue_pin import read_continue_openvsx_version, resolve_continue_openvsx_pin_path


def test_resolve_honors_le_vibe_continue_pin_file(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    pin = tmp_path / "pin.txt"
    pin.write_text("9.8.7\n", encoding="utf-8")
    monkeypatch.setenv("LE_VIBE_CONTINUE_PIN_FILE", str(pin))
    assert resolve_continue_openvsx_pin_path() == pin.resolve()
    assert read_continue_openvsx_version() == "9.8.7"


def test_read_skips_comments(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    pin = tmp_path / "p.txt"
    pin.write_text("# c\n  2.0.0 \n", encoding="utf-8")
    monkeypatch.setenv("LE_VIBE_CONTINUE_PIN_FILE", str(pin))
    assert read_continue_openvsx_version() == "2.0.0"
