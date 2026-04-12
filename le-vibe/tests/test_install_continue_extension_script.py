"""Sanity checks for packaging/scripts/install-continue-extension.sh (H4 pin)."""

from __future__ import annotations

import subprocess
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_install_continue_extension_bash_syntax() -> None:
    script = _repo_root() / "packaging" / "scripts" / "install-continue-extension.sh"
    assert script.is_file(), script
    subprocess.run(["bash", "-n", str(script)], check=True, capture_output=True)


def test_install_continue_extension_header_points_at_pin_doc_and_pm_map() -> None:
    script = _repo_root() / "packaging" / "scripts" / "install-continue-extension.sh"
    head = "\n".join(script.read_text(encoding="utf-8").splitlines()[:12])
    assert "continue-extension-pin.md" in head
    assert "PM_STAGE_MAP" in head or "STEP 7" in head


def test_install_continue_extension_documents_pin_path_tool_checks() -> None:
    text = (_repo_root() / "packaging" / "scripts" / "install-continue-extension.sh").read_text(
        encoding="utf-8"
    )
    assert "grep not on PATH" in text
    assert "head not on PATH" in text
    assert "tr not on PATH" in text


def test_continue_openvsx_pin_file_exists_and_semver() -> None:
    pin = _repo_root() / "packaging" / "continue-openvsx-version"
    assert pin.is_file(), pin
    first = pin.read_text(encoding="utf-8").strip().splitlines()[0].strip()
    assert first and first != "latest"
    parts = first.split(".")
    assert len(parts) >= 2
    assert all(p.isdigit() for p in parts)
