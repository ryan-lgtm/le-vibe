"""Contract: docs/apt-repo-releases.md keeps H1 release story (STEP 8)."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_apt_repo_releases_doc_lists_ci_artifact_and_changelog():
    text = (_repo_root() / "docs" / "apt-repo-releases.md").read_text(encoding="utf-8")
    assert "le-vibe-deb" in text
    assert "SHA256SUMS" in text
    assert "ci.yml" in text
    assert "debian/changelog" in text
    assert "CHANGELOG.md" in text
    assert "H1" in text or "Roadmap H1" in text
