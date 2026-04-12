"""Contract: build-le-vibe-ide.yml + build-linux.yml (alias) keep STEP 14 metadata story (H6)."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


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


def test_build_linux_yaml_uses_build_le_vibe_ide_and_documents_inherited_metadata():
    text = (_repo_root() / ".github" / "workflows" / "build-linux.yml").read_text(encoding="utf-8")
    assert "uses: ./.github/workflows/build-le-vibe-ide.yml" in text
    assert "ide-ci-metadata.txt" in text
    assert "retention-days" in text
    assert "permissions" in text
    assert "LE_VIBE_EDITOR" in text
