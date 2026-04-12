"""Contract: editor/print-*-codium-path.sh — tarball / VSCode-linux layout (STEP 14.f)."""

from __future__ import annotations

import subprocess
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _bash_n(rel: str) -> None:
    script = _repo_root() / rel
    assert script.is_file(), script
    subprocess.run(["bash", "-n", str(script)], check=True, capture_output=True)


def test_print_vsbuild_and_ci_tarball_scripts_bash_syntax() -> None:
    _bash_n("editor/print-vsbuild-codium-path.sh")
    _bash_n("editor/print-ci-tarball-codium-path.sh")


def test_print_vsbuild_codium_path_documents_14f():
    text = (_repo_root() / "editor" / "print-vsbuild-codium-path.sh").read_text(encoding="utf-8")
    assert "14.f" in text
    assert "realpath not on PATH" in text
    assert "not a directory:" in text
    assert "git submodule update --init editor/vscodium" in text
    assert "Fresh clone (14.b)" in text
    assert "VSCode-linux-" in text
    assert "vscodium-linux-build.tar.gz" in text
    assert "linux_compile" in text or "BUILD.md" in text


def test_print_ci_tarball_codium_path_documents_14f():
    text = (_repo_root() / "editor" / "print-ci-tarball-codium-path.sh").read_text(encoding="utf-8")
    assert "14.f" in text
    assert "not a regular file:" in text
    assert "realpath not on PATH" in text
    assert "tar not on PATH" in text
    assert "tar extract failed" in text
    assert "mktemp failed" in text
    assert "exactly one argument" in text
    assert "git submodule update --init editor/vscodium" in text
    assert "Fresh clone (14.b)" in text
    assert "vscodium-linux-build.tar.gz" in text
    assert "VSCode-linux-" in text
    assert ".zip" in text
    assert "unzip first" in text
    assert "GitHub Actions" in text
