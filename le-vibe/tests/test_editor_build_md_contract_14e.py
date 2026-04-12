"""Contract: editor/BUILD.md keeps 14.e CI compile + tarball artifact pointers."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_editor_build_md_contract_linux_compile_14e():
    text = (_repo_root() / "editor" / "BUILD.md").read_text(encoding="utf-8")
    assert "14.e" in text
    assert "vscodium-linux-build.tar.gz" in text
    assert "le-vibe-vscodium-linux-" in text
    assert "linux_compile" in text
    assert "actions/cache" in text
    assert ".cargo/registry" in text
