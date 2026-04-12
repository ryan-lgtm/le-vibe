"""Contract: .github/dependabot.yml header stays aligned with ci.yml H1 / STEP 14 scope."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_dependabot_yml_header_documents_le_vibe_deb_stack_only_step14():
    """STEP 14 / §7.3: Dependabot header matches ci.yml — le-vibe-deb excludes le-vibe-ide."""
    text = (_repo_root() / ".github" / "dependabot.yml").read_text(encoding="utf-8")
    assert "le-vibe-deb" in text
    assert "not le-vibe-ide" in text
    assert "apt-repo-releases.md" in text
