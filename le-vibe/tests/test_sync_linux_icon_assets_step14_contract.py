"""Contract: sync-linux-icon-assets.sh + workflow dep for §7.3 Linux icons."""

from __future__ import annotations

import subprocess
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_sync_linux_icon_assets_script_bash_syntax() -> None:
    script = _repo_root() / "editor" / "le-vibe-overrides" / "sync-linux-icon-assets.sh"
    assert script.is_file(), script
    subprocess.run(["bash", "-n", str(script)], check=True, capture_output=True)


def test_sync_linux_icon_assets_documents_14b():
    text = (
        _repo_root() / "editor" / "le-vibe-overrides" / "sync-linux-icon-assets.sh"
    ).read_text(encoding="utf-8")
    assert "§7.3" in text
    assert "ci-vscodium-linux-dev-build.sh" in text
    assert "src/stable/resources/linux" in text
    assert "expected editor/vscodium/product.json" in text
    assert "packaging/icons/hicolor/scalable/apps/le-vibe.svg" in text
    assert "git submodule update --init editor/vscodium" in text
    assert "Fresh clone (14.b)" in text
    assert "sudo apt install librsvg2-bin" in text
    assert "sudo apt install imagemagick" in text
    assert "restore packaging/icons from git" in text
    assert "mkdir not on PATH" in text
    assert "cp not on PATH" in text
    assert "Usage:" in text
    assert "--help" in text
    assert "--check" in text


def test_build_le_vibe_ide_linux_compile_installs_librsvg_for_icon_sync():
    wf = (_repo_root() / ".github" / "workflows" / "build-le-vibe-ide.yml").read_text(encoding="utf-8")
    assert "linux-vscodium-ci-apt.pkgs" in wf
    pkgs = (_repo_root() / "packaging" / "linux-vscodium-ci-apt.pkgs").read_text(encoding="utf-8")
    assert "librsvg2-bin" in pkgs
