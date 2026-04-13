"""packaging/scripts/build-le-vibe-debs.sh — bash syntax (PM_DEB_BUILD_ITERATION.md)."""

from __future__ import annotations

import subprocess
from pathlib import Path


def test_build_le_vibe_debs_script_bash_syntax():
    root = Path(__file__).resolve().parents[2]
    script = root / "packaging" / "scripts" / "build-le-vibe-debs.sh"
    assert script.is_file()
    subprocess.run(["bash", "-n", str(script)], check=True)


def test_build_le_vibe_debs_script_header_documents_ci_vs_with_ide_step14():
    """STEP 14 / §7.3: one-shot script header ties ci.yml le-vibe-deb to optional --with-ide."""
    root = Path(__file__).resolve().parents[2]
    text = (root / "packaging" / "scripts" / "build-le-vibe-debs.sh").read_text(encoding="utf-8")
    assert "0 → 1 → 14 → 2–13 → 15–17" in text
    assert "PROMPT_BUILD_LE_VIBE.md" in text
    assert "PM_STAGE_MAP.md" in text
    assert "le-vibe-deb" in text
    assert "apt-repo-releases.md" in text
    assert "IDE package" in text


def test_build_le_vibe_debs_script_mentions_submodule_14b():
    root = Path(__file__).resolve().parents[2]
    text = (root / "packaging" / "scripts" / "build-le-vibe-debs.sh").read_text(encoding="utf-8")
    assert "git submodule update --init editor/vscodium" in text
    assert "Fresh clone (14.b)" in text
    assert "could not locate le-vibe_*.deb" in text
    assert "fix errors above" in text
    assert "could not locate le-vibe-ide_*.deb" in text
    assert "PM_STAGE_MAP.md" in text
    assert "H1 vs §7.3 .deb bundles" in text
    assert "14.c" in text
    assert "find not on PATH" in text
    assert "sort not on PATH" in text
    assert "head not on PATH" in text
    assert "apt-get not on PATH" in text
    assert "build-le-vibe-ide-deb.sh" in text
    assert "LEVIBE_IDE_LINTIAN_STRICT" in text
    assert "LEVIBE_STAGE_IDE_ASSERT_BRAND" in text
    assert "LEVIBE_STAGE_IDE_VERBOSE" in text
    assert "LEVIBE_EDITOR_GATE_ASSERT_BRAND" in text
    assert "ci-editor-gate.sh" in text
    assert "stage-le-vibe-ide-deb.sh" in text
    assert "print-built-codium-path.sh" in text
    assert "Partial tree" in text


def test_build_le_vibe_debs_script_prints_full_product_install_hint_step14():
    """STEP 14: after --with-ide success, script echoes sudo apt install with both resolved .deb paths."""
    root = Path(__file__).resolve().parents[2]
    text = (root / "packaging" / "scripts" / "build-le-vibe-debs.sh").read_text(encoding="utf-8")
    assert "Full-product install" in text
    assert "paths printed above" in text
    assert "sudo apt install" in text
    assert "$STACK_DEB" in text and "$IDE_DEB" in text
    assert "/usr/share/doc/le-vibe/README.Debian" in text
    assert "debian-le-vibe-ide/README.md" in text
    assert "verify-73-maintainer.sh" in text
    assert "verify-step14-closeout.sh" in text
    assert "verify-step14-closeout.sh --require-stack-deb" in text
    assert "optional --apt-sim, --json" in text
    assert "apt_sim_note" in text


def test_build_le_vibe_debs_usage_documents_full_product_output_step14():
    """STEP 14: --help text documents Full-product stdout vs PM_DEB / apt-repo-releases."""
    root = Path(__file__).resolve().parents[2]
    text = (root / "packaging" / "scripts" / "build-le-vibe-debs.sh").read_text(encoding="utf-8")
    assert "resolves the monorepo root from its own path" in text
    assert "cwd does not need to be the clone root" in text
    assert "-h, --help" in text
    assert "Show this message and exit" in text
    assert "DEB_BUILD_OPTIONS=parallel=$(nproc)" in text
    assert "parallel=$(nproc) for faster stack" in text
    assert "dpkg-parsechangelog" in text
    assert "dpkg-parsechangelog -S Version -l debian/changelog (stack) / packaging/debian-le-vibe-ide/debian/changelog (IDE)" in text
    assert "full-product checklist step 2" in text
    assert "Dual changelog discipline" in text
    assert "full-product GitHub Release" in text
    assert "Related docs (H1 index)" in text
    assert "CHANGELOG.md" in text
    assert "ci-qa-hardening" in text
    assert "editor/README" in text
    assert "H1 quick pointer" in text
    assert "PM_STAGE_MAP" in text
    assert "Full-product (--with-ide)" in text
    assert "docs/PM_DEB_BUILD_ITERATION.md" in text
    assert "docs/apt-repo-releases.md" in text
    assert "Success output" in text
    assert "Maintainer build output" in text
    assert "Pre-publish artifact checklist" in text
    assert "Checklist shorthand" in text
    assert "Pre-publish — Checklist shorthand" in text
    assert "packaging/debian-le-vibe-ide/debian/changelog" in text
    assert "IDE le-vibe-ide changelog" in text
    assert "Tagging discipline" in text
    assert "Exit codes:" in text
    assert "PM_DEB_BUILD_ITERATION.md (Exit codes" in text
    assert "lvibe verify-checksums" in text
    assert "le-vibe-deb artifact is a .zip" in text
    assert "Stack v" in text and "ide-v*" in text
    assert "le-vibe-python.cdx.json" in text
    assert "full-product checklist step 3" in text
    assert "Pre-publish Integrity" in text
    assert "Combined drop" in text


