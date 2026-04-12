"""Contract: privacy + AI Pilot docs keep test_product_spec_section8 *Prioritization* Cargo cache strings."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_privacy_and_telemetry_e1_row_lists_linux_compile_cargo_cache():
    text = (_repo_root() / "docs" / "privacy-and-telemetry.md").read_text(encoding="utf-8")
    assert "test_product_spec_section8.py" in text
    assert "linux_compile" in text
    assert "ci-vscodium-bash-syntax.sh" in text
    assert "ci-vscodium-linux-dev-build.sh" in text
    assert "LEVIBE_SKIP_NODE_VERSION_CHECK" in text
    assert "fail fast" in text
    assert "vscodium-linux-build.tar.gz" in text
    assert "actions/cache@v4" in text
    assert ".cargo" in text
    assert "spec-phase2.md" in text and "§14" in text


def test_ai_pilot_and_continue_table_lists_linux_compile_cargo_cache():
    text = (_repo_root() / "docs" / "AI_PILOT_AND_CONTINUE.md").read_text(encoding="utf-8")
    assert "test_product_spec_section8.py" in text
    assert "linux_compile" in text
    assert "ci-vscodium-bash-syntax.sh" in text
    assert "ci-vscodium-linux-dev-build.sh" in text
    assert "LEVIBE_SKIP_NODE_VERSION_CHECK" in text
    assert "fail fast" in text
    assert "vscodium-linux-build.tar.gz" in text
    assert "actions/cache@v4" in text
    assert ".cargo" in text
    assert "spec-phase2.md" in text and "§14" in text
