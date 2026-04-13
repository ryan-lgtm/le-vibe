"""STEP 11: ``lvibe brand-paths``."""

from __future__ import annotations

import json
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


def test_brand_paths_json_in_checkout(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.setattr(sys, "argv", ["launcher", "brand-paths", "--json"])
    assert launcher.main() == 0
    data = json.loads(capsys.readouterr().out)
    assert data["ok"] is True
    assert data["monorepo_svg"].endswith("le-vibe.svg")
    assert "packaging/icons/hicolor/scalable/apps/le-vibe.svg" in data["scalable_svg_relpath"].replace("\\", "/")


def test_brand_paths_json_missing_both(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.setattr(
        "le_vibe.brand_paths.resolve_scalable_icon_paths",
        lambda: (None, None),
    )
    monkeypatch.setattr(sys, "argv", ["launcher", "brand-paths", "--json"])
    assert launcher.main() == 1
    data = json.loads(capsys.readouterr().out)
    assert data["ok"] is False
    assert data["error"] == "no_le_vibe_svg"


def test_brand_paths_path_only_json_rejected(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.setattr(sys, "argv", ["launcher", "brand-paths", "--path-only", "--json"])
    with pytest.raises(SystemExit) as exc:
        launcher.main()
    assert exc.value.code == 2
    err = capsys.readouterr().err.lower()
    assert "not allowed" in err or "path-only" in err
