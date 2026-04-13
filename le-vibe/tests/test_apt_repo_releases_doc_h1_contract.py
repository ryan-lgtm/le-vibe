"""Contract: docs/apt-repo-releases.md keeps H1 release story (STEP 8)."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_apt_repo_releases_doc_lists_ci_artifact_and_changelog():
    text = (_repo_root() / "docs" / "apt-repo-releases.md").read_text(encoding="utf-8")
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


def test_apt_repo_releases_github_releases_section_links_combined_drop_step8():
    """STEP 8 / H1: GitHub Releases flow reminds Combined drop before verify / gh release create."""
    text = (_repo_root() / "docs" / "apt-repo-releases.md").read_text(encoding="utf-8")
    head, rest = text.split("## GitHub Releases + checksums", 1)
    gh_section = rest.split("\n## ", 1)[0]
    assert "Combined drop" in gh_section
    assert "gh release create" in gh_section
    assert "Pre-publish artifact checklist" in gh_section


def test_apt_repo_releases_related_docs_lists_pm_deb_and_stage_map():
    """H1 Related docs table links PM_DEB one-shot + PM_STAGE_MAP H1 vs §7.3."""
    text = (_repo_root() / "docs" / "apt-repo-releases.md").read_text(encoding="utf-8")
    assert "## Related docs" in text
    _, related = text.split("## Related docs", 1)
    table = related.split("\n## ", 1)[0]
    assert "PM_DEB_BUILD_ITERATION.md" in table
    assert "build-le-vibe-debs.sh" in table
    assert "PM_STAGE_MAP.md" in table
    assert "STEP 14" in table
    assert "§7.3" in table
    assert "spec-phase2.md" in table


def test_apt_repo_releases_doc_opens_with_ci_le_vibe_deb_stack_only_step14():
    """STEP 14: H1 doc states ci.yml artifact excludes le-vibe-ide; points at spec-phase2 honesty."""
    text = (_repo_root() / "docs" / "apt-repo-releases.md").read_text(encoding="utf-8")
    assert "CI vs IDE bundle" in text
    assert "not** **`le-vibe-ide_*_amd64.deb`**" in text
    assert "CI `le-vibe-deb` vs maintainer `le-vibe-ide`" in text
