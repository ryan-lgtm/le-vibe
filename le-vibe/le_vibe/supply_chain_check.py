"""STEP 9 / H2: optional ``pip-audit`` against ``requirements.txt`` (``docs/sbom-signing-audit.md``)."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

# Distinct from subprocess exit codes (audit failures use pip-audit's own codes).
EXIT_NO_REQUIREMENTS_TXT = 125
EXIT_NO_PIP_AUDIT = 127


def requirements_txt_path() -> Path:
    """``le-vibe/requirements.txt`` next to this package (git clone / editable install)."""
    return Path(__file__).resolve().parent.parent / "requirements.txt"


def run_pip_audit(extra_args: list[str]) -> int:
    """
    Run ``pip-audit -r <requirements.txt>`` if the file exists and ``pip-audit`` is on ``PATH``.

    Returns ``0`` on success, subprocess exit code on audit failure,
    ``EXIT_NO_REQUIREMENTS_TXT`` if ``requirements.txt`` is absent (stack ``.deb`` does not ship it),
    ``EXIT_NO_PIP_AUDIT`` if ``pip-audit`` is missing.
    """
    req = requirements_txt_path()
    if not req.is_file():
        return EXIT_NO_REQUIREMENTS_TXT
    if not shutil.which("pip-audit"):
        return EXIT_NO_PIP_AUDIT
    cmd = ["pip-audit", "-r", str(req), *extra_args]
    proc = subprocess.run(cmd, cwd=req.parent)
    return int(proc.returncode)


def run_pip_audit_captured(extra_args: list[str]) -> tuple[int, str, str]:
    """
    Same as ``run_pip_audit`` but capture stdout/stderr (for ``lvibe pip-audit --json``).

    Caller must ensure ``requirements.txt`` exists and ``pip-audit`` is on ``PATH``.
    """
    req = requirements_txt_path()
    cmd = ["pip-audit", "-r", str(req), *extra_args]
    proc = subprocess.run(cmd, cwd=req.parent, capture_output=True, text=True)
    return int(proc.returncode), proc.stdout or "", proc.stderr or ""
