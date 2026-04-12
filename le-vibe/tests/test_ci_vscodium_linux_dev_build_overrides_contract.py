"""Contract: linux compile wrapper sources optional editor/le-vibe-overrides/build-env.sh."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_ci_vscodium_linux_dev_build_documents_overrides_hook():
    text = (_repo_root() / "packaging" / "scripts" / "ci-vscodium-linux-dev-build.sh").read_text(encoding="utf-8")
    assert "le-vibe-overrides/build-env.sh" in text
    assert "dev/build.sh" in text
    assert "build-env.sh.example" in text or "build-env.sh" in text
