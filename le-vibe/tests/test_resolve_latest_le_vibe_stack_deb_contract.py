"""Contract: resolve-latest-le-vibe-stack-deb.sh — single stack .deb discovery (STEP 14)."""

from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_resolve_latest_le_vibe_stack_deb_script_bash_syntax_and_executable() -> None:
    script = _repo_root() / "packaging" / "scripts" / "resolve-latest-le-vibe-stack-deb.sh"
    assert script.is_file(), script
    assert script.stat().st_mode & 0o111, "script should be executable"
    subprocess.run(["bash", "-n", str(script)], check=True, capture_output=True)


def test_resolve_latest_le_vibe_stack_deb_script_documents_callers_and_globs() -> None:
    text = (
        _repo_root() / "packaging" / "scripts" / "resolve-latest-le-vibe-stack-deb.sh"
    ).read_text(encoding="utf-8")
    assert "verify-step14-closeout.sh" in text
    assert "manual-step14-install-smoke.sh" in text
    assert "build-le-vibe-debs.sh" in text
    assert "PM_DEB_BUILD_ITERATION.md" in text
    assert "sort -V" in text
    assert "dpkg-deb --field" in text
    assert "le-vibe_*.deb" in text
    assert "test_resolve_latest_le_vibe_stack_deb_contract.py" in text
    assert "test_verify_step14_closeout_contract.py" in text
    assert ".pytest-verify-step14-contract.lock" in text


def test_resolve_latest_le_vibe_stack_deb_prints_nothing_when_no_deb() -> None:
    root = _repo_root()
    script = root / "packaging" / "scripts" / "resolve-latest-le-vibe-stack-deb.sh"
    with subprocess.Popen(
        ["bash", str(script), "/nonexistent/r-vibe-clone-root"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    ) as proc:
        out, err = proc.communicate()
        rc = proc.returncode
    assert rc == 0
    assert out.strip() == ""
    assert err == ""


def test_resolve_latest_le_vibe_stack_deb_skips_unreadable_archives() -> None:
    root = _repo_root()
    script = root / "packaging" / "scripts" / "resolve-latest-le-vibe-stack-deb.sh"
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        repo_root = tmp / "repo"
        repo_root.mkdir()
        older = repo_root.parent / "le-vibe_0.1.9_all.deb"
        newer_bad = repo_root / "le-vibe_9999.0.0_all.deb"
        older.write_bytes(b"ok")
        newer_bad.write_bytes(b"bad")
        stub_dir = tmp / "bin"
        stub_dir.mkdir()
        (stub_dir / "dpkg-deb").write_text(
            """#!/usr/bin/env bash
set -euo pipefail
if [[ "$1" == "--field" ]]; then
  if [[ "$2" == *"9999.0.0_all.deb" ]]; then
    exit 2
  fi
  printf 'le-vibe\\n'
  exit 0
fi
exit 1
""",
            encoding="utf-8",
        )
        (stub_dir / "dpkg-deb").chmod(0o755)
        result = subprocess.run(
            ["bash", str(script), str(repo_root)],
            capture_output=True,
            text=True,
            env={"PATH": f"{stub_dir}:/usr/bin:/bin"},
            check=False,
        )
        assert result.returncode == 0
        assert result.stdout.strip().endswith("le-vibe_0.1.9_all.deb")
