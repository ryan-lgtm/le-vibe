"""Contract: editor/BUILD.md keeps STEP 14 prepare story (toolchain + get_repo + howto pointer)."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_editor_build_md_contract_vendoring_pointer():
    text = (_repo_root() / "editor" / "BUILD.md").read_text(encoding="utf-8")
    assert "git submodule update --init editor/vscodium" in text
    assert "VENDORING.md" in text
    assert "git submodule" in text.lower()
    assert "vscodium-linux-build.tar.gz" in text


def test_editor_build_md_compile_wrapper_node_parity_14a_14e():
    text = (_repo_root() / "editor" / "BUILD.md").read_text(encoding="utf-8")
    assert "Compile wrapper vs Node" in text
    assert "ci-vscodium-linux-dev-build.sh" in text
    assert "node --version" in text
    assert "LEVIBE_SKIP_NODE_VERSION_CHECK" in text


def test_editor_build_md_contract_get_repo_and_howto():
    text = (_repo_root() / "editor" / "BUILD.md").read_text(encoding="utf-8")
    assert "get_repo.sh" in text
    assert "cwd-sensitive" in text
    assert "vscode/" in text
    assert "vscodium/docs/howto-build.md" in text
    assert "#build-ci" in text
    assert "dev/build.sh" in text
    assert "editor/vscodium/" in text
    assert ".nvmrc" in text
    assert "nvm" in text.lower()
    assert "use-node-toolchain.sh" in text
    assert "14.a" in text
    assert "stderr" in text
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
    assert (root / "editor" / "use-node-toolchain.sh").is_file()


def test_editor_build_md_contract_lvibe_smoke_pointer():
    text = (_repo_root() / "editor" / "BUILD.md").read_text(encoding="utf-8")
    assert "verify-14c-local-binary.sh" in text
    assert "smoke-lvibe-editor.sh" in text
    assert "smoke-built-codium-lvibe.sh" in text
    assert "LE_VIBE_EDITOR" in text
    assert "--version" in text
    assert "print-built-codium-path.sh" in text
    assert "executable" in text
    assert "VSCode-linux-" in text
    assert "branding-staging.checklist.md" in text
    assert "read before overrides" in text
    assert "14.c" in text and "14.d" in text


def test_editor_print_built_codium_script_exists_when_vscodium_present():
    root = _repo_root()
    if not (root / "editor" / "vscodium" / "product.json").is_file():
        return
    assert (root / "editor" / "print-built-codium-path.sh").is_file()
    assert (root / "editor" / "verify-14c-local-binary.sh").is_file()


def test_editor_build_md_contract_ci_compile_pointer():
    text = (_repo_root() / "editor" / "BUILD.md").read_text(encoding="utf-8")
    assert "linux_compile" in text
    assert "NODE_OPTIONS" in text
    assert "max-old-space-size=8192" in text
    assert "ci-vscodium-bash-syntax.sh" in text
    assert "ci-editor-nvmrc-sync.sh" in text
    assert "ci-vscodium-linux-dev-build.sh" in text
    assert "Compile wrapper vs Node" in text
    assert "LEVIBE_SKIP_NODE_VERSION_CHECK" in text
    assert "dev/build.sh" in text
    assert "vscodium_linux_compile" in text
    assert "build-env.sh" in text
    assert "build-env.sh.example" in text
    assert "retention-days: 14" in text
    assert "retention-days: 90" in text


def test_editor_build_md_contract_linux_compile_troubleshooting_14e():
    """14.e honesty: BUILD.md calls out apt gap vs howto-build, runner limits, 14.i."""
    text = (_repo_root() / "editor" / "BUILD.md").read_text(encoding="utf-8")
    assert "When full compile fails" in text
    assert "14.e" in text
    assert "vscodium/docs/howto-build.md" in text
    assert "Dependencies" in text
    assert "build-le-vibe-ide.yml" in text
    assert "Install Linux build dependencies" in text
    assert "dpkg-dev" in text
    assert "python3.11-dev" in text
    assert "rpm" in text
    assert "jq" in text
    assert "librsvg2-bin" in text
    assert "spec-phase2.md" in text and "§14" in text
    assert "OOM" in text
    assert "self-hosted" in text.lower()
    assert "vscodium-fork-le-vibe.md" in text
    assert "14.i" in text


def test_editor_build_md_contract_tarball_and_codium_path_14f():
    text = (_repo_root() / "editor" / "BUILD.md").read_text(encoding="utf-8")
    assert "14.f" in text
    assert "Installable layout" in text
    assert "CI artifact →" in text and "14.e output" in text
    assert "installable tree" in text.lower()
    assert "VSCode-linux-" in text
    assert "bin/codium" in text
    assert "vscodium-linux-build.tar.gz" in text
    assert "le-vibe-vscodium-linux-" in text
    assert "realpath" in text
    assert "print-ci-tarball-codium-path.sh" in text
    assert "print-vsbuild-codium-path.sh" in text
    assert ".zip" in text
    assert "vscodium/docs/usage.md" in text
    assert "VSCodium-linux-" in text


def test_editor_print_vsbuild_codium_script_exists():
    assert (_repo_root() / "editor" / "print-vsbuild-codium-path.sh").is_file()


def test_editor_print_ci_tarball_codium_script_exists():
    assert (_repo_root() / "editor" / "print-ci-tarball-codium-path.sh").is_file()


def test_editor_build_md_contract_default_le_vibe_editor_packaging_14g():
    text = (_repo_root() / "editor" / "BUILD.md").read_text(encoding="utf-8")
    assert "14.g" in text
    assert "Unpacked trees" in text
    assert "_default_editor" in text
    assert "le_vibe.launcher._default_editor" in text
    assert "le-vibe/le_vibe/launcher.py" in text
    assert "le-vibe.README.Debian" in text
    assert "_default_editor" in text
    assert "/usr/lib/le-vibe/bin/codium" in text
    assert "le-vibe-ide" in text
    assert "packaging/debian-le-vibe-ide" in text
    assert "le-vibe.desktop" in text
    assert "Recommends:" in text
    assert "§7.2" in text
    assert "/usr/bin/codium" in text


def test_editor_build_md_contract_continue_pin_14h():
    text = (_repo_root() / "editor" / "BUILD.md").read_text(encoding="utf-8")
    assert "14.h" in text
    assert "verify-14c-local-binary.sh" in text
    assert "continue-extension-pin.md" in text
    assert "continue-openvsx-version" in text
    assert "install-continue-extension.sh" in text
    assert "verify-continue-pin.sh" in text
    assert "sync-continue-config.sh" in text
    assert "le-vibe-setup-continue" in text
    assert "ci-smoke.sh" in text
    assert "_default_editor" in text
    assert "14.g" in text
    assert "print-ci-tarball-codium-path.sh" in text
    assert "vscodium-linux-build.tar.gz" in text
