"""Contract: print-step14-vscode-linux-bin-files.sh — single source for partial bin/ listing (STEP 14)."""

from __future__ import annotations

import subprocess
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_print_step14_vscode_linux_bin_files_script_exists_and_bash_syntax() -> None:
    script = _repo_root() / "packaging" / "scripts" / "print-step14-vscode-linux-bin-files.sh"
    assert script.is_file(), script
    assert script.stat().st_mode & 0o111, "script should be executable"
    subprocess.run(["bash", "-n", str(script)], check=True, capture_output=True)


def test_print_step14_vscode_linux_bin_files_uses_ide_packaging_paths() -> None:
    text = (
        _repo_root() / "packaging" / "scripts" / "print-step14-vscode-linux-bin-files.sh"
    ).read_text(encoding="utf-8")
    assert "ide_packaging_paths" in text
    assert "vscode_linux_build_status" in text
    assert "vscode_linux_bin_filenames" in text
    assert "--help" in text
    assert "probe-vscode-linux-build.sh" in text
    assert "ide-prereqs" in text
    assert "vscode_linux_bin_files" in text
    assert "print-github-linux-compile-artifact-hint.sh" in text
    assert "install-vscodium-linux-tarball-to-editor-vendor.sh" in text


def test_print_step14_vscode_linux_bin_files_help_stdout() -> None:
    script = _repo_root() / "packaging" / "scripts" / "print-step14-vscode-linux-bin-files.sh"
    r = subprocess.run(
        [str(script), "--help"],
        cwd=str(_repo_root()),
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0
    out = f"{r.stdout}\n{r.stderr}"
    assert "Usage:" in out
    assert "print-step14-vscode-linux-bin-files.sh" in out
    assert "print-github-linux-compile-artifact-hint.sh" in out
    assert "install-vscodium-linux-tarball-to-editor-vendor.sh" in out
