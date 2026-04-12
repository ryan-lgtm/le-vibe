"""Contract: packaging/scripts/ci-editor-gate.sh — STEP 14 / H6 IDE layout + bash -n gate."""

from __future__ import annotations

import subprocess
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_ci_editor_gate_script_bash_syntax() -> None:
    script = _repo_root() / "packaging" / "scripts" / "ci-editor-gate.sh"
    assert script.is_file(), script
    subprocess.run(["bash", "-n", str(script)], check=True, capture_output=True)


def test_ci_editor_gate_documents_step14_smoke_and_overrides_e1():
    text = (_repo_root() / "packaging" / "scripts" / "ci-editor-gate.sh").read_text(encoding="utf-8")
    assert "git submodule update --init editor/vscodium" in text
    assert "Fresh clone (14.b)" in text
    assert "STEP 14" in text
    assert "H6" in text
    assert "build-le-vibe-ide.yml" in text
    assert "editor/le-vibe-overrides/README.md" in text
    assert "test_editor_le_vibe_overrides_readme_contract.py" in text
    assert "14.d" in text
    assert "branding-staging.checklist.md" in text
    assert "bash not on PATH" in text
