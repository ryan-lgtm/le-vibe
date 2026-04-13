"""Contract: docs/README.md apt-repo-releases row ties H1 to STEP 14 / §7.3 le-vibe-ide demo path."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_docs_readme_apt_repo_releases_row_lists_step14_ide_deb_path():
    text = (_repo_root() / "docs" / "README.md").read_text(encoding="utf-8")
    assert "| [`apt-repo-releases.md`]" in text
    assert "STEP 14" in text
    assert "§7.3" in text
    assert "le-vibe-ide" in text
    assert "packaging/debian-le-vibe-ide/" in text
    assert "build-le-vibe-ide-deb.sh" in text
    assert "build-le-vibe-debs.sh --with-ide" in text
    assert "PM_DEB_BUILD_ITERATION.md" in text
    assert "Full-product install" in text
    assert "verify-step14-closeout.sh --require-stack-deb" in text
    assert "--apt-sim" in text
    assert "--json" in text
    assert "apt_sim_note" in text
    assert "manual-step14-install-smoke.sh" in text
    assert "build machine" in text
    assert "test host" in text
    assert "Success output (`--with-ide`)" in text
    assert "debian-le-vibe-ide/README.md" in text
    assert "Install both packages" in text
    assert "PM_STAGE_MAP.md" in text
    assert "H1 vs §7.3 .deb bundles" in text
