"""STEP 4 — `.lvibe/WELCOME.md` from product template (PRODUCT_SPEC §4)."""

from __future__ import annotations

from pathlib import Path

from le_vibe.editor_welcome import WELCOME_MD_NAME, ensure_lvibe_welcome_md


def test_ensure_lvibe_welcome_md_writes_template_once(tmp_path: Path):
    p = ensure_lvibe_welcome_md(tmp_path)
    assert p is not None
    dest = tmp_path / ".lvibe" / WELCOME_MD_NAME
    assert dest == p
    assert dest.is_file()
    text = dest.read_text(encoding="utf-8")
    assert "Welcome to Lé Vibe" in text
    assert "PRODUCT_SPEC.md" in text and "§4" in text
    assert ensure_lvibe_welcome_md(tmp_path) is None


def test_ensure_lvibe_welcome_md_preserves_user_edits(tmp_path: Path):
    ensure_lvibe_welcome_md(tmp_path)
    dest = tmp_path / ".lvibe" / WELCOME_MD_NAME
    dest.write_text("# User override\n", encoding="utf-8")
    assert ensure_lvibe_welcome_md(tmp_path) is None
    assert dest.read_text(encoding="utf-8").startswith("# User override")
