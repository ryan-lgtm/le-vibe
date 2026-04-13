"""Contract: docs/AGENT_MODE_ORCHESTRATION.md keeps STEP 14 full-product close-out gate references."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_agent_mode_orchestration_lists_step14_full_product_closeout_gate():
    text = (_repo_root() / "docs" / "AGENT_MODE_ORCHESTRATION.md").read_text(encoding="utf-8")
    assert "PM_DEB_BUILD_ITERATION.md" in text
    assert "build-le-vibe-debs.sh --with-ide" in text
    assert "Full-product install" in text
    assert "verify-step14-closeout.sh --require-stack-deb" in text
    assert "preflight-step14-closeout.sh" in text
    assert "ide-prereqs --print-closeout-commands" in text
    assert "--apt-sim" in text
    assert "--json" in text
    assert "apt_sim_note" in text
    assert "le-vibe-deb" in text
    assert "Partial VSCode-linux" in text
    assert "print-built-codium-path" in text
    assert "print-vsbuild-codium-path" in text
    assert "print-step14-vscode-linux-bin-files.sh" in text
    assert "print-github-linux-compile-artifact-hint.sh" in text
    assert "install-vscodium-linux-tarball-to-editor-vendor.sh" in text
    assert "print-ci-tarball-codium-path.sh" in text
    assert "debian/lvibe.1" in text
    assert "build-le-vibe-ide-deb.sh --help" in text
