"""Contract: packaging/applications/le-vibe.desktop — template Freedesktop entry (STEP 14 / §7.3)."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_packaging_applications_le_vibe_desktop_documents_pytest_verify_lock() -> None:
    desktop = _repo_root() / "packaging" / "applications" / "le-vibe.desktop"
    assert desktop.is_file(), desktop
    text = desktop.read_text(encoding="utf-8")
    assert "[Desktop Entry]" in text
    assert "Name=Lé Vibe" in text
    assert "test_packaging_applications_desktop_step14_contract.py" in text
    assert "test_verify_step14_closeout_contract.py" in text
    assert ".pytest-verify-step14-contract.lock" in text
