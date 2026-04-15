"""One-shot Cline extension wiring after first-run.

Runs ``le-vibe-setup-cline`` when first-run is complete and automatic Cline setup has not
already been suppressed.

Disable with ``LE_VIBE_AUTO_CLINE_SETUP=0``. Failure writes
``.auto-cline-setup-suppressed`` so repeated launches do not hammer the marketplace.
Delete that file to retry.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

from .structured_log import append_structured_log

_SUPPRESSED = ".auto-cline-setup-suppressed"


def _first_run_complete(cfg_dir: Path) -> bool:
    return (cfg_dir / ".first-run-complete").is_file()


def maybe_auto_setup_cline_after_first_run(cfg_dir: Path) -> None:
    """Best-effort: run ``le-vibe-setup-cline`` once until success or suppressed failure."""
    if os.environ.get("LE_VIBE_AUTO_CLINE_SETUP", "1").lower() in ("0", "false", "no"):
        return
    suppressed = cfg_dir / _SUPPRESSED
    if suppressed.is_file():
        return
    if not _first_run_complete(cfg_dir):
        return
    exe = shutil.which("le-vibe-setup-cline")
    if not exe:
        append_structured_log(
            "launcher",
            "cline_auto_setup_skipped",
            reason="le-vibe-setup-cline not on PATH",
        )
        return
    try:
        r = subprocess.run(
            [exe],
            capture_output=True,
            text=True,
            timeout=900,
            env=os.environ.copy(),
        )
    except (OSError, subprocess.TimeoutExpired) as e:
        append_structured_log("launcher", "cline_auto_setup_error", error=str(e)[:300])
        try:
            suppressed.write_text(
                "error: exception invoking le-vibe-setup-cline\n", encoding="utf-8"
            )
        except OSError:
            pass
        print(
            "Lé Vibe: automatic Cline setup failed. Run: le-vibe-setup-cline",
            file=sys.stderr,
        )
        return

    if r.returncode == 0:
        append_structured_log("launcher", "cline_auto_setup_ok", setup_path=exe)
        return

    append_structured_log(
        "launcher",
        "cline_auto_setup_failed",
        exit_code=r.returncode,
        stderr_tail=(r.stderr or "")[-800:],
    )
    if r.returncode == 4:
        print(
            "Lé Vibe: no editor on PATH for Cline setup — install VSCodium or Lé Vibe IDE, "
            "or run: le-vibe-setup-cline",
            file=sys.stderr,
        )
        return

    try:
        suppressed.write_text(
            f"exit_code={r.returncode}\n",
            encoding="utf-8",
        )
    except OSError:
        pass
    print(
        "Lé Vibe: Cline extension setup did not complete automatically. "
        "When online, run: le-vibe-setup-cline",
        file=sys.stderr,
    )
