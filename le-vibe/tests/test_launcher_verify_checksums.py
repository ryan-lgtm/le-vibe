"""STEP 8: ``lvibe verify-checksums``."""

from __future__ import annotations

import shutil
import subprocess
import sys

import pytest

from le_vibe import launcher

requires_sha256sum = pytest.mark.skipif(
    not shutil.which("sha256sum"),
    reason="sha256sum not on PATH",
)


def test_verify_checksums_no_manifest(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(sys, "argv", ["launcher", "verify-checksums"])
    assert launcher.main() == 1
    err = capsys.readouterr().err
    assert "SHA256SUMS" in err
    assert "apt-repo-releases.md" in err


@requires_sha256sum
def test_verify_checksums_ok(tmp_path, monkeypatch):
    f = tmp_path / "x.deb"
    f.write_bytes(b"fake-deb")
    proc = subprocess.run(
        ["sha256sum", str(f)],
        capture_output=True,
        text=True,
        check=True,
    )
    (tmp_path / "SHA256SUMS").write_text(proc.stdout, encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(sys, "argv", ["launcher", "verify-checksums", "-C", str(tmp_path)])
    assert launcher.main() == 0
