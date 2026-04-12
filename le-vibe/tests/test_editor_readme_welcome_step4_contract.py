"""Contract: editor/README.md documents §4 workspace welcome (STEP 4 / E3)."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_editor_readme_step4_welcome_not_terminal_only():
    text = (_repo_root() / "editor" / "README.md").read_text(encoding="utf-8")
    assert "PRODUCT_SPEC §4" in text
    assert "STEP 4" in text
    assert ".lvibe/WELCOME.md" in text
    assert "lvibe-editor-welcome.md" in text
    assert "**not** terminal-only" in text
