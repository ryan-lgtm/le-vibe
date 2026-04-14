"""Contract: docs/PM_STAGE_MAP.md STEP 14 row keeps H6 IDE CI + build-linux alias (E1 roster)."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _step14_table_row(text: str) -> str:
    rows = [ln for ln in text.splitlines() if ln.lstrip().startswith("| **14 — H6 IDE**")]
    assert len(rows) == 1, f"expected single STEP 14 table row, got {len(rows)}"
    return rows[0]


def test_pm_stage_map_step14_lists_ide_workflows_smoke_and_e1_test_build():
    text = (_repo_root() / "docs" / "PM_STAGE_MAP.md").read_text(encoding="utf-8")
    row = _step14_table_row(text)
    assert "build-le-vibe-ide.yml" in row
    assert "build-linux.yml" in row
    assert "test_build_le_vibe_ide_workflow_contract.py" in row
    assert "linux_compile" in row
    assert "ci-vscodium-bash-syntax.sh" in row
    assert "ci-editor-nvmrc-sync.sh" in row
    assert "ci-vscodium-linux-dev-build.sh" in row
    assert "LEVIBE_SKIP_NODE_VERSION_CHECK" in row
    assert "fail fast" in row
    assert "vscodium-linux-build.tar.gz" in row
    assert "le_vibe_editor_docs" in row
    assert "LE_VIBE_EDITOR" in row
    assert "ide-ci-metadata" in row
    assert "./editor/smoke.sh" in row
    assert "editor/smoke.sh --help" in row
    assert "14.g" in row
    assert "test_launcher_default_editor.py" in row
    assert "test_editor_readme_launcher_order_14g_contract.py" in row
    assert "test_debian_readme_launcher_order_14g_contract.py" in row
    assert "test_editor_build_md_contract.py" in row
    assert "test_spec_phase2_section14_snapshot_contract.py" in row
    assert "test_editor_readme_step14_contract.py" in row
    assert "test_editor_vendoring_md_contract.py" in row
    assert "preflight-step14-closeout.sh" in row
    assert "ide-prereqs --print-closeout-commands" in row
    assert "debian/lvibe.1" in row
    assert "print-ci-tarball-codium-path.sh" in row
    assert "print-step14-vscode-linux-bin-files.sh" in row
    assert "print-github-linux-compile-artifact-hint.sh" in row
    assert "trigger-le-vibe-ide-linux-compile.sh" in row
    assert "download-vscodium-linux-compile-artifact.sh" in row
    assert "install-vscodium-linux-tarball-to-editor-vendor.sh" in row
    assert "verify-step14-closeout.sh" in row
    assert "--require-stack-deb" in row
    assert "test_verify_step14_closeout_contract.py" in row


def test_pm_stage_map_lists_h1_vs_ide_deb_bundles_step14():
    """STEP 14: PM map names ci.yml le-vibe-deb (stack) vs maintainer le-vibe-ide (§7.3)."""
    text = (_repo_root() / "docs" / "PM_STAGE_MAP.md").read_text(encoding="utf-8")
    assert "H1 vs §7.3 .deb bundles" in text
    assert "le-vibe-deb" in text
    assert "apt-repo-releases.md" in text
    assert "CI `le-vibe-deb` vs maintainer `le-vibe-ide`" in text
    assert "Compile fail-fast (STEP 14, before IDE `.deb`)" in text
    assert "packaging/scripts/ci-vscodium-bash-syntax.sh" in text
    assert "packaging/scripts/ci-editor-nvmrc-sync.sh" in text
    assert "packaging/scripts/ci-vscodium-linux-dev-build.sh" in text
    assert "./editor/smoke.sh" in text
    assert "linux_compile" in text
    assert "build-le-vibe-debs.sh" in text and "--with-ide" in text
    assert "probe-vscode-linux-build.sh" in text or "vscode_linux_build" in text
    assert "dpkg-buildpackage" in text
    assert "Failure (`--with-ide`)" in text
    assert "Full-product install" in text
    assert "PM_DEB_BUILD_ITERATION.md" in text
    assert "Success output (`--with-ide`)" in text
    assert "debian-le-vibe-ide/README.md" in text
    assert "Install both packages" in text
    assert "Maintainer build output" in text


def test_pm_stage_map_notes_step14_fine_grain_closure_and_remaining_gap():
    text = (_repo_root() / "docs" / "PM_STAGE_MAP.md").read_text(encoding="utf-8")
    assert "14.a" in text and "14.j" in text
    assert "CHANGELOG.md" in text
    assert "spec-phase2.md" in text
    assert "linux_compile" in text
    assert ".zip" in text
    assert "test_spec_phase2_section14_snapshot_contract.py" in text
    assert "branding-staging.checklist.md" in text
    assert "ci-editor-gate" in text
    assert "git -C editor/vscodium checkout" in text
    assert "test_editor_build_md_vscodium_submodule_restore_after_prepare_step14" in text
