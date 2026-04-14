"""Smoke: §7.3 packaging / editor scripts accept --help and exit 0 (STEP 14 maintainer UX)."""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


@pytest.mark.parametrize(
    "relative",
    [
        "packaging/scripts/build-le-vibe-debs.sh",
        "packaging/scripts/build-le-vibe-ide-deb.sh",
        "packaging/scripts/stage-le-vibe-ide-deb.sh",
        "packaging/scripts/ci-vscodium-linux-dev-build.sh",
        "packaging/scripts/ci-editor-gate.sh",
        "packaging/scripts/ci-editor-nvmrc-sync.sh",
        "packaging/scripts/ci-vscodium-bash-syntax.sh",
        "editor/smoke.sh",
        "editor/le-vibe-overrides/sync-linux-icon-assets.sh",
        "packaging/scripts/check-linux-vscodium-build-deps.sh",
        "packaging/scripts/install-linux-vscodium-build-deps.sh",
        "packaging/scripts/verify-linux-vscodium-ci-apt-docker.sh",
        "packaging/scripts/docker-le-vibe-vscodium-prepare-only.sh",
        "packaging/scripts/docker-le-vibe-vscodium-linux-compile.sh",
        "packaging/scripts/verify-product-branding-merge-parity.sh",
        "packaging/scripts/verify-step14-closeout.sh",
        "packaging/scripts/probe-vscode-linux-build.sh",
        "packaging/scripts/preflight-step14-closeout.sh",
        "packaging/scripts/print-step14-vscode-linux-bin-files.sh",
        "packaging/scripts/install-vscodium-linux-tarball-to-editor-vendor.sh",
        "packaging/scripts/print-github-linux-compile-artifact-hint.sh",
        "packaging/scripts/download-vscodium-linux-compile-artifact.sh",
        "packaging/scripts/trigger-le-vibe-ide-linux-compile.sh",
        "packaging/scripts/resolve-latest-le-vibe-stack-deb.sh",
        "packaging/scripts/manual-step14-install-smoke.sh",
        "editor/print-built-codium-path.sh",
        "editor/print-vsbuild-codium-path.sh",
        "editor/print-ci-tarball-codium-path.sh",
        "editor/verify-14c-local-binary.sh",
        "editor/smoke-lvibe-editor.sh",
        "editor/smoke-built-codium-lvibe.sh",
        "editor/verify-73-maintainer.sh",
        "editor/use-node-toolchain.sh",
        "editor/fetch-vscode-sources.sh",
    ],
)
def test_step14_script_help_exits_zero(relative: str) -> None:
    root = _repo_root()
    script = root / relative
    assert script.is_file(), script
    r = subprocess.run(
        ["bash", str(script), "--help"],
        cwd=root,
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert r.returncode == 0, f"stderr={r.stderr!r} stdout={r.stdout!r}"
    out = f"{r.stdout}\n{r.stderr}"
    assert "Usage" in out, out[:500]
