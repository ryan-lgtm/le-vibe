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


def test_ci_editor_gate_header_documents_le_vibe_deb_vs_ide_deb_step14():
    """STEP 14 / §7.3: editor gate header ties H6 smoke to out-of-band IDE .deb builds."""
    text = (_repo_root() / "packaging" / "scripts" / "ci-editor-gate.sh").read_text(encoding="utf-8")
    assert "le-vibe-deb" in text
    assert "apt-repo-releases.md" in text
    assert "build-le-vibe-debs.sh --with-ide" in text
    assert "Full-product install" in text
    assert "PM_DEB_BUILD_ITERATION.md" in text


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
    assert "LEVIBE_EDITOR_GATE_ASSERT_BRAND" in text
    assert "linuxIconName" in text
    assert "brand-assets.md" in text
    assert "product-branding-merge.json" in text
    assert "sync-linux-icon-assets.sh" in text
    assert "src/stable/resources/linux/le-vibe.svg" in text
    assert "usage()" in text or "Usage:" in text
    assert "--help" in text
    assert "bash not on PATH" in text
    # layout=none skip path — engineers must keep the vendoring hint + interim launcher story
    assert "IDE sources not vendored" in text
    assert "LE_VIBE_EDITOR" in text
    assert "editor/VENDORING.md" in text
    # vscodium branch: bash -n inventory must stay aligned with editor helper scripts (14.c / 14.f)
    assert 'bash -n "${ROOT}/editor/smoke-lvibe-editor.sh"' in text
    assert 'bash -n "${ROOT}/editor/verify-14c-local-binary.sh"' in text
    assert 'bash -n "${ROOT}/editor/smoke-built-codium-lvibe.sh"' in text
    assert 'bash -n "${ROOT}/editor/verify-73-maintainer.sh"' in text
    assert 'bash -n "${ROOT}/editor/print-ci-tarball-codium-path.sh"' in text
    assert "ci-vscodium-linux-dev-build.sh" in text