def test_pm_deb_build_iteration_doc_submodule_prereq_14b():
    root = Path(__file__).resolve().parents[2]
    text = (root / "docs" / "PM_DEB_BUILD_ITERATION.md").read_text(encoding="utf-8")
    assert "git submodule update --init editor/vscodium" in text
    assert "Fresh clone (14.b" in text


def test_pm_deb_build_iteration_doc_master_orchestrator_queue_step14():
    """STEP 14: PM deb doc ties --with-ide to Master queue before Invocations."""
    root = Path(__file__).resolve().parents[2]
    text = (root / "docs" / "PM_DEB_BUILD_ITERATION.md").read_text(encoding="utf-8")
    head = text.split("## Invocations", 1)[0]
    assert "0 → 1 → 14 → 2–13 → 15–17" in head
    assert "PROMPT_BUILD_LE_VIBE.md" in head
    assert "Rolling iteration — prefer continuation" in head
    assert "build-le-vibe-debs.sh --with-ide" in head
    assert "verify-step14-closeout.sh --require-stack-deb" in head
    assert "--apt-sim" in head
    assert "--json" in head
    assert "apt_sim_note" in head


def test_pm_deb_build_iteration_doc_success_output_orders_build_vs_test_host_step14():
    """STEP 14: Success output paragraph distinguishes build machine vs test host."""
    root = Path(__file__).resolve().parents[2]
    text = (root / "docs" / "PM_DEB_BUILD_ITERATION.md").read_text(encoding="utf-8")
    sec = text.split("**Success output (`--with-ide`):**", 1)[1].split(
        "**`--json` close-out payload:**", 1
    )[0]
    assert "manual-step14-install-smoke.sh" in sec
    assert "build machine" in sec
    assert "test host" in sec
    assert "apt-repo-releases.md" in sec


def test_pm_deb_build_iteration_doc_sibling_docs_links_apt_repo_h1_related_round_trip():
    """H1: PM header lists apt-repo-releases Related docs round-trip (STEP 8)."""
    root = Path(__file__).resolve().parents[2]
    text = (root / "docs" / "PM_DEB_BUILD_ITERATION.md").read_text(encoding="utf-8")
    head = text.split("## Invocations", 1)[0]
    assert "**Sibling docs:**" in head
    assert "PRODUCT_SPEC_SECTION8_EVIDENCE.md" in head
    assert "Last verified" in head
    assert "apt-repo-releases.md" in head
    assert "CHANGELOG.md" in head
    assert "ci-qa-hardening.md" in head
    assert "editor/README.md" in head
    assert "Full Linux compile" in head
    assert "Related docs" in head
    assert "PM_STAGE_MAP.md" in head


def test_pm_deb_build_iteration_doc_links_h1_stack_release_checklist():
    """H1: PM doc points at apt-repo-releases stack-only Release checklist."""
    root = Path(__file__).resolve().parents[2]
    text = (root / "docs" / "PM_DEB_BUILD_ITERATION.md").read_text(encoding="utf-8")
    head = text.split("## Invocations", 1)[0]
    assert "**Release checklist (H1):**" in head
    assert "Checklist — stack-only GitHub Release" in head
    assert "Checklist — full-product GitHub Release" in head
    assert "Dual changelog discipline" in head
    assert "**Stack vs IDE changelogs:**" in head
    assert "packaging/debian-le-vibe-ide/debian/changelog" in head
    assert "IDE `le-vibe-ide` changelog" in head
    assert "**`dpkg-parsechangelog` (IDE):**" in head
    assert "dpkg-parsechangelog -S Version -l packaging/debian-le-vibe-ide/debian/changelog" in head
    assert "CHANGELOG.md" in head
    assert "le-vibe-deb" in head
    assert "verify-step14-closeout.sh --require-stack-deb" in head
    assert "--apt-sim" in head
    assert "--json" in head
    assert "apt_sim_note" in head


