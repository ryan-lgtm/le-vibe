"""STEP 11: ``lvibe brand-paths``."""

from __future__ import annotations

import sys

import pytest

from le_vibe import launcher


def test_brand_paths_path_only_in_checkout(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.setattr(sys, "argv", ["launcher", "brand-paths", "--path-only"])
    assert launcher.main() == 0
    out = capsys.readouterr().out.strip()
    assert out.endswith("le-vibe.svg")
    assert "packaging" in out.replace("\\", "/")


def test_brand_paths_verbose_lists_authority(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.setattr(sys, "argv", ["launcher", "brand-paths"])
    assert launcher.main() == 0
    out = capsys.readouterr().out
    assert "brand-assets.md" in out
    assert "monorepo" in out
