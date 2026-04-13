"""Contract tests for docs/PRODUCT_SPEC.md — welcome §4, launcher copy, §8 secrets strings in rules, § Prioritization editor smoke."""

from __future__ import annotations

from pathlib import Path

import pytest

from le_vibe import launcher
from le_vibe.continue_workspace import _lvibe_continue_rule_body
from le_vibe.welcome import WELCOME_BANNER
from le_vibe.workspace_hub import LVIBE_DIR_NAME


def test_welcome_banner_matches_product_spec_section4():
    assert "Welcome to Lé Vibe" in WELCOME_BANNER
    assert "Cursor" in WELCOME_BANNER
    assert "open source" in WELCOME_BANNER.lower() or "free" in WELCOME_BANNER.lower()
    assert "lvibe welcome" in WELCOME_BANNER
    assert "open-welcome" in WELCOME_BANNER
    assert ".lvibe/WELCOME.md" in WELCOME_BANNER
    assert "--skip-first-run" in WELCOME_BANNER
    assert "--force-first-run" in WELCOME_BANNER
    assert "lvibe --help" in WELCOME_BANNER
    assert "lvibe logs" in WELCOME_BANNER
    assert "Live:" in WELCOME_BANNER
    assert "tail -f" in WELCOME_BANNER
    assert "lvibe logs --tail 50" in WELCOME_BANNER
    assert "STEP 6" in WELCOME_BANNER


def test_lvibe_workspace_dir_name():
    assert LVIBE_DIR_NAME == ".lvibe"


def test_launcher_user_facing_description_uses_le_vibe_name():
    p = Path(launcher.__file__).read_text(encoding="utf-8")
    assert "Lé Vibe" in p


@pytest.mark.parametrize(
    "rel",
    [
        "templates/continue-config.yaml.j2",
        "templates/lvibe-editor-welcome.md",
    ],
)
def test_continue_template_lists_product_name(rel: str):
    root = Path(__file__).resolve().parents[1]
    text = (root / rel).read_text(encoding="utf-8")
    assert "Lé Vibe" in text
    assert "AUTODETECT" not in text


def test_lvibe_editor_welcome_template_section4_positioning():
    root = Path(__file__).resolve().parents[1]
    text = (root / "templates" / "lvibe-editor-welcome.md").read_text(encoding="utf-8")
    assert "Welcome to Lé Vibe" in text
    assert "open source" in text.lower()
    assert "Cursor" in text
    assert "PRODUCT_SPEC.md" in text
    assert "§4" in text
    assert "In-editor" in text
    assert "Quick Open" in text


def test_continue_memory_rule_documents_secrets_policy_section8():
    body = _lvibe_continue_rule_body()
    assert "PRODUCT_SPEC §8" in body
    assert ".env.local" in body or ".env.*" in body
    assert "Never paste secret" in body


def test_product_spec_section73_resolved_ide_decisions_step14():
    """§7.3 — material STEP 14 decisions recorded (H6)."""
    root = Path(__file__).resolve().parents[2]
    text = (root / "docs" / "PRODUCT_SPEC.md").read_text(encoding="utf-8")
    assert "### 7.3 Material Lé Vibe IDE" in text
    assert "**Only `lvibe`**" in text
    assert "Debian package for the IDE" in text
    assert "GitHub Actions must not" in text


def test_continue_memory_rule_documents_user_gate_section72():
    body = _lvibe_continue_rule_body()
    assert "PRODUCT_SPEC §7.2" in body
    assert "USER RESPONSE REQUIRED" in body
    assert "numbered questions" in body
    assert "schemas/session-manifest.v1.example.json" in body
    assert ".lvibe/session-manifest.json" in body
    assert "session_manifest_example_source_path" in body


def test_workspace_hub_agents_seed_documents_secrets_section8():
    p = Path(__file__).resolve().parents[1] / "le_vibe" / "workspace_hub.py"
    text = p.read_text(encoding="utf-8")
    assert "PRODUCT_SPEC §8" in text
    assert ".env" in text


def test_workspace_policy_reflects_product_spec_section5_defaults():
    p = Path(__file__).resolve().parents[1] / "le_vibe" / "workspace_policy.py"
    text = p.read_text(encoding="utf-8")
    assert "DEFAULT_CAP_MB = 50" in text
    assert "workspace-policy.json" in text


