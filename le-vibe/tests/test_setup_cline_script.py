"""Sanity checks for packaging/bin/le-vibe-setup-cline."""

from __future__ import annotations

import subprocess
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_setup_cline_script_exists_and_bash_syntax() -> None:
    script = _repo_root() / "packaging" / "bin" / "le-vibe-setup-cline"
    assert script.is_file(), script
    subprocess.run(["bash", "-n", str(script)], check=True, capture_output=True)


def test_setup_cline_script_uses_cline_installer() -> None:
    text = (_repo_root() / "packaging" / "bin" / "le-vibe-setup-cline").read_text(encoding="utf-8")
    assert "install-cline-extension.sh" in text
    assert "LE_VIBE_EDITOR" in text
    assert "le-vibe-setup-cline: [exit 0] Done." in text
