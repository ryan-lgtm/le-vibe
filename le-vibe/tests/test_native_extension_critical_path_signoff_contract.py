"""Contract: native-extension critical path ends with CP6 Product / Eng / QA sign-off (task-cp6-3)."""

from __future__ import annotations

from pathlib import Path


def _workflow_text() -> str:
    root = Path(__file__).resolve().parents[2]
    path = root / "le-vibe" / "templates" / "workflows" / "native-extension-critical-path.md"
    return path.read_text(encoding="utf-8")


def test_native_extension_critical_path_has_cp6_track_complete_signoff_block() -> None:
    text = _workflow_text()
    assert "CP6 — Track complete (product freeze sign-off)" in text
    assert "**`track complete`:**" in text
    assert "| Product |" in text
    assert "| Engineering |" in text
    assert "| QA |" in text
    assert "Sign-off (name or handle)" in text
