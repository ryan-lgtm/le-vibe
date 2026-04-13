"""STEP 4 (E3): ``lvibe welcome`` — path or ``--text`` for terminal §4 copy."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

from le_vibe import launcher


def test_welcome_errors_without_lvibe(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr(sys, "argv", ["launcher", "welcome", str(tmp_path)])
    assert launcher.main() == 1
    assert "§5.1" in capsys.readouterr().err


def test_welcome_prints_path(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    (tmp_path / ".lvibe").mkdir()
    monkeypatch.setattr(sys, "argv", ["launcher", "welcome", str(tmp_path)])
    assert launcher.main() == 0
    out = capsys.readouterr().out.strip()
    assert out.endswith("WELCOME.md")
    assert Path(out).is_file()


def test_welcome_text_includes_section4(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    (tmp_path / ".lvibe").mkdir()
    monkeypatch.setattr(sys, "argv", ["launcher", "welcome", "--text", str(tmp_path)])
    assert launcher.main() == 0
    out = capsys.readouterr().out
    assert "Welcome to Lé Vibe" in out
    assert "PRODUCT_SPEC" in out and "§4" in out
