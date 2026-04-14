"""Contract: probe-vscode-linux-build.sh + probe_vscode_linux_build.py match ide_packaging_paths (14.c)."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

from le_vibe.ide_packaging_paths import vscode_linux_build_status, vscode_linux_compile_gate_progress


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _probe_py() -> Path:
    return _repo_root() / "packaging" / "scripts" / "probe_vscode_linux_build.py"


def test_probe_vscode_linux_build_py_docstring_documents_verify_contract() -> None:
    text = _probe_py().read_text(encoding="utf-8")
    assert "test_probe_vscode_linux_build_script_contract.py" in text
    assert "test_verify_step14_closeout_contract.py" in text
    assert ".pytest-verify-step14-contract.lock" in text


def test_probe_vscode_linux_build_py_compiles_and_help_lists_json_keys() -> None:
    py = _probe_py()
    assert py.is_file(), py
    subprocess.run([sys.executable, "-m", "py_compile", str(py)], check=True, capture_output=True)
    r = subprocess.run(
        [sys.executable, str(py), "-h"],
        cwd=str(_repo_root()),
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0
    out = f"{r.stdout}\n{r.stderr}"
    assert "vscode_linux_build" in out
    assert "--json" in out and "--progress" in out
    assert "print-github-linux-compile-artifact-hint.sh" in out
    assert "preflight-step14-closeout.sh" in out


def test_probe_vscode_linux_build_py_default_stdout_matches_ide_packaging_paths() -> None:
    root = _repo_root()
    py_st, _ = vscode_linux_build_status(root)
    r = subprocess.run(
        [sys.executable, str(_probe_py()), str(root)],
        cwd=str(root),
        capture_output=True,
        text=True,
        env={**os.environ, "PYTHONPATH": str(root / "le-vibe")},
    )
    assert r.returncode == 0
    assert r.stdout.strip() == py_st
    direct = vscode_linux_compile_gate_progress(root)
    rj = subprocess.run(
        [sys.executable, str(_probe_py()), "--json", str(root)],
        cwd=str(root),
        capture_output=True,
        text=True,
        env={**os.environ, "PYTHONPATH": str(root / "le-vibe")},
    )
    assert rj.returncode == 0
    data = json.loads(rj.stdout)
    assert data["vscode_linux_build"] == direct["vscode_linux_build"]
    assert int(data["compile_gate_pct"]) == int(direct["compile_gate_pct"])


def test_probe_vscode_linux_build_sh_documents_pytest_verify_lock() -> None:
    text = (_repo_root() / "packaging" / "scripts" / "probe-vscode-linux-build.sh").read_text(encoding="utf-8")
    assert "test_probe_vscode_linux_build_script_contract.py" in text
    assert "test_verify_step14_closeout_contract.py" in text
    assert ".pytest-verify-step14-contract.lock" in text


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
    assert "print-github-linux-compile-artifact-hint.sh" in out
    assert "trigger-le-vibe-ide-linux-compile.sh" in out
    assert "download-vscodium-linux-compile-artifact.sh" in out
    assert "install-vscodium-linux-tarball-to-editor-vendor.sh" in out
    assert "preflight-step14-closeout.sh" in out
    assert "vscode_linux_bin_files" in out
    assert "--progress" in out
    assert "--json" in out
    assert "compile_gate_pct" in out
    assert "vscode_linux_path" in out


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


def test_probe_vscode_linux_build_progress_lists_pct() -> None:
    root = _repo_root()
    script = root / "packaging" / "scripts" / "probe-vscode-linux-build.sh"
    r = subprocess.run(
        [str(script), "--progress", str(root)],
        cwd=str(root),
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0
    out = f"{r.stdout}\n{r.stderr}"
    assert "compile_gate_pct:" in out
    assert "vscode_linux_build:" in out
    assert "Linux compile gate" in out


def test_probe_vscode_linux_build_json_has_milestones() -> None:
    root = _repo_root()
    script = root / "packaging" / "scripts" / "probe-vscode-linux-build.sh"
    r = subprocess.run(
        [str(script), "--json", str(root)],
        cwd=str(root),
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0
    data = json.loads(r.stdout)
    assert "compile_gate_pct" in data
    assert "compile_gate_milestones" in data
    assert "vscode_linux_path" in data
    assert data["vscode_linux_build"] in ("ready", "partial", "absent")
