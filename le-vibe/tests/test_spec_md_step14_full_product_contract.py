"""Contract: spec.md intro points maintainers at full-product .deb build (STEP 14 / §7.3)."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_spec_md_intro_documents_full_product_install_step14():
    text = (_repo_root() / "spec.md").read_text(encoding="utf-8")
    assert "Full-product maintainer build (STEP 14 / §7.3)" in text
    assert "build-le-vibe-debs.sh --with-ide" in text
    assert "le-vibe_*_all.deb" in text
    assert "le-vibe-ide_*_amd64.deb" in text
    assert "VSCode-linux-*" in text
    assert "Full-product install" in text
    assert "PM_DEB_BUILD_ITERATION.md" in text
    assert "Success output (`--with-ide`)" in text
    assert "debian-le-vibe-ide/README.md" in text
    assert "Install both packages" in text