def test_pm_deb_build_iteration_doc_lists_deb_build_options_parallel_invocation():
    """PM doc invocations table documents DEB_BUILD_OPTIONS=parallel for stack builds."""
    root = Path(__file__).resolve().parents[2]
    text = (root / "docs" / "PM_DEB_BUILD_ITERATION.md").read_text(encoding="utf-8")
    assert "DEB_BUILD_OPTIONS=parallel=" in text
    assert "$(nproc)" in text
    assert "Faster stack" in text


def test_pm_deb_build_iteration_doc_invocations_working_directory_step14():
    """STEP 14: PM doc states script cds to repo root from script path (any cwd)."""
    root = Path(__file__).resolve().parents[2]
    text = (root / "docs" / "PM_DEB_BUILD_ITERATION.md").read_text(encoding="utf-8")
    sec = text.split("## Invocations (repository root)", 1)[1].split("### Output paths", 1)[0]
    assert "**Working directory:**" in sec
    assert "from any cwd" in sec
    assert "from the script path" in sec


def test_pm_deb_build_iteration_doc_quick_version_check_pair_h1():
    """H1: Invocations section pairs stack vs IDE dpkg-parsechangelog before iterating builds."""
    root = Path(__file__).resolve().parents[2]
    text = (root / "docs" / "PM_DEB_BUILD_ITERATION.md").read_text(encoding="utf-8")
    sec = text.split("## Invocations (repository root)", 1)[1].split("### Output paths", 1)[0]
    assert "**Quick version check (repo root):**" in sec
    assert "dpkg-parsechangelog -S Version -l debian/changelog" in sec
    assert "dpkg-parsechangelog -S Version -l packaging/debian-le-vibe-ide/debian/changelog" in sec
    assert "Checklist — full-product GitHub Release" in sec
    assert "step **2**" in sec


def test_pm_deb_build_iteration_doc_release_folder_matches_apt_repo_full_product_step3_h1():
    """H1: Release folder paragraph ties le-vibe-deb trio + IDE .deb to apt-repo step 3."""
    root = Path(__file__).resolve().parents[2]
    text = (root / "docs" / "PM_DEB_BUILD_ITERATION.md").read_text(encoding="utf-8")
    sec = text.split("**Release folder (H1):**", 1)[1].split("**Publishing (STEP 8", 1)[0]
    assert "Checklist — full-product GitHub Release" in sec
    assert "step **3**" in sec
    assert "**`le-vibe-deb`** tree" in sec
    assert "le-vibe-python.cdx.json" in sec
    assert "Minimum directory layout (readiness gate)" in sec


def test_pm_deb_build_iteration_doc_lists_output_paths_table_step14():
    """STEP 14: PM doc names stack .deb beside repo vs IDE .deb under packaging/."""
    root = Path(__file__).resolve().parents[2]
    text = (root / "docs" / "PM_DEB_BUILD_ITERATION.md").read_text(encoding="utf-8")
    assert "### Output paths (from repo root)" in text
    assert "../le-vibe_*_all.deb" in text
    assert "packaging/le-vibe-ide_*.deb" in text
    assert "Full-product install" in text


def test_pm_deb_build_iteration_doc_releases_h1_step14_pointer():
    """STEP 14 / §7.3: PM deb doc points at apt-repo-releases for dual-.deb demo + H1 checksums."""
    root = Path(__file__).resolve().parents[2]
    text = (root / "docs" / "PM_DEB_BUILD_ITERATION.md").read_text(encoding="utf-8")
    assert "**Script help:**" in text
    assert "Minimum directory layout (readiness gate)" in text
    assert "apt-repo-releases.md" in text
    assert "le-vibe-ide_*_amd64.deb" in text
    assert "le-vibe-deb" in text
    assert "SHA256SUMS" in text
    assert "PM_STAGE_MAP.md" in text
    assert "H1 vs §7.3 .deb bundles" in text
    assert "spec-phase2.md" in text
    assert "CI `le-vibe-deb` vs maintainer `le-vibe-ide`" in text
    assert "Pre-publish artifact checklist" in text
    assert "Tagging discipline" in text
    assert "verify-checksums" in text
    assert ".zip" in text
    assert "GitHub Releases + checksums" in text
    assert "H1 quick pointer" in text
    assert "Stack `v…` release tags" in text
    assert "Stack release tags vs `ide-v`*" in text
    assert "dpkg-parsechangelog" in text
    assert "*Versioned changelog*" in text
    assert "**Integrity**" in text
    assert "**Combined drop:**" in text
    assert "CI manifest" in text or "CI SHA256SUMS" in text
    assert "**Checklist shorthand**" in text
    assert "three lines for stack-only" in text


