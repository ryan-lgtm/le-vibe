"""packaging/scripts/build-le-vibe-debs.sh — bash syntax (PM_DEB_BUILD_ITERATION.md)."""

from __future__ import annotations

import subprocess
from pathlib import Path


def test_build_le_vibe_debs_script_bash_syntax():
    root = Path(__file__).resolve().parents[2]
    script = root / "packaging" / "scripts" / "build-le-vibe-debs.sh"
    assert script.is_file()
    subprocess.run(["bash", "-n", str(script)], check=True)


def test_build_le_vibe_debs_script_mentions_submodule_14b():
    root = Path(__file__).resolve().parents[2]
    text = (root / "packaging" / "scripts" / "build-le-vibe-debs.sh").read_text(encoding="utf-8")
    assert "git submodule update --init editor/vscodium" in text
    assert "Fresh clone (14.b)" in text


def test_pm_deb_build_iteration_doc_submodule_prereq_14b():
    root = Path(__file__).resolve().parents[2]
    text = (root / "docs" / "PM_DEB_BUILD_ITERATION.md").read_text(encoding="utf-8")
    assert "git submodule update --init editor/vscodium" in text
    assert "Fresh clone (14.b" in text


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
