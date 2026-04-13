"""Contract: root README lists STEP 11 / H5 brand + screenshots (Roadmap H5)."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_root_readme_step11_h5_brand_section():
    text = (_repo_root() / "README.md").read_text(encoding="utf-8")
    assert "### Brand & screenshots — STEP 11 / H5" in text
    assert "Master orchestrator STEP 11" in text
    assert "brand-assets.md" in text
    assert "le-vibe.svg" in text
    assert "screenshots/README.md" in text
    assert "test_brand_assets_doc_h5_contract.py" in text
