"""Contract: build-le-vibe-ide.yml keeps ide-ci-metadata LE_VIBE_EDITOR docs pointer (STEP 14 / H6)."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_build_le_vibe_ide_workflow_writes_le_vibe_editor_docs_to_metadata():
    text = (_repo_root() / ".github" / "workflows" / "build-le-vibe-ide.yml").read_text(encoding="utf-8")
    assert "ide-ci-metadata.txt" in text
    assert "le_vibe_editor_docs=editor/README.md" in text
    assert "GITHUB_STEP_SUMMARY" in text
    assert "**Pre-binary artifact:**" in text
    assert "LE_VIBE_EDITOR" in text
    assert "retention-days:" in text
    assert "permissions:" in text
    assert "contents: read" in text
    assert "actions: write" in text
