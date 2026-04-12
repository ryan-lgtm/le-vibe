"""Contract: editor/.nvmrc stays aligned with editor/vscodium/.nvmrc (STEP 14.a / ci-editor-nvmrc-sync.sh)."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_editor_nvmrc_matches_vscodium_when_submodule_present():
    root = _repo_root()
    vscodium_nvmrc = root / "editor" / "vscodium" / ".nvmrc"
    editor_nvmrc = root / "editor" / ".nvmrc"
    if not vscodium_nvmrc.is_file():
        return
    assert editor_nvmrc.is_file(), "editor/.nvmrc must exist when editor/vscodium/.nvmrc exists"
    assert (
        editor_nvmrc.read_text(encoding="utf-8").strip()
        == vscodium_nvmrc.read_text(encoding="utf-8").strip()
    ), "run packaging/scripts/ci-editor-nvmrc-sync.sh — editor/.nvmrc must match editor/vscodium/.nvmrc"


def test_ci_editor_nvmrc_sync_script_contract():
    text = (_repo_root() / "packaging" / "scripts" / "ci-editor-nvmrc-sync.sh").read_text(encoding="utf-8")
    assert "editor/.nvmrc" in text
    assert "editor/vscodium/.nvmrc" in text
    assert "cmp" in text
