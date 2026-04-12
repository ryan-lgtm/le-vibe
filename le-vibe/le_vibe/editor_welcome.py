"""In-editor welcome: `.lvibe/WELCOME.md` seeded from the product template (`docs/PRODUCT_SPEC.md` §4)."""

from __future__ import annotations

from pathlib import Path

WELCOME_MD_NAME = "WELCOME.md"


def _welcome_template_path() -> Path:
    return Path(__file__).resolve().parent.parent / "templates" / "lvibe-editor-welcome.md"


def ensure_lvibe_welcome_md(workspace_root: Path) -> Path | None:
    """
    If ``.lvibe/WELCOME.md`` is missing, copy ``templates/lvibe-editor-welcome.md``.
    Idempotent: does not overwrite user edits.
    """
    lvibe = workspace_root / ".lvibe"
    lvibe.mkdir(parents=True, exist_ok=True)
    dest = lvibe / WELCOME_MD_NAME
    if dest.exists():
        return None
    src = _welcome_template_path()
    text = src.read_text(encoding="utf-8")
    dest.write_text(text, encoding="utf-8")
    return dest
