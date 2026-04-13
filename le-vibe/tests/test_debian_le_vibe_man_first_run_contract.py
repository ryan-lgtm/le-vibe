"""Contract: debian/le-vibe.1 documents first-run failure observability (STEP 6)."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_debian_lvibe_man_description_lists_first_run_cross_ref_le_vibe_step6():
    """lvibe(1) DESCRIPTION echoes first-run observability; defers full OPTIONS to le-vibe(1)."""
    text = (_repo_root() / "debian" / "lvibe.1").read_text(encoding="utf-8")
    assert "LE_VIBE_VERBOSE" in text
    assert "\\-\\-path\\-only" in text
    assert "\\-\\-tail" in text
    assert "STEP 6" in text
    assert "\\fBle\\-vibe\\fR(1) OPTIONS" in text
    assert "First\\-run (launcher)" in text
    assert "PRODUCT_SPEC_SECTION8_EVIDENCE.md" in text


def test_debian_le_vibe_man_lists_first_run_observability_step6():
    text = (_repo_root() / "debian" / "le-vibe.1").read_text(encoding="utf-8")
    assert "LE_VIBE_VERBOSE" in text
    assert "lvibe logs" in text
    assert "\\-\\-path\\-only" in text
    assert "\\-\\-tail" in text
    assert "STEP 6" in text
    assert "First\\-run (launcher)" in text
    assert "PRODUCT_SPEC_SECTION8_EVIDENCE.md" in text
