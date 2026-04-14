"""Contract: docs/README.md lists LOCAL_INSTALL_ONE_SHOT + install-le-vibe-local.sh."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_docs_readme_local_install_one_shot_row():
    text = (_repo_root() / "docs" / "README.md").read_text(encoding="utf-8")
    assert "| [`LOCAL_INSTALL_ONE_SHOT.md`]" in text
    assert "install-le-vibe-local.sh" in text
    assert "SHIP_REPORT_LOCAL_INSTALL.md" in text
