"""Contract: packaging/bin/* sh stubs require python3 on PATH before exec."""

from __future__ import annotations

import subprocess
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_lvibe_bin_header_documents_ci_le_vibe_deb_vs_ide_deb_step14() -> None:
    """STEP 14 / §7.3: lvibe wrapper trust header matches H1 stack vs IDE .deb story."""
    root = _repo_root()
    text = (root / "packaging/bin/lvibe").read_text(encoding="utf-8")
    assert "0 → 1 → 14 → 2–13 → 15–17" in text
    assert "PROMPT_BUILD_LE_VIBE.md" in text
    assert "le-vibe-deb" in text
    assert "build-le-vibe-debs.sh --with-ide" in text
    assert "Full-product install" in text
    assert "PM_DEB_BUILD_ITERATION.md" in text
    assert "apt-repo-releases.md" in text
    assert "IDE package" in text
    assert "PM_STAGE_MAP.md" in text
    assert "H1 vs §7.3 .deb bundles" in text


def test_le_vibe_bin_header_documents_ci_le_vibe_deb_vs_ide_deb_step14() -> None:
    """STEP 14 / §7.3: le-vibe alias wrapper keeps same H1 / §7.3 trust line as lvibe."""
    root = _repo_root()
    text = (root / "packaging/bin/le-vibe").read_text(encoding="utf-8")
    assert "0 → 1 → 14 → 2–13 → 15–17" in text
    assert "PROMPT_BUILD_LE_VIBE.md" in text
    assert "le-vibe-deb" in text
    assert "build-le-vibe-debs.sh --with-ide" in text
    assert "Full-product install" in text
    assert "PM_DEB_BUILD_ITERATION.md" in text
    assert "apt-repo-releases.md" in text
    assert "IDE package" in text
    assert "PM_STAGE_MAP.md" in text
    assert "H1 vs §7.3 .deb bundles" in text


def test_lvibe_hygiene_bin_header_documents_ci_le_vibe_deb_vs_ide_deb_step14() -> None:
    """STEP 14 / §7.3: lvibe-hygiene wrapper keeps same H1 trust line as lvibe."""
    root = _repo_root()
    text = (root / "packaging/bin/lvibe-hygiene").read_text(encoding="utf-8")
    assert "0 → 1 → 14 → 2–13 → 15–17" in text
    assert "PROMPT_BUILD_LE_VIBE.md" in text
    assert "le-vibe-deb" in text
    assert "build-le-vibe-debs.sh --with-ide" in text
    assert "Full-product install" in text
    assert "PM_DEB_BUILD_ITERATION.md" in text
    assert "apt-repo-releases.md" in text
    assert "IDE package" in text
    assert "PM_STAGE_MAP.md" in text
    assert "H1 vs §7.3 .deb bundles" in text


def test_packaging_bin_sh_launchers_syntax_and_python3_guard() -> None:
    root = _repo_root()
    for rel, needle in (
        ("packaging/bin/le-vibe", "le-vibe: python3 not on PATH"),
        ("packaging/bin/lvibe", "lvibe: python3 not on PATH"),
        ("packaging/bin/lvibe-hygiene", "lvibe-hygiene: python3 not on PATH"),
    ):
        script = root / rel
        assert script.is_file(), script
        subprocess.run(["sh", "-n", str(script)], check=True, capture_output=True)
        text = script.read_text(encoding="utf-8")
        assert needle in text
        assert "Requires: python3 on PATH" in text
