"""Contract: packaging/scripts/check-linux-vscodium-build-deps.sh — CI parity preflight (STEP 14.e)."""

from __future__ import annotations

import subprocess
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_check_linux_vscodium_build_deps_script_bash_syntax() -> None:
    script = _repo_root() / "packaging" / "scripts" / "check-linux-vscodium-build-deps.sh"
    assert script.is_file(), script
    assert script.stat().st_mode & 0o111, "script should be executable"
    subprocess.run(["bash", "-n", str(script)], check=True, capture_output=True)


def test_install_linux_vscodium_build_deps_script_bash_syntax() -> None:
    script = _repo_root() / "packaging" / "scripts" / "install-linux-vscodium-build-deps.sh"
    assert script.is_file(), script
    assert script.stat().st_mode & 0o111, "script should be executable"
    subprocess.run(["bash", "-n", str(script)], check=True, capture_output=True)
    text = script.read_text(encoding="utf-8")
    assert "0 → 1 → 14 → 2–13 → 15–17" in text
    assert "PROMPT_BUILD_LE_VIBE.md" in text
    assert "PM_STAGE_MAP.md" in text
    assert "EUID" in text
    assert "_apt" in text
    assert "--print-install-command" in text
    assert "sudo -n true" in text
    assert "interactive password" in text
    assert "test_check_linux_vscodium_build_deps_contract.py" in text
    assert "test_verify_step14_closeout_contract.py" in text
    assert ".pytest-verify-step14-contract.lock" in text


def test_check_linux_vscodium_build_deps_matches_ci_apt_list() -> None:
    text = (
        _repo_root() / "packaging" / "scripts" / "check-linux-vscodium-build-deps.sh"
    ).read_text(encoding="utf-8")
    assert "0 → 1 → 14 → 2–13 → 15–17" in text
    assert "PROMPT_BUILD_LE_VIBE.md" in text
    assert "PM_STAGE_MAP.md" in text
    assert "linux-vscodium-ci-apt.pkgs" in text
    assert "install-linux-vscodium-build-deps.sh" in text
    assert "--print-install-command" in text
    assert "libxkbfile-dev" in text
    assert "_python_dev_headers_ok" in text
    assert "python3.12-dev" in text
    assert "python3.11-dev" in text
    assert "pkg-config --exists xkbfile" in text
    assert "DEBS+=(" in text
    assert "test_check_linux_vscodium_build_deps_contract.py" in text
    assert "test_verify_step14_closeout_contract.py" in text
    assert ".pytest-verify-step14-contract.lock" in text