def test_product_spec_section9_evidence_row_links_test_build_to_build_linux_alias():
    """§9 table — PRODUCT_SPEC_SECTION8_EVIDENCE row keeps `build-linux.yml` (`uses:`) beside `build-le-vibe-ide.yml`."""
    root = Path(__file__).resolve().parents[2]
    text = (root / "docs" / "PRODUCT_SPEC.md").read_text(encoding="utf-8")
    rows = [
        ln
        for ln in text.splitlines()
        if ln.lstrip().startswith("|")
        and "PRODUCT_SPEC_SECTION8_EVIDENCE" in ln
        and "test_build_le_vibe_ide_workflow_contract" in ln
    ]
    assert len(rows) == 1, "expected exactly one §9 table row tying SECTION8 evidence to test_build_*"
    row = rows[0]
    assert "build-le-vibe-ide.yml" in row
    assert "build-linux.yml" in row
    assert "uses:" in row


def test_product_spec_prioritization_names_ci_le_vibe_deb_vs_ide_deb_step14():
    """§ Prioritization — default CI le-vibe-deb vs §7.3 le-vibe-ide (north star releases)."""
    root = Path(__file__).resolve().parents[2]
    text = (root / "docs" / "PRODUCT_SPEC.md").read_text(encoding="utf-8")
    assert "Release bundles (H1 / STEP 8 vs STEP 14 / §7.3)" in text
    assert "le-vibe-deb" in text
    assert "le-vibe-ide_*_amd64.deb" in text
    assert "build-le-vibe-debs.sh --with-ide" in text
    assert "Full-product install" in text
    assert "PM_DEB_BUILD_ITERATION.md" in text
    assert "Success output (`--with-ide`)" in text
    assert "verify-step14-closeout.sh --require-stack-deb" in text
    assert "--apt-sim" in text
    assert "--json" in text
    assert "apt_sim_note" in text
    assert "debian-le-vibe-ide/README.md" in text
    assert "Install both packages" in text
    assert "apt-repo-releases.md" in text
    assert "Maintainer build output" in text
    assert "PM_STAGE_MAP.md" in text
    assert "H1 vs §7.3 .deb bundles" in text
    assert "build machine" in text
    assert "test host" in text


def test_product_spec_prioritization_sequences_editor_smoke_before_full_ide_ci():
    """§ Prioritization — vendoring gate for editor/ (H6 / STEP 14) stays documented."""
    root = Path(__file__).resolve().parents[2]
    text = (root / "docs" / "PRODUCT_SPEC.md").read_text(encoding="utf-8")
    assert "**How to sequence work:**" in text
    assert "14.d" in text
    assert "branding-staging.checklist.md" in text
    assert "./editor/smoke.sh" in text
    assert "build-le-vibe-ide.yml" in text
    assert "build-linux.yml" in text
    assert "ide-ci-metadata.txt" in text
    assert "le_vibe_editor_docs" in text
    assert "retention-days" in text
    assert "permissions:" in text
    assert "contents: read" in text
    assert "actions: write" in text
    assert "Pre-binary artifact" in text
    assert "editor/BUILD.md" in text
    assert "editor/VENDORING.md" in text
    assert "linux_compile" in text
    assert "ci-vscodium-bash-syntax.sh" in text
    assert "ci-editor-nvmrc-sync.sh" in text
    assert "ci-vscodium-linux-dev-build.sh" in text
    assert "node --version" in text
    assert "LEVIBE_SKIP_NODE_VERSION_CHECK" in text
    assert "fail fast" in text
    assert "vscodium-linux-build.tar.gz" in text
    assert "actions/cache@v4" in text
    assert ".cargo" in text
    assert "spec-phase2.md" in text and "§14" in text
    assert "NODE_OPTIONS" in text
    assert "max-old-space-size=8192" in text
    assert "When full compile fails" in text


def test_product_spec_section10_regression_evidence_lists_step14_editor_contracts():
    """§10 — regression evidence paragraph cites editor STEP 14 E1 modules (H6 / 14.j)."""
    root = Path(__file__).resolve().parents[2]
    text = (root / "docs" / "PRODUCT_SPEC.md").read_text(encoding="utf-8")
    assert "Regression evidence" in text
    assert "test_editor_build_md_contract.py" in text
    assert "test_editor_readme_step14_contract.py" in text
    assert "test_spec_phase2_section14_snapshot_contract.py" in text
    assert "NODE_OPTIONS" in text
    assert "When full compile fails" in text


