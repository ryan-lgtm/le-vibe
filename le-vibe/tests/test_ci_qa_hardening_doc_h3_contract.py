"""Contract: docs/ci-qa-hardening.md keeps H3 QA CI story (STEP 10)."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_ci_qa_hardening_doc_upload_artifact_row_stack_only_vs_ide_deb_step14():
    """STEP 14 / §7.3: H3 doc table states le-vibe-deb artifact excludes le-vibe-ide."""
    text = (_repo_root() / "docs" / "ci-qa-hardening.md").read_text(encoding="utf-8")
    assert "| **Upload artifact** |" in text
    assert "**not** **`le-vibe-ide`**" in text
    assert "apt-repo-releases.md" in text
    assert "CI `le-vibe-deb` vs maintainer `le-vibe-ide`" in text
    assert "PM_STAGE_MAP.md" in text
    assert "H1 vs §7.3 .deb bundles" in text


def test_ci_qa_hardening_doc_maintainer_full_product_deb_step14():
    """STEP 10 / STEP 14: H3 doc names build-le-vibe-debs --with-ide Full-product install + PM doc."""
    text = (_repo_root() / "docs" / "ci-qa-hardening.md").read_text(encoding="utf-8")
    assert "Maintainer full-product stack + IDE" in text
    assert "build-le-vibe-debs.sh --with-ide" in text
    assert "VSCode-linux-*" in text
    assert "Full-product install" in text
    assert "PM_DEB_BUILD_ITERATION.md" in text
    assert "Success output (`--with-ide`)" in text
    assert "Install both packages" in text


def test_ci_qa_hardening_doc_lists_smoke_and_pytest():
    text = (_repo_root() / "docs" / "ci-qa-hardening.md").read_text(encoding="utf-8")
    assert "ci-smoke.sh" in text
    assert "pytest" in text
    assert "ci.yml" in text
    assert "H3" in text or "Roadmap H3" in text
    assert "PM_STAGE_MAP" in text
    assert "STEP 10" in text
    assert "ci-editor-gate.sh" in text
    assert "build-le-vibe-ide-deb.sh" in text
    assert "LEVIBE_IDE_LINTIAN_STRICT" in text


def test_ci_qa_hardening_doc_linux_compile_maintainer_triage_step14e():
    """STEP 14.e: H3 doc triage table when linux_compile OOM/timeout — still not a merge gate."""
    text = (_repo_root() / "docs" / "ci-qa-hardening.md").read_text(encoding="utf-8")
    assert "### Maintainer triage" in text
    assert "**not** a merge gate" in text
    assert "OOM" in text
    assert "Timeout" in text
    assert "Download / unpack mistakes" in text
    assert "Honesty vs CI" in text


def test_ci_qa_hardening_doc_linux_compile_fork_org_tuning_step14e():
    """STEP 14.e: H3 doc names optional runs-on/timeout fork tuning — not a merge gate."""
    text = (_repo_root() / "docs" / "ci-qa-hardening.md").read_text(encoding="utf-8")
    assert "**Fork / org tuning (optional):**" in text
    assert "timeout-minutes" in text
    assert "runs-on" in text
    assert "Runner realism" in text
    assert "Honesty vs CI" in text


def test_ci_qa_hardening_doc_linux_compile_gh_run_list_finding_run_id_step14f():
    """STEP 14.f: H3 doc names gh run list + workflow file for linux_compile artifact download."""
    text = (_repo_root() / "docs" / "ci-qa-hardening.md").read_text(encoding="utf-8")
    assert "**Finding `RUN_ID`:**" in text
    assert "gh run list" in text
    assert "gh run view" in text
    assert "--log-failed" in text
    assert "build-le-vibe-ide.yml" in text
    assert "/actions/runs/" in text


def test_ci_qa_hardening_doc_linux_compile_quick_path_triggers_step14e():
    """STEP 14.e: H3 doc lists opt-in linux_compile triggers — not a merge gate; points at BUILD.md + tarball."""
    text = (_repo_root() / "docs" / "ci-qa-hardening.md").read_text(encoding="utf-8")
    assert "Optional full Linux compile" in text
    assert "`linux_compile`, STEP 14.e" in text
    assert "vscodium_linux_compile" in text
    assert "build-linux.yml" in text
    assert "ide-v" in text
    assert "refs/tags/ide-v" in text
    assert "Honesty vs CI" in text
    assert "vscodium-linux-build.tar.gz" in text
    assert "docker-le-vibe-vscodium-linux-compile.sh" in text
    assert "docker-le-vibe-vscodium-prepare-only.sh" in text
    assert "Prepare-only (no `dev/build.sh`)" in text
    assert "Download shape" in text
    assert ".zip" in text
    assert "print-ci-tarball-codium-path.sh" in text
    assert "CI artifact → `LE_VIBE_EDITOR`" in text
    assert "gh run download" in text
    assert "le-vibe-vscodium-linux-<RUN_ID>" in text
    assert "build-le-vibe-ide.yml" in text
    assert "**Publishing (H1 / STEP 14):**" in text
    assert "Pre-publish artifact checklist" in text
    assert "**Integrity**" in text
    assert "PM_DEB_BUILD_ITERATION.md" in text


def test_ci_qa_hardening_related_docs_lists_docker_linux_compile_fallback():
    """STEP 14.e: Related docs points at docker full-compile script when CI linux_compile is flaky."""
    text = (_repo_root() / "docs" / "ci-qa-hardening.md").read_text(encoding="utf-8")
    assert "## Related docs" in text
    related = text.split("## Related docs", 1)[1]
    assert "docker-le-vibe-vscodium-linux-compile.sh" in related
    assert "docker-le-vibe-vscodium-prepare-only.sh" in related
    assert "ubuntu:22.04" in related


def test_ci_qa_hardening_ide_smoke_section_distinguishes_fast_gate_vs_linux_compile():
    """STEP 14: smoke is fast; vendoring / optional linux_compile + tarball live in editor docs."""
    text = (_repo_root() / "docs" / "ci-qa-hardening.md").read_text(encoding="utf-8")
    assert "editor/smoke.sh --help" in text
    assert "same arguments" in text
    assert "git submodule update --init editor/vscodium" in text
    assert "Local clone (14.b)" in text
    assert "editor/VENDORING.md" in text
    assert "linux_compile" in text
    assert "vscodium-linux-build.tar.gz" in text
    assert "print-ci-tarball-codium-path.sh" in text
    assert "Vendoring upstream" in text
    assert "branding-staging.checklist.md" in text
    assert "read before overrides" in text
    assert "14.c vs 14.d" in text
    assert "ci-vscodium-bash-syntax.sh" in text
    assert "ci-editor-nvmrc-sync.sh" in text
    assert "ci-vscodium-linux-dev-build.sh" in text
    assert "LEVIBE_SKIP_NODE_VERSION_CHECK" in text
    assert "fail fast" in text
    assert "NODE_OPTIONS" in text
    assert "max-old-space-size=8192" in text
    assert "When full compile fails" in text
