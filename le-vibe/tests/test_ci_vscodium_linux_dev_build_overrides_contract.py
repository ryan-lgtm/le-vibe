"""Contract: linux compile wrapper sources optional editor/le-vibe-overrides/build-env.sh."""

from __future__ import annotations

import subprocess
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_ci_vscodium_linux_dev_build_documents_overrides_hook():
    text = (_repo_root() / "packaging" / "scripts" / "ci-vscodium-linux-dev-build.sh").read_text(encoding="utf-8")
    assert "git submodule update --init editor/vscodium" in text
    assert "Fresh clone (14.b)" in text
    assert "restore from git" in text
    assert "must match editor/vscodium/.nvmrc" in text
    assert "le-vibe-overrides/build-env.sh" in text
    assert "build-env.lvibe-defaults.sh" in text
    assert "product-branding-merge.json" in text
    assert "sync-linux-icon-assets.sh" in text
    assert "APP_NAME:-VSCodium" in text
    assert "§7.3" in text
    assert "dev/build.sh" in text
    assert "build-env.sh.example" in text or "build-env.sh" in text
    assert "14.a" in text
    assert "editor/.nvmrc" in text
    assert "LEVIBE_SKIP_NODE_VERSION_CHECK" in text
    assert "node --version" in text


def test_ci_vscodium_linux_dev_build_script_bash_syntax() -> None:
    script = _repo_root() / "packaging" / "scripts" / "ci-vscodium-linux-dev-build.sh"
    assert script.is_file(), script
    subprocess.run(["bash", "-n", str(script)], check=True, capture_output=True)
