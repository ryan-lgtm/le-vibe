"""Package README must list the same E1 contract highlights as the repository README (Track D)."""

from __future__ import annotations

from pathlib import Path


def _le_vibe_dir() -> Path:
    # le-vibe/tests/this_file.py -> parents[1] == le-vibe package root
    return Path(__file__).resolve().parents[1]


def test_le_vibe_readme_production_install_step14_lists_ide_deb_path():
    """STEP 14 / §7.3: package README names IDE .deb build + one-shot stack+IDE script."""
    text = (_le_vibe_dir() / "README.md").read_text(encoding="utf-8")
    assert "Production install (STEP 14 / §7.3)" in text
    assert "ide-prereqs" in text
    assert "build-le-vibe-ide-deb.sh" in text
    assert "packaging/debian-le-vibe-ide/README.md" in text
    assert "build-le-vibe-debs.sh" in text
    assert "--with-ide" in text
    assert "Full-product install" in text
    assert "Success output (`--with-ide`)" in text
    assert "PM_DEB_BUILD_ITERATION.md" in text
    assert "Maintainer build output" in text


def test_le_vibe_readme_h6_submodule_init_14b():
    """STEP 14 / 14.b: package README names submodule init for empty editor/vscodium/."""
    text = (_le_vibe_dir() / "README.md").read_text(encoding="utf-8")
    assert "git submodule update --init editor/vscodium" in text
    assert "Fresh clone (14.b)" in text


def test_le_vibe_readme_ide_smoke_help_forwards_ci_editor_gate_step14():
    """STEP 14: package README states ./editor/smoke.sh --help → ci-editor-gate usage."""
    text = (_le_vibe_dir() / "README.md").read_text(encoding="utf-8")
    assert "IDE shell (H6)" in text
    assert "editor/smoke.sh --help" in text
    assert "ci-editor-gate" in text
    assert "forwarded" in text.lower() or "forwards" in text.lower()


def test_le_vibe_readme_ide_honesty_14d_matches_root_readme():
    """STEP 14.d: package README states smoke ≠ Lé Vibe branding (parity with root README *CI*)."""
    text = (_le_vibe_dir() / "README.md").read_text(encoding="utf-8")
    assert "Honesty (14.d)" in text
    assert "branding-staging.checklist.md" in text
    assert "read before overrides" in text
    assert "14.c vs 14.d" in text


def test_le_vibe_readme_lists_step7_h4_continue_pin():
    text = (_le_vibe_dir() / "README.md").read_text(encoding="utf-8")
    assert "Continue / Open VSX pin (STEP 7 / H4)" in text
    assert "continue-openvsx-version" in text
    assert "continue-pin" in text
    assert "--path-only" in text
    assert "--json" in text
    assert "verify-continue-pin.sh" in text
    assert "continue-extension-pin.md" in text
    assert "install-continue-extension.sh" in text


def test_le_vibe_readme_lists_step8_h1_release_channel():
    text = (_le_vibe_dir() / "README.md").read_text(encoding="utf-8")
    assert "Release channel / checksums (STEP 8 / H1)" in text
    assert "verify-checksums" in text
    assert "apt-repo-releases.md" in text
    assert "le-vibe-deb" in text
    assert "SHA256SUMS" in text
    assert "debian/changelog" in text
    assert "CHANGELOG.md" in text


def test_le_vibe_readme_step8_h1_ties_full_product_to_step14_ide_deb():
    """H1 row links default CI artifact (stack) to STEP 14 le-vibe-ide for full demo releases."""
    text = (_le_vibe_dir() / "README.md").read_text(encoding="utf-8")
    assert "full product (STEP 14 / §7.3)" in text
    assert "le-vibe-ide_*_amd64.deb" in text
    assert "IDE package" in text
    assert "PM_STAGE_MAP.md" in text
    assert "H1 vs §7.3 .deb bundles" in text


def test_le_vibe_readme_lists_step9_h2_sbom():
    text = (_le_vibe_dir() / "README.md").read_text(encoding="utf-8")
    assert "Supply chain / SBOM (STEP 9 / H2)" in text
    assert "lvibe pip-audit" in text
    assert "sbom-signing-audit.md" in text
    assert "le-vibe-python.cdx.json" in text
    assert "pip-audit" in text
    assert "dependabot.yml" in text


def test_le_vibe_readme_lists_step10_h3_qa_ci():
    text = (_le_vibe_dir() / "README.md").read_text(encoding="utf-8")
    assert "QA CI (STEP 10 / H3)" in text
    assert "lvibe ci-smoke" in text
    assert "ci-editor-gate" in text
    assert "ci-qa-hardening.md" in text
    assert "ci-smoke.sh" in text
    assert "ci-editor-gate.sh" in text


def test_le_vibe_readme_lists_step11_h5_brand_assets():
    text = (_le_vibe_dir() / "README.md").read_text(encoding="utf-8")
    assert "Brand assets (STEP 11 / H5)" in text
    assert "brand-paths" in text
    assert "--path-only" in text
    assert "brand-assets.md" in text
    assert "packaging/icons/hicolor/scalable/apps/le-vibe.svg" in text


