"""Contract: docker-le-vibe-vscodium-linux-compile.sh — full linux compile in Docker (STEP 14.e)."""

from __future__ import annotations

import subprocess
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_docker_le_vibe_vscodium_linux_compile_script_bash_syntax() -> None:
    script = _repo_root() / "packaging" / "scripts" / "docker-le-vibe-vscodium-linux-compile.sh"
    assert script.is_file(), script
    assert script.stat().st_mode & 0o111, "script should be executable"
    subprocess.run(["bash", "-n", str(script)], check=True, capture_output=True)
    text = script.read_text(encoding="utf-8")
    assert "linux-vscodium-ci-apt.pkgs" in text
    assert "ci-vscodium-linux-dev-build.sh" in text
    assert "rustup.rs" in text
    assert "nvm.sh" in text
    assert "max-old-space-size=8192" in text
    assert "LEVIBE_DOCKER_COMPILE_CARGO_VOLUME" in text
    assert "ci-qa-hardening.md" in text
    assert "Optional full Linux compile" in text
