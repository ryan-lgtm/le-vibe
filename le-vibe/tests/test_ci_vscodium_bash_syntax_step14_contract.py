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
    assert "STEP 14" in text
    assert "get_repo.sh" in text
    assert "ci-editor-gate" in text
    assert "editor/vscodium" in text
