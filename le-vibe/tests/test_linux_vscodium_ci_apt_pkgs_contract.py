"""Contract: packaging/linux-vscodium-ci-apt.pkgs — single source for CI + local STEP 14.e."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_linux_vscodium_ci_apt_pkgs_matches_workflow_intent():
    p = _repo_root() / "packaging" / "linux-vscodium-ci-apt.pkgs"
    text = p.read_text(encoding="utf-8")
    assert "build-le-vibe-ide.yml" in text
    for pkg in (
        "build-essential",
        "libxkbfile-dev",
        "python3.11-dev",
        "librsvg2-bin",
        "jq",
        "pkg-config",
    ):
        assert pkg in text, pkg
