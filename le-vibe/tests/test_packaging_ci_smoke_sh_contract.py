"""Contract: packaging/scripts/ci-smoke.sh — STEP 10 + STEP 14 / H6 after pytest."""

from __future__ import annotations

import subprocess
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_packaging_ci_smoke_sh_bash_syntax() -> None:
    script = _repo_root() / "packaging" / "scripts" / "ci-smoke.sh"
    assert script.is_file(), script
    subprocess.run(["bash", "-n", str(script)], check=True, capture_output=True)


def test_packaging_ci_smoke_sh_documents_step14_gate_and_submodule_14b():
    text = (_repo_root() / "packaging" / "scripts" / "ci-smoke.sh").read_text(encoding="utf-8")
    assert "STEP 14" in text and "H6" in text
    assert "ci-editor-gate.sh" in text
    assert "git submodule update --init editor/vscodium" in text
    assert "Fresh clone (14.b)" in text
    assert "ci-qa-hardening.md" in text
    assert "find not on PATH" in text
    assert "mktemp not on PATH" in text
    assert "python3 not on PATH" in text


def test_packaging_ci_smoke_sh_header_lists_le_vibe_deb_stack_only_step14():
    """STEP 14 / §7.3: smoke script header matches ci.yml — le-vibe-deb artifact excludes le-vibe-ide."""
    text = (_repo_root() / "packaging" / "scripts" / "ci-smoke.sh").read_text(encoding="utf-8")
    assert "le-vibe-deb" in text
    assert "not le-vibe-ide" in text
    assert "build-le-vibe-debs.sh --with-ide" in text
    assert "apt-repo-releases.md" in text
