"""STEP 8 / H1: verify ``SHA256SUMS`` via ``sha256sum -c`` (``docs/apt-repo-releases.md``)."""

from __future__ import annotations

import subprocess
from pathlib import Path

SHA256SUMS_NAME = "SHA256SUMS"


def run_sha256sum_check(root: Path) -> int:
    """
    Run ``sha256sum -c SHA256SUMS`` in ``root``.

    Caller must ensure ``root/SHA256SUMS`` exists and ``sha256sum`` is on ``PATH``.
    """
    proc = subprocess.run(
        ["sha256sum", "-c", SHA256SUMS_NAME],
        cwd=root,
    )
    return int(proc.returncode)


def run_sha256sum_check_capture(root: Path) -> tuple[int, str, str]:
    """
    Same as ``run_sha256sum_check`` but capture stdout/stderr (for ``lvibe verify-checksums --json``).
    """
    proc = subprocess.run(
        ["sha256sum", "-c", SHA256SUMS_NAME],
        cwd=root,
        capture_output=True,
        text=True,
    )
    return int(proc.returncode), proc.stdout or "", proc.stderr or ""
