"""Contract: build-le-vibe-ide.yml + build-linux.yml (alias) keep STEP 14 metadata story (H6)."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_build_le_vibe_ide_workflow_header_documents_out_of_band_deb_step14():
    """§7.3: IDE workflow header — not ci.yml le-vibe-deb; .deb via maintainer scripts."""
    text = (_repo_root() / ".github" / "workflows" / "build-le-vibe-ide.yml").read_text(encoding="utf-8")
    assert "Out-of-band .deb" in text
    assert "le-vibe-deb" in text
    assert "build-le-vibe-debs.sh --with-ide" in text
    assert "Full-product install" in text
    assert "PM_DEB_BUILD_ITERATION.md" in text
    assert "apt-repo-releases.md" in text


def test_build_le_vibe_ide_workflow_writes_le_vibe_editor_docs_to_metadata():
    text = (_repo_root() / ".github" / "workflows" / "build-le-vibe-ide.yml").read_text(encoding="utf-8")
    assert "ide-ci-metadata.txt" in text
    assert "le_vibe_editor_docs=editor/README.md" in text
    assert "GITHUB_STEP_SUMMARY" in text
    assert "**Pre-binary artifact:**" in text
    assert "LE_VIBE_EDITOR" in text
    assert "retention-days:" in text
    assert "permissions:" in text
    assert "contents: read" in text
    assert "actions: write" in text
    assert "linux_compile:" in text
    assert "ci-vscodium-linux-dev-build.sh" in text
    assert "linux-vscodium-ci-apt.pkgs" in text
    assert "vscodium_linux_compile" in text
    assert "dev/build.sh" in text


def test_build_le_vibe_ide_workflow_linux_compile_artifact_14e():
    """STEP 14.e — opt-in full compile uploads vscodium-linux-build.tar.gz when VSCode-linux-* exists."""
    text = (_repo_root() / ".github" / "workflows" / "build-le-vibe-ide.yml").read_text(encoding="utf-8")
    assert "14.e" in text
    assert "vscodium-linux-build.tar.gz" in text
    assert "le-vibe-vscodium-linux-" in text
    assert "VSCode-linux-" in text
    assert "upload-artifact@v4" in text
    assert "actions/cache@v4" in text
    assert "linux_compile-cargo" in text
    assert "workflow_call:" in text
    assert "inputs.vscodium_linux_compile" in text
    assert "github.event_name == 'workflow_call'" in text
    assert "Collect linux output tree" in text
    assert "Pack VSCode-linux artifact" in text
    assert "retention-days: 14" in text
    assert "retention-days: 90" in text
    assert "ubuntu-22.04" in text
    assert "timeout-minutes: 360" in text
    assert "node-version-file: editor/.nvmrc" in text
    assert "ci-editor-nvmrc-sync" in text
    assert "build-env.sh.example" in text
    assert "print-ci-tarball-codium-path.sh" in text
    assert "verify-14c-local-binary.sh" in text
    assert "Fail-fast editor gates" in text
    assert "./packaging/scripts/ci-vscodium-bash-syntax.sh" in text
    assert "./packaging/scripts/ci-editor-nvmrc-sync.sh" in text
    assert "linux-vscodium-ci-apt.pkgs" in text
    _pkgs = (_repo_root() / "packaging" / "linux-vscodium-ci-apt.pkgs").read_text(encoding="utf-8")
    assert "python3.11-dev" in _pkgs
    assert "rpm" in _pkgs
    assert "NODE_OPTIONS" in text
    assert "max-old-space-size=8192" in text


def test_build_linux_yaml_header_out_of_band_deb_matches_ide_workflow_step14():
    """§7.3: build-linux alias inherits honest .deb scope from build-le-vibe-ide.yml."""
    text = (_repo_root() / ".github" / "workflows" / "build-linux.yml").read_text(encoding="utf-8")
    assert "Out-of-band .deb" in text
    assert "le-vibe-deb" in text
    assert "build-le-vibe-debs.sh --with-ide" in text
    assert "Full-product install" in text
    assert "PM_DEB_BUILD_ITERATION.md" in text
    assert "apt-repo-releases.md" in text


def test_build_linux_yaml_uses_build_le_vibe_ide_and_documents_inherited_metadata():
    text = (_repo_root() / ".github" / "workflows" / "build-linux.yml").read_text(encoding="utf-8")
    assert "STEP 14" in text
    assert "name: build-linux" in text
    assert "uses: ./.github/workflows/build-le-vibe-ide.yml" in text
    assert "ide-ci-metadata.txt" in text
    assert "retention-days" in text
    assert "permissions" in text
    assert "LE_VIBE_EDITOR" in text
    assert "with:" in text
    assert "vscodium_linux_compile" in text
    assert "github.event.inputs.vscodium_linux_compile" in text
