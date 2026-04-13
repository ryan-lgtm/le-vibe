"""STEP 13 / H7: flatpak_appimage_paths manifest matches checkout."""

from __future__ import annotations

from pathlib import Path

from le_vibe.flatpak_appimage_paths import H7_MANIFEST, iter_h7_paths


def _root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_h7_manifest_lists_doc_flatpak_appimage():
    rels = [p for _, p in H7_MANIFEST]
    assert Path("docs/flatpak-appimage.md") in rels
    assert Path("packaging/flatpak/org.le_vibe.Launcher.yml") in rels
    assert Path("packaging/appimage/build-appimage.sh") in rels


def test_iter_h7_paths_all_ok_in_repo():
    root = _root()
    for _label, path, ok in iter_h7_paths(root):
        assert ok, path
