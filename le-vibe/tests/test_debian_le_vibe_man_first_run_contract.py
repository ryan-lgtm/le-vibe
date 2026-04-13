"""Contract: debian/le-vibe.1 documents first-run failure observability (STEP 6)."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_debian_lvibe_man_description_lists_first_run_cross_ref_le_vibe_step6():
    """lvibe(1) DESCRIPTION echoes first-run observability; defers full OPTIONS to le-vibe(1)."""
    text = (_repo_root() / "debian" / "lvibe.1").read_text(encoding="utf-8")
    assert "LE_VIBE_VERBOSE" in text
    assert "\\fBtail \\-f\\fR" in text
    assert "\\-\\-path\\-only" in text
    assert "\\-\\-tail" in text
    assert "STEP 6" in text
    assert "\\fBlvibe \\-\\-help\\fR" in text
    assert "\\-\\-skip\\-first\\-run" in text
    assert "\\-\\-force\\-first\\-run" in text
    assert "\\fBle\\-vibe\\fR(1) OPTIONS" in text
    assert "First\\-run (launcher)" in text
    assert "PRODUCT_SPEC_SECTION8_EVIDENCE.md" in text


def test_debian_lvibe_man_ide_prereqs_synopsis_print_closeout_commands_step14():
    """STEP 14: lvibe(1) ide-prereqs lists --print-closeout-commands (preflight + verify)."""
    text = (_repo_root() / "debian" / "lvibe.1").read_text(encoding="utf-8")
    assert ".B lvibe ide\\-prereqs" in text
    assert "\\-\\-print\\-closeout\\-commands" in text
    assert "preflight\\-step14\\-closeout.sh" in text
    assert "verify\\-step14\\-closeout.sh" in text


def test_debian_le_vibe_man_ide_prereqs_synopsis_print_closeout_commands_step14():
    """STEP 14: le-vibe(1) ide-prereqs matches lvibe(1) close-out flag."""
    text = (_repo_root() / "debian" / "le-vibe.1").read_text(encoding="utf-8")
    assert ".B lvibe ide\\-prereqs" in text
    assert "\\-\\-print\\-closeout\\-commands" in text


def test_debian_le_vibe_man_lists_first_run_observability_step6():
    text = (_repo_root() / "debian" / "le-vibe.1").read_text(encoding="utf-8")
    assert "LE_VIBE_VERBOSE" in text
    assert "lvibe logs" in text
    assert "\\fBtail \\-f\\fR" in text
    assert "\\-\\-path\\-only" in text
    assert "\\-\\-tail" in text
    assert "STEP 6" in text
    assert "First\\-run (launcher)" in text
    assert "PRODUCT_SPEC_SECTION8_EVIDENCE.md" in text
