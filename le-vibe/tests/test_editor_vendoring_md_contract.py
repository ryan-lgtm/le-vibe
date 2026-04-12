"""Contract: editor/VENDORING.md — submodule + smoke/CI gate story (STEP 14)."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_editor_vendoring_md_documents_smoke_gate_and_metadata():
    text = (_repo_root() / "editor" / "VENDORING.md").read_text(encoding="utf-8")
    assert "editor/vscodium" in text
    assert "howto-build.md" in text
    assert "./editor/smoke.sh" in text
    assert "ci-editor-gate.sh" in text
    assert "ci-vscodium-bash-syntax.sh" in text
    assert "ci-editor-nvmrc-sync.sh" in text
    assert "build-le-vibe-ide.yml" in text
    assert "build-linux.yml" in text
    assert "ide-ci-metadata.txt" in text
    assert "le_vibe_editor_docs" in text
    assert "retention-days" in text
    assert "vscodium-fork-le-vibe.md" in text
    assert "le-vibe-overrides/README.md" in text
    assert "branding-staging.checklist.md" in text
    assert "read before overrides" in text
    assert "14.c" in text and "14.d" in text and "14.e" in text
    assert "PRODUCT_SPEC" in text and "§7.2" in text
    assert "linux_compile" in text
    assert "ci-vscodium-linux-dev-build.sh" in text
    assert "node --version" in text
    assert "LEVIBE_SKIP_NODE_VERSION_CHECK" in text
    assert "Compile wrapper vs Node" in text
    assert "fail fast" in text
    assert "vscodium-linux-build.tar.gz" in text
    assert "print-ci-tarball-codium-path.sh" in text
    assert "NODE_OPTIONS" in text
    assert "max-old-space-size=8192" in text
    assert "When full compile fails" in text
