"""Contract: editor/BUILD.md keeps STEP 14 prepare story (toolchain + get_repo + howto pointer)."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_editor_build_md_contract_get_repo_and_howto():
    text = (_repo_root() / "editor" / "BUILD.md").read_text(encoding="utf-8")
    assert "get_repo.sh" in text
    assert "cwd-sensitive" in text
    assert "vscode/" in text
    assert "vscodium/docs/howto-build.md" in text
    assert "dev/build.sh" in text
    assert "editor/vscodium/" in text
    assert ".nvmrc" in text
    assert "nvm" in text.lower()
    assert "fetch-vscode-sources.sh" in text
    assert "14.b" in text


def test_editor_build_md_get_repo_upstream_paths_exist_when_vscodium_present():
    """STEP 14.b — upstream scripts/docs must exist when the submodule is checked out."""
    root = _repo_root()
    if not (root / "editor" / "vscodium" / "product.json").is_file():
        return
    assert (root / "editor" / "vscodium" / "get_repo.sh").is_file()
    assert (root / "editor" / "vscodium" / "docs" / "howto-build.md").is_file()
    assert (root / "editor" / "fetch-vscode-sources.sh").is_file()


def test_editor_build_md_contract_lvibe_smoke_pointer():
    text = (_repo_root() / "editor" / "BUILD.md").read_text(encoding="utf-8")
    assert "smoke-lvibe-editor.sh" in text
    assert "LE_VIBE_EDITOR" in text
    assert "--version" in text
    assert "print-built-codium-path.sh" in text
    assert "VSCode-linux-" in text


def test_editor_print_built_codium_script_exists_when_vscodium_present():
    root = _repo_root()
    if not (root / "editor" / "vscodium" / "product.json").is_file():
        return
    assert (root / "editor" / "print-built-codium-path.sh").is_file()


def test_editor_build_md_contract_ci_compile_pointer():
    text = (_repo_root() / "editor" / "BUILD.md").read_text(encoding="utf-8")
    assert "linux_compile" in text
    assert "ci-vscodium-linux-dev-build.sh" in text
    assert "dev/build.sh" in text
    assert "vscodium_linux_compile" in text
    assert "build-env.sh" in text
    assert "build-env.sh.example" in text


def test_editor_build_md_contract_tarball_and_codium_path_14f():
    text = (_repo_root() / "editor" / "BUILD.md").read_text(encoding="utf-8")
    assert "14.f" in text
    assert "Installable layout" in text
    assert "VSCode-linux-" in text
    assert "bin/codium" in text
    assert "vscodium-linux-build.tar.gz" in text
    assert "le-vibe-vscodium-linux-" in text
    assert "realpath" in text
    assert "print-vsbuild-codium-path.sh" in text
    assert "vscodium/docs/usage.md" in text
    assert "VSCodium-linux-" in text


def test_editor_print_vsbuild_codium_script_exists():
    assert (_repo_root() / "editor" / "print-vsbuild-codium-path.sh").is_file()


def test_editor_build_md_contract_default_le_vibe_editor_packaging_14g():
    text = (_repo_root() / "editor" / "BUILD.md").read_text(encoding="utf-8")
    assert "14.g" in text
    assert "le_vibe.launcher._default_editor" in text
    assert "le-vibe/le_vibe/launcher.py" in text
    assert "le-vibe.README.Debian" in text
    assert "_default_editor" in text
    assert "/usr/bin/le-vibe-ide" in text
    assert "le-vibe-ide" in text
    assert "Recommends:" in text
    assert "§7.2" in text
    assert "/usr/bin/codium" in text


def test_editor_build_md_contract_continue_pin_14h():
    text = (_repo_root() / "editor" / "BUILD.md").read_text(encoding="utf-8")
    assert "14.h" in text
    assert "continue-extension-pin.md" in text
    assert "continue-openvsx-version" in text
    assert "install-continue-extension.sh" in text
    assert "verify-continue-pin.sh" in text
    assert "sync-continue-config.sh" in text
    assert "le-vibe-setup-continue" in text
    assert "ci-smoke.sh" in text
