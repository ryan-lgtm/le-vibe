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


def test_stack_debian_install_shows_lvibe_on_path_step14():
    """PRODUCT_SPEC §2 / §7.3 — primary discoverable CLI is ``lvibe`` on PATH (stack .deb)."""
    inst = (_repo_root() / "debian" / "le-vibe.install").read_text(encoding="utf-8")
    assert "packaging/bin/lvibe usr/bin" in inst


def test_stack_deb_does_not_ship_ide_desktop_assets():
    """Avoid dpkg file conflicts: IDE desktop/icon assets belong to le-vibe-ide package."""
    inst = (_repo_root() / "debian" / "le-vibe.install").read_text(encoding="utf-8")
    assert "packaging/applications/le-vibe.desktop usr/share/applications" not in inst
    assert "packaging/icons/hicolor/scalable/apps/le-vibe.svg usr/share/icons/hicolor/scalable/apps" not in inst


def test_debian_control_allows_non_apt_ollama_installs():
    """Manual / script Ollama installs (for example /usr/local/bin/ollama) must not block apt install."""
    text = (_repo_root() / "debian" / "control").read_text(encoding="utf-8")
    assert "Depends: python3," in text
    assert "ollama | ollama-bin" not in text.split("Depends:", 1)[1].split("Recommends:", 1)[0]
    assert "Suggests: le-vibe-ide," in text
    assert "ollama | ollama-bin" in text.split("Suggests:", 1)[1]
