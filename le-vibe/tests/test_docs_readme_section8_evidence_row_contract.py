"""Contract: docs/README.md document table keeps PRODUCT_SPEC_SECTION8_EVIDENCE row aligned with PRODUCT_SPEC *Prioritization*."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_docs_readme_section8_evidence_row_lists_linux_compile_cargo_cache():
    text = (_repo_root() / "docs" / "README.md").read_text(encoding="utf-8")
    assert "PRODUCT_SPEC_SECTION8_EVIDENCE.md" in text
    assert "test_product_spec_section8.py" in text
    assert "14.d" in text
    assert "branding-staging.checklist.md" in text
    assert "linux_compile" in text
    assert "ci-vscodium-bash-syntax.sh" in text
    assert "ci-vscodium-linux-dev-build.sh" in text
    assert "LEVIBE_SKIP_NODE_VERSION_CHECK" in text
    assert "fail fast" in text
    assert "vscodium-linux-build.tar.gz" in text
    assert "actions/cache@v4" in text
    assert ".cargo" in text
    assert "spec-phase2.md" in text and "§14" in text
