"""Contract: debian/le-vibe.README.Debian documents launcher order (STEP 14.g)."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_debian_readme_documents_default_editor_resolution_14g():
    text = (_repo_root() / "debian" / "le-vibe.README.Debian").read_text(encoding="utf-8")
    assert "14.g" in text
    assert "_default_editor" in text
    assert "le-vibe/le_vibe/launcher.py" in text
    assert "LE_VIBE_EDITOR" in text
    assert "/usr/bin/le-vibe-ide" in text
    assert "/usr/bin/codium" in text
    assert "Recommends: codium" in text
    assert "debian/control" in text
