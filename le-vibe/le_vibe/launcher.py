"""Lé Vibe session launcher: managed Ollama on open, stop on exit (spec-phase2 §7.1). Linux-first.

Authority: ``docs/PRODUCT_SPEC.md`` (must-ship). Workspace open uses ``prepare_workspaces_for_editor_args`` — **§5**
consent before ``.lvibe/`` (``load_user_settings`` does **not** replace consent); **§7.2** user gate copy lives in Continue rules (``le_vibe.continue_workspace``).
"""

from __future__ import annotations

import argparse
import atexit
import os
import signal
import subprocess
import sys
from pathlib import Path

from .first_run import ensure_product_first_run
from .managed_ollama import ensure_managed_ollama, stop_managed_ollama
from .paths import LE_VIBE_MANAGED_OLLAMA_PORT, le_vibe_config_dir
from .user_settings import load_user_settings
from .welcome import maybe_print_welcome
from .structured_log import append_structured_log
from .editor_welcome import WELCOME_MD_NAME, ensure_lvibe_welcome_md
from .workspace_hub import prepare_workspaces_for_editor_args

_stopped = False


def _cmd_sync_agent_skills(argv: list[str]) -> int:
    """
    STEP 3 (E2): copy missing ``templates/agents/*.md`` into ``.lvibe/agents/<id>/skill.md``.
    Same behavior as ``packaging/scripts/sync-lvibe-agent-skills.sh`` — no editor or Ollama.
    """
    from le_vibe.session_orchestrator import sync_agent_skills_from_templates

    p = argparse.ArgumentParser(
        prog="lvibe sync-agent-skills",
        description="Copy missing Lé Vibe agent skill templates into .lvibe/agents/<id>/skill.md (idempotent).",
    )
    p.add_argument(
        "workspace",
        nargs="?",
        default=".",
        help="workspace root (default: current directory)",
    )
    args = p.parse_args(argv)
    root = Path(args.workspace).resolve()
    lv = root / ".lvibe"
    if not lv.is_dir():
        print(
            f"lvibe sync-agent-skills: missing {lv} — run lvibe on this workspace first.",
            file=sys.stderr,
        )
        return 1
    written = sync_agent_skills_from_templates(lv)
    if written:
        print(f"lvibe sync-agent-skills: wrote {len(written)} skill.md file(s)")
        for path in written:
            print(f"  {path}")
    else:
        print(
            "lvibe sync-agent-skills: no missing skill.md "
            "(delete a file under .lvibe/agents/*/ to force re-copy)",
        )
    return 0


def _cmd_open_welcome(argv: list[str]) -> int:
    """
    STEP 4 (E3): open ``.lvibe/WELCOME.md`` in the resolved editor — PRODUCT_SPEC §4 running welcome surface.
    Does not start Ollama or run first-run bootstrap. Requires an existing ``.lvibe/`` (§5.1 consent path).
    """
    p = argparse.ArgumentParser(
        prog="lvibe open-welcome",
        description="Open .lvibe/WELCOME.md in the editor (PRODUCT_SPEC §4); no Ollama session.",
    )
    p.add_argument(
        "workspace",
        nargs="?",
        default=".",
        help="workspace root (default: current directory)",
    )
    args = p.parse_args(argv)
    root = Path(args.workspace).resolve()
    lv = root / ".lvibe"
    if not lv.is_dir():
        print(
            "lvibe open-welcome: missing .lvibe/ — open this workspace with lvibe once and accept "
            "workspace memory (PRODUCT_SPEC §5.1).",
            file=sys.stderr,
        )
        return 1
    ensure_lvibe_welcome_md(root)
    welcome = lv / WELCOME_MD_NAME
    if not welcome.is_file():
        print(f"lvibe open-welcome: missing {welcome} after seeding.", file=sys.stderr)
        return 2
    editor = _default_editor()
    append_structured_log("launcher", "open_welcome", editor=editor, path=str(welcome))
    try:
        proc = subprocess.run([editor, str(welcome)])
    except OSError as e:
        print(f"lvibe open-welcome: failed to start {editor}: {e}", file=sys.stderr)
        return 127
    return proc.returncode if proc.returncode is not None else 1


def _cmd_hygiene(argv: list[str]) -> int:
    """
    STEP 5 (E4): validate ``.lvibe/`` — same entry as ``lvibe-hygiene`` / ``python3 -m le_vibe.hygiene``.
    """
    from le_vibe.hygiene import main as hygiene_main

    return hygiene_main(argv)


def _cmd_logs(argv: list[str]) -> int:
    """
    STEP 6 (E5): operator surface for local JSONL — path, optional tail (``docs/privacy-and-telemetry.md``).
    """
    from le_vibe.structured_log import structured_log_enabled, structured_log_path

    p = argparse.ArgumentParser(
        prog="lvibe logs",
        description=(
            "Print the path to the local structured log (JSON Lines). "
            "No third-party telemetry — see docs/privacy-and-telemetry.md."
        ),
    )
    p.add_argument(
        "--tail",
        "-n",
        type=int,
        metavar="N",
        default=None,
        help="print the last N lines if the log file exists",
    )
    p.add_argument(
        "--path-only",
        action="store_true",
        help="print the absolute log path only",
    )
    args = p.parse_args(argv)
    path = structured_log_path()
    if not structured_log_enabled():
        print(
            "lvibe logs: LE_VIBE_STRUCTURED_LOG is disabled — no new lines are written.",
            file=sys.stderr,
        )
    if args.path_only:
        print(path)
        return 0
    if args.tail is not None:
        if args.tail < 0:
            print("lvibe logs: --tail requires N >= 0", file=sys.stderr)
            return 2
        if not path.is_file():
            print(f"lvibe logs: no file at {path} yet.", file=sys.stderr)
            return 1
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        for line in lines[-args.tail :]:
            print(line)
        return 0
    print(path)
    print(f"Live: tail -f {path}")
    print(f"Pretty (if jq is installed): tail -f {path} | jq .")
    return 0


