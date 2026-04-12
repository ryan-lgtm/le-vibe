"""Contract: editor/README.md keeps launcher resolution order aligned with le_vibe.launcher (14.g)."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_editor_readme_lists_le_vibe_ide_before_codium():
    text = (_repo_root() / "editor" / "README.md").read_text(encoding="utf-8")
    assert "14.g" in text
    assert "le-vibe/le_vibe/launcher.py" in text
    assert "/usr/lib/le-vibe/bin/codium" in text
    assert "/usr/bin/codium" in text
    pos_ide = text.index("/usr/lib/le-vibe/bin/codium")
    pos_cod = text.index("/usr/bin/codium")
    assert pos_ide < pos_cod


def test_editor_readme_documents_persisting_le_vibe_editor_14g():
    text = (_repo_root() / "editor" / "README.md").read_text(encoding="utf-8")
    assert "Persisting `LE_VIBE_EDITOR`" in text
    assert "environment.d" in text
    assert "debian/le-vibe.README.Debian" in text
