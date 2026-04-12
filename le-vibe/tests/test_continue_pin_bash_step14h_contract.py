"""Contract: packaging/scripts verify/sync Continue helpers — STEP 14.h (with H4 pin)."""

from __future__ import annotations

import subprocess
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _bash_n(rel: str) -> None:
    script = _repo_root() / rel
    assert script.is_file(), script
    subprocess.run(["bash", "-n", str(script)], check=True, capture_output=True)


def test_verify_continue_pin_and_sync_continue_config_bash_syntax() -> None:
    _bash_n("packaging/scripts/verify-continue-pin.sh")
    _bash_n("packaging/scripts/sync-continue-config.sh")


def test_sync_continue_config_script_documents_missing_generated_yaml():
    text = (_repo_root() / "packaging" / "scripts" / "sync-continue-config.sh").read_text(
        encoding="utf-8"
    )
    assert "le-vibe/README.md" in text
    assert "PRODUCT_SPEC §5" in text or "PRODUCT_SPEC §5–§8" in text
    assert "~/.config/le-vibe/" in text


def test_verify_continue_pin_script_documents_pin_file():
    text = (_repo_root() / "packaging" / "scripts" / "verify-continue-pin.sh").read_text(
        encoding="utf-8"
    )
    assert "continue-openvsx-version" in text
    assert "restore packaging/continue-openvsx-version from git" in text
    assert "add one semver line" in text
    assert "continue-extension-pin.md" in text


def test_continue_extension_pin_doc_has_step_14h_block():
    text = (_repo_root() / "docs" / "continue-extension-pin.md").read_text(encoding="utf-8")
    assert "STEP 14.h" in text
    assert "install-continue-extension.sh" in text
