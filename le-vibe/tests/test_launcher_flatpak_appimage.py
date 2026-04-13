"""STEP 13: ``lvibe flatpak-appimage``."""

from __future__ import annotations

import sys

import pytest

from le_vibe import launcher


def test_flatpak_appimage_path_only_doc(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.setattr(sys, "argv", ["launcher", "flatpak-appimage", "--path-only", "doc"])
    assert launcher.main() == 0
    out = capsys.readouterr().out.strip()
    assert out.endswith("flatpak-appimage.md")


def test_flatpak_appimage_unknown_key(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.setattr(sys, "argv", ["launcher", "flatpak-appimage", "--path-only", "nope"])
    assert launcher.main() == 2
    assert "unknown key" in capsys.readouterr().err


def test_flatpak_appimage_no_monorepo(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.setattr("le_vibe.qa_scripts.find_monorepo_root", lambda: None)
    monkeypatch.setattr(sys, "argv", ["launcher", "flatpak-appimage"])
    assert launcher.main() == 1
    assert "PM_STAGE_MAP" in capsys.readouterr().err
