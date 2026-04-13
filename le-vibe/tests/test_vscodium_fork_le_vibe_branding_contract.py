"""Contract: docs/vscodium-fork-le-vibe.md keeps §7.2 branding + overrides pointers (STEP 14.d)."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_vscodium_fork_doc_bootstrap_lists_production_deb_pair_step14():
    """STEP 14 / §7.3: H6 policy doc opens with stack + IDE .deb build path."""
    text = (_repo_root() / "docs" / "vscodium-fork-le-vibe.md").read_text(encoding="utf-8")
    assert "build-le-vibe-debs.sh --with-ide" in text
    assert "PM_DEB_BUILD_ITERATION.md" in text
    assert "apt-repo-releases.md" in text
    assert "le-vibe-ide_*_amd64.deb" in text
    assert "SHA256SUMS" in text
    assert "le-vibe-deb" in text
    assert "PM_STAGE_MAP.md" in text
    assert "H1 vs §7.3 .deb bundles" in text
    assert "Full-product install" in text
    assert "Success output (`--with-ide`)" in text
    assert "verify-step14-closeout.sh --require-stack-deb" in text
    assert "Install both packages" in text
    assert "Maintainer build output" in text


def test_vscodium_fork_doc_branding_section_honesty_and_overrides():
    text = (_repo_root() / "docs" / "vscodium-fork-le-vibe.md").read_text(encoding="utf-8")
    assert "git submodule update --init editor/vscodium" in text
    assert "Fresh clone (14.b)" in text
    assert "read before overrides" in text
    assert "Branding & overrides" in text
    assert "VENDORING.md" in text
    assert "14.d" in text
    assert "§7.2" in text
    assert "§7.3" in text
    assert "sync-linux-icon-assets.sh" in text
    assert "build-env.lvibe-defaults.sh" in text
    assert "editor/le-vibe-overrides/README.md" in text
    assert "branding-staging.checklist.md" in text
    assert "Upstream touchpoints (14.d)" in text
    assert "src/stable/resources/linux" in text
    assert "spec-phase2.md" in text and "§14" in text
    assert "USER RESPONSE REQUIRED" in text
    assert "CHANGELOG.md" in text
    assert "14.f" in text
    assert "editor/BUILD.md" in text
    assert "VSCode-linux-" in text
    assert "vscodium-linux-build.tar.gz" in text
    assert "14.g" in text
    assert "le-vibe.README.Debian" in text
    assert "build-env.sh.example" in text
    assert "ci-vscodium-linux-dev-build.sh" in text
    assert "ci-vscodium-bash-syntax.sh" in text
    assert "ci-editor-nvmrc-sync.sh" in text
    assert "LEVIBE_SKIP_NODE_VERSION_CHECK" in text
    assert "fail fast" in text
    assert "fetch-vscode-sources.sh" in text
    assert "print-built-codium-path.sh" in text
    assert "verify-14c-local-binary.sh" in text
    assert "smoke-built-codium-lvibe.sh" in text
    assert "smoke-lvibe-editor.sh" in text
    assert "test_launcher_default_editor.py" in text
    assert "brand-assets.md" in text


def test_vscodium_fork_doc_installable_tree_14f():
    text = (_repo_root() / "docs" / "vscodium-fork-le-vibe.md").read_text(encoding="utf-8")
    assert "Tarball / installable tree (14.f)" in text
    assert "VSCode-linux-" in text and "bin/codium" in text
    assert "vscodium-linux-build.tar.gz" in text
    assert "linux_compile" in text
    assert "Installable layout" in text
    assert "print-ci-tarball-codium-path.sh" in text


def test_vscodium_fork_doc_release_smoke_checklist_14i():
    text = (_repo_root() / "docs" / "vscodium-fork-le-vibe.md").read_text(encoding="utf-8")
    assert "Release smoke checklist (14.i)" in text
    assert "14.i" in text
    assert "PM_STAGE_MAP.md" in text
    assert "STEP **10**" in text
    assert "STEP **14**" in text
    assert "§14 honesty gate" in text
    assert "test_spec_phase2_section14_snapshot_contract.py" in text
    assert "use-node-toolchain.sh" in text
    assert "verify-14c-local-binary.sh" in text
    assert "smoke-built-codium-lvibe.sh" in text
    assert "./editor/smoke.sh" in text
    assert "smoke-lvibe-editor.sh" in text
    assert "verify-continue-pin.sh" in text
    assert "vscodium_linux_compile" in text
    assert "le-vibe-setup-continue" in text
    assert "11435" in text
    assert "python3 -m pytest tests/" in text
    assert "dpkg-buildpackage" in text
    assert "debian/changelog" in text
    assert "vscodium-linux-build.tar.gz" in text
    assert "continue-config.yaml" in text
    assert "continue-extension-pin.md" in text
    assert "ci-editor-gate" in text
    assert "layout=vscodium" in text
    assert "build-linux.yml" in text
    assert "workflow_call" in text
    assert "test_build_env_example_step14_contract.py" in text
    assert "test_branding_staging_checklist_14d_contract" in text
    assert "branding-staging.checklist.md" in text
    assert "Compile hook + branding staging" in text
    assert "**1c." in text
    assert "test_docs_readme_ci_qa_hardening_row_contract.py" in text
    assert "print-ci-tarball-codium-path.sh" in text
    assert "print-vsbuild-codium-path.sh" in text
    assert "print-built-codium-path.sh" in text
    assert "fetch-vscode-sources.sh" in text
    assert "Optional preflight" in text
    assert "1 → 9" in text
    assert ".zip" in text
    assert "test_print_paths_14f_contract.py" in text
    assert "exit code **`2`**" in text
