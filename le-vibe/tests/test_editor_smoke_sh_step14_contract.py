"""Contract: editor/smoke.sh — repo-root IDE smoke gate (STEP 14; same as ci-editor-gate / workflows)."""

from __future__ import annotations

import subprocess
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_editor_smoke_sh_bash_syntax() -> None:
    script = _repo_root() / "editor" / "smoke.sh"
    assert script.is_file(), script
    subprocess.run(["bash", "-n", str(script)], check=True, capture_output=True)


def test_editor_smoke_sh_header_documents_le_vibe_deb_vs_ide_deb_step14():
    """STEP 14: repo-root smoke header states H1 CI scope vs maintainer IDE .deb."""
    text = (_repo_root() / "editor" / "smoke.sh").read_text(encoding="utf-8")
    assert "le-vibe-deb" in text
    assert "apt-repo-releases.md" in text
    assert "build-le-vibe-debs.sh --with-ide" in text
    assert "Full-product install" in text
    assert "PM_DEB_BUILD_ITERATION.md" in text


def test_verify_73_maintainer_bash_syntax() -> None:
    script = _repo_root() / "editor" / "verify-73-maintainer.sh"
    assert script.is_file(), script
    subprocess.run(["bash", "-n", str(script)], check=True, capture_output=True)


def test_verify_73_maintainer_header_step14():
    text = (_repo_root() / "editor" / "verify-73-maintainer.sh").read_text(encoding="utf-8")
    assert "§7.3" in text
    assert "ide-prereqs" in text
    assert "ci-editor-gate" in text
    assert "LEVIBE_EDITOR_GATE_ASSERT_BRAND" in text
    assert "static_prereq_files_ok" in text


def test_editor_smoke_sh_delegates_ci_editor_gate():
    text = (_repo_root() / "editor" / "smoke.sh").read_text(encoding="utf-8")
    assert 'exec "${ROOT}/packaging/scripts/ci-editor-gate.sh" "$@"' in text
    assert "git submodule update --init editor/vscodium" in text
    assert "Fresh clone (14.b)" in text
    assert "STEP 14" in text
    assert "ci-editor-gate.sh" in text
    assert "build-le-vibe-ide.yml" in text or "build-linux.yml" in text
    assert "14.d" in text
    assert "branding-staging.checklist.md" in text
