"""Contract: docs/flatpak-appimage.md keeps H7 deliverables + Flathub track (STEP 13)."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_flatpak_appimage_doc_lists_paths_flathub_and_spec_phase2_h7():
    text = (_repo_root() / "docs" / "flatpak-appimage.md").read_text(encoding="utf-8")
    assert "git submodule update --init editor/vscodium" in text
    assert "Fresh clone (14.b)" in text
    assert "Flathub" in text
    assert "packaging/flatpak" in text
    assert "org.le_vibe.Launcher.yml" in text
    assert "packaging/appimage" in text
    assert "build-appimage.sh" in text
    assert "spec-phase2.md" in text or "spec-phase2" in text
    assert "H7" in text or "Roadmap H7" in text
    assert "STEP 13" in text
    assert "PM_STAGE_MAP" in text


def test_h7_packaging_files_exist():
    root = _repo_root()
    assert (root / "packaging" / "flatpak" / "org.le_vibe.Launcher.yml").is_file()
    assert (root / "packaging" / "flatpak" / "README.md").is_file()
    assert (root / "packaging" / "appimage" / "AppRun").is_file()
    assert (root / "packaging" / "appimage" / "build-appimage.sh").is_file()
    assert (root / "packaging" / "appimage" / "README.md").is_file()
