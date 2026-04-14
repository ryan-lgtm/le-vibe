"""Contract: preflight-step14-closeout.sh reports STEP 14 gaps before verify-step14-closeout.sh."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_preflight_step14_closeout_script_bash_syntax() -> None:
    script = _repo_root() / "packaging" / "scripts" / "preflight-step14-closeout.sh"
    assert script.is_file(), script
    assert script.stat().st_mode & 0o111, "script should be executable"
    subprocess.run(["bash", "-n", str(script)], check=True, capture_output=True)


def test_preflight_step14_closeout_script_documents_checks() -> None:
    text = (_repo_root() / "packaging" / "scripts" / "preflight-step14-closeout.sh").read_text(encoding="utf-8")
    assert "0 → 1 → 14" in text or "0 -> 1 -> 14" in text
    assert "PROMPT_BUILD_LE_VIBE.md" in text
    assert "verify-step14-closeout.sh" in text
    assert "ci-editor-gate.sh" in text
    assert "verify-14c-local-binary.sh" in text
    assert "*Partial tree*" in text or "Partial tree" in text
    assert "resolve-latest-le-vibe-stack-deb.sh" in text
    assert "le-vibe-ide_*.deb" in text
    assert "--require-stack-deb" in text
    assert "--skip-gate" in text
    assert "vscode_linux_build:" in text
    assert "probe-vscode-linux-build.sh" in text
    assert "build-le-vibe-debs.sh --with-ide exits before stack dpkg-buildpackage" in text
    assert "PM_DEB_BUILD_ITERATION.md" in text
    assert "vscode_linux_bin_files" in text
    assert "print-step14-vscode-linux-bin-files.sh" in text
    assert "install-vscodium-linux-tarball-to-editor-vendor.sh" in text
    assert "print-github-linux-compile-artifact-hint.sh" in text
    assert "trigger-le-vibe-ide-linux-compile.sh" in text
    assert "download-vscodium-linux-compile-artifact.sh" in text
    assert "desktop-file-validate" in text
    assert "build-le-vibe-ide-deb.sh" in text


def test_preflight_step14_closeout_prints_vscode_linux_build_line() -> None:
    """Same classifier as lvibe ide-prereqs --json (ready | partial | absent | unknown)."""
    root = _repo_root()
    script = root / "packaging" / "scripts" / "preflight-step14-closeout.sh"
    result = subprocess.run(
        [str(script), "--skip-gate"],
        cwd=str(root),
        capture_output=True,
        text=True,
    )
    combined = result.stdout + result.stderr
    assert re.search(r"^vscode_linux_build: (ready|partial|absent|unknown)\s*$", combined, re.MULTILINE), combined


def test_verify_step14_closeout_mentions_preflight() -> None:
    text = (_repo_root() / "packaging" / "scripts" / "verify-step14-closeout.sh").read_text(encoding="utf-8")
    assert "preflight-step14-closeout.sh" in text


def test_trigger_le_vibe_ide_linux_compile_script_contract() -> None:
    """STEP 14.e: curl workflow_dispatch for linux_compile without gh CLI."""
    text = (_repo_root() / "packaging" / "scripts" / "trigger-le-vibe-ide-linux-compile.sh").read_text(encoding="utf-8")
    assert "build-le-vibe-ide.yml" in text
    assert "vscodium_linux_compile" in text
    assert "dispatches" in text
    assert "204" in text
    subprocess.run(
        ["bash", "-n", str(_repo_root() / "packaging" / "scripts" / "trigger-le-vibe-ide-linux-compile.sh")],
        check=True,
        capture_output=True,
    )


def test_download_vscodium_linux_compile_artifact_script_contract() -> None:
    """STEP 14.f: curl+token path for linux_compile tarball (no gh CLI)."""
    text = (_repo_root() / "packaging" / "scripts" / "download-vscodium-linux-compile-artifact.sh").read_text(
        encoding="utf-8"
    )
    assert "build-le-vibe-ide.yml" in text
    assert "le-vibe-vscodium-linux-" in text
    assert "GITHUB_TOKEN" in text
    assert "_github_api_get" in text
    assert "LEVIBE_DOWNLOAD_ARTIFACT_MAX_PAGES" in text
    assert "archive download requires" in text
    assert "install-vscodium-linux-tarball-to-editor-vendor.sh" in text
    subprocess.run(
        ["bash", "-n", str(_repo_root() / "packaging" / "scripts" / "download-vscodium-linux-compile-artifact.sh")],
        check=True,
        capture_output=True,
    )


def test_print_github_linux_compile_artifact_hint_lists_browser_and_gh() -> None:
    """STEP 14: offline hint documents Actions UI (no gh), gh run download, and curl+token helper."""
    root = _repo_root()
    script = root / "packaging" / "scripts" / "print-github-linux-compile-artifact-hint.sh"
    r = subprocess.run([str(script)], cwd=str(root), capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    out = r.stdout
    assert "Actions" in out
    assert "gh run" in out
    assert "install-vscodium-linux-tarball-to-editor-vendor.sh" in out
    assert "download-vscodium-linux-compile-artifact.sh" in out
    assert "public repos" in out
    assert "trigger-le-vibe-ide-linux-compile.sh" in out
