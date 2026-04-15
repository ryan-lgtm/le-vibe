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
    assert "0 → 1 → 14 → 2–13 → 15–17" in text
    assert "PROMPT_BUILD_LE_VIBE.md" in text
    assert "PM_STAGE_MAP.md" in text
    assert "STEP 14.h" in text
    assert "continue-config.yaml" in text
    assert "le-vibe: missing" in text
    assert "le-vibe/README.md" in text
    assert "PRODUCT_SPEC §5" in text or "PRODUCT_SPEC §5–§8" in text
    assert "~/.config/le-vibe/" in text
    assert "mkdir not on PATH" in text
    assert "cp not on PATH" in text
    assert "ln not on PATH" in text
    assert "realpath not on PATH" in text
    assert "readlink not on PATH" in text
    assert "ln -sfn" in text
    assert "config.yaml.bak" in text or ".bak" in text
    assert "test_continue_pin_bash_step14h_contract.py" in text
    assert "test_verify_step14_closeout_contract.py" in text
    assert ".pytest-verify-step14-contract.lock" in text


def test_verify_continue_pin_script_documents_pin_file():
    text = (_repo_root() / "packaging" / "scripts" / "verify-continue-pin.sh").read_text(
        encoding="utf-8"
    )
    assert "0 → 1 → 14 → 2–13 → 15–17" in text
    assert "PROMPT_BUILD_LE_VIBE.md" in text
    assert "PM_STAGE_MAP.md" in text
    assert "STEP 14.h" in text
    assert "continue-openvsx-version" in text
    assert "vscode-yaml-openvsx-version" in text
    assert "restore from git" in text
    assert "add one semver line" in text
    assert "no non-comment version line" in text
    assert "expected semver" in text
    assert "verify-continue-pin: OK" in text
    assert "continue-extension-pin.md" in text
    assert "grep not on PATH" in text
    assert "head not on PATH" in text
    assert "tr not on PATH" in text
    assert "test_continue_pin_bash_step14h_contract.py" in text
    assert "test_verify_step14_closeout_contract.py" in text
    assert ".pytest-verify-step14-contract.lock" in text


def test_continue_extension_pin_doc_has_step_14h_block():
    text = (_repo_root() / "docs" / "continue-extension-pin.md").read_text(encoding="utf-8")
    assert "STEP 14.h" in text
    assert "install-continue-extension.sh" in text
