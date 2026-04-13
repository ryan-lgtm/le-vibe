"""Contract: spec-phase2.md §14 table + honesty paragraph stay aligned with STEP 14 (14.j)."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_spec_phase2_monorepo_table_h6_row_lists_14d_branding_staging():
    """§1 monorepo table — H6 row stays honest about smoke vs branding (14.d)."""
    text = (_repo_root() / "spec-phase2.md").read_text(encoding="utf-8")
    assert "| **Lé Vibe IDE** (H6)" in text
    assert "editor/le-vibe-overrides/branding-staging.checklist.md" in text
    assert "fast smoke" in text


def test_spec_phase2_monorepo_lists_ci_le_vibe_deb_vs_le_vibe_ide_step14():
    """§14 honesty: spec-phase2 names stack CI artifact vs sibling IDE .deb (H1 / §7.3)."""
    text = (_repo_root() / "spec-phase2.md").read_text(encoding="utf-8")
    assert "CI `le-vibe-deb` vs maintainer `le-vibe-ide` (H1 / §7.3)" in text
    assert "build-le-vibe-debs.sh --with-ide" in text
    assert "apt-repo-releases.md" in text
    assert "IDE package" in text
    assert "PM_STAGE_MAP.md" in text
    assert "H1 vs §7.3 .deb bundles" in text
    assert "Full-product install" in text
    assert "PM_DEB_BUILD_ITERATION.md" in text
    assert "Success output (`--with-ide`)" in text
    assert "debian-le-vibe-ide/README.md" in text
    assert "Install both packages" in text
    assert "Maintainer build output" in text
    assert "probe-vscode-linux-build.sh" in text
    assert "dpkg-buildpackage" in text
    assert "Failure (`--with-ide`)" in text
    assert "Fail-fast (`build-le-vibe-debs.sh --with-ide`)" in text


def test_spec_phase2_section14_ide_row_honesty_strings():
    text = (_repo_root() / "spec-phase2.md").read_text(encoding="utf-8")
    assert "§7.3" in text
    assert "## 14." in text or "§14" in text
    assert "STEP 14.j" in text
    assert "linux_compile" in text
    assert "ci-vscodium-bash-syntax.sh" in text
    assert "ci-editor-nvmrc-sync.sh" in text
    assert "fail fast" in text
    assert "retention-days: 14" in text
    assert "linux_compile-cargo" in text
    assert "actions/cache@v4" in text
    assert ".cargo/registry" in text
    assert "vscodium-linux-build.tar.gz" in text
    assert "14.j" in text
    assert "test_spec_phase2_section14_snapshot_contract.py" in text
    assert "test_editor_build_md_contract.py" in text
    assert "test_continue_extension_pin_doc_step14_contract.py" in text
    assert "test_vscodium_fork_le_vibe_branding_contract.py" in text
    assert "release smoke **1b** + **1c**" in text
    assert "CHANGELOG.md" in text
    assert "[Unreleased]" in text
    assert "test_launcher_default_editor.py" in text
    assert "test_debian_readme_launcher_order_14g_contract.py" in text
    assert "/usr/lib/le-vibe/bin/codium" in text
    assert "build-env.sh.example" in text
    assert "test_build_env_example_step14_contract.py" in text
    assert "workflow_call" in text
    assert "fetch-vscode-sources.sh" in text
    assert "test_vscodium_howto_build_get_repo_14b_contract.py" in text
    assert "editor/vscodium/docs/howto-build.md" in text
    assert "smoke-built-codium-lvibe.sh" in text
    assert "verify-14c-local-binary.sh" in text
    assert "use-node-toolchain.sh" in text
    assert "print-ci-tarball-codium-path.sh" in text
    assert ".zip" in text
    assert "Artifact download" in text
    assert "test_print_paths_14f_contract.py" in text
    assert "unzip first" in text
    assert "print-vsbuild-codium-path.sh" in text
    assert "14.a–14.j" in text
    assert "Queue advance (honest)" in text
    assert "test_pm_stage_map_step2_contract.py" in text
    assert "test_pm_stage_map_step14_contract.py" in text
    assert "test_pm_stage_map_queue_advance_honest_step14_vs_rest" in text
    assert "docs/ci-qa-hardening.md" in text
    assert "test_ci_qa_hardening_doc_h3_contract.py" in text
    assert "test_le_vibe_readme_e1_contract.py" in text
    assert "test_docs_readme_ci_qa_hardening_row_contract.py" in text
    assert "test_pm_stage_map_step10_contract.py" in text
    assert "test_editor_readme_step14_contract.py" in text
    assert "test_editor_vendoring_md_contract.py" in text
    assert "Vendoring upstream" in text
    assert "test_editor_build_md_contract_vendoring_pointer" in text
    assert "branding-staging.checklist.md" in text
    assert "test_branding_staging_checklist_14d_contract" in text
    assert "14.c vs 14.d" in text
    assert "IDE smoke" in text and "test_ci_qa_hardening_doc_h3_contract.py" in text
    assert "test_root_readme_ci_section_linux_compile_fail_fast_14e" in text
    assert "LEVIBE_SKIP_NODE_VERSION_CHECK" in text
    assert "test_ci_vscodium_linux_dev_build_overrides_contract.py" in text
    assert "SESSION_ORCHESTRATION_SPEC.md" in text
    assert "test_session_orchestration_spec_phase2_paragraph_lists_linux_compile_tarball" in text
