"""Contract: probe-vscode-linux-build.sh matches ide_packaging_paths (STEP 14 / 14.c)."""

from __future__ import annotations

import subprocess
from pathlib import Path

from le_vibe.ide_packaging_paths import vscode_linux_build_status


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_probe_vscode_linux_build_script_exists_bash_syntax_and_help() -> None:
    script = _repo_root() / "packaging" / "scripts" / "probe-vscode-linux-build.sh"
    assert script.is_file(), script
    assert script.stat().st_mode & 0o111, "script should be executable"
    subprocess.run(["bash", "-n", str(script)], check=True, capture_output=True)
    r = subprocess.run(
        [str(script), "--help"],
        cwd=str(_repo_root()),
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0
    out = f"{r.stdout}\n{r.stderr}"
    assert "Usage" in out
    assert "ready" in out and "partial" in out
    assert "print-step14-vscode-linux-bin-files.sh" in out
    assert "vscode_linux_bin_files" in out


def test_probe_vscode_linux_build_matches_python_classifier() -> None:
    root = _repo_root()
    script = root / "packaging" / "scripts" / "probe-vscode-linux-build.sh"
    py_st, _ = vscode_linux_build_status(root)
    r = subprocess.run(
        [str(script), str(root)],
        cwd=str(root),
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0
    assert r.stdout.strip() == py_st
