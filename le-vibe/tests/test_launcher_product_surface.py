"""STEP 12: ``lvibe product-surface``."""

from __future__ import annotations

import sys

import pytest

from le_vibe import launcher


def test_product_surface_path_only_ci(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.setattr(sys, "argv", ["launcher", "product-surface", "--path-only", "ci"])
    assert launcher.main() == 0
    out = capsys.readouterr().out.strip()
    assert out.endswith("ci.yml")


def test_product_surface_unknown_key(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.setattr(sys, "argv", ["launcher", "product-surface", "--path-only", "nope"])
    assert launcher.main() == 2
    assert "unknown key" in capsys.readouterr().err


def test_product_surface_no_monorepo(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.setattr("le_vibe.qa_scripts.find_monorepo_root", lambda: None)
    monkeypatch.setattr(sys, "argv", ["launcher", "product-surface"])
    assert launcher.main() == 1
    assert "PM_STAGE_MAP" in capsys.readouterr().err
