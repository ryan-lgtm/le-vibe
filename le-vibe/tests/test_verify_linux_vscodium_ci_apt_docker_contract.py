"""Contract: verify-linux-vscodium-ci-apt-docker.sh — optional CI-parity check without host sudo (STEP 14.e)."""

from __future__ import annotations

import subprocess
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_verify_linux_vscodium_ci_apt_docker_script_bash_syntax() -> None:
    script = _repo_root() / "packaging" / "scripts" / "verify-linux-vscodium-ci-apt-docker.sh"
    assert script.is_file(), script
    assert script.stat().st_mode & 0o111, "script should be executable"
    subprocess.run(["bash", "-n", str(script)], check=True, capture_output=True)
    text = script.read_text(encoding="utf-8")
    assert "0 → 1 → 14 → 2–13 → 15–17" in text
    assert "PROMPT_BUILD_LE_VIBE.md" in text
    assert "PM_STAGE_MAP.md" in text
    assert "linux-vscodium-ci-apt.pkgs" in text
    assert "ubuntu:22.04" in text or "LEVIBE_VERIFY_APT_DOCKER_IMAGE" in text
