"""Sanity checks for packaging/bin/le-vibe-setup-continue (G-A2 GUI + exit codes)."""

from __future__ import annotations

import subprocess
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_setup_continue_script_bash_syntax() -> None:
    script = _repo_root() / "packaging" / "bin" / "le-vibe-setup-continue"
    assert script.is_file(), script
    subprocess.run(["bash", "-n", str(script)], check=True, capture_output=True)


def test_setup_continue_help_exits_zero() -> None:
    script = _repo_root() / "packaging" / "bin" / "le-vibe-setup-continue"
    r = subprocess.run(
        ["bash", str(script), "--help"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0
    assert "--gui" in r.stdout


def test_setup_continue_short_help_matches_long_help() -> None:
    script = _repo_root() / "packaging" / "bin" / "le-vibe-setup-continue"
    rh = subprocess.run(
        ["bash", str(script), "-h"],
        check=False,
        capture_output=True,
        text=True,
    )
    rhelp = subprocess.run(
        ["bash", str(script), "--help"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert rh.returncode == 0 and rhelp.returncode == 0
    assert rh.stdout == rhelp.stdout


def test_setup_continue_unknown_option_exit_125() -> None:
    script = _repo_root() / "packaging" / "bin" / "le-vibe-setup-continue"
    r = subprocess.run(
        ["bash", str(script), "--not-a-real-flag"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert r.returncode == 125
    assert "unknown option" in r.stderr


def test_setup_continue_gui_requires_zenity_exit_127_documented() -> None:
    """--gui path must fail with 127 when zenity is unavailable (see script stderr)."""
    text = (_repo_root() / "packaging" / "bin" / "le-vibe-setup-continue").read_text(
        encoding="utf-8"
    )
    assert "command -v zenity" in text
    assert "[exit 127]" in text
    assert "--gui requires zenity" in text
