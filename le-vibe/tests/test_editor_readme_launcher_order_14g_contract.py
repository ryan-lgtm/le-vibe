"""Contract: editor/README.md keeps launcher resolution order aligned with le_vibe.launcher (14.g)."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_editor_readme_lists_le_vibe_ide_before_codium():
    text = (_repo_root() / "editor" / "README.md").read_text(encoding="utf-8")
    assert "14.g" in text
    assert "le-vibe/le_vibe/launcher.py" in text
    assert "/usr/bin/le-vibe-ide" in text
    assert "/usr/bin/codium" in text
    pos_ide = text.index("/usr/bin/le-vibe-ide")
    pos_cod = text.index("/usr/bin/codium")
    assert pos_ide < pos_cod
