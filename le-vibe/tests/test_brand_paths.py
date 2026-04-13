"""STEP 11 / H5: ``brand_paths.resolve_scalable_icon_paths``."""

from __future__ import annotations

from pathlib import Path

from le_vibe.brand_paths import SCALABLE_SVG_REL, resolve_scalable_icon_paths


def test_monorepo_icon_exists_in_checkout():
    mono, _pkg = resolve_scalable_icon_paths()
    assert mono is not None
    assert mono.name == "le-vibe.svg"
    assert "packaging" in mono.parts
    assert mono.is_file()


def test_relative_constant_matches_brand_assets_doc():
    root = Path(__file__).resolve().parents[2]
    assert (root / SCALABLE_SVG_REL).is_file()
