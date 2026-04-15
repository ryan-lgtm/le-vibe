"""One-shot Continue + YAML extension wiring after first-run (H4 / STEP 7).

Runs ``le-vibe-setup-continue`` when the stack pin + sync path is available on PATH,
``~/.config/le-vibe/continue-config.yaml`` exists, and ``~/.continue/config.yaml`` is not
yet linked — same order as the manual command (``docs/continue-extension-pin.md``).

Disable with ``LE_VIBE_AUTO_CONTINUE_SETUP=0``. Failure (except no editor on PATH) writes
``.auto-continue-setup-suppressed`` so repeated launches do not hammer the marketplace;
delete that file to retry. ``PRODUCT_SPEC`` remains authoritative over ``.lvibe/`` manifests.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

from .structured_log import append_structured_log

_SUPPRESSED = ".auto-continue-setup-suppressed"


def _xdg_config_home() -> Path:
    xdg = os.environ.get("XDG_CONFIG_HOME")
    return Path(xdg).expanduser() if xdg else Path.home() / ".config"


def continue_symlink_ok(cfg_dir: Path) -> bool:
    """True when Continue's config path is a symlink to Lé Vibe's generated YAML."""
    src = cfg_dir / "continue-config.yaml"
    if not src.is_file():
        return False
    cont = _xdg_config_home() / "continue" / "config.yaml"
    if not cont.is_symlink() or not cont.exists():
        return False
    try:
        return cont.resolve() == src.resolve()
    except OSError:
        return False


def maybe_auto_setup_continue_after_first_run(cfg_dir: Path) -> None:
    """
    Best-effort: run ``le-vibe-setup-continue`` once until success or suppressed failure.

    Does not raise. Logs structured events; prints a one-line stderr hint on hard failure.
    """
    if os.environ.get("LE_VIBE_AUTO_CONTINUE_SETUP", "1").lower() in ("0", "false", "no"):
        return
    if continue_symlink_ok(cfg_dir):
        return
    suppressed = cfg_dir / _SUPPRESSED
    if suppressed.is_file():
        return
    if not (cfg_dir / "continue-config.yaml").is_file():
        return
    exe = shutil.which("le-vibe-setup-continue")
    if not exe:
        append_structured_log(
            "launcher",
            "continue_auto_setup_skipped",
            reason="le-vibe-setup-continue not on PATH",
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
        append_structured_log("launcher", "continue_auto_setup_error", error=str(e)[:300])
        try:
            suppressed.write_text(
                "error: exception invoking le-vibe-setup-continue\n", encoding="utf-8"
            )
        except OSError:
            pass
        print(
            "Lé Vibe: automatic Continue setup failed. Run: le-vibe-setup-continue",
            file=sys.stderr,
        )
        return

    if r.returncode == 0:
        append_structured_log("launcher", "continue_auto_setup_ok", setup_path=exe)
        return

    append_structured_log(
        "launcher",
        "continue_auto_setup_failed",
        exit_code=r.returncode,
        stderr_tail=(r.stderr or "")[-800:],
    )
    # Exit 4: no editor — user may install IDE later; retry next launch.
    if r.returncode == 4:
        print(
            "Lé Vibe: no editor on PATH for Continue setup — install VSCodium or Lé Vibe IDE, "
            "or run: le-vibe-setup-continue",
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
        "Lé Vibe: Continue extension setup did not complete automatically. "
        "When online, run: le-vibe-setup-continue",
        file=sys.stderr,
    )
