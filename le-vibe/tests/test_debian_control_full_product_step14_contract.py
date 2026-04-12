"""Contract: debian/control Description mentions full-product maintainer .deb path (STEP 14)."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_debian_control_description_documents_full_product_install_step14():
    text = (_repo_root() / "debian" / "control").read_text(encoding="utf-8")
    assert "le-vibe-ide" in text
    assert "README.Debian" in text
    assert "PM_DEB_BUILD_ITERATION.md" in text
    assert "build-le-vibe-debs.sh --with-ide" in text
    assert "Full-product install" in text
