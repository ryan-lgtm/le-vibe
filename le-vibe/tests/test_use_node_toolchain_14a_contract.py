"""Contract: editor/use-node-toolchain.sh + .nvmrc parity — STEP 14.a."""

from __future__ import annotations

import subprocess
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_use_node_toolchain_script_bash_syntax() -> None:
    script = _repo_root() / "editor" / "use-node-toolchain.sh"
    assert script.is_file(), script
    subprocess.run(["bash", "-n", str(script)], check=True, capture_output=True)


def test_use_node_toolchain_script_documents_14a_nvmrc():
    text = (_repo_root() / "editor" / "use-node-toolchain.sh").read_text(encoding="utf-8")
    assert "0 → 1 → 14 → 2–13 → 15–17" in text
    assert "PROMPT_BUILD_LE_VIBE.md" in text
    assert "PM_STAGE_MAP.md" in text
    assert "git submodule update --init editor/vscodium" in text
    assert "Fresh clone (14.b)" in text
    assert "restore from git" in text
    assert "ci-editor-nvmrc-sync.sh" in text
    assert "14.a" in text
    assert ".nvmrc" in text
    assert "ci-editor-nvmrc-sync" in text or "vscodium/.nvmrc" in text
    assert "command -v node" in text
    assert "node not on PATH after nvm" in text
    assert "stderr" in text.lower()


def test_ci_editor_nvmrc_sync_script_bash_syntax() -> None:
    script = _repo_root() / "packaging" / "scripts" / "ci-editor-nvmrc-sync.sh"
    assert script.is_file(), script
    subprocess.run(["bash", "-n", str(script)], check=True, capture_output=True)


def test_editor_nvmrc_matches_vscodium_when_submodule_present():
    root = _repo_root()
    if not (root / "editor" / "vscodium" / "product.json").is_file():
        return
    a = (root / "editor" / ".nvmrc").read_text(encoding="utf-8")
    b = (root / "editor" / "vscodium" / ".nvmrc").read_text(encoding="utf-8")
    assert a == b, "editor/.nvmrc must match editor/vscodium/.nvmrc (14.a)"
