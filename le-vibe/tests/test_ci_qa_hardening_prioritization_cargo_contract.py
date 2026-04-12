"""Contract: docs/ci-qa-hardening.md keeps test_product_spec_section8 *Prioritization* Cargo cache strings."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_ci_qa_hardening_lists_linux_compile_cargo_cache():
    text = (_repo_root() / "docs" / "ci-qa-hardening.md").read_text(encoding="utf-8")
    assert "test_product_spec_section8.py" in text
    assert "linux_compile" in text
    assert "vscodium-linux-build.tar.gz" in text
    assert "actions/cache@v4" in text
    assert ".cargo" in text
    assert "spec-phase2.md" in text and "§14" in text
