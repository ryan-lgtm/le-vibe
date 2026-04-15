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
    assert "sync-linux-icon-assets.sh" in text
    assert "workbench" in text
    assert "--check" in text
    assert "mktemp" in text


def test_brand_assets_doc_e1_acceptance_and_h6_fork_pointer():
    """H5: E1 names ci-smoke + PRODUCT_SPEC_SECTION8_EVIDENCE; H6 names fork doc + spec-phase2 honesty."""
    text = (_repo_root() / "docs" / "brand-assets.md").read_text(encoding="utf-8")
    assert "ci-smoke.sh" in text
    assert "PRODUCT_SPEC_SECTION8_EVIDENCE.md" in text
    assert "ci-qa-hardening.md" in text
    assert "vscodium-fork-le-vibe.md" in text
    assert "spec-phase2.md" in text
