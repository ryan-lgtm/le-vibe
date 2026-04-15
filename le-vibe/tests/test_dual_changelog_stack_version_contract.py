"""Contract: CHANGELOG.md aligns with stack + IDE Debian changelogs (STEP 8 / H1)."""

from __future__ import annotations

import re
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_changelog_md_has_heading_for_each_debian_stack_version():
    """Dual changelog discipline — docs/apt-repo-releases.md *Versioned changelog* / E1."""
    root = _repo_root()
    debian_changelog = (root / "debian" / "changelog").read_text(encoding="utf-8")
    changelog_md = (root / "CHANGELOG.md").read_text(encoding="utf-8")
    versions = re.findall(r"^le-vibe \(([^)]+)\) unstable", debian_changelog, re.MULTILINE)
    assert versions, "expected le-vibe stanzas in debian/changelog"
    for version in versions:
        heading = f"## [{version}]"
        assert heading in changelog_md, (
            f"CHANGELOG.md missing `{heading}` — fold debian/changelog into Keep a Changelog "
            f"(docs/apt-repo-releases.md *Dual changelog discipline*)."
        )


def test_changelog_md_documents_independent_ide_debian_changelog_h1():
    """H1: root CHANGELOG names packaging/debian-le-vibe-ide/debian/changelog vs stack debian/changelog."""
    root = _repo_root()
    changelog_md = (root / "CHANGELOG.md").read_text(encoding="utf-8")
    assert "packaging/debian-le-vibe-ide/debian/changelog" in changelog_md
    assert "dpkg-parsechangelog -S Version -l packaging/debian-le-vibe-ide/debian/changelog" in changelog_md
    assert "docs/apt-repo-releases.md" in changelog_md


def test_changelog_md_points_at_step14_verify_closeout_after_full_product_debs():
    """STEP 14 / H1: maintainers see verify-step14-closeout.sh when both .deb artifacts exist (manifest close-out path)."""
    root = _repo_root()
    changelog_md = (root / "CHANGELOG.md").read_text(encoding="utf-8")
    assert "packaging/scripts/verify-step14-closeout.sh --require-stack-deb" in changelog_md
    assert "docs/PM_DEB_BUILD_ITERATION.md" in changelog_md
