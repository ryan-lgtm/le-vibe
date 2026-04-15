"""Sanity checks for G-A3 Continue setup autostart helper."""

from __future__ import annotations

import subprocess
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_continue_autostart_bash_syntax() -> None:
    script = _repo_root() / "packaging" / "scripts" / "le-vibe-continue-setup-autostart.sh"
    assert script.is_file(), script
    subprocess.run(["bash", "-n", str(script)], check=True, capture_output=True)


def test_continue_autostart_documents_mkdir_touch_path_checks() -> None:
    text = (
        _repo_root() / "packaging" / "scripts" / "le-vibe-continue-setup-autostart.sh"
    ).read_text(encoding="utf-8")
    assert "0 → 1 → 14 → 2–13 → 15–17" in text
    assert "PROMPT_BUILD_LE_VIBE.md" in text
    assert "PM_STAGE_MAP.md" in text
    assert "mkdir not on PATH" in text
    assert "touch not on PATH" in text
    assert "continue_setup_auto" in text
    assert "next lvibe launch tries" in text
    assert "test_continue_autostart_script.py" in text
    assert "test_verify_step14_closeout_contract.py" in text
    assert ".pytest-verify-step14-contract.lock" in text


def test_continue_autostart_desktop_exists() -> None:
    desktop = _repo_root() / "packaging" / "autostart" / "le-vibe-continue-setup.desktop"
    assert desktop.is_file()
    text = desktop.read_text(encoding="utf-8")
    assert "le-vibe-continue-setup-autostart.sh" in text
    assert "etc/xdg/autostart" not in text  # installed path is Exec= under /usr/share
    assert "test_continue_autostart_script.py" in text
    assert "test_verify_step14_closeout_contract.py" in text
    assert ".pytest-verify-step14-contract.lock" in text
