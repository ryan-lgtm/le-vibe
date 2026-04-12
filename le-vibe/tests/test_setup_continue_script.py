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


def test_setup_continue_requires_bash_readlink_documented() -> None:
    text = (_repo_root() / "packaging" / "bin" / "le-vibe-setup-continue").read_text(encoding="utf-8")
    assert "bash not on PATH" in text
    assert "readlink not on PATH" in text


def test_setup_continue_header_documents_ci_le_vibe_deb_vs_ide_deb_step14() -> None:
    """STEP 14 / §7.3: setup-continue wrapper keeps same H1 trust line as other packaging/bin stubs."""
    text = (_repo_root() / "packaging" / "bin" / "le-vibe-setup-continue").read_text(encoding="utf-8")
    assert "le-vibe-deb" in text
    assert "apt-repo-releases.md" in text
    assert "IDE package" in text
    assert "PM_STAGE_MAP.md" in text
    assert "H1 vs §7.3 .deb bundles" in text
