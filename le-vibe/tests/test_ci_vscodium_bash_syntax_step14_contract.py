"""Contract: packaging/scripts/ci-vscodium-bash-syntax.sh — upstream script bash -n (STEP 14)."""

from __future__ import annotations

import subprocess
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_ci_vscodium_bash_syntax_helper_script_bash_syntax() -> None:
    script = _repo_root() / "packaging" / "scripts" / "ci-vscodium-bash-syntax.sh"
    assert script.is_file(), script
    subprocess.run(["bash", "-n", str(script)], check=True, capture_output=True)


def test_ci_vscodium_bash_syntax_documents_step14_and_upstream_scripts():
    text = (
        _repo_root() / "packaging" / "scripts" / "ci-vscodium-bash-syntax.sh"
    ).read_text(encoding="utf-8")
    assert "--help" in text
    assert "unexpected argument" in text
    assert "exit 2" in text
    assert "0 → 1 → 14 → 2–13 → 15–17" in text
    assert "PROMPT_BUILD_LE_VIBE.md" in text
    assert "PM_STAGE_MAP.md" in text
    assert "git submodule update --init editor/vscodium" in text
    assert "Fresh clone (14.b)" in text
    assert "STEP 14" in text
    assert "get_repo.sh" in text
    assert "ci-editor-gate" in text
    assert "editor/vscodium" in text
    assert "repair editor/vscodium" in text
    assert "bash not on PATH" in text
    # Core path toward a Linux build — keep list in sync with script (short upstream bash -n set)
    assert 'scripts=(' in text
    assert "build.sh" in text
    assert "build_cli.sh" in text
    assert "prepare_src.sh" in text
    assert "prepare_vscode.sh" in text
    assert 'bash -n "$p"' in text
    assert "ci-vscodium-bash-syntax: OK" in text
