"""Contract: packaging/debian-le-vibe-ide exists for PRODUCT_SPEC §7.3 IDE .deb."""

from __future__ import annotations

import subprocess
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_stage_le_vibe_ide_deb_script_documents_14b_submodule_and_bash_syntax():
    root = _repo_root()
    script = root / "packaging" / "scripts" / "stage-le-vibe-ide-deb.sh"
    text = script.read_text(encoding="utf-8")
    assert "git submodule update --init editor/vscodium" in text
    assert "Fresh clone (14.b)" in text
    assert "not executable:" in text
    assert "14.c" in text
    assert "restore packaging/debian-le-vibe-ide" in text
    assert "restore packaging/icons from git" in text
    assert "PRODUCT_SPEC §7.3" in text
    subprocess.run(["bash", "-n", str(script)], check=True, capture_output=True)


def test_build_le_vibe_ide_deb_script_documents_14b_and_bash_syntax():
    root = _repo_root()
    script = root / "packaging" / "scripts" / "build-le-vibe-ide-deb.sh"
    text = script.read_text(encoding="utf-8")
    assert "git submodule update --init editor/vscodium" in text
    assert "Fresh clone (14.b)" in text
    assert "stage-le-vibe-ide-deb.sh" in text
    subprocess.run(["bash", "-n", str(script)], check=True, capture_output=True)


def test_debian_le_vibe_ide_control_and_scripts():
    root = _repo_root()
    control = (root / "packaging" / "debian-le-vibe-ide" / "debian" / "control").read_text(encoding="utf-8")
    assert "Package: le-vibe-ide" in control
    assert "/usr/lib/le-vibe/bin/codium" in control
    assert "le-vibe.desktop" in control
    assert "hicolor-icon-theme" in control
    assert "roadmap" in control.lower() and "§7.3" in control
    assert (root / "packaging" / "scripts" / "stage-le-vibe-ide-deb.sh").is_file()
    assert (root / "packaging" / "scripts" / "build-le-vibe-ide-deb.sh").is_file()
    readme = (root / "packaging" / "debian-le-vibe-ide" / "README.md").read_text(encoding="utf-8")
    assert "git submodule update --init editor/vscodium" in readme
    assert "Fresh clone (14.b)" in readme
    assert "§7.3" in readme
    assert "/usr/lib/le-vibe/bin/codium" in readme
    assert "applications" in readme.lower()
    assert "roadmap" in readme.lower() and "apt-repo-releases" in readme
    desktop = (root / "packaging" / "debian-le-vibe-ide" / "debian" / "le-vibe.desktop").read_text(
        encoding="utf-8"
    )
    assert "Lé Vibe" in desktop
    assert "Exec=/usr/lib/le-vibe/bin/codium" in desktop
    assert "Icon=le-vibe" in desktop
    install = (root / "packaging" / "debian-le-vibe-ide" / "debian" / "le-vibe-ide.install").read_text(
        encoding="utf-8"
    )
    assert "usr/share/applications/le-vibe.desktop" in install
    assert "le-vibe.svg" in install
    rules = (root / "packaging" / "debian-le-vibe-ide" / "debian" / "rules").read_text(encoding="utf-8")
    assert "staging/usr/share/applications/le-vibe.desktop" in rules