def test_pm_deb_build_iteration_doc_exit_codes_table_step14():
    """PM doc lists 0/1/2 exit semantics; mirrors build-le-vibe-debs.sh --help."""
    root = Path(__file__).resolve().parents[2]
    text = (root / "docs" / "PM_DEB_BUILD_ITERATION.md").read_text(encoding="utf-8")
    assert "### Exit codes (`build-le-vibe-debs.sh`)" in text
    assert "| **0** |" in text
    assert "| **1** |" in text
    assert "| **2** |" in text
    assert "Same table is summarized" in text
    assert "see *Failure (`--with-ide`)* below" in text


def test_pm_deb_build_iteration_doc_documents_full_product_install_echo_step14():
    """STEP 14: PM deb doc matches build-le-vibe-debs.sh post-success Full-product install output."""
    root = Path(__file__).resolve().parents[2]
    text = (root / "docs" / "PM_DEB_BUILD_ITERATION.md").read_text(encoding="utf-8")
    assert "Success output (`--with-ide`)" in text
    assert "Full-product install" in text
    assert "sudo apt install" in text
    assert "/usr/share/doc/le-vibe/README.Debian" in text
    assert "debian-le-vibe-ide/README.md" in text
    assert "verify-step14-closeout.sh" in text
    assert "--require-stack-deb" in text
    assert "manual-step14-install-smoke.sh" in text
    assert "--print-install-cmd" in text
    assert "--json" in text
    success = text.split("**Success output (`--with-ide`):**", 1)[1].split("**Failure (`--with-ide`):**", 1)[0]
    assert "verify-step14-closeout.sh --require-stack-deb" in success
    assert "--apt-sim" in success
    assert "--json" in success
    assert "optional **`--require-stack-deb`**" not in success
    payload = text.split("**`--json` close-out payload:**", 1)[1].split("**Failure (`--with-ide`):**", 1)[0]
    assert "apt_sim_note" in payload
    assert "not_requested" in payload
    assert "requested_without_stack_requirement" in payload


def test_pm_deb_build_iteration_doc_731_staging_identity_step14():
    """STEP 14: PM deb doc names §7.3 staging env + ci-vscodium path before stage-le-vibe-ide-deb.sh."""
    root = Path(__file__).resolve().parents[2]
    text = (root / "docs" / "PM_DEB_BUILD_ITERATION.md").read_text(encoding="utf-8")
    assert "§7.3 IDE staging" in text
    assert "ci-vscodium-linux-dev-build.sh" in text
    assert "product-branding-merge.json" in text
    assert "sync-linux-icon-assets.sh" in text
    assert "LEVIBE_STAGE_IDE_ASSERT_BRAND" in text
    assert "LEVIBE_STAGE_IDE_VERBOSE" in text
    assert "LEVIBE_EDITOR_GATE_ASSERT_BRAND" in text
    assert "ci-editor-gate.sh" in text
    assert "One-shot:" in text
    assert "IDE-only:" in text
    assert "build-le-vibe-debs.sh --with-ide" in text
    assert "build-le-vibe-ide-deb.sh" in text
    assert "stage-le-vibe-ide-deb.sh" in text
    assert "resources/app/product.json" in text


def test_print_pm_deb_build_prompt_extractable():
    root = Path(__file__).resolve().parents[2]
    text = (root / "docs" / "PM_DEB_BUILD_ITERATION.md").read_text(encoding="utf-8")
    fence: str | None = None
    for part in text.split("```"):
        if part.lstrip().startswith("You are the Lé Vibe **packaging / .deb build**"):
            fence = part
            break
    assert fence is not None
    assert "build-le-vibe-debs.sh" in fence
    assert "LÉ VIBE PACKAGING COMPLETE" in fence
    assert "PM_STAGE_MAP.md" in fence
    assert "H1 vs §7.3 .deb bundles" in fence
    assert "CI `le-vibe-deb` vs maintainer `le-vibe-ide`" in fence
    assert "LEVIBE_STAGE_IDE_ASSERT_BRAND" in fence
    assert "LEVIBE_EDITOR_GATE_ASSERT_BRAND" in fence
    assert "stage-le-vibe-ide-deb.sh" in fence
    assert "Full-product install" in fence
    assert "Success output (`--with-ide`)" in fence
    assert "Exit codes:" in fence
    assert "*Exit codes (`build-le-vibe-debs.sh`)*" in fence
    assert "**H1 publishing:**" in fence
    assert "lvibe verify-checksums" in fence
    assert "GitHub Releases + checksums" in fence
    assert "stack `v…` vs `ide-v*`" in fence
