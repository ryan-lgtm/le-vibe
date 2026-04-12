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


def test_check_linux_vscodium_build_deps_matches_ci_apt_list() -> None:
    text = (
        _repo_root() / "packaging" / "scripts" / "check-linux-vscodium-build-deps.sh"
    ).read_text(encoding="utf-8")
    assert "build-le-vibe-ide.yml" in text
    assert "libxkbfile-dev" in text
    assert "python3.11-dev" in text
    assert "pkg-config --exists xkbfile" in text
    assert "DEBS=(" in text