def _cmd_continue_pin(argv: list[str]) -> int:
    """STEP 7 (H4): print pinned Open VSX semver for Continue — ``docs/continue-extension-pin.md``."""
    from le_vibe.continue_pin import read_continue_openvsx_version, resolve_continue_openvsx_pin_path

    p = argparse.ArgumentParser(
        prog="lvibe continue-pin",
        description="Print the pinned Continue Open VSX version (continue.continue@<semver>).",
    )
    p.add_argument(
        "--path-only",
        action="store_true",
        help="print the pin file path only",
    )
    args = p.parse_args(argv)
    try:
        path = resolve_continue_openvsx_pin_path()
        if args.path_only:
            print(path)
            return 0
        ver = read_continue_openvsx_version()
        print(ver)
        return 0
    except FileNotFoundError as e:
        print(f"lvibe continue-pin: missing pin file: {e}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"lvibe continue-pin: {e}", file=sys.stderr)
        return 2


def _cmd_verify_checksums(argv: list[str]) -> int:
    """STEP 8 (H1): ``sha256sum -c SHA256SUMS`` — same as ``docs/apt-repo-releases.md``."""
    import shutil

    from le_vibe.release_checksums import SHA256SUMS_NAME, run_sha256sum_check

    p = argparse.ArgumentParser(
        prog="lvibe verify-checksums",
        description="Verify SHA256SUMS in a release directory (sha256sum -c).",
    )
    p.add_argument(
        "--directory",
        "-C",
        default=".",
        help="directory containing SHA256SUMS (default: current directory)",
    )
    args = p.parse_args(argv)
    try:
        root = Path(args.directory).expanduser().resolve()
    except OSError as e:
        print(f"lvibe verify-checksums: bad --directory: {e}", file=sys.stderr)
        return 2
    if not root.is_dir():
        print(f"lvibe verify-checksums: not a directory: {root}", file=sys.stderr)
        return 1
    if not (root / SHA256SUMS_NAME).is_file():
        print(f"lvibe verify-checksums: no {SHA256SUMS_NAME} in {root}", file=sys.stderr)
        print("See docs/apt-repo-releases.md (STEP 8 / H1).", file=sys.stderr)
        return 1
    if not shutil.which("sha256sum"):
        print("lvibe verify-checksums: sha256sum not on PATH (install coreutils).", file=sys.stderr)
        return 127
    return run_sha256sum_check(root)


def _cmd_pip_audit(argv: list[str]) -> int:
    """STEP 9 (H2): ``pip-audit -r le-vibe/requirements.txt`` — ``docs/sbom-signing-audit.md``."""
    from le_vibe.supply_chain_check import (
        EXIT_NO_PIP_AUDIT,
        EXIT_NO_REQUIREMENTS_TXT,
        run_pip_audit,
    )

    rc = run_pip_audit(argv)
    if rc == EXIT_NO_REQUIREMENTS_TXT:
        print(
            "lvibe pip-audit: le-vibe/requirements.txt not found — supply-chain audit runs from a "
            "git clone (the stack .deb omits this file). See docs/sbom-signing-audit.md (STEP 9 / H2).",
            file=sys.stderr,
        )
        return 1
    if rc == EXIT_NO_PIP_AUDIT:
        print(
            "lvibe pip-audit: pip-audit not on PATH — pip install pip-audit "
            "(docs/sbom-signing-audit.md).",
            file=sys.stderr,
        )
        return 127
    return rc


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
    if len(sys.argv) >= 2 and sys.argv[1] == "sync-agent-skills":
        return _cmd_sync_agent_skills(sys.argv[2:])
    if len(sys.argv) >= 2 and sys.argv[1] == "open-welcome":
        return _cmd_open_welcome(sys.argv[2:])
    if len(sys.argv) >= 2 and sys.argv[1] == "hygiene":
        return _cmd_hygiene(sys.argv[2:])
    if len(sys.argv) >= 2 and sys.argv[1] == "logs":
        return _cmd_logs(sys.argv[2:])
    if len(sys.argv) >= 2 and sys.argv[1] == "continue-pin":
        return _cmd_continue_pin(sys.argv[2:])
    if len(sys.argv) >= 2 and sys.argv[1] == "verify-checksums":
        return _cmd_verify_checksums(sys.argv[2:])
    if len(sys.argv) >= 2 and sys.argv[1] == "pip-audit":
        return _cmd_pip_audit(sys.argv[2:])

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
    us = load_user_settings(config_dir=cfg)
    append_structured_log(
        "launcher",
        "user_settings_loaded",
        lvibe_cap_default_explicit=us.get("lvibe_cap_mb_default") is not None,
    )
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
