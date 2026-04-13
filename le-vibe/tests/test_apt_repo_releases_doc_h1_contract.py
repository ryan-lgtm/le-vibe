"""Contract: docs/apt-repo-releases.md keeps H1 release story (STEP 8)."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_apt_repo_releases_doc_lists_release_assets_vs_sha256sums_sanity_h1():
    """H1: optional attachments must not leave dangling SHA256SUMS lines."""
    text = (_repo_root() / "docs" / "apt-repo-releases.md").read_text(encoding="utf-8")
    assert "### Release assets vs `SHA256SUMS` (sanity)" in text
    assert "right-hand side" in text
    assert "le-vibe-python.cdx.json" in text
    assert "Integrity" in text


def test_apt_repo_releases_doc_lists_minimum_directory_layout_gate():
    """H1: Pre-publish checklist names readiness gate + CI three-file bundle vs stack+IDE rewrite."""
    text = (_repo_root() / "docs" / "apt-repo-releases.md").read_text(encoding="utf-8")
    assert "### Minimum directory layout" in text
    assert "readiness gate" in text
    assert "**rewrite** **`SHA256SUMS`**" in text
    assert "do **not** reuse the CI file unchanged" in text
    assert "gh run download" in text and "le-vibe-deb" in text


def test_apt_repo_releases_doc_dual_changelog_discipline_h1():
    """H1: debian/changelog vs CHANGELOG.md must match before stack tag + checklist."""
    text = (_repo_root() / "docs" / "apt-repo-releases.md").read_text(encoding="utf-8")
    assert "**Dual changelog discipline:**" in text
    assert "dpkg -l le-vibe" in text
    assert "Checklist — stack-only GitHub Release" in text


def test_apt_repo_releases_doc_ide_debian_changelog_separate_from_stack_h1():
    """H1: le-vibe-ide has packaging/debian-le-vibe-ide/debian/changelog; ide-v* does not replace stack v…"""
    text = (_repo_root() / "docs" / "apt-repo-releases.md").read_text(encoding="utf-8")
    assert "**IDE `le-vibe-ide` changelog:**" in text
    assert "packaging/debian-le-vibe-ide/debian/changelog" in text
    assert "ide-v*" in text
    assert "linux_compile" in text


def test_apt_repo_releases_doc_lists_full_product_release_checklist_h1():
    """H1: full-product checklist — dual deb + Combined drop + PM_DEB."""
    text = (_repo_root() / "docs" / "apt-repo-releases.md").read_text(encoding="utf-8")
    assert "### Checklist — full-product GitHub Release" in text
    assert "stack + IDE" in text
    assert "Dual changelog discipline" in text
    assert "Combined drop" in text
    assert "PM_DEB_BUILD_ITERATION.md" in text
    assert "Success output (`--with-ide`)" in text
    full_product = text.split("### Checklist — full-product GitHub Release", 1)[1].split("## CI artifacts", 1)[0]
    assert "packaging/debian-le-vibe-ide/debian/changelog" in full_product
    assert "Produce IDE" in full_product
    assert "dpkg-parsechangelog -S Version -l packaging/debian-le-vibe-ide/debian/changelog" in full_product
    assert "verify-step14-closeout.sh --require-stack-deb" in full_product
    assert "--apt-sim" in full_product
    assert "--json" in full_product
    assert "apt_sim_note" in full_product
    assert "Before a stack tag / Release" in full_product or "Before a stack tag" in full_product
    assert "le-vibe-python.cdx.json" in full_product
    assert "**`le-vibe-deb`** tree" in full_product


def test_apt_repo_releases_doc_lists_stack_release_checklist_h1():
    """H1: ordered checklist ties changelog, tag, ci artifact, verify, gh release."""
    text = (_repo_root() / "docs" / "apt-repo-releases.md").read_text(encoding="utf-8")
    assert "### Checklist — stack-only GitHub Release" in text
    stack_only = text.split("### Checklist — stack-only GitHub Release", 1)[1].split(
        "### Checklist — full-product", 1
    )[0]
    assert "*GitHub Releases + checksums* (below)" in stack_only
    assert "Pre-publish artifact checklist" in stack_only
    assert "minimal ordered path" in text
    assert "dpkg-parsechangelog -S Version" in text
    assert "le-vibe-deb" in text
    assert "sha256sum -c SHA256SUMS" in text
    assert "gh release create" in text
    assert "le-vibe-ide_*_amd64.deb" in text


def test_apt_repo_releases_doc_lists_artifact_sources_at_glance_h1():
    """H1: doc maps CI le-vibe-deb vs maintainer ../ stack deb + packaging/ IDE deb."""
    text = (_repo_root() / "docs" / "apt-repo-releases.md").read_text(encoding="utf-8")
    assert "### Artifact sources at a glance" in text
    assert "CI vs maintainer output" in text
    assert "../le-vibe_*_all.deb" in text
    assert "packaging/le-vibe-ide_*.deb" in text
    assert "Output paths (from repo root)" in text


def test_apt_repo_releases_doc_lists_ci_artifact_and_changelog():
    text = (_repo_root() / "docs" / "apt-repo-releases.md").read_text(encoding="utf-8")
    assert "**Checklist shorthand (what lands in one release directory / GitHub Release):**" in text
    assert "**Stack only** — from **`le-vibe-deb`**" in text
    assert "**Combined drop**" in text
    assert "CI manifest alone" in text
    assert "ci-qa-hardening.md" in text
    assert "**Integrity:**" in text
    assert "Regenerate **`SHA256SUMS`**" in text
    assert "Manual checksums" in text
    assert "le-vibe-deb" in text
    assert "SHA256SUMS" in text
    assert "ci.yml" in text
    assert "debian/changelog" in text
    assert "CHANGELOG.md" in text
    assert "H1" in text or "Roadmap H1" in text
    assert "PM_STAGE_MAP" in text
    assert "STEP 8" in text
    assert "linux_compile" in text
    assert "vscodium-linux-build.tar.gz" in text
    assert "Optional full Linux compile" in text
    assert "ide-v" in text
    assert "Tagging discipline" in text
    assert "Honesty vs CI" in text
    assert "gh release create" in text
    assert "verify-checksums" in text
    assert ".zip" in text
    assert "Stack release tags vs `ide-v*`" in text
    assert "dpkg -l le-vibe" in text
    assert "dpkg-parsechangelog" in text


def test_apt_repo_releases_doc_lists_le_vibe_ide_release_path_step14():
    """STEP 14 / §7.3: H1 doc names sibling le-vibe-ide .deb + build scripts for full demo releases."""
    text = (_repo_root() / "docs" / "apt-repo-releases.md").read_text(encoding="utf-8")
    assert "le-vibe-ide" in text
    assert "build-le-vibe-ide-deb.sh" in text
    assert "packaging/debian-le-vibe-ide/README.md" in text
    assert "STEP 14" in text
    assert "Full-product install" in text
    assert "Success output (`--with-ide`)" in text
    assert "PM_DEB_BUILD_ITERATION.md" in text
    assert "Install both packages" in text
    assert "LEVIBE_EDITOR_GATE_ASSERT_BRAND" in text
    assert "ci-editor-gate.sh" in text
    assert "verify-step14-closeout.sh" in text
    assert "verify-step14-closeout.sh --require-stack-deb" in text
    assert "--apt-sim" in text
    assert "--json" in text
    assert "manual-step14-install-smoke.sh" in text
    assert "--print-install-cmd" in text
    assert "--json" in text
    assert "build machine" in text
    assert "test host" in text
    assert "Incomplete Linux build" in text
    assert "Partial tree" in text
    assert "Partial VSCode-linux tree" in text
    assert "print-built-codium-path.sh" in text
    assert "print-vsbuild-codium-path.sh" in text
    assert "build-le-vibe-ide-deb.sh --help" in text
    assert "Compile fail-fast (STEP 14" in text
    assert "ci-vscodium-bash-syntax.sh" in text
    assert "ci-editor-nvmrc-sync.sh" in text
    assert "ci-vscodium-linux-dev-build.sh" in text


def test_apt_repo_releases_github_releases_section_links_combined_drop_step8():
    """STEP 8 / H1: GitHub Releases flow reminds Combined drop before verify / gh release create."""
    text = (_repo_root() / "docs" / "apt-repo-releases.md").read_text(encoding="utf-8")
    head, rest = text.split("## GitHub Releases + checksums", 1)
    gh_section = rest.split("\n## ", 1)[0]
    assert "H1 quick pointer" in gh_section
    assert "Checklist — stack-only GitHub Release" in gh_section
    assert "Checklist — full-product GitHub Release" in gh_section
    assert "Combined drop" in gh_section
    assert "gh release create" in gh_section
    assert "Pre-publish artifact checklist" in gh_section


def test_apt_repo_releases_related_docs_lists_pm_deb_and_stage_map():
    """H1 Related docs table links PM_DEB one-shot + PM_STAGE_MAP H1 vs §7.3."""
    text = (_repo_root() / "docs" / "apt-repo-releases.md").read_text(encoding="utf-8")
    assert "## Related docs" in text
    _, related = text.split("## Related docs", 1)
    table = related.split("\n## ", 1)[0]
    assert "CHANGELOG.md" in table
    assert "Keep a Changelog" in table
    assert "Dual changelog discipline" in table
    assert "PRODUCT_SPEC_SECTION8_EVIDENCE.md" in table
    assert "Last verified" in table
    assert "PM_DEB_BUILD_ITERATION.md" in table
    assert "build-le-vibe-debs.sh" in table
    assert "PM_STAGE_MAP.md" in table
    assert "STEP 14" in table
    assert "§7.3" in table
    assert "spec-phase2.md" in table
    assert "ci-qa-hardening.md" in table
    assert "editor/README.md" in table
    assert "Full Linux compile" in table
    assert "maintainer index" in table


def test_apt_repo_releases_doc_opens_with_ci_le_vibe_deb_stack_only_step14():
    """STEP 14: H1 doc states ci.yml artifact excludes le-vibe-ide; points at spec-phase2 honesty."""
    text = (_repo_root() / "docs" / "apt-repo-releases.md").read_text(encoding="utf-8")
    assert "CI vs IDE bundle" in text
    assert "not** **`le-vibe-ide_*_amd64.deb`**" in text
    assert "CI `le-vibe-deb` vs maintainer `le-vibe-ide`" in text
