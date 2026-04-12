"""Contract: editor/le-vibe-overrides/README.md keeps LE_VIBE_EDITOR + STEP 14 / H6 CI pointers."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_branding_staging_checklist_14d_contract():
    """editor/le-vibe-overrides/branding-staging.checklist.md stays a usable 14.d staging map."""
    text = (
        _repo_root() / "editor" / "le-vibe-overrides" / "branding-staging.checklist.md"
    ).read_text(encoding="utf-8")
    assert "verify-14c-local-binary.sh" in text
    assert "14.d" in text
    assert "PRODUCT_SPEC §7.2" in text
    assert "User gate" in text
    assert "spec-phase2.md" in text
    assert "§7.2" in text
    assert "USER RESPONSE REQUIRED" in text
    assert "build-env.sh.example" in text
    assert "ci-vscodium-linux-dev-build.sh" in text
    assert "product.json" in text
    assert "vscodium-fork-le-vibe.md" in text


def test_editor_le_vibe_overrides_readme_documents_launcher_and_h6_gate():
    text = (_repo_root() / "editor" / "le-vibe-overrides" / "README.md").read_text(encoding="utf-8")
    assert "Lé Vibe" in text
    assert "§7.3" in text
    assert "product-branding-merge.json" in text
    assert "sync-linux-icon-assets.sh" in text
    assert "build-env.lvibe-defaults.sh" in text
    assert "LE_VIBE_EDITOR" in text
    assert "build-le-vibe-ide.yml" in text
    assert "build-linux.yml" in text
    assert "linux_compile" in text
    assert "ci-vscodium-bash-syntax.sh" in text
    assert "ci-editor-nvmrc-sync.sh" in text
    assert "node --version" in text
    assert "LEVIBE_SKIP_NODE_VERSION_CHECK" in text
    assert "fail fast" in text
    assert "vscodium-linux-build.tar.gz" in text
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
    assert "test_build_env_example_step14_contract.py" in text
    assert "ci-vscodium-linux-dev-build.sh" in text
    assert "14.d" in text
    assert "vscodium-fork-le-vibe.md" in text
    assert "use-node-toolchain.sh" in text
    assert "14.a" in text
    assert "fetch-vscode-sources.sh" in text
    assert "verify-14c-local-binary.sh" in text
    assert "print-built-codium-path.sh" in text
    assert "smoke-built-codium-lvibe.sh" in text
    assert "smoke-lvibe-editor.sh" in text
    assert "Upstream touchpoints (14.d)" in text
    assert "src/stable/resources/linux" in text
    assert "prepare_vscode.sh" in text or "prepare_src.sh" in text
    assert "Build flow vs branding layers" in text
    assert "brand-assets.md" in text
    assert "screenshots/README.md" in text
    assert "branding-staging.checklist.md" in text
    assert "read before overrides" in text
