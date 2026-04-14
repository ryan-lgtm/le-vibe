"""Contract: editor/smoke.sh — repo-root IDE smoke gate (STEP 14; same as ci-editor-gate / workflows)."""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_editor_smoke_sh_bash_syntax() -> None:
    script = _repo_root() / "editor" / "smoke.sh"
    assert script.is_file(), script
    subprocess.run(["bash", "-n", str(script)], check=True, capture_output=True)


def test_editor_smoke_sh_header_documents_le_vibe_deb_vs_ide_deb_step14():
    """STEP 14: repo-root smoke header states H1 CI scope vs maintainer IDE .deb."""
    text = (_repo_root() / "editor" / "smoke.sh").read_text(encoding="utf-8")
    assert "0 → 1 → 14 → 2–13 → 15–17" in text
    assert "PROMPT_BUILD_LE_VIBE.md" in text
    assert "PM_STAGE_MAP.md" in text
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
    assert "--help" in text
    assert "unexpected argument" in text
    assert "0 → 1 → 14 → 2–13 → 15–17" in text
    assert "PROMPT_BUILD_LE_VIBE.md" in text
    assert "PM_STAGE_MAP.md" in text
    assert "§7.3" in text
    assert "ide-prereqs" in text
    assert "ci-editor-gate" in text
    assert "LEVIBE_EDITOR_GATE_ASSERT_BRAND" in text
    assert "exit 2" in text
    assert "static_prereq_files_ok" in text
    assert "sync-linux-icon-assets.sh --check" in text
    assert "mktemp" in text


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


@pytest.mark.parametrize(
    "relative",
    [
        "editor/smoke.sh",
        "editor/le-vibe-overrides/sync-linux-icon-assets.sh",
        "editor/print-built-codium-path.sh",
        "editor/verify-14c-local-binary.sh",
        "editor/smoke-lvibe-editor.sh",
        "editor/print-vsbuild-codium-path.sh",
        "editor/print-ci-tarball-codium-path.sh",
        "editor/smoke-built-codium-lvibe.sh",
        "editor/verify-73-maintainer.sh",
        "editor/use-node-toolchain.sh",
        "editor/fetch-vscode-sources.sh",
    ],
)
def test_editor_step14_scripts_document_pytest_verify_lock(relative: str) -> None:
    """STEP 14 editor/ helpers link pytest + verify-step14 JSON contract + flock (same as packaging/scripts)."""
    text = (_repo_root() / relative).read_text(encoding="utf-8")
    assert "test_editor_smoke_sh_step14_contract.py" in text
    assert "test_verify_step14_closeout_contract.py" in text
    assert ".pytest-verify-step14-contract.lock" in text
