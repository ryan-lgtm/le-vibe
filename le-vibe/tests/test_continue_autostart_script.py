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


def test_continue_autostart_desktop_exists() -> None:
    desktop = _repo_root() / "packaging" / "autostart" / "le-vibe-continue-setup.desktop"
    assert desktop.is_file()
    text = desktop.read_text(encoding="utf-8")
    assert "le-vibe-continue-setup-autostart.sh" in text
    assert "etc/xdg/autostart" not in text  # installed path is Exec= under /usr/share
