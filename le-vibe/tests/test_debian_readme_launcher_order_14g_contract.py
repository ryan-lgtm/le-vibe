"""Contract: debian/le-vibe.README.Debian documents launcher order (STEP 14.g)."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_debian_readme_documents_submodule_14b_for_clone_maintainers():
    text = (_repo_root() / "debian" / "le-vibe.README.Debian").read_text(encoding="utf-8")
    assert "git submodule update --init editor/vscodium" in text
    assert "Fresh clone (14.b)" in text


def test_debian_readme_documents_ci_vs_maintainer_deb_bundles_step14():
    """STEP 14: packaged README names default le-vibe-deb vs le-vibe-ide (§7.3 honesty)."""
    text = (_repo_root() / "debian" / "le-vibe.README.Debian").read_text(encoding="utf-8")
    assert "CI vs maintainer .deb bundles" in text
    assert "le-vibe-deb" in text
    assert "le-vibe-ide_*_amd64.deb" in text
    assert "apt-repo-releases.md" in text
    assert "PM_STAGE_MAP.md" in text
    assert "H1 vs §7.3 .deb bundles" in text
    assert "build-le-vibe-debs.sh --with-ide" in text
    assert "Full-product install" in text
    assert "PM_DEB_BUILD_ITERATION.md" in text
    assert "Success output (`--with-ide`)" in text


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


def test_debian_readme_documents_partial_tree_maintainer_scripts_14f():
    """STEP 14.f: installed README.Debian lists linux_compile tarball maintainer path."""
    text = (_repo_root() / "debian" / "le-vibe.README.Debian").read_text(encoding="utf-8")
    assert "Partial `VSCode-linux` tree" in text
    assert "print-github-linux-compile-artifact-hint.sh" in text
    assert "trigger-le-vibe-ide-linux-compile.sh" in text
    assert "download-vscodium-linux-compile-artifact.sh" in text
    assert "install-vscodium-linux-tarball-to-editor-vendor.sh" in text
    assert "hicolor_icon_in_deb" in text
    assert "preflight-step14-closeout.sh" in text
    assert "verify-step14-closeout.sh" in text
