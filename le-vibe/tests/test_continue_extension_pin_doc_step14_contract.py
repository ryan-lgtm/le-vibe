"""Contract: docs/continue-extension-pin.md keeps STEP 14.h + LE_VIBE_EDITOR pin story."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_continue_extension_pin_doc_step14_h_strings():
    text = (_repo_root() / "docs" / "continue-extension-pin.md").read_text(encoding="utf-8")
    assert "14.h" in text
    assert "LE_VIBE_EDITOR" in text
    assert "install-continue-extension.sh" in text
    assert "continue-openvsx-version" in text
    assert "le-vibe-setup-continue" in text
    assert "editor/BUILD.md" in text
