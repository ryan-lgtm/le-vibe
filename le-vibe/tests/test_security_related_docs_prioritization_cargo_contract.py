"""Contract: SECURITY.md *Related docs* keeps test_product_spec_section8 *Prioritization* Cargo cache strings."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_security_related_docs_lists_pm_deb_maintainer_full_product_step14():
    """STEP 14: SECURITY Related docs points triagers at PM deb doc + ci.yml stack-only honesty."""
    text = (_repo_root() / "SECURITY.md").read_text(encoding="utf-8")
    assert "PM_DEB_BUILD_ITERATION.md" in text
    assert "build-le-vibe-debs.sh --with-ide" in text
    assert "Full-product install" in text
    assert "le-vibe-deb" in text
    assert "apt-repo-releases.md" in text
    assert "H1 vs §7.3 .deb bundles" in text
    assert "Partial VSCode-linux" in text


def test_security_related_docs_lists_linux_compile_cargo_cache():
    text = (_repo_root() / "SECURITY.md").read_text(encoding="utf-8")
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