def test_product_spec_section8_evidence_h1_ci_artifact_vs_ide_deb_step14():
    """E1: audit doc states CI le-vibe-deb (stack) vs maintainer le-vibe-ide (§7.3)."""
    root = Path(__file__).resolve().parents[2]
    text = (root / "docs" / "PRODUCT_SPEC_SECTION8_EVIDENCE.md").read_text(encoding="utf-8")
    assert "H1 CI artifact vs §7.3 IDE `.deb`" in text
    assert "test_spec_phase2_monorepo_lists_ci_le_vibe_deb_vs_le_vibe_ide_step14" in text
    assert "CI `le-vibe-deb` vs maintainer `le-vibe-ide`" in text
    assert "Release bundles (H1 / STEP 8 vs STEP 14 / §7.3)" in text
    assert "test_product_spec_prioritization_names_ci_le_vibe_deb_vs_ide_deb_step14" in text
    assert "PM_STAGE_MAP.md" in text
    assert "build-le-vibe-debs.sh --with-ide" in text
    assert "Full-product install" in text
    assert "verify-step14-closeout.sh --require-stack-deb" in text
    assert "--apt-sim" in text
    assert "PM_DEB_BUILD_ITERATION.md" in text
    assert "Success output (`--with-ide`)" in text
    assert "verify-step14-closeout.sh --require-stack-deb" in text
    assert "test_build_le_vibe_debs_script_contract.py" in text
    sec73 = text.split("**§7.3 Full-product `.deb` (maintainer, non-CI):**", 1)[1].split(
        "## §10", 1
    )[0]
    assert "required close-out gate" in sec73
    assert "Verified 2026-04-13" in sec73
    assert "held broken packages" in sec73
    assert "verify-step14-closeout.sh --require-stack-deb" in sec73
    assert "--json" in sec73
    assert "apt_sim_note" in sec73
    assert "repo root" in sec73
    assert "resolve-latest-le-vibe-stack-deb.sh" in sec73
    assert "Compile fail-fast" in sec73
    assert "packaging/scripts/ci-vscodium-bash-syntax.sh" in sec73
    assert "packaging/scripts/ci-editor-nvmrc-sync.sh" in sec73
    assert "packaging/scripts/ci-vscodium-linux-dev-build.sh" in sec73
    assert "H1 vs §7.3 .deb bundles" in sec73
    assert "./editor/smoke.sh" in sec73
    assert "linux_compile" in sec73
    assert "523" in text


def test_product_spec_section8_evidence_section10_lists_ide_deb_desktop_step14():
    """E1: §10 evidence row cites le-vibe-ide Freedesktop file + packaging contract (§7.3)."""
    root = Path(__file__).resolve().parents[2]
    text = (root / "docs" / "PRODUCT_SPEC_SECTION8_EVIDENCE.md").read_text(encoding="utf-8")
    assert "packaging/debian-le-vibe-ide/debian/le-vibe.desktop" in text
    assert "build-le-vibe-ide-deb.sh" in text
    assert "stage-le-vibe-ide-deb.sh" in text
    assert "lintian" in text
    assert "test_packaging_le_vibe_ide_deb_contract.py" in text
    assert "packaging/debian-le-vibe-ide/README.md" in text
    assert "apt-repo-releases.md" in text
    assert "roadmap" in text


def test_product_spec_section8_evidence_section10_welcome_row_lists_welcome_banner_e1():
    """E1: §10 table Welcome row cites WELCOME_BANNER + test_product_spec_section8."""
    root = Path(__file__).resolve().parents[2]
    text = (root / "docs" / "PRODUCT_SPEC_SECTION8_EVIDENCE.md").read_text(encoding="utf-8")
    assert "| **Welcome to Lé Vibe**" in text
    assert "WELCOME_BANNER" in text
    assert "terminal onboarding + **`lvibe --help`**" in text
    assert "`Live:`** / **`tail -f`**" in text
    assert "`--path-only`**; concrete **`lvibe logs --tail 50`" in text
    assert "test_product_spec_section8.py" in text


