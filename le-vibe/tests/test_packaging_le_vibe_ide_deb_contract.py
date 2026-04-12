"""Contract: packaging/debian-le-vibe-ide exists for PRODUCT_SPEC §7.3 IDE .deb."""

from __future__ import annotations

import subprocess
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_stage_le_vibe_ide_deb_script_header_documents_h1_vs_ci_step14():
    """STEP 14: staging script header matches ci.yml stack-only vs maintainer IDE .deb."""
    root = _repo_root()
    text = (root / "packaging" / "scripts" / "stage-le-vibe-ide-deb.sh").read_text(encoding="utf-8")
    assert "le-vibe-deb" in text
    assert "apt-repo-releases.md" in text
    assert "build-le-vibe-debs.sh --with-ide" in text


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
    assert "no VSCode-linux-* under editor/vscodium" in text
    assert "PM_STAGE_MAP.md" in text
    assert "H1 vs §7.3 .deb bundles" in text
    assert "find not on PATH" in text
    assert "basename not on PATH" in text
    assert "rm not on PATH" in text
    assert "mkdir not on PATH" in text
    assert "cp not on PATH" in text
    assert "ln not on PATH" in text
    assert "install not on PATH" in text
    assert "ln -sfn" in text
    assert "usr/share/applications/le-vibe.desktop" in text
    assert "resources/app/product.json" in text
    assert "LEVIBE_STAGE_IDE_ASSERT_BRAND" in text
    assert "LEVIBE_STAGE_IDE_VERBOSE" in text
    assert "ci-vscodium-linux-dev-build.sh" in text
    assert "stage-le-vibe-ide-deb: staged" in text
    subprocess.run(["bash", "-n", str(script)], check=True, capture_output=True)


def test_build_le_vibe_ide_deb_script_header_documents_h1_vs_ci_step14():
    """STEP 14: IDE .deb script header states out-of-band vs ci.yml le-vibe-deb."""
    root = _repo_root()
    text = (root / "packaging" / "scripts" / "build-le-vibe-ide-deb.sh").read_text(encoding="utf-8")
    assert "le-vibe-deb" in text
    assert "apt-repo-releases.md" in text
    assert "build-le-vibe-debs.sh --with-ide" in text


def test_build_le_vibe_ide_deb_script_documents_14b_and_bash_syntax():
    root = _repo_root()
    script = root / "packaging" / "scripts" / "build-le-vibe-ide-deb.sh"
    text = script.read_text(encoding="utf-8")
    assert "LEVIBE_STAGE_IDE_ASSERT_BRAND" in text
    assert "LEVIBE_STAGE_IDE_VERBOSE" in text
    assert "git submodule update --init editor/vscodium" in text
    assert "Fresh clone (14.b)" in text
    assert "stage-le-vibe-ide-deb.sh" in text
    assert "expected packaging/le-vibe-ide_*.deb" in text
    assert "PM_STAGE_MAP.md" in text
    assert "H1 vs §7.3 .deb bundles" in text
    assert "dpkg-buildpackage not on PATH" in text
    assert "lintian" in text
    assert "LEVIBE_IDE_LINTIAN_STRICT" in text
    assert "ci-qa-hardening.md" in text
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
    assert "lvibe" in readme
    assert "VSCode-linux-" in readme
    assert "dev/build.sh" in readme
    assert "stage-le-vibe-ide-deb.sh" in readme
    assert "build-le-vibe-ide-deb.sh" in readme
    assert "applications" in readme.lower()
    assert "roadmap" in readme.lower() and "apt-repo-releases" in readme
    assert "build-le-vibe-debs.sh --with-ide" in readme
    assert "PM_DEB_BUILD_ITERATION.md" in readme
    assert "SHA256SUMS" in readme
    assert "PM_STAGE_MAP.md" in readme
    assert "H1 vs §7.3 .deb bundles" in readme
    assert "LEVIBE_STAGE_IDE_ASSERT_BRAND" in readme
    assert "LEVIBE_STAGE_IDE_VERBOSE" in readme
    assert "resources/app/product.json" in readme
    assert "spec-phase2.md" in readme
    assert "CI `le-vibe-deb` vs maintainer `le-vibe-ide`" in readme
    assert "## Install both packages" in readme
    assert "sudo apt install ./le-vibe_" in readme
    assert "/usr/share/doc/le-vibe/README.Debian" in readme
    desktop = (root / "packaging" / "debian-le-vibe-ide" / "debian" / "le-vibe.desktop").read_text(
        encoding="utf-8"
    )
    assert "Lé Vibe" in desktop
    assert "GenericName=" in desktop
    assert "Exec=/usr/lib/le-vibe/bin/codium" in desktop
    assert "Icon=le-vibe" in desktop
    install = (root / "packaging" / "debian-le-vibe-ide" / "debian" / "le-vibe-ide.install").read_text(
        encoding="utf-8"
    )
    assert "usr/share/applications/le-vibe.desktop" in install
    assert "le-vibe.svg" in install
    rules = (root / "packaging" / "debian-le-vibe-ide" / "debian" / "rules").read_text(encoding="utf-8")
    assert "staging/usr/share/applications/le-vibe.desktop" in rules
