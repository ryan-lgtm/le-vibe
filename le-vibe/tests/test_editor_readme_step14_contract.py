"""Contract: editor/README.md — STEP 14 path table + CI story (H6)."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_editor_readme_step14_fine_grain_vs_h6_honesty():
    text = (_repo_root() / "editor" / "README.md").read_text(encoding="utf-8")
    assert "14.a–14.j" in text
    assert "H6" in text
    assert "spec-phase2.md" in text and "§14" in text
    assert "ide-ci-metadata.txt" in text
    assert "docs/PM_STAGE_MAP.md" in text
    assert "14.c vs 14.d" in text
    assert "branding-staging.checklist.md" in text
    assert "read before overrides" in text


def test_editor_readme_path_table_lists_fine_grain_scripts():
    text = (_repo_root() / "editor" / "README.md").read_text(encoding="utf-8")
    assert "**14.a**" in text
    assert "**14.b**" in text
    assert "dev/build.sh" in text and "VSCODE_QUALITY" in text
    assert "| **`editor/verify-14c-local-binary.sh`** |" in text
    assert "**14.c**" in text
    assert "**14.f**" in text
    assert "| **`editor/smoke.sh`** |" in text
    assert "ci-editor-gate.sh" in text
    assert "print-ci-tarball-codium-path.sh" in text


def test_editor_readme_ci_paragraph_build_workflows():
    text = (_repo_root() / "editor" / "README.md").read_text(encoding="utf-8")
    assert "build-le-vibe-ide.yml" in text
    assert "build-linux.yml" in text
    assert "ide-ci-metadata.txt" in text
    assert "le_vibe_editor_docs=editor/README.md" in text
    assert "retention-days" in text
    assert "Pre-binary artifact" in text
    assert "workflow_call" in text


def test_editor_readme_documents_linux_compile_and_tarball_14ef():
    """STEP 14.e / 14.f — README names linux_compile, dev build hook, CI tarball, LE_VIBE_EDITOR helper."""
    text = (_repo_root() / "editor" / "README.md").read_text(encoding="utf-8")
    assert "(14.e / 14.f)" in text
    assert "linux_compile" in text
    assert "ci-vscodium-bash-syntax.sh" in text
    assert "ci-editor-nvmrc-sync.sh" in text
    assert "fail fast" in text
    assert "ci-vscodium-linux-dev-build.sh" in text
    assert "node --version" in text
    assert "LEVIBE_SKIP_NODE_VERSION_CHECK" in text
    assert "Compile wrapper vs Node" in text
    assert "dev/build.sh" in text
    assert "vscodium_linux_compile" in text
    assert "vscodium-linux-build.tar.gz" in text
    assert "le-vibe-vscodium-linux-" in text
    assert "print-ci-tarball-codium-path.sh" in text
    assert "NODE_OPTIONS" in text
    assert "max-old-space-size=8192" in text
    assert "When full compile fails" in text
