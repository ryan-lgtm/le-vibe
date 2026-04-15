"""Contract: packaging/debian-le-vibe-ide exists for PRODUCT_SPEC §7.3 IDE .deb."""

from __future__ import annotations

import subprocess
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_stage_le_vibe_ide_deb_script_header_documents_h1_vs_ci_step14():
    """STEP 14: staging script header matches ci.yml stack-only vs maintainer IDE .deb."""
    root = _repo_root()
    text = (root / "packaging" / "scripts" / "stage-le-vibe-ide-deb.sh").read_text(encoding="utf-8")
    assert "0 → 1 → 14 → 2–13 → 15–17" in text
    assert "PROMPT_BUILD_LE_VIBE.md" in text
    assert "PM_STAGE_MAP.md" in text
    assert "le-vibe-deb" in text
    assert "apt-repo-releases.md" in text
    assert "build-le-vibe-debs.sh --with-ide" in text
    assert "Full-product install" in text
    assert "PM_DEB_BUILD_ITERATION.md" in text
    assert "Success output (--with-ide)" in text
    assert "test_packaging_le_vibe_ide_deb_contract.py" in text
    assert "test_verify_step14_closeout_contract.py" in text
    assert ".pytest-verify-step14-contract.lock" in text


def test_stage_le_vibe_ide_deb_script_documents_14b_submodule_and_bash_syntax():
    root = _repo_root()
    script = root / "packaging" / "scripts" / "stage-le-vibe-ide-deb.sh"
    text = script.read_text(encoding="utf-8")
    assert "git submodule update --init editor/vscodium" in text
    assert "Fresh clone (14.b)" in text
    assert "not executable:" in text
    assert "missing $BIN (partial" in text
    assert "partial VSCode-linux tree" in text
    assert "print-built-codium-path.sh" in text
    assert "install-vscodium-linux-tarball-to-editor-vendor.sh" in text
    assert "print-github-linux-compile-artifact-hint.sh" in text
    assert "trigger-le-vibe-ide-linux-compile.sh" in text
    assert "download-vscodium-linux-compile-artifact.sh" in text
    assert "14.c" in text
    assert "restore packaging/debian-le-vibe-ide" in text
    assert "restore packaging/icons from git" in text
    assert "PRODUCT_SPEC §7.3" in text
    assert "no VSCode-linux-* under editor/vscodium" in text
    assert "PM_STAGE_MAP.md" in text
    assert "H1 vs §7.3 .deb bundles" in text
    assert "find not on PATH" in text
    assert "basename not on PATH" in text
    assert "rm not on PATH" in text
    assert "mkdir not on PATH" in text
    assert "cp not on PATH" in text
    assert "ln not on PATH" in text
    assert "install not on PATH" in text
    assert "linuxIconName" in text
    assert "brand-assets.md" in text
    assert "product-branding-merge.json" in text
    assert "ln -sfn" in text
    assert "usr/share/applications/le-vibe.desktop" in text
    assert "resources/app/product.json" in text
    assert "LEVIBE_STAGE_IDE_ASSERT_BRAND" in text
    assert "LEVIBE_STAGE_IDE_VERBOSE" in text
    assert "usage()" in text
    assert "--help" in text
    assert "Partial VSCode-linux tree" in text
    assert "verify-step14-closeout.sh" in text
    assert "preflight-step14-closeout.sh" in text
    assert "print-vsbuild-codium-path.sh" in text
    assert "ci-vscodium-linux-dev-build.sh" in text
    assert "stage-le-vibe-ide-deb: staged" in text
    assert "desktop-file-validate" in text
    subprocess.run(["bash", "-n", str(script)], check=True, capture_output=True)


def test_build_le_vibe_ide_deb_script_header_documents_h1_vs_ci_step14():
    """STEP 14: IDE .deb script header states out-of-band vs ci.yml le-vibe-deb."""
    root = _repo_root()
    text = (root / "packaging" / "scripts" / "build-le-vibe-ide-deb.sh").read_text(encoding="utf-8")
    assert "0 → 1 → 14 → 2–13 → 15–17" in text
    assert "PROMPT_BUILD_LE_VIBE.md" in text
    assert "PM_STAGE_MAP.md" in text
    assert "le-vibe-deb" in text
    assert "apt-repo-releases.md" in text
    assert "build-le-vibe-debs.sh --with-ide" in text
    assert "Full-product install" in text
    assert "PM_DEB_BUILD_ITERATION.md" in text
    assert "Success output (--with-ide)" in text
    assert "test_packaging_le_vibe_ide_deb_contract.py" in text
    assert "test_verify_step14_closeout_contract.py" in text
    assert ".pytest-verify-step14-contract.lock" in text


