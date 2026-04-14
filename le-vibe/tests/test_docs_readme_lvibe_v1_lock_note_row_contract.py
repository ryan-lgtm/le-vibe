"""Contract: docs/README.md lists LVIBE_V1_LOCK_NOTE as the `.lvibe/` v1 freeze artifact."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_docs_readme_lists_lvibe_v1_lock_note_row() -> None:
    text = (_repo_root() / "docs" / "README.md").read_text(encoding="utf-8")
    assert "| [`LVIBE_V1_LOCK_NOTE.md`]" in text
    assert ".lvibe" in text
    assert "v1" in text


def test_lvibe_v1_lock_note_doc_exists_and_freezes_scope() -> None:
    note = _repo_root() / "docs" / "LVIBE_V1_LOCK_NOTE.md"
    assert note.is_file()
    text = note.read_text(encoding="utf-8")
    assert "v1-locked" in text
    assert "maintenance" in text.lower()
    assert "Out of scope" in text
    assert "PRODUCT_SPEC.md" in text