def test_product_spec_section8_evidence_section10_first_run_observability_step6():
    """E1: §10 narrative cites first-run failure remediation → lvibe logs (STEP 6)."""
    root = Path(__file__).resolve().parents[2]
    text = (root / "docs" / "PRODUCT_SPEC_SECTION8_EVIDENCE.md").read_text(encoding="utf-8")
    assert "debian/lvibe.1" in text
    assert "test_debian_le_vibe_man_first_run_contract.py" in text
    assert "- [x] **First-run / STEP 6**" in text
    assert "lvibe logs --tail 50" in text
    assert "§10 acceptance" in text
    assert "First-run vs observability" in text
    assert "ensure_product_first_run" in text
    assert "test_first_run_bootstrap_failure_message_lists_remediation" in text
    assert "lvibe logs" in text
    assert "test_first_run.py" in text
    assert "STEP 6" in text
    assert "WELCOME_BANNER" in text
    assert "welcome.py" in text
    assert "test_welcome_banner_matches_product_spec_section4" in text
    assert "lvibe --help" in text
    assert "launcher.py" in text
    assert "test_launcher_argparse_first_run_flags_help_mentions_logs_step6" in text
    assert "**`LE_VIBE_VERBOSE`**, **`--skip-first-run`**, and **`--force-first-run`**" in text
    checklist_block = text.split("## Checklist (mirrors §10)", 1)[1].split("**§7.3 Full-product", 1)[0]
    first_run_lines = [ln for ln in checklist_block.splitlines() if "**First-run / STEP 6**" in ln]
    assert len(first_run_lines) == 1
    assert "**`argparse`** **`--help`**" in first_run_lines[0]
    assert "`--skip-first-run`" in first_run_lines[0]


def test_product_spec_section8_evidence_h6_lists_editor_readme_h3_linux_compile_index():
    """E1: H6/H7 paragraph cites editor/README H3 linux_compile index + test_editor_readme contract."""
    root = Path(__file__).resolve().parents[2]
    text = (root / "docs" / "PRODUCT_SPEC_SECTION8_EVIDENCE.md").read_text(encoding="utf-8")
    assert "**H6 / H7:**" in text
    assert "editor/README.md" in text
    assert "Optional full Linux compile" in text
    assert "test_editor_readme_step14_contract.py" in text
    assert "Download shape (14.f)" in text
    assert "test_editor_readme_documents_linux_compile_and_tarball_14ef" in text


def test_product_spec_section8_evidence_h3_ci_qa_lists_docker_linux_compile_fallback():
    """E1: H3 maintainer guide row documents ci-qa Related docs docker script (14.e vs flaky linux_compile)."""
    root = Path(__file__).resolve().parents[2]
    text = (root / "docs" / "PRODUCT_SPEC_SECTION8_EVIDENCE.md").read_text(encoding="utf-8")
    assert "Roadmap H1–H3 maintainer guides" in text
    assert "docker-le-vibe-vscodium-linux-compile.sh" in text
    assert "docker-le-vibe-vscodium-prepare-only.sh" in text
    assert "Prepare-only (no `dev/build.sh`)" in text
    assert "test_ci_qa_hardening_related_docs_lists_docker_linux_compile_fallback" in text


def test_product_spec_section8_evidence_intro_lists_linux_compile_cargo_cache():
    """E1: PRODUCT_SPEC_SECTION8_EVIDENCE intro stays aligned with PRODUCT_SPEC *Prioritization* (STEP 14.d / 14.e)."""
    root = Path(__file__).resolve().parents[2]
    text = (root / "docs" / "PRODUCT_SPEC_SECTION8_EVIDENCE.md").read_text(encoding="utf-8")
    assert "docker-le-vibe-vscodium-prepare-only.sh" in text
    assert "test_product_spec_section8.py" in text
    assert "14.d" in text
    assert "branding-staging.checklist.md" in text
    assert "linux_compile" in text
    assert "ci-vscodium-bash-syntax.sh" in text
    assert "ci-vscodium-linux-dev-build.sh" in text
    assert "LEVIBE_SKIP_NODE_VERSION_CHECK" in text
    assert "fail fast" in text
    assert "vscodium-linux-build.tar.gz" in text
    assert "actions/cache@v4" in text
    assert ".cargo" in text
    assert "spec-phase2.md" in text and "§14" in text
    assert "test_editor_build_md_contract.py" in text
    assert "test_editor_readme_step14_contract.py" in text
    assert "test_spec_phase2_section14_snapshot_contract.py" in text
    assert "NODE_OPTIONS" in text
    assert "When full compile fails" in text
    assert "test_ci_qa_hardening_doc_h3_contract.py" in text
    assert "test_docker_le_vibe_vscodium_linux_compile_contract.py" in text
    assert "docker-le-vibe-vscodium-linux-compile.sh" in text
    assert "Optional full Linux compile" in text
    assert "(*At a glance*)" in text
    assert "**`NODE_OPTIONS`** heap parity" in text
    assert "Fork / org tuning" in text
    assert "Maintainer triage" in text
    assert "RUN_ID discovery" in text
