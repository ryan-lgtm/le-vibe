"""Contract: docs/README.md STEP14_AUTONOMOUS_ENGINEER_RUNBOOK row lists manifest + icon path."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_docs_readme_step14_autonomous_runbook_row():
    text = (_repo_root() / "docs" / "README.md").read_text(encoding="utf-8")
    assert "| [`STEP14_AUTONOMOUS_ENGINEER_RUNBOOK.md`]" in text
    assert "session-manifest.step14-closeout.v1.example.json" in text
    assert "packaging/icons/.../le-vibe.svg" in text


def test_docs_readme_apt_repo_releases_row_lists_stack_deb_resolver():
    text = (_repo_root() / "docs" / "README.md").read_text(encoding="utf-8")
    assert "| [`apt-repo-releases.md`]" in text
    assert "resolve-latest-le-vibe-stack-deb.sh" in text
    assert "PM_DEB_BUILD_ITERATION.md" in text


def test_step14_autonomous_runbook_documents_closeout_verifier():
    text = (_repo_root() / "docs" / "STEP14_AUTONOMOUS_ENGINEER_RUNBOOK.md").read_text(encoding="utf-8")
    assert "build-le-vibe-debs.sh --with-ide" in text
    assert "verify-step14-closeout.sh --require-stack-deb" in text
    assert "--apt-sim" in text
    assert "--json" in text
    assert "apt_sim_note" in text
    assert "build machine" in text
    assert "test host" in text
    assert "Definition of done (STEP 14 honest)" in text
    assert "Partial tree" in text
    assert "print-built-codium-path" in text
    assert "print-vsbuild-codium-path" in text
    assert "print-step14-vscode-linux-bin-files.sh" in text
    assert "build-le-vibe-ide-deb.sh --help" in text
    assert "resolve-latest-le-vibe-stack-deb.sh" in text
    assert "Compile fail-fast (STEP 14" in text
    assert "H1 vs §7.3 .deb bundles" in text
    assert "Compile fail-fast (STEP 14, before IDE `.deb`)" in text
    assert "ci-vscodium-bash-syntax.sh" in text
    assert "ci-editor-nvmrc-sync.sh" in text
    assert "ci-vscodium-linux-dev-build.sh" in text
    assert "2.1 Full-product" in text
    assert "probe-vscode-linux-build.sh" in text
    assert "dpkg-buildpackage" in text
    assert "Failure (`--with-ide`)" in text
    assert "preflight-step14-closeout.sh" in text
    assert "stderr hint" in text
