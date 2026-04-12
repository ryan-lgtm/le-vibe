"""Contract: docs/vscodium-fork-le-vibe.md keeps §7.2 branding + overrides pointers (STEP 14.d)."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_vscodium_fork_doc_branding_section_honesty_and_overrides():
    text = (_repo_root() / "docs" / "vscodium-fork-le-vibe.md").read_text(encoding="utf-8")
    assert "Branding & overrides" in text
    assert "14.d" in text
    assert "§7.2" in text
    assert "editor/le-vibe-overrides/README.md" in text
    assert "spec-phase2.md" in text and "§14" in text
    assert "USER RESPONSE REQUIRED" in text
    assert "CHANGELOG.md" in text
    assert "14.f" in text
    assert "editor/BUILD.md" in text
    assert "VSCode-linux-" in text
    assert "vscodium-linux-build.tar.gz" in text
    assert "14.g" in text
    assert "le-vibe.README.Debian" in text
    assert "build-env.sh.example" in text
    assert "ci-vscodium-linux-dev-build.sh" in text
    assert "fetch-vscode-sources.sh" in text
    assert "print-built-codium-path.sh" in text
    assert "smoke-lvibe-editor.sh" in text


def test_vscodium_fork_doc_installable_tree_14f():
    text = (_repo_root() / "docs" / "vscodium-fork-le-vibe.md").read_text(encoding="utf-8")
    assert "Tarball / installable tree (14.f)" in text
    assert "VSCode-linux-" in text and "bin/codium" in text
    assert "vscodium-linux-build.tar.gz" in text
    assert "linux_compile" in text
    assert "Installable layout" in text


def test_vscodium_fork_doc_release_smoke_checklist_14i():
    text = (_repo_root() / "docs" / "vscodium-fork-le-vibe.md").read_text(encoding="utf-8")
    assert "Release smoke checklist (14.i)" in text
    assert "14.i" in text
    assert "./editor/smoke.sh" in text
    assert "smoke-lvibe-editor.sh" in text
    assert "verify-continue-pin.sh" in text
    assert "vscodium_linux_compile" in text
    assert "le-vibe-setup-continue" in text
    assert "11435" in text
    assert "python3 -m pytest tests/" in text
    assert "dpkg-buildpackage" in text
    assert "debian/changelog" in text
    assert "vscodium-linux-build.tar.gz" in text
    assert "continue-config.yaml" in text
    assert "continue-extension-pin.md" in text
    assert "ci-editor-gate" in text
    assert "layout=vscodium" in text
