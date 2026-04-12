"""Contract: debian/le-vibe.README.Debian documents launcher order (STEP 14.g)."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_debian_readme_documents_submodule_14b_for_clone_maintainers():
    text = (_repo_root() / "debian" / "le-vibe.README.Debian").read_text(encoding="utf-8")
    assert "git submodule update --init editor/vscodium" in text
    assert "Fresh clone (14.b)" in text


def test_debian_readme_documents_default_editor_resolution_14g():
    text = (_repo_root() / "debian" / "le-vibe.README.Debian").read_text(encoding="utf-8")
    assert "14.g" in text
    assert "_default_editor" in text
    assert "le-vibe/le_vibe/launcher.py" in text
    assert "LE_VIBE_EDITOR" in text
    assert "/usr/lib/le-vibe/bin/codium" in text
    assert "packaging/debian-le-vibe-ide" in text
    assert "/usr/bin/codium" in text
    assert "Recommends: codium" in text
    assert "debian/control" in text
    assert "environment.d" in text


def test_debian_readme_documents_14d_branding_honesty():
    text = (_repo_root() / "debian" / "le-vibe.README.Debian").read_text(encoding="utf-8")
    assert "Honesty (14.d)" in text
    assert "branding-staging.checklist.md" in text
    assert "read before overrides" in text
    assert "14.c vs 14.d" in text


def test_debian_readme_documents_optional_linux_compile_node_parity_14e():
    """STEP 14.e: packaged README points clone maintainers at compile-wrapper Node gate."""
    text = (_repo_root() / "debian" / "le-vibe.README.Debian").read_text(encoding="utf-8")
    assert "linux_compile" in text
    assert "ci-vscodium-linux-dev-build.sh" in text
    assert "node --version" in text
    assert "LEVIBE_SKIP_NODE_VERSION_CHECK" in text
    assert "Compile wrapper vs Node" in text
