"""Contract: editor/le-vibe-overrides/README.md keeps LE_VIBE_EDITOR + STEP 14 / H6 CI pointers."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_editor_le_vibe_overrides_readme_documents_launcher_and_h6_gate():
    text = (_repo_root() / "editor" / "le-vibe-overrides" / "README.md").read_text(encoding="utf-8")
    assert "Lé Vibe" in text
    assert "LE_VIBE_EDITOR" in text
    assert "build-le-vibe-ide.yml" in text
    assert "build-linux.yml" in text
    assert "./editor/smoke.sh" in text
    assert "ci-qa-hardening.md" in text
    assert "ide-ci-metadata.txt" in text
    assert "le_vibe_editor_docs" in text
    assert "test_build_le_vibe_ide_workflow_contract.py" in text
    assert "USER RESPONSE REQUIRED" in text
    assert "§7.2" in text
    assert "product.json" in text
    assert "packaging/icons/" in text
    assert "build-env.sh.example" in text
    assert "ci-vscodium-linux-dev-build.sh" in text
    assert "14.d" in text
    assert "vscodium-fork-le-vibe.md" in text
    assert "use-node-toolchain.sh" in text
    assert "14.a" in text
    assert "fetch-vscode-sources.sh" in text
    assert "print-built-codium-path.sh" in text
    assert "smoke-built-codium-lvibe.sh" in text
    assert "smoke-lvibe-editor.sh" in text
    assert "Upstream touchpoints (14.d)" in text
    assert "src/stable/resources/linux" in text
    assert "prepare_vscode.sh" in text or "prepare_src.sh" in text
    assert "Build flow vs branding layers" in text
