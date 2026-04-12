"""Lé Vibe session launcher: managed Ollama on open, stop on exit (spec-phase2 §7.1). Linux-first.

Authority: ``docs/PRODUCT_SPEC.md`` (must-ship). Workspace open uses ``prepare_workspaces_for_editor_args`` — **§5**
consent before ``.lvibe/``; **§7.2** user gate copy lives in Continue rules (``le_vibe.continue_workspace``).
"""

from __future__ import annotations

import argparse
import atexit
import os
import signal
import subprocess
import sys

from .first_run import ensure_product_first_run
from .managed_ollama import ensure_managed_ollama, stop_managed_ollama
from .paths import LE_VIBE_MANAGED_OLLAMA_PORT, le_vibe_config_dir
from .welcome import maybe_print_welcome
from .structured_log import append_structured_log
from .workspace_hub import prepare_workspaces_for_editor_args

_stopped = False


def _default_editor() -> str:
    env = os.environ.get("LE_VIBE_EDITOR")
    if env:
        return env
    # Packaged Lé Vibe IDE (PRODUCT_SPEC §7.3): internal path only — public CLI remains `lvibe`.
    lv_ide = "/usr/lib/le-vibe/bin/codium"
    if os.path.isfile(lv_ide) and os.access(lv_ide, os.X_OK):
        return lv_ide
    if os.path.isfile("/usr/bin/codium") and os.access("/usr/bin/codium", os.X_OK):
        return "/usr/bin/codium"
    return "codium"


def _cleanup() -> None:
    global _stopped
    if _stopped:
        return
    _stopped = True
    stop_managed_ollama()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Lé Vibe: start managed Ollama, then run the editor; stops Ollama on quit.",
    )
    parser.add_argument("--host", default="127.0.0.1", help="bind address for managed Ollama (default localhost)")
    parser.add_argument(
        "--port",
        type=int,
        default=None,
        help=f"managed Ollama port (default {LE_VIBE_MANAGED_OLLAMA_PORT}, spec §7.2-A)",
    )
    parser.add_argument(
        "--editor",
        default=_default_editor(),
        help="editor binary (default $LE_VIBE_EDITOR, else /usr/lib/le-vibe/bin/codium, /usr/bin/codium, else codium)",
    )
    parser.add_argument(
        "editor_args",
        nargs="*",
        help="extra arguments for the editor",
    )
    parser.add_argument(
        "--skip-first-run",
        action="store_true",
        help="do not run Phase 1 product bootstrap (Ollama install/model pull) before the editor",
    )
    parser.add_argument(
        "--force-first-run",
        action="store_true",
        help="re-run first-run bootstrap even if ~/.config/le-vibe/.first-run-complete exists",
    )
    args = parser.parse_args()
    port = args.port if args.port is not None else LE_VIBE_MANAGED_OLLAMA_PORT

    append_structured_log(
        "launcher",
        "session_start",
        host=args.host,
        port=port,
        editor=args.editor,
        skip_first_run=bool(args.skip_first_run),
        force_first_run=bool(args.force_first_run),
    )

    if sys.platform != "linux":
        print(
            "Lé Vibe: managed launcher targets Linux for this milestone.",
            file=sys.stderr,
        )
        return 2

    atexit.register(_cleanup)

    def _signal_handler(signum: int, _frame: object) -> None:
        _cleanup()
        if signum == signal.SIGINT:
            raise SystemExit(130)
        raise SystemExit(128 + signum)

    signal.signal(signal.SIGTERM, _signal_handler)
    signal.signal(signal.SIGINT, _signal_handler)
    signal.signal(signal.SIGHUP, _signal_handler)

    if not args.skip_first_run:
        assume = os.environ.get("LE_VIBE_ASSUME_YES", "1").lower()
        install_yes = assume not in ("0", "false", "no")
        fr_code, fr_msg = ensure_product_first_run(
            yes=install_yes,
            verbose=os.environ.get("LE_VIBE_VERBOSE", "").lower() in ("1", "true", "yes"),
            force=args.force_first_run,
        )
        if fr_code != 0:
            append_structured_log("launcher", "first_run_exit", exit_code=fr_code, message=fr_msg[:300])
            print(fr_msg, file=sys.stderr)
            return fr_code

    ok, msg, _state = ensure_managed_ollama(host=args.host, port=port)
    if not ok:
        append_structured_log("launcher", "managed_ollama_blocked_session", ok=False, message=msg[:400])
        print(msg, file=sys.stderr)
        return 6

    cfg = le_vibe_config_dir()
    maybe_print_welcome(cfg)
    prepare_workspaces_for_editor_args(args.editor_args)

    cmd = [args.editor, *args.editor_args]
    try:
        proc = subprocess.Popen(cmd)
    except OSError as e:
        append_structured_log("launcher", "editor_spawn_failed", editor=cmd[0], error=str(e))
        print(f"failed to start editor {cmd[0]}: {e}", file=sys.stderr)
        _cleanup()
        return 127

    rc = proc.wait()
    append_structured_log("launcher", "editor_exit", editor=cmd[0], exit_code=rc)
    _cleanup()
    if rc < 0:
        return 128 - rc
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