def test_build_le_vibe_ide_deb_script_documents_14b_and_bash_syntax():
    root = _repo_root()
    script = root / "packaging" / "scripts" / "build-le-vibe-ide-deb.sh"
    text = script.read_text(encoding="utf-8")
    assert "LEVIBE_STAGE_IDE_ASSERT_BRAND" in text
    assert "LEVIBE_STAGE_IDE_VERBOSE" in text
    assert "LEVIBE_EDITOR_GATE_ASSERT_BRAND" in text
    assert "ci-editor-gate.sh" in text
    assert "usage()" in text
    assert "--help" in text
    assert "LEVIBE_IDE_LINTIAN_STRICT" in text
    assert "git submodule update --init editor/vscodium" in text
    assert "Fresh clone (14.b)" in text
    assert "stage-le-vibe-ide-deb.sh" in text
    assert "Partial tree" in text
    assert "Partial VSCode-linux tree" in text
    assert "print-built-codium-path.sh" in text
    assert "print-vsbuild-codium-path.sh" in text
    assert "print-github-linux-compile-artifact-hint.sh" in text
    assert "trigger-le-vibe-ide-linux-compile.sh" in text
    assert "download-vscodium-linux-compile-artifact.sh" in text
    assert "install-vscodium-linux-tarball-to-editor-vendor.sh" in text
    assert "verify-step14-closeout.sh" in text
    assert "preflight-step14-closeout.sh" in text
    assert "expected packaging/le-vibe-ide_*.deb" in text
    assert "PM_STAGE_MAP.md" in text
    assert "H1 vs §7.3 .deb bundles" in text
    assert "dpkg-buildpackage not on PATH" in text
    assert "lintian" in text
    assert "LEVIBE_IDE_LINTIAN_STRICT" in text
    assert "ci-qa-hardening.md" in text
    assert "desktop-file-validate" in text
    assert "usr/share/applications/le-vibe.desktop" in text
    subprocess.run(["bash", "-n", str(script)], check=True, capture_output=True)


