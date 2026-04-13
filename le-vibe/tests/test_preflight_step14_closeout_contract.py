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
