"""Contract: root README lists STEP 14 / H6 IDE close-out (PRODUCT_SPEC §7.3)."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_root_readme_step14_h6_ide_section():
    text = (_repo_root() / "README.md").read_text(encoding="utf-8")
    assert "### Lé Vibe IDE — STEP 14 / H6" in text
    assert "Master orchestrator STEP 14" in text
    assert "PRODUCT_SPEC.md" in text and "§7.3" in text
    assert "vscodium-fork-le-vibe.md" in text
    assert "packaging/debian-le-vibe-ide" in text
    assert "verify-step14-closeout.sh" in text
    assert "test_editor_readme_step14_contract.py" in text
    assert "test_verify_step14_closeout_contract.py" in text