def test_debian_le_vibe_ide_control_and_scripts():
    root = _repo_root()
    control = (root / "packaging" / "debian-le-vibe-ide" / "debian" / "control").read_text(encoding="utf-8")
    assert "Package: le-vibe-ide" in control
    assert "Depends:" in control and "le-vibe" in control
    assert "/usr/lib/le-vibe/bin/codium" in control
    assert "le-vibe.desktop" in control
    assert "hicolor-icon-theme" in control
    assert "roadmap" in control.lower() and "§7.3" in control
    assert (root / "packaging" / "scripts" / "stage-le-vibe-ide-deb.sh").is_file()
    assert (root / "packaging" / "scripts" / "build-le-vibe-ide-deb.sh").is_file()
    readme = (root / "packaging" / "debian-le-vibe-ide" / "README.md").read_text(encoding="utf-8")
    assert "0 → 1 → 14 → 2–13 → 15–17" in readme
    assert "PROMPT_BUILD_LE_VIBE.md" in readme
    assert "Rolling iteration — prefer continuation" in readme
    assert "git submodule update --init editor/vscodium" in readme
    assert "Fresh clone (14.b)" in readme
    assert "Compile fail-fast (STEP 14" in readme
    assert "ci-vscodium-bash-syntax.sh" in readme
    assert "ci-editor-nvmrc-sync.sh" in readme
    assert "workbench-icon" in readme
    assert "code-icon.svg" in readme
    assert "§7.3" in readme
    assert "/usr/lib/le-vibe/bin/codium" in readme
    assert "lvibe" in readme
    assert "VSCode-linux-" in readme
    assert "Partial VSCode-linux tree" in readme
    assert "print-built-codium-path.sh" in readme
    assert "install-vscodium-linux-tarball-to-editor-vendor.sh" in readme
    assert "print-github-linux-compile-artifact-hint.sh" in readme
    assert "trigger-le-vibe-ide-linux-compile.sh" in readme
    assert "download-vscodium-linux-compile-artifact.sh" in readme
    assert "print-vsbuild-codium-path.sh" in readme
    assert "print-step14-vscode-linux-bin-files.sh" in readme
    assert "vscode_linux_bin_files" in readme
    assert "build-le-vibe-ide-deb.sh --help" in readme
    assert "Incomplete Linux build" in readme
    assert "dev/build.sh" in readme
    assert "stage-le-vibe-ide-deb.sh" in readme
    assert "build-le-vibe-ide-deb.sh" in readme
    assert "applications" in readme.lower()
    assert "roadmap" in readme.lower() and "apt-repo-releases" in readme
    assert "build-le-vibe-debs.sh --with-ide" in readme
    assert "LEVIBE_EDITOR_GATE_ASSERT_BRAND" in readme
    assert "ci-editor-gate.sh" in readme
    assert "Full-product install" in readme
    assert "Success output (`--with-ide`)" in readme
    assert "verify-step14-closeout.sh --require-stack-deb" in readme
    assert "preflight-step14-closeout.sh" in readme
    assert "ide-prereqs --print-closeout-commands" in readme
    assert "--json" in readme
    assert "apt_sim_note" in readme
    assert "desktop_file_validate" in readme
    assert "hicolor_icon_in_deb" in readme
    assert "desktop_file_validate_on_path" in readme
    assert "PM_DEB_BUILD_ITERATION.md" in readme
    assert "SHA256SUMS" in readme
    assert "PM_STAGE_MAP.md" in readme
    assert "H1 vs §7.3 .deb bundles" in readme
    assert "LEVIBE_STAGE_IDE_ASSERT_BRAND" in readme
    assert "LEVIBE_STAGE_IDE_VERBOSE" in readme
    assert "LEVIBE_EDITOR_GATE_ASSERT_BRAND" in readme
    assert "ci-editor-gate.sh" in readme
    assert "resources/app/product.json" in readme
    assert "spec-phase2.md" in readme
    assert "CI `le-vibe-deb` vs maintainer `le-vibe-ide`" in readme
    assert "## Install both packages" in readme
    assert "sudo apt install ./le-vibe_" in readme
    assert "/usr/share/doc/le-vibe/README.Debian" in readme
    assert "manual-step14-install-smoke.sh" in readme
    assert "--verify-only" in readme
    assert "desktop-file-validate" in readme
    assert "build machine" in readme
    assert "printed steps" in readme
    assert "repo root" in readme
    assert "default **`STACK_DEB`**" in readme
    assert "resolve-latest-le-vibe-stack-deb.sh" in readme
    desktop = (root / "packaging" / "debian-le-vibe-ide" / "debian" / "le-vibe.desktop").read_text(
        encoding="utf-8"
    )
    assert "Lé Vibe" in desktop
    assert "GenericName=" in desktop
    assert "Exec=/usr/bin/lvibe" in desktop
    assert "Icon=le-vibe" in desktop
    assert "Categories=Development;IDE;" in desktop
    assert "test_packaging_le_vibe_ide_deb_contract.py" in desktop
    assert "test_verify_step14_closeout_contract.py" in desktop
    assert ".pytest-verify-step14-contract.lock" in desktop
    install = (root / "packaging" / "debian-le-vibe-ide" / "debian" / "le-vibe-ide.install").read_text(
        encoding="utf-8"
    )
    assert "usr/share/applications/le-vibe.desktop" in install
    assert "le-vibe.svg" in install
    # PRODUCT_SPEC §7.3 — only `lvibe` as public PATH CLI; IDE .deb uses Freedesktop + /usr/lib/le-vibe/bin/codium.
    assert "usr/bin" not in install
    rules = (root / "packaging" / "debian-le-vibe-ide" / "debian" / "rules").read_text(encoding="utf-8")
    assert "staging/usr/share/applications/le-vibe.desktop" in rules
    assert "override_dh_install" in rules
    assert "dh_install --sourcedir=staging" in rules
    assert "override_dh_dwz" in rules
    assert "override_dh_strip" in rules