def test_le_vibe_readme_lists_step12_h8_product_surface():
    text = (_le_vibe_dir() / "README.md").read_text(encoding="utf-8")
    assert "Alternate bundles / H7 (STEP 13)" in text
    assert "flatpak-appimage" in text
    assert "Trust / H8 — product surface (STEP 12)" in text
    assert "product-surface" in text
    assert "ISSUE_TEMPLATE" in text
    assert "dependabot.yml" in text


def test_le_vibe_readme_lists_step13_h7_flatpak_appimage():
    text = (_le_vibe_dir() / "README.md").read_text(encoding="utf-8")
    assert "STEP 13 / H7" in text
    assert "flatpak-appimage.md" in text
    assert "org.le_vibe.Launcher.yml" in text
    assert "Flathub" in text


def test_le_vibe_readme_lists_step15_lvibe_governance():
    text = (_le_vibe_dir() / "README.md").read_text(encoding="utf-8")
    assert "`.lvibe/` governance (STEP 15)" in text
    assert "workspace_consent" in text
    assert "50 MB" in text
    assert "STEP **15**" in text


def test_le_vibe_readme_lists_step16_pm_map_orchestrator():
    text = (_le_vibe_dir() / "README.md").read_text(encoding="utf-8")
    assert "PM map & master orchestrator (STEP 16)" in text
    assert "PROMPT_BUILD_LE_VIBE.md" in text
    assert "print-master-orchestrator-prompt.py" in text
    assert "continue_construction_note" in text


def test_le_vibe_readme_lists_step17_ai_pilot_continue():
    text = (_le_vibe_dir() / "README.md").read_text(encoding="utf-8")
    assert "AI Pilot & Continue contracts (STEP 17)" in text
    assert "AI_PILOT_AND_CONTINUE.md" in text
    assert "continue_workspace" in text


def test_le_vibe_readme_lists_pm_ide_settings_contract_tests():
    text = (_le_vibe_dir() / "README.md").read_text(encoding="utf-8")
    assert "IDE settings / workflows (PM phase)" in text
    assert "test_pm_ide_settings_workflows_contract.py" in text
    assert "test_le_vibe_settings_extension_contract.py" in text


def test_le_vibe_readme_lists_core_e1_contract_modules():
    text = (_le_vibe_dir() / "README.md").read_text(encoding="utf-8")
    assert "Observability (STEP 6 / E5)" in text
    assert "le-vibe.log.jsonl" in text
    assert "lvibe logs" in text
    assert "logs --json" in text
    assert "--path-only" in text
    assert "Maintainer hygiene (STEP 5 / E4)" in text
    assert "lvibe hygiene" in text
    assert "le_vibe.hygiene" in text
    assert "storage-state.json" in text
    assert "--json" in text
    assert "--seed-missing" in text
    assert "Continue (STEP 3 / E2)" in text
    assert "continue-rules" in text
    assert "sync-agent-skills" in text
    assert "sync-lvibe-agent-skills.sh" in text
    assert "In-editor welcome (STEP 4 / E3)" in text
    assert "lvibe welcome" in text
    assert "--text" in text
    assert "open-welcome" in text
    assert "test_launcher_open_welcome.py" in text
    assert "test_launcher_welcome_cmd.py" in text
    assert "PM session (STEP 2)" in text
    assert "apply-opening-skip" in text
    assert "schemas/session-manifest.v1.example.json" in text
    assert "session_manifest_example_source_path" in text
    assert "ensure_pm_session_artifacts" in text
    assert "apply_opening_skip" in text
    assert "resolve_next_step_after_opening_skip" in text
    assert "PRODUCT_SPEC_SECTION8_EVIDENCE.md" in text
    assert "test_session_orchestrator.py" in text
    assert "test_session_orchestration_spec_step2_contract.py" in text
    assert "test_issue_template_h8_contract.py" in text
    assert "test_ci_yml_submodules_contract.py" in text
    assert "test_root_readme_ai_pilot_contract.py" in text
    assert "test_build_le_vibe_ide_workflow_contract.py" in text
    assert "linux_compile" in text
    assert "ci-vscodium-bash-syntax.sh" in text
    assert "ci-vscodium-linux-dev-build.sh" in text
    assert "LEVIBE_SKIP_NODE_VERSION_CHECK" in text
    assert "fail fast" in text
    assert "vscodium-linux-build.tar.gz" in text
    assert "actions/cache@v4" in text
    assert ".cargo" in text
    assert "spec-phase2.md" in text
    assert "ide-ci-metadata.txt" in text
    assert "retention-days" in text
    assert "permissions:" in text
    assert "contents: read" in text
    assert "actions: write" in text
    assert "Pre-binary artifact" in text
    assert "editor/BUILD.md" in text
    assert "editor/VENDORING.md" in text
    assert "test_editor_build_md_contract.py" in text
    assert "test_editor_readme_step14_contract.py" in text
    assert "test_spec_phase2_section14_snapshot_contract.py" in text
    assert "Vendoring upstream" in text
    assert "test_ci_qa_hardening_doc_h3_contract.py" in text
    assert "ci-qa-hardening.md" in text
