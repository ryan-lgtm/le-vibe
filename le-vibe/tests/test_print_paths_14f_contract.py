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
    assert "0 → 1 → 14 → 2–13 → 15–17" in text
    assert "PROMPT_BUILD_LE_VIBE.md" in text
    assert "PM_STAGE_MAP.md" in text
    assert "14.f" in text
    assert "14.c" in text
    assert "no VSCode-linux-*/bin/codium under" in text
    assert "bin/codium is missing" in text
    assert "partial or incomplete build" in text
    assert "./dev/build.sh" in text
    assert "stat not on PATH" in text
    assert "realpath not on PATH" in text
    assert "not a directory:" in text
    assert "git submodule update --init editor/vscodium" in text
    assert "Fresh clone (14.b)" in text
    assert "VSCode-linux-" in text
    assert "vscodium-linux-build.tar.gz" in text
    assert "install-vscodium-linux-tarball-to-editor-vendor.sh" in text
    assert "print-github-linux-compile-artifact-hint.sh" in text
    assert "linux_compile" in text or "BUILD.md" in text


def test_print_ci_tarball_codium_path_documents_14f():
    text = (_repo_root() / "editor" / "print-ci-tarball-codium-path.sh").read_text(encoding="utf-8")
    assert "--help" in text
    assert "-h" in text
    assert "0 → 1 → 14 → 2–13 → 15–17" in text
    assert "PROMPT_BUILD_LE_VIBE.md" in text
    assert "PM_STAGE_MAP.md" in text
    assert "14.f" in text
    assert "LE_VIBE_EDITOR" in text
    assert 'exec "${ROOT}/editor/print-vsbuild-codium-path.sh"' in text
    assert "linux_compile" in text
    assert "not a regular file:" in text
    assert "realpath not on PATH" in text
    assert "tar not on PATH" in text
    assert "tar extract failed" in text
    assert "mktemp not on PATH" in text
    assert "mktemp failed" in text
    assert "find not on PATH" in text
    assert "extract produced no files" in text
    assert "exactly one argument" in text
    assert "git submodule update --init editor/vscodium" in text
    assert "Fresh clone (14.b)" in text
    assert "vscodium-linux-build.tar.gz" in text
    assert "VSCode-linux-" in text
    assert ".zip" in text
    assert "unzip first" in text
    assert "GitHub Actions" in text
