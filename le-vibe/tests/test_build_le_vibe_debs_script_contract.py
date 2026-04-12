"""packaging/scripts/build-le-vibe-debs.sh — bash syntax (PM_DEB_BUILD_ITERATION.md)."""

from __future__ import annotations

import subprocess
from pathlib import Path


def test_build_le_vibe_debs_script_bash_syntax():
    root = Path(__file__).resolve().parents[2]
    script = root / "packaging" / "scripts" / "build-le-vibe-debs.sh"
    assert script.is_file()
    subprocess.run(["bash", "-n", str(script)], check=True)


def test_build_le_vibe_debs_script_header_documents_ci_vs_with_ide_step14():
    """STEP 14 / §7.3: one-shot script header ties ci.yml le-vibe-deb to optional --with-ide."""
    root = Path(__file__).resolve().parents[2]
    text = (root / "packaging" / "scripts" / "build-le-vibe-debs.sh").read_text(encoding="utf-8")
    assert "le-vibe-deb" in text
    assert "apt-repo-releases.md" in text
    assert "IDE package" in text


def test_build_le_vibe_debs_script_mentions_submodule_14b():
    root = Path(__file__).resolve().parents[2]
    text = (root / "packaging" / "scripts" / "build-le-vibe-debs.sh").read_text(encoding="utf-8")
    assert "git submodule update --init editor/vscodium" in text
    assert "Fresh clone (14.b)" in text
    assert "could not locate le-vibe_*.deb" in text
    assert "fix errors above" in text
    assert "could not locate le-vibe-ide_*.deb" in text
    assert "14.c" in text
    assert "find not on PATH" in text
    assert "sort not on PATH" in text
    assert "head not on PATH" in text
    assert "apt-get not on PATH" in text
    assert "build-le-vibe-ide-deb.sh" in text
    assert "LEVIBE_IDE_LINTIAN_STRICT" in text


def test_pm_deb_build_iteration_doc_submodule_prereq_14b():
    root = Path(__file__).resolve().parents[2]
    text = (root / "docs" / "PM_DEB_BUILD_ITERATION.md").read_text(encoding="utf-8")
    assert "git submodule update --init editor/vscodium" in text
    assert "Fresh clone (14.b" in text


def test_pm_deb_build_iteration_doc_releases_h1_step14_pointer():
    """STEP 14 / §7.3: PM deb doc points at apt-repo-releases for dual-.deb demo + H1 checksums."""
    root = Path(__file__).resolve().parents[2]
    text = (root / "docs" / "PM_DEB_BUILD_ITERATION.md").read_text(encoding="utf-8")
    assert "apt-repo-releases.md" in text
    assert "le-vibe-ide_*_amd64.deb" in text
    assert "le-vibe-deb" in text
    assert "SHA256SUMS" in text
    assert "PM_STAGE_MAP.md" in text
    assert "H1 vs §7.3 .deb bundles" in text
    assert "spec-phase2.md" in text
    assert "CI `le-vibe-deb` vs maintainer `le-vibe-ide`" in text


def test_print_pm_deb_build_prompt_extractable():
    root = Path(__file__).resolve().parents[2]
    text = (root / "docs" / "PM_DEB_BUILD_ITERATION.md").read_text(encoding="utf-8")
    fence: str | None = None
    for part in text.split("```"):
        if part.lstrip().startswith("You are the Lé Vibe **packaging / .deb build**"):
            fence = part
            break
    assert fence is not None
    assert "build-le-vibe-debs.sh" in fence
    assert "LÉ VIBE PACKAGING COMPLETE" in fence
