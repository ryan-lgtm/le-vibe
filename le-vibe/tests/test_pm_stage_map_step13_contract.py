"""Contract: docs/PM_STAGE_MAP.md STEP 13 row lists H7 Flatpak/AppImage + E1 (STEP 13)."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_pm_stage_map_step13_row_lists_h7_and_e1():
    text = (_repo_root() / "docs" / "PM_STAGE_MAP.md").read_text(encoding="utf-8")
    rows = [ln for ln in text.splitlines() if ln.lstrip().startswith("| 13 — H7 Flatpak")]
    assert len(rows) == 1
    row = rows[0]
    assert "flatpak-appimage.md" in row
    assert "org.le_vibe.Launcher.yml" in row
    assert "packaging/appimage" in row
    assert "Flathub" in row
    assert "test_flatpak_appimage_doc_h7_contract.py" in row
    assert "test_pm_stage_map_step13_contract.py" in row
    assert "spec-phase2.md" in row
    assert "H7" in row or "STEP 13" in row
