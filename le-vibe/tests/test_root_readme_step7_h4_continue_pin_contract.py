"""Contract: root README lists STEP 7 / H4 Continue Open VSX pin (Roadmap H4)."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_root_readme_step7_h4_continue_pin_section():
    text = (_repo_root() / "README.md").read_text(encoding="utf-8")
    assert "### Continue extension pin — STEP 7 / H4" in text
    assert "Master orchestrator STEP 7" in text
    assert "continue-openvsx-version" in text
    assert "verify-continue-pin.sh" in text
    assert "install-continue-extension.sh" in text
    assert "continue-extension-pin.md" in text
    assert "test_continue_openvsx_pin.py" in text
