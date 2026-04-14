"""Contract: root README lists STEP 8 / H1 releases + checksums (Roadmap H1)."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_root_readme_step8_h1_releases_section():
    text = (_repo_root() / "docs" / "MONOREPO_DEVELOPER_REFERENCE.md").read_text(encoding="utf-8")
    assert "### Releases & checksums — STEP 8 / H1" in text
    assert "Master orchestrator STEP 8" in text
    assert "le-vibe-deb" in text
    assert "SHA256SUMS" in text
    assert "apt-repo-releases.md" in text
    assert "lvibe verify-checksums" in text
    assert "test_apt_repo_releases_doc_h1_contract.py" in text
