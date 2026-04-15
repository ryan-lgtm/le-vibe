"""Root README must retain §7.1 Please continue / AI Pilot UX copy (PRODUCT_SPEC, STEP 17) and E1 Tests roster (STEP 2 session orchestrator + H8 issue-template contracts)."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    # le-vibe/tests/this_file.py -> parents[2] == monorepo root
    return Path(__file__).resolve().parents[2]


def test_root_readme_feedback_row_submodule_init_fallback_14b():
    """STEP 14 / 14.b: top-level README names plain-clone submodule recovery."""
    text = (_repo_root() / "docs" / "MONOREPO_DEVELOPER_REFERENCE.md").read_text(encoding="utf-8")
    assert "git submodule update --init editor/vscodium" in text
    assert "recurse-submodules" in text
    assert "Fresh clone (14.b)" in text


def test_root_readme_releases_h1_lists_stack_artifact_vs_ide_deb_step14():
    """H1: root README distinguishes CI le-vibe-deb (stack) from optional le-vibe-ide (§7.3)."""
    text = (_repo_root() / "docs" / "MONOREPO_DEVELOPER_REFERENCE.md").read_text(encoding="utf-8")
    assert "Releases & apt (Roadmap H1)" in text
    assert "le-vibe-deb" in text
    assert "Full product (STEP 14 / §7.3)" in text
    assert "le-vibe-ide_*_amd64.deb" in text
    assert "IDE package" in text
    assert "PM_STAGE_MAP.md" in text
    assert "H1 vs §7.3 .deb bundles" in text


def test_root_readme_prioritization_demoinstall_apt_install_both_debs_step14():
    """STEP 14: landing README copies apt install both .debs next to IDE README pointer."""
    text = (_repo_root() / "docs" / "MONOREPO_DEVELOPER_REFERENCE.md").read_text(encoding="utf-8")
    assert "sudo apt install ./le-vibe_*_all.deb ./le-vibe-ide_*_amd64.deb" in text
    assert "Install both packages" in text
    assert "packaging/debian-le-vibe-ide/README.md" in text
    assert "verify-step14-closeout.sh --require-stack-deb" in text
    assert "--json" in text
    assert "apt_sim_note" in text
    assert "desktop_file_validate" in text
    assert "desktop_file_validate_on_path" in text
    assert "build machine" in text
    assert "test host" in text
    assert "manual-step14-install-smoke.sh" in text
    assert "--verify-only" in text
    assert "desktop-file-validate" in text


def test_root_readme_current_status_works_well_today_full_product_install_step14():
    """STEP 14: *Current status* table names Full-product install stdout + PM deb doc."""
    text = (_repo_root() / "docs" / "MONOREPO_DEVELOPER_REFERENCE.md").read_text(encoding="utf-8")
    assert "**Works well today**" in text
    assert "build-le-vibe-debs.sh --with-ide" in text
    assert "Full-product install" in text
    assert "PM_DEB_BUILD_ITERATION.md" in text
    assert "Success output (`--with-ide`)" in text
    assert "verify-step14-closeout.sh --require-stack-deb" in text
    assert "print-closeout-commands" in text
    assert "probe-vscode-linux-build.sh" in text
    assert "preflight-step14-closeout.sh" in text
    assert "le-vibe/README.md" in text
    assert "--json" in text
    assert "apt_sim_note" in text
    assert "desktop_file_validate" in text
    assert "vscode_linux_build" in text
    assert "ide-prereqs --json" in text
    assert "build machine" in text
    assert "test host" in text
    assert "Compile fail-fast" in text
    assert "packaging/scripts/ci-vscodium-bash-syntax.sh" in text
    assert "packaging/scripts/ci-editor-nvmrc-sync.sh" in text
    assert "packaging/scripts/ci-vscodium-linux-dev-build.sh" in text
    assert "linux_compile" in text
    assert "Partial VSCode-linux triage" in text
    assert "print-vsbuild-codium-path" in text
    assert "print-step14-vscode-linux-bin-files.sh" in text
    assert "vscode_linux_bin_files" in text
    assert "build-le-vibe-ide-deb.sh --help" in text
    assert "print-github-linux-compile-artifact-hint.sh" in text
    assert "trigger-le-vibe-ide-linux-compile.sh" in text
    assert "download-vscodium-linux-compile-artifact.sh" in text
    assert "install-vscodium-linux-tarball-to-editor-vendor.sh" in text


def test_root_readme_pm_session_section_labels_master_step2():
    """STEP 2: landing README names PM session manifest + queue order + orchestration spec."""
    text = (_repo_root() / "docs" / "MONOREPO_DEVELOPER_REFERENCE.md").read_text(encoding="utf-8")
    assert "### PM session manifest — STEP 2" in text
    assert "0 → 1 → 14 → 2" in text
    assert "iter_tasks_in_epic_order" in text
    assert "session_manifest_example_source_path" in text
    assert "apply-opening-skip" in text


def test_root_readme_continue_section_labels_step3_e2():
    """STEP 3 / E2: landing README names Continue rules + primary .lvibe/ memory path."""
    text = (_repo_root() / "docs" / "MONOREPO_DEVELOPER_REFERENCE.md").read_text(encoding="utf-8")
    assert "### Continue workspace rules — STEP 3 / E2" in text
    assert "Master orchestrator STEP 3" in text
    assert "00-le-vibe-lvibe-memory.md" in text
    assert "continue-rules" in text
    assert "sync-lvibe-agent-skills.sh" in text
    assert "le_vibe.continue_workspace" in text


def test_root_readme_welcome_section_labels_step4_e3():
    """STEP 4 / E3: §4 in-editor welcome surfaces (WELCOME.md, Continue rule 01, lvibe welcome)."""
    text = (_repo_root() / "docs" / "MONOREPO_DEVELOPER_REFERENCE.md").read_text(encoding="utf-8")
    assert "### In-editor welcome — STEP 4 / E3" in text
    assert "Master orchestrator STEP 4" in text
    assert "01-le-vibe-product-welcome.md" in text
    assert "lvibe open-welcome" in text
    assert "test_editor_welcome.py" in text


def test_root_readme_hygiene_section_labels_step5_e4():
    """STEP 5 / E4: lvibe-hygiene manifest + session-manifest + chunk/rag path checks."""
    text = (_repo_root() / "docs" / "MONOREPO_DEVELOPER_REFERENCE.md").read_text(encoding="utf-8")
    assert "### Maintainer hygiene — STEP 5 / E4" in text
    assert "Master orchestrator STEP 5" in text
    assert "--seed-missing" in text
    assert "--json" in text
    assert "storage-state.json" in text
    assert "test_hygiene.py" in text


def test_root_readme_documents_ai_pilot_and_user_gate():
    text = (_repo_root() / "docs" / "MONOREPO_DEVELOPER_REFERENCE.md").read_text(encoding="utf-8")
    assert "Lé Vibe" in text
    assert "Please continue" in text
    assert "AI Pilot" in text
    assert "USER RESPONSE REQUIRED" in text
    assert "AI_PILOT_AND_CONTINUE.md" in text
    assert "PM_STAGE_MAP.md" in text


def test_root_readme_tests_section_cites_issue_template_h8_contract():
    """E1 / §10: *Tests* / **E1 mapping** must keep **H8** **`test_issue_template_h8_contract.py`** (STEP 12)."""
    text = (_repo_root() / "docs" / "MONOREPO_DEVELOPER_REFERENCE.md").read_text(encoding="utf-8")
    assert "test_issue_template_h8_contract.py" in text
    assert "PRODUCT_SPEC_SECTION8_EVIDENCE.md" in text


def test_root_readme_tests_section_cites_session_orchestrator_contract():
    """E1 / STEP 2: *E1 mapping* must cite **`test_session_orchestrator.py`** (bundled example ↔ schema; PM manifests)."""
    text = (_repo_root() / "docs" / "MONOREPO_DEVELOPER_REFERENCE.md").read_text(encoding="utf-8")
    assert "test_session_orchestrator.py" in text


def test_root_readme_tests_section_cites_session_orchestration_spec_step2_contract():
    """E1 / STEP 2: *E1 mapping* must cite doc-lock **`test_session_orchestration_spec_step2_contract.py`**."""
    text = (_repo_root() / "docs" / "MONOREPO_DEVELOPER_REFERENCE.md").read_text(encoding="utf-8")
    assert "test_session_orchestration_spec_step2_contract.py" in text


def test_root_readme_e1_mapping_cites_le_vibe_readme_contract():
    """*Tests* / **E1 mapping** must cite **`test_le_vibe_readme_e1_contract.py`** (package README roster alignment)."""
    text = (_repo_root() / "docs" / "MONOREPO_DEVELOPER_REFERENCE.md").read_text(encoding="utf-8")
    assert "test_le_vibe_readme_e1_contract.py" in text


def test_root_readme_e1_mapping_prioritization_lists_linux_compile_tarball():
    """§ *Prioritization* roster — **`PRODUCT_SPEC`** / SECTION8 evidence parity (**14.e / 14.f**)."""
    text = (_repo_root() / "docs" / "MONOREPO_DEVELOPER_REFERENCE.md").read_text(encoding="utf-8")
    assert "*Prioritization*" in text
    assert "linux_compile" in text
    assert "ci-vscodium-bash-syntax.sh" in text
    assert "ci-vscodium-linux-dev-build.sh" in text
    assert "LEVIBE_SKIP_NODE_VERSION_CHECK" in text
    assert "fail fast" in text
    assert "vscodium-linux-build.tar.gz" in text


def test_root_readme_e1_mapping_cites_editor_build_md_and_spec_phase2_section14_contracts():
    """STEP 14 / 14.j: *E1 mapping* cites **`editor/BUILD.md`**, **`editor/README.md`**, and **`spec-phase2.md` §14** snapshot tests."""
    text = (_repo_root() / "docs" / "MONOREPO_DEVELOPER_REFERENCE.md").read_text(encoding="utf-8")
    assert "test_editor_build_md_contract.py" in text
    assert "test_editor_readme_step14_contract.py" in text
    assert "test_spec_phase2_section14_snapshot_contract.py" in text
    assert "Vendoring upstream" in text


def test_root_readme_e1_mapping_cites_ci_qa_hardening_ide_smoke_contract():
    """STEP 10 / 14.e / 14.f: *E1 mapping* cites **`test_ci_qa_hardening_doc_h3_contract.py`** (H3 IDE smoke doc)."""
    text = (_repo_root() / "docs" / "MONOREPO_DEVELOPER_REFERENCE.md").read_text(encoding="utf-8")
    assert "test_ci_qa_hardening_doc_h3_contract.py" in text
    assert "ci-qa-hardening.md" in text


def test_root_readme_ci_section_14d_branding_honesty():
    """STEP 14.d: CI § distinguishes fast smoke from shipped Lé Vibe branding."""
    text = (_repo_root() / "docs" / "MONOREPO_DEVELOPER_REFERENCE.md").read_text(encoding="utf-8")
    assert "Honesty (14.d)" in text
    assert "editor/smoke.sh --help" in text
    assert "ci-editor-gate" in text
    assert "branding-staging.checklist.md" in text
    assert "read before overrides" in text
    assert "14.c vs 14.d" in text


def test_root_readme_ci_section_linux_compile_fail_fast_14e():
    """STEP 14.e: root README documents linux_compile fail-fast gates before dev/build."""
    text = (_repo_root() / "docs" / "MONOREPO_DEVELOPER_REFERENCE.md").read_text(encoding="utf-8")
    assert "Lé Vibe IDE (Roadmap H6, STEP 14)" in text
    assert "linux_compile" in text
    assert "ci-vscodium-bash-syntax.sh" in text
    assert "ci-editor-nvmrc-sync.sh" in text
    assert "ci-vscodium-linux-dev-build.sh" in text
    assert "node --version" in text
    assert "LEVIBE_SKIP_NODE_VERSION_CHECK" in text
    assert "fail fast" in text
    assert "editor/BUILD.md" in text
