"""Sanity checks for packaging/scripts/install-cline-extension.sh."""

from __future__ import annotations

import subprocess
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_install_cline_extension_bash_syntax() -> None:
    script = _repo_root() / "packaging" / "scripts" / "install-cline-extension.sh"
    assert script.is_file(), script
    subprocess.run(["bash", "-n", str(script)], check=True, capture_output=True)


def test_install_cline_extension_contract_strings() -> None:
    text = (_repo_root() / "packaging" / "scripts" / "install-cline-extension.sh").read_text(
        encoding="utf-8"
    )
    assert "saoudrizwan.claude-dev" in text
    assert "redhat.vscode-yaml" in text
    assert "LE_VIBE_CLINE_PIN_FILE" in text
    assert "LE_VIBE_CLINE_OPENVSX_VERSION" in text
    assert "LE_VIBE_VSCODE_YAML_PIN_FILE" in text
    assert "LE_VIBE_VSCODE_YAML_OPENVSX_VERSION" in text
    assert "LE_VIBE_CLINE_INSTALL_ATTEMPTS" in text
    assert "LE_VIBE_DISALLOWED_CONTINUE_EXTENSION" in text
    assert "LE_VIBE_CLEANUP_CONTINUE_STATE" in text
    assert "--uninstall-extension" in text
    assert "continue.continue" in text
    assert "--install-extension" in text


def test_cline_openvsx_pin_file_exists_and_semver() -> None:
    pin = _repo_root() / "packaging" / "cline-openvsx-version"
    assert pin.is_file(), pin
    lines = [
        ln.strip()
        for ln in pin.read_text(encoding="utf-8").splitlines()
        if ln.strip() and not ln.strip().startswith("#")
    ]
    assert lines, pin
    first = lines[0]
    assert first != "latest"
    parts = first.split(".")
    assert len(parts) >= 2
    assert all(p.isdigit() for p in parts)
