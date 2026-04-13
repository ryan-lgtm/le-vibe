"""Contract: docs/continue-extension-pin.md keeps STEP 14.h + LE_VIBE_EDITOR pin story."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_continue_extension_pin_doc_step14_h_strings():
    text = (_repo_root() / "docs" / "continue-extension-pin.md").read_text(encoding="utf-8")
    assert "git submodule update --init editor/vscodium" in text
    assert "Fresh clone (14.b)" in text
    assert "### STEP 14.h" in text
    assert "14.h" in text
    assert "LE_VIBE_EDITOR" in text
    assert "install-continue-extension.sh" in text
    assert "continue-openvsx-version" in text
    assert "le-vibe-setup-continue" in text
    assert "editor/BUILD.md" in text
    assert "verify-continue-pin.sh" in text
    assert "sync-continue-config.sh" in text
    assert "VSCode-linux-" in text
    assert "print-built-codium-path.sh" in text
    assert "print-vsbuild-codium-path.sh" in text
    assert "print-ci-tarball-codium-path.sh" in text
    assert "print-step14-vscode-linux-bin-files.sh" in text
    assert "probe-vscode-linux-build.sh" in text
    assert "verify-14c-local-binary.sh" in text
    assert "_default_editor" in text
    assert "14.g" in text
    assert ".zip" in text
    assert "linux_compile" in text
    assert "branding-staging.checklist.md" in text
    assert "§7.2" in text
    assert "§7.3" in text
