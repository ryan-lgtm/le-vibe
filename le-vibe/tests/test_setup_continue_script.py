"""Sanity checks for packaging/bin/le-vibe-setup-cline."""

from __future__ import annotations

import subprocess
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_setup_continue_script_bash_syntax() -> None:
    script = _repo_root() / "packaging" / "bin" / "le-vibe-setup-cline"
    assert script.is_file(), script
    subprocess.run(["bash", "-n", str(script)], check=True, capture_output=True)


def test_setup_continue_help_exits_zero() -> None:
    script = _repo_root() / "packaging" / "bin" / "le-vibe-setup-cline"
    r = subprocess.run(
        ["bash", str(script), "--help"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0
    assert "Usage: le-vibe-setup-cline" in r.stdout


def test_setup_continue_short_help_matches_long_help() -> None:
    script = _repo_root() / "packaging" / "bin" / "le-vibe-setup-cline"
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
    script = _repo_root() / "packaging" / "bin" / "le-vibe-setup-cline"
    r = subprocess.run(
        ["bash", str(script), "--not-a-real-flag"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert r.returncode == 125
    assert "unknown option" in r.stderr


def test_setup_continue_cline_installer_contract() -> None:
    text = (_repo_root() / "packaging" / "bin" / "le-vibe-setup-cline").read_text(encoding="utf-8")
    assert "install-cline-extension.sh" in text
    assert "install Cline + Red Hat YAML extensions" in text
    assert "Extension install failed (Cline or YAML" in text


def test_setup_continue_requires_bash_readlink_documented() -> None:
    text = (_repo_root() / "packaging" / "bin" / "le-vibe-setup-cline").read_text(encoding="utf-8")
    assert "readlink not on PATH" in text


def test_debian_le_vibe_setup_continue_man_documents_dual_extension_and_auto() -> None:
    """debian/le-vibe-setup-cline.1 matches install-cline-extension.sh (H4) + launcher auto."""
    text = (_repo_root() / "debian" / "le-vibe-setup-cline.1").read_text(encoding="utf-8")
    assert "saoudrizwan.claude-dev" in text
    assert "redhat.vscode\\-yaml" in text
    assert "LE_VIBE_AUTO_CLINE_SETUP" in text
    assert "continue\\-extension\\-pin.md" in text


def test_setup_continue_header_documents_ci_le_vibe_deb_vs_ide_deb_step14() -> None:
    """STEP 14 / §7.3: setup-cline wrapper documents Cline install flow."""
    text = (_repo_root() / "packaging" / "bin" / "le-vibe-setup-cline").read_text(encoding="utf-8")
    assert "install-cline-extension.sh" in text
    assert "No editor binary" in text
