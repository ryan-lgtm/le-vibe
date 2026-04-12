"""Contract: editor/vscodium/docs/howto-build.md documents get_repo + dev build (STEP 14.b)."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_howto_build_doc_exists_when_vscodium_submodule_present():
    root = _repo_root()
    if not (root / "editor" / "vscodium" / "product.json").is_file():
        return
    howto = root / "editor" / "vscodium" / "docs" / "howto-build.md"
    assert howto.is_file()
    text = howto.read_text(encoding="utf-8")
    assert "get_repo" in text
    assert "dev/build.sh" in text
    assert "Build for Development" in text or "build-dev" in text
    assert "Build for CI" in text or "build-ci" in text


def test_get_repo_script_exists_when_vscodium_submodule_present():
    root = _repo_root()
    if not (root / "editor" / "vscodium" / "product.json").is_file():
        return
    assert (root / "editor" / "vscodium" / "get_repo.sh").is_file()
