"""Contract: editor/fetch-vscode-sources.sh — monorepo get_repo entrypoint (STEP 14.b)."""

from __future__ import annotations

import subprocess
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_fetch_vscode_sources_script_bash_syntax() -> None:
    script = _repo_root() / "editor" / "fetch-vscode-sources.sh"
    assert script.is_file(), script
    subprocess.run(["bash", "-n", str(script)], check=True, capture_output=True)


def test_fetch_vscode_sources_script_documents_14b_get_repo_flow() -> None:
    text = (_repo_root() / "editor" / "fetch-vscode-sources.sh").read_text(encoding="utf-8")
    assert "expected editor/vscodium/" in text
    assert "fetch-vscode-sources: done" in text
    assert "LE_VIBE_EDITOR" in text
    assert "git submodule update --init editor/vscodium" in text
    assert "Fresh clone (14.b)" in text
    assert "differs from" in text
    assert "14.a" in text
    assert "14.b" in text
    assert "get_repo.sh" in text
    assert "set +u" in text and "set -u" in text
    assert "howto-build.md" in text
    assert "use-node-toolchain.sh" in text
    assert "editor/vscodium" in text
    assert "dev/build.sh" in text
    assert "VSCODE_QUALITY" in text and "VSCODE_LATEST" in text and "CI_BUILD" in text
    assert "#build-ci" in text or "build-ci" in text
    assert "cmp not on PATH" in text
    assert "tr not on PATH" in text
