"""Contract: root README lists STEP 13 / H7 Flatpak & AppImage (Roadmap H7)."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_root_readme_step13_h7_flatpak_appimage_section():
    text = (_repo_root() / "docs" / "MONOREPO_DEVELOPER_REFERENCE.md").read_text(encoding="utf-8")
    assert "### Flatpak & AppImage — STEP 13 / H7" in text
    assert "Master orchestrator STEP 13" in text
    assert "flatpak-appimage.md" in text
    assert "org.le_vibe.Launcher.yml" in text
    assert "packaging/appimage" in text
    assert "test_flatpak_appimage_doc_h7_contract.py" in text
    assert "test_pm_stage_map_step13_contract.py" in text
    assert "spec-phase2.md" in text
