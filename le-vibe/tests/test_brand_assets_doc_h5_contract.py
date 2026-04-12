"""Contract: docs/brand-assets.md keeps H5 brand handoff (STEP 11)."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_brand_assets_doc_lists_icons_and_h5():
    text = (_repo_root() / "docs" / "brand-assets.md").read_text(encoding="utf-8")
    assert "packaging/icons" in text
    assert "H5" in text or "Roadmap H5" in text
    assert "STEP 11" in text or "screenshots" in text.lower()
    assert "PM_STAGE_MAP" in text
    assert "le-vibe.svg" in text
