"""STEP 8 / H1: ``release_checksums.run_sha256sum_check``."""

from __future__ import annotations

import shutil
import subprocess

import pytest

from le_vibe.release_checksums import run_sha256sum_check

requires_sha256sum = pytest.mark.skipif(
    not shutil.which("sha256sum"),
    reason="sha256sum not on PATH",
)


@requires_sha256sum
def test_run_sha256sum_check_ok(tmp_path):
    f = tmp_path / "artifact.bin"
    f.write_bytes(b"payload-bytes")
    proc = subprocess.run(
        ["sha256sum", str(f)],
        capture_output=True,
        text=True,
        check=True,
    )
    (tmp_path / "SHA256SUMS").write_text(proc.stdout, encoding="utf-8")
    assert run_sha256sum_check(tmp_path) == 0


@requires_sha256sum
def test_run_sha256sum_check_detects_tamper(tmp_path):
    f = tmp_path / "artifact.bin"
    f.write_bytes(b"a")
    proc = subprocess.run(
        ["sha256sum", str(f)],
        capture_output=True,
        text=True,
        check=True,
    )
    (tmp_path / "SHA256SUMS").write_text(proc.stdout, encoding="utf-8")
    f.write_bytes(b"b")
    assert run_sha256sum_check(tmp_path) != 0
