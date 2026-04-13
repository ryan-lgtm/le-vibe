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


def _cmd_welcome(argv: list[str]) -> int:
    """STEP 4 (E3): ``.lvibe/WELCOME.md`` path or full §4 text for terminal-only sessions."""
    from le_vibe.editor_welcome import WELCOME_MD_NAME, ensure_lvibe_welcome_md

    p = argparse.ArgumentParser(
        prog="lvibe welcome",
        description=(
            "Print the path to .lvibe/WELCOME.md (default) or the full file with --text "
            "(PRODUCT_SPEC §4). Requires .lvibe/ from prior consent (§5.1)."
        ),
    )
    p.add_argument(
        "workspace",
        nargs="?",
        default=".",
        help="workspace root (default: current directory)",
    )
    p.add_argument(
        "--text",
        action="store_true",
        help="print WELCOME.md contents to stdout (terminal welcome surface)",
    )
    args = p.parse_args(argv)
    root = Path(args.workspace).resolve()
    lv = root / ".lvibe"
    if not lv.is_dir():
        print(
            "lvibe welcome: missing .lvibe/ — open this workspace with lvibe once and accept "
            "workspace memory (PRODUCT_SPEC §5.1).",
            file=sys.stderr,
        )
        return 1
    ensure_lvibe_welcome_md(root)
    path = lv / WELCOME_MD_NAME
    if not path.is_file():
        print(f"lvibe welcome: missing {path} after seeding.", file=sys.stderr)
        return 2
    if args.text:
        print(path.read_text(encoding="utf-8"), end="")
        return 0
    print(path.resolve())
    return 0


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
    import json as json_mod

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
    p.add_argument(
        "--json",
        action="store_true",
        help="print log file metadata as JSON (path, enabled, line count, first/last ts)",
    )
    args = p.parse_args(argv)
    path = structured_log_path()
    if not structured_log_enabled():
        print(
            "lvibe logs: LE_VIBE_STRUCTURED_LOG is disabled — no new lines are written.",
            file=sys.stderr,
        )
    if args.json:
        if args.tail is not None or args.path_only:
            print(
                "lvibe logs: --json cannot be combined with --tail or --path-only",
                file=sys.stderr,
            )
            return 2
        payload: dict[str, object] = {
            "path": str(path.resolve()),
            "structured_log_enabled": structured_log_enabled(),
            "exists": path.is_file(),
        }
        if path.is_file():
            text = path.read_text(encoding="utf-8", errors="replace")
            lines = text.splitlines()
            payload["lines"] = len(lines)
            if lines:
                try:
                    first = json_mod.loads(lines[0])
                    last = json_mod.loads(lines[-1])
                    if isinstance(first, dict):
                        payload["first_ts"] = first.get("ts")
                    if isinstance(last, dict):
                        payload["last_ts"] = last.get("ts")
                except json_mod.JSONDecodeError:
                    payload["parse_note"] = "first or last line is not valid JSON"
        print(json_mod.dumps(payload, indent=2, ensure_ascii=False))
        return 0
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
    import json as json_mod

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
    p.add_argument(
        "--json",
        action="store_true",
        help="print pin file path, semver, and continue.continue@… id as JSON",
    )
    args = p.parse_args(argv)
    if args.json and args.path_only:
        print(
            "lvibe continue-pin: --json cannot be combined with --path-only",
            file=sys.stderr,
        )
        return 2
    try:
        path = resolve_continue_openvsx_pin_path()
        if args.json:
            out: dict[str, object] = {"pin_file": str(path.resolve())}
            try:
                ver = read_continue_openvsx_version()
            except FileNotFoundError:
                out["error"] = "missing_pin_file"
                print(json_mod.dumps(out, indent=2, ensure_ascii=False))
                return 1
            except ValueError as e:
                out["error"] = "invalid_pin"
                out["detail"] = str(e)
                print(json_mod.dumps(out, indent=2, ensure_ascii=False))
                return 2
            out["semver"] = ver
            out["openvsx_id"] = f"continue.continue@{ver}"
            print(json_mod.dumps(out, indent=2, ensure_ascii=False))
            return 0
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
    import json as json_mod
    import shutil

    from le_vibe.release_checksums import SHA256SUMS_NAME, run_sha256sum_check, run_sha256sum_check_capture

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
    p.add_argument(
        "--json",
        action="store_true",
        help="print directory, paths, exit code, and sha256sum stdout/stderr as JSON",
    )
    args = p.parse_args(argv)
    try:
        root = Path(args.directory).expanduser().resolve()
    except OSError as e:
        if args.json:
            print(
                json_mod.dumps({"error": "bad_directory", "detail": str(e)}, indent=2),
                file=sys.stdout,
            )
            return 2
        print(f"lvibe verify-checksums: bad --directory: {e}", file=sys.stderr)
        return 2
    sums_path = root / SHA256SUMS_NAME

    def _json_payload(**extra: object) -> None:
        base = {"directory": str(root), "sha256sums_path": str(sums_path)}
        base.update(extra)
        print(json_mod.dumps(base, indent=2, ensure_ascii=False), file=sys.stdout)

    if not root.is_dir():
        if args.json:
            _json_payload(error="not_a_directory")
            return 1
        print(f"lvibe verify-checksums: not a directory: {root}", file=sys.stderr)
        return 1
    if not sums_path.is_file():
        if args.json:
            _json_payload(error="missing_sha256sums", hint="docs/apt-repo-releases.md STEP 8 / H1")
            return 1
        print(f"lvibe verify-checksums: no {SHA256SUMS_NAME} in {root}", file=sys.stderr)
        print("See docs/apt-repo-releases.md (STEP 8 / H1).", file=sys.stderr)
        return 1
    if not shutil.which("sha256sum"):
        if args.json:
            _json_payload(error="sha256sum_not_on_path")
            return 127
        print("lvibe verify-checksums: sha256sum not on PATH (install coreutils).", file=sys.stderr)
        return 127
    if args.json:
        rc, out, err = run_sha256sum_check_capture(root)
        _json_payload(
            exit_code=rc,
            sha256sum_stdout=out.rstrip("\n"),
            sha256sum_stderr=err.rstrip("\n"),
            ok=(rc == 0),
        )
        return 0 if rc == 0 else 1
    return run_sha256sum_check(root)


def _cmd_pip_audit(argv: list[str]) -> int:
    """STEP 9 (H2): ``pip-audit -r le-vibe/requirements.txt`` — ``docs/sbom-signing-audit.md``."""
    import json as json_mod
    import shutil

    from le_vibe.supply_chain_check import (
        requirements_txt_path,
        run_pip_audit,
        run_pip_audit_captured,
    )

    json_mode = False
    rest: list[str] = []
    for a in argv:
        if a == "--json":
            json_mode = True
        else:
            rest.append(a)

    req = requirements_txt_path()

    def _emit_json(**payload: object) -> None:
        print(json_mod.dumps(payload, indent=2, ensure_ascii=False), file=sys.stdout)

    if not req.is_file():
        if json_mode:
            _emit_json(
                error="requirements_txt_missing",
                requirements_path=str(req),
                hint="docs/sbom-signing-audit.md STEP 9 / H2 — git clone; stack .deb omits file",
            )
            return 1
        print(
            "lvibe pip-audit: le-vibe/requirements.txt not found — supply-chain audit runs from a "
            "git clone (the stack .deb omits this file). See docs/sbom-signing-audit.md (STEP 9 / H2).",
            file=sys.stderr,
        )
        return 1
    if not shutil.which("pip-audit"):
        if json_mode:
            _emit_json(error="pip_audit_not_on_path", requirements_path=str(req))
            return 127
        print(
            "lvibe pip-audit: pip-audit not on PATH — pip install pip-audit "
            "(docs/sbom-signing-audit.md).",
            file=sys.stderr,
        )
        return 127
    if json_mode:
        rc, out, err = run_pip_audit_captured(rest)
        _emit_json(
            requirements_path=str(req),
            pip_audit_extra_args=rest,
            exit_code=rc,
            ok=(rc == 0),
            stdout=out.rstrip("\n"),
            stderr=err.rstrip("\n"),
        )
        return rc
    return run_pip_audit(rest)


def _split_lvibe_json_flag(argv: list[str]) -> tuple[bool, list[str]]:
    """Strip leading ``lvibe``-level ``--json`` (STEP 10 / H3); remaining args go to bash scripts."""
    json_mode = False
    rest: list[str] = []
    for a in argv:
        if a == "--json":
            json_mode = True
        else:
            rest.append(a)
    return json_mode, rest


def _cmd_ci_smoke(argv: list[str]) -> int:
    """STEP 10 (H3): ``packaging/scripts/ci-smoke.sh`` — ``docs/ci-qa-hardening.md``."""
    import json as json_mod

    from le_vibe.qa_scripts import EXIT_NO_MONOREPO, find_monorepo_root, run_ci_smoke, run_ci_smoke_captured

    json_mode, rest = _split_lvibe_json_flag(argv)

    def _emit_json(**payload: object) -> None:
        print(json_mod.dumps(payload, indent=2, ensure_ascii=False), file=sys.stdout)

    if json_mode:
        rc, out, err = run_ci_smoke_captured(rest)
        if rc == EXIT_NO_MONOREPO:
            _emit_json(
                error="monorepo_not_found",
                script="packaging/scripts/ci-smoke.sh",
                hint="docs/ci-qa-hardening.md STEP 10 / H3 — set LE_VIBE_REPO_ROOT or run from clone",
            )
            return 1
        root = find_monorepo_root()
        assert root is not None
        _emit_json(
            monorepo_root=str(root),
            script="packaging/scripts/ci-smoke.sh",
            script_args=rest,
            exit_code=rc,
            ok=(rc == 0),
            stdout=out.rstrip("\n"),
            stderr=err.rstrip("\n"),
        )
        return rc

    rc = run_ci_smoke(rest)
    if rc == EXIT_NO_MONOREPO:
        print(
            "lvibe ci-smoke: could not find Lé Vibe monorepo (packaging/scripts/ci-smoke.sh). "
            "Set LE_VIBE_REPO_ROOT to the git checkout, or run from inside the clone. "
            "See docs/ci-qa-hardening.md (STEP 10 / H3).",
            file=sys.stderr,
        )
        return 1
    return rc


def _cmd_ci_editor_gate(argv: list[str]) -> int:
    """STEP 10 (H3): ``packaging/scripts/ci-editor-gate.sh`` (editor/ gate)."""
    import json as json_mod

    from le_vibe.qa_scripts import EXIT_NO_MONOREPO, find_monorepo_root, run_ci_editor_gate, run_ci_editor_gate_captured

    json_mode, rest = _split_lvibe_json_flag(argv)

    def _emit_json(**payload: object) -> None:
        print(json_mod.dumps(payload, indent=2, ensure_ascii=False), file=sys.stdout)

    if json_mode:
        rc, out, err = run_ci_editor_gate_captured(rest)
        if rc == EXIT_NO_MONOREPO:
            _emit_json(
                error="monorepo_not_found",
                script="packaging/scripts/ci-editor-gate.sh",
                hint="docs/ci-qa-hardening.md STEP 10 / H3 — set LE_VIBE_REPO_ROOT or run from clone",
            )
            return 1
        root = find_monorepo_root()
        assert root is not None
        _emit_json(
            monorepo_root=str(root),
            script="packaging/scripts/ci-editor-gate.sh",
            script_args=rest,
            exit_code=rc,
            ok=(rc == 0),
            stdout=out.rstrip("\n"),
            stderr=err.rstrip("\n"),
        )
        return rc

    rc = run_ci_editor_gate(rest)
    if rc == EXIT_NO_MONOREPO:
        print(
            "lvibe ci-editor-gate: could not find Lé Vibe monorepo "
            "(packaging/scripts/ci-editor-gate.sh). Set LE_VIBE_REPO_ROOT or run from the clone. "
            "See docs/ci-qa-hardening.md (STEP 10 / H3).",
            file=sys.stderr,
        )
        return 1
    return rc


def _cmd_brand_paths(argv: list[str]) -> int:
    """STEP 11 (H5): canonical ``le-vibe.svg`` paths — ``docs/brand-assets.md``."""
    import json as json_mod

    from le_vibe.brand_paths import SCALABLE_SVG_REL, resolve_scalable_icon_paths

    p = argparse.ArgumentParser(
        prog="lvibe brand-paths",
        description="Show paths to the scalable Lé Vibe app icon (le-vibe.svg).",
    )
    mode = p.add_mutually_exclusive_group()
    mode.add_argument(
        "--path-only",
        action="store_true",
        help="print one path (monorepo preferred, else packaged hicolor icon)",
    )
    mode.add_argument(
        "--json",
        action="store_true",
        help="print monorepo and packaged paths as JSON (docs/brand-assets.md table)",
    )
    args = p.parse_args(argv)
    mono, pkg = resolve_scalable_icon_paths()

    if args.json:
        chosen = mono or pkg
        payload = {
            "scalable_svg_relpath": str(SCALABLE_SVG_REL).replace("\\", "/"),
            "monorepo_svg": str(mono) if mono else None,
            "packaged_svg": str(pkg) if pkg else None,
            "chosen_for_scripts": str(chosen) if chosen else None,
            "ok": chosen is not None,
        }
        if chosen is None:
            payload["error"] = "no_le_vibe_svg"
            payload["hint"] = "docs/brand-assets.md STEP 11 / H5 — git clone or install le-vibe .deb"
        print(json_mod.dumps(payload, indent=2, ensure_ascii=False), file=sys.stdout)
        return 0 if chosen is not None else 1

    if args.path_only:
        chosen = mono or pkg
        if chosen is None:
            print(
                "lvibe brand-paths: no le-vibe.svg found (git clone or install le-vibe .deb). "
                "See docs/brand-assets.md (STEP 11 / H5).",
                file=sys.stderr,
            )
            return 1
        print(chosen)
        return 0
    print("Authority: docs/brand-assets.md (Roadmap H5)")
    if mono:
        print(f"monorepo (source): {mono}")
    else:
        print("monorepo (source): (not found — run inside git clone or set LE_VIBE_REPO_ROOT)")
    if pkg:
        print(f"installed .deb icon: {pkg}")
    else:
        print("installed .deb icon: (le-vibe package not installed or icon missing)")
    return 0


def _cmd_product_surface(argv: list[str]) -> int:
    """STEP 12 (H8): print paths to ``.github/`` + trust docs — ``docs/PM_STAGE_MAP.md``."""
    import json as json_mod

    from le_vibe.product_surface_paths import H8_MANIFEST, iter_h8_paths
    from le_vibe.qa_scripts import find_monorepo_root

    p = argparse.ArgumentParser(
        prog="lvibe product-surface",
        description="List paths for H8 product-surface files (CI, Dependabot, issue templates, docs).",
    )
    mode = p.add_mutually_exclusive_group()
    mode.add_argument(
        "--path-only",
        metavar="KEY",
        nargs="?",
        const="ci",
        default=None,
        help=(
            "print one path: ci, dependabot, issues, docs-index, privacy, security "
            "(default key when flag is present: ci)"
        ),
    )
    mode.add_argument(
        "--json",
        action="store_true",
        help="print monorepo root and each H8 path with exists flags (machine-readable)",
    )
    args = p.parse_args(argv)

    def _emit_json(**payload: object) -> None:
        print(json_mod.dumps(payload, indent=2, ensure_ascii=False), file=sys.stdout)

    root = find_monorepo_root()
    if root is None:
        if args.json:
            _emit_json(
                error="monorepo_not_found",
                hint="docs/PM_STAGE_MAP.md STEP 12 / H8 — set LE_VIBE_REPO_ROOT or run from clone",
            )
            return 1
        print(
            "lvibe product-surface: could not find monorepo root "
            "(set LE_VIBE_REPO_ROOT or run from a git clone). "
            "See docs/PM_STAGE_MAP.md STEP 12 / H8.",
            file=sys.stderr,
        )
        return 1
    key_map = {
        "ci": H8_MANIFEST[0][1],
        "dependabot": H8_MANIFEST[1][1],
        "issues": H8_MANIFEST[2][1],
        "docs-index": H8_MANIFEST[3][1],
        "privacy": H8_MANIFEST[4][1],
        "security": H8_MANIFEST[5][1],
    }
    if args.json:
        entries = []
        for label, rel in H8_MANIFEST:
            abs_p = (root / rel).resolve()
            exists = abs_p.is_file()
            entries.append(
                {
                    "label": label,
                    "relative": str(rel).replace("\\", "/"),
                    "path": str(abs_p),
                    "exists": exists,
                }
            )
        all_present = all(e["exists"] for e in entries)
        _emit_json(
            monorepo_root=str(root),
            entries=entries,
            all_present=all_present,
        )
        return 0
    if args.path_only is not None:
        k = args.path_only
        if k not in key_map:
            print(
                f"lvibe product-surface: unknown key {k!r} — use: {', '.join(sorted(key_map))}",
                file=sys.stderr,
            )
            return 2
        rel = key_map[k]
        path = (root / rel).resolve()
        if not path.is_file():
            print(f"lvibe product-surface: missing {path}", file=sys.stderr)
            return 1
        print(path)
        return 0
    print("Authority: docs/PM_STAGE_MAP.md (STEP 12 / H8), docs/README.md *Product surface*")
    for label, path, ok in iter_h8_paths(root):
        status = "OK" if ok else "MISSING"
        print(f"[{status}] {label}: {path}")
    return 0


def _cmd_flatpak_appimage(argv: list[str]) -> int:
    """STEP 13 (H7): print paths to Flatpak/AppImage templates — ``docs/flatpak-appimage.md``."""
    import json as json_mod

    from le_vibe.flatpak_appimage_paths import H7_MANIFEST, iter_h7_paths
    from le_vibe.qa_scripts import find_monorepo_root

    p = argparse.ArgumentParser(
        prog="lvibe flatpak-appimage",
        description="List paths for H7 alternate-bundle templates (Flatpak, AppImage).",
    )
    mode = p.add_mutually_exclusive_group()
    mode.add_argument(
        "--path-only",
        metavar="KEY",
        nargs="?",
        const="doc",
        default=None,
        help=(
            "print one path: doc, flatpak, flatpak-readme, apprun, build, appimage-readme "
            "(default key when flag is present: doc)"
        ),
    )
    mode.add_argument(
        "--json",
        action="store_true",
        help="print monorepo root and each H7 path with exists flags (machine-readable)",
    )
    args = p.parse_args(argv)

    def _emit_json(**payload: object) -> None:
        print(json_mod.dumps(payload, indent=2, ensure_ascii=False), file=sys.stdout)

    root = find_monorepo_root()
    if root is None:
        if args.json:
            _emit_json(
                error="monorepo_not_found",
                hint="docs/PM_STAGE_MAP.md STEP 13 / H7 — set LE_VIBE_REPO_ROOT or run from clone",
            )
            return 1
        print(
            "lvibe flatpak-appimage: could not find monorepo root "
            "(set LE_VIBE_REPO_ROOT or run from a git clone). "
            "See docs/PM_STAGE_MAP.md STEP 13 / H7.",
            file=sys.stderr,
        )
        return 1
    key_map = {
        "doc": H7_MANIFEST[0][1],
        "flatpak": H7_MANIFEST[1][1],
        "flatpak-readme": H7_MANIFEST[2][1],
        "apprun": H7_MANIFEST[3][1],
        "build": H7_MANIFEST[4][1],
        "appimage-readme": H7_MANIFEST[5][1],
    }
    if args.json:
        entries = []
        for label, rel in H7_MANIFEST:
            abs_p = (root / rel).resolve()
            exists = abs_p.is_file()
            entries.append(
                {
                    "label": label,
                    "relative": str(rel).replace("\\", "/"),
                    "path": str(abs_p),
                    "exists": exists,
                }
            )
        all_present = all(e["exists"] for e in entries)
        _emit_json(
            monorepo_root=str(root),
            entries=entries,
            all_present=all_present,
        )
        return 0
    if args.path_only is not None:
        k = args.path_only
        if k not in key_map:
            print(
                f"lvibe flatpak-appimage: unknown key {k!r} — use: {', '.join(sorted(key_map))}",
                file=sys.stderr,
            )
            return 2
        rel = key_map[k]
        path = (root / rel).resolve()
        if not path.is_file():
            print(f"lvibe flatpak-appimage: missing {path}", file=sys.stderr)
            return 1
        print(path)
        return 0
    print("Authority: docs/flatpak-appimage.md (STEP 13 / H7), docs/PM_STAGE_MAP.md")
    for label, path, ok in iter_h7_paths(root):
        status = "OK" if ok else "MISSING"
        print(f"[{status}] {label}: {path}")
    return 0


def _cmd_ide_prereqs(argv: list[str]) -> int:
    """STEP 14 (H6 / §7.3): print paths for IDE ``.deb`` packaging and optional VSCode-linux build."""
    import json as json_mod

    from le_vibe.ide_packaging_paths import (
        IDE_PREREQ_PATH_ONLY,
        find_vscode_linux_tree,
        iter_ide_prereq_paths,
    )
    from le_vibe.qa_scripts import find_monorepo_root

    all_keys = sorted(IDE_PREREQ_PATH_ONLY.keys()) + ["vscode"]
    p = argparse.ArgumentParser(
        prog="lvibe ide-prereqs",
        description="List §7.3 IDE packaging paths and whether a VSCode-linux build exists.",
    )
    mode = p.add_mutually_exclusive_group()
    mode.add_argument(
        "--path-only",
        metavar="KEY",
        nargs="?",
        const="branding",
        default=None,
        help=(
            "print one path: vscode, branding, sync-icons, svg, stage, build-ide-deb, "
            "build-debs, control (default key when flag is present: branding)"
        ),
    )
    mode.add_argument(
        "--json",
        action="store_true",
        help="print monorepo root, VSCode-linux status, and each §7.3 path with exists flags",
    )
    args = p.parse_args(argv)

    def _emit_json(**payload: object) -> None:
        print(json_mod.dumps(payload, indent=2, ensure_ascii=False), file=sys.stdout)

    root = find_monorepo_root()
    if root is None:
        if args.json:
            _emit_json(
                error="monorepo_not_found",
                hint="docs/PM_STAGE_MAP.md STEP 14 / H6 — set LE_VIBE_REPO_ROOT or run from clone",
            )
            return 1
        print(
            "lvibe ide-prereqs: could not find monorepo root "
            "(set LE_VIBE_REPO_ROOT or run from a git clone). "
            "See docs/PM_STAGE_MAP.md STEP 14 / H6.",
            file=sys.stderr,
        )
        return 1

    vs_tree = find_vscode_linux_tree(root)
    static_ok = all((root / rel).is_file() for rel in IDE_PREREQ_PATH_ONLY.values())

    if args.json:
        entries = []
        for label, path, ok in iter_ide_prereq_paths(root):
            entries.append({"label": label, "path": str(path), "exists": ok})
        _emit_json(
            monorepo_root=str(root),
            vscode_linux_path=str(vs_tree) if vs_tree else None,
            vscode_linux_ready=vs_tree is not None,
            static_prereq_files_ok=static_ok,
            entries=entries,
        )
        return 0

    if args.path_only is not None:
        k = args.path_only
        if k not in all_keys:
            print(
                f"lvibe ide-prereqs: unknown key {k!r} — use: {', '.join(all_keys)}",
                file=sys.stderr,
            )
            return 2
        if k == "vscode":
            if vs_tree is None:
                print(
                    "lvibe ide-prereqs: no editor/vscodium/VSCode-linux-*/bin/codium — "
                    "build per editor/BUILD.md (§7.3).",
                    file=sys.stderr,
                )
                return 1
            print(vs_tree)
            return 0
        rel = IDE_PREREQ_PATH_ONLY[k]
        path = (root / rel).resolve()
        if not path.is_file():
            print(f"lvibe ide-prereqs: missing {path}", file=sys.stderr)
            return 1
        print(path)
        return 0
    print("Authority: PRODUCT_SPEC §7.3, docs/PM_STAGE_MAP.md STEP 14, packaging/debian-le-vibe-ide/README.md")
    for label, path, ok in iter_ide_prereq_paths(root):
        status = "OK" if ok else "MISSING"
        print(f"[{status}] {label}: {path}")
    return 0


def _cmd_workspace_governance(argv: list[str]) -> int:
    """STEP 15: consent, cap, usage vs cap — ``PRODUCT_SPEC`` §5, ``docs/PM_STAGE_MAP.md`` STEP 15."""
    import json as json_mod

    from le_vibe.workspace_policy import cap_mb_from_environ, get_cap_mb, get_consent, policy_path
    from le_vibe.workspace_storage import lvibe_tree_usage_bytes

    p = argparse.ArgumentParser(
        prog="lvibe workspace-governance",
        description="Show §5 workspace consent, storage cap, and .lvibe/ usage (read-only).",
    )
    p.add_argument(
        "--workspace",
        "-C",
        default=".",
        help="workspace root (default: current directory)",
    )
    p.add_argument(
        "--json",
        action="store_true",
        help="print consent, caps, usage, and storage-state as JSON",
    )
    args = p.parse_args(argv)
    try:
        ws = Path(args.workspace).expanduser().resolve()
    except OSError as e:
        print(f"lvibe workspace-governance: bad --workspace: {e}", file=sys.stderr)
        return 2

    env_cap = cap_mb_from_environ()
    effective_cap = env_cap if env_cap is not None else get_cap_mb(ws)
    consent = get_consent(ws)
    usage = lvibe_tree_usage_bytes(ws)
    cap_bytes = effective_cap * 1024 * 1024
    within_cap = usage <= cap_bytes
    state_path = ws / ".lvibe" / "storage-state.json"
    storage_state: dict[str, object] | None = None
    if state_path.is_file():
        try:
            raw = json_mod.loads(state_path.read_text(encoding="utf-8"))
            if isinstance(raw, dict):
                storage_state = raw
        except (OSError, json_mod.JSONDecodeError):
            storage_state = None

    payload = {
        "workspace_root": str(ws),
        "policy_file": str(policy_path()),
        "consent": consent,
        "cap_mb_effective": effective_cap,
        "cap_mb_env_override": env_cap,
        "usage_bytes": usage,
        "cap_bytes": cap_bytes,
        "within_cap": within_cap,
        "storage_state_path": str(state_path),
        "storage_state": storage_state,
    }

    if args.json:
        print(json_mod.dumps(payload, indent=2, ensure_ascii=False), file=sys.stdout)
        return 0

    print("Authority: PRODUCT_SPEC §5, docs/PM_STAGE_MAP.md STEP 15")
    print(f"Workspace: {ws}")
    print(f"Policy file: {payload['policy_file']}")
    c = consent
    print(f"Consent: {c if c is not None else 'undecided'}")
    if env_cap is not None:
        print(f"Cap (effective): {effective_cap} MB (LE_VIBE_LVIBE_CAP_MB={env_cap})")
    else:
        print(f"Cap (effective): {effective_cap} MB")
    print(f"Usage: {usage} bytes ({usage / (1024 * 1024):.2f} MB) / {effective_cap} MB budget")
    print(f"Within cap: {'yes' if within_cap else 'no'}")
    print(f"storage-state.json: {state_path} ({'present' if state_path.is_file() else 'absent'})")
    return 0


def _cmd_master_orchestrator(argv: list[str]) -> int:
    """STEP 16: PM map + ``PROMPT_BUILD_LE_VIBE.md`` paths; optional fenced Master prompt — ``docs/PM_STAGE_MAP.md``."""
    import json as json_mod

    from le_vibe.master_orchestrator import extract_master_orchestrator_fence
    from le_vibe.qa_scripts import find_monorepo_root

    p = argparse.ArgumentParser(
        prog="lvibe master-orchestrator",
        description="Locate STEP 16 docs and optionally print the fenced Master queue prompt.",
    )
    mode = p.add_mutually_exclusive_group()
    mode.add_argument(
        "--print",
        action="store_true",
        help="print the fenced Master orchestrator block (same as print-master-orchestrator-prompt.py)",
    )
    mode.add_argument(
        "--json",
        action="store_true",
        help="print monorepo paths and whether the fence is extractable",
    )
    args = p.parse_args(argv)

    root = find_monorepo_root()
    if root is None:
        if args.json:
            print(
                json_mod.dumps(
                    {
                        "error": "monorepo_not_found",
                        "hint": "docs/PM_STAGE_MAP.md STEP 16 — set LE_VIBE_REPO_ROOT or run from clone",
                    },
                    indent=2,
                    ensure_ascii=False,
                ),
                file=sys.stdout,
            )
            return 1
        print(
            "lvibe master-orchestrator: could not find monorepo root "
            "(set LE_VIBE_REPO_ROOT or run from a git clone). "
            "See docs/PM_STAGE_MAP.md STEP 16.",
            file=sys.stderr,
        )
        return 1

    prompt_md = root / "docs" / "PROMPT_BUILD_LE_VIBE.md"
    pm_map_md = root / "docs" / "PM_STAGE_MAP.md"
    extract_py = root / "packaging" / "scripts" / "print-master-orchestrator-prompt.py"
    fence = extract_master_orchestrator_fence(root)

    if args.print:
        if fence is None:
            print(
                "lvibe master-orchestrator: fenced block not found in docs/PROMPT_BUILD_LE_VIBE.md",
                file=sys.stderr,
            )
            return 1
        print(fence)
        return 0

    if args.json:
        payload: dict[str, object] = {
            "monorepo_root": str(root),
            "prompt_build_le_vibe_md": str(prompt_md),
            "pm_stage_map_md": str(pm_map_md),
            "print_master_orchestrator_prompt_py": str(extract_py),
            "master_fence_extractable": fence is not None,
        }
        if fence is not None:
            payload["fence_char_count"] = len(fence)
        print(json_mod.dumps(payload, indent=2, ensure_ascii=False), file=sys.stdout)
        return 0

    print("Authority: docs/PM_STAGE_MAP.md STEP 16, docs/PROMPT_BUILD_LE_VIBE.md")
    print(f"Monorepo root: {root}")
    print(f"PM stage map:  {pm_map_md}")
    print(f"Master queue:  {prompt_md}")
    print(f"Extract script: {extract_py}")
    if fence is None:
        print("Master fence:  MISSING (see test_prompt_build_orchestrator_fence.py)")
    else:
        print(f"Master fence:  OK ({len(fence)} chars) — lvibe master-orchestrator --print")
    return 0


def _cmd_ai_pilot_continue(argv: list[str]) -> int:
    """STEP 17: **Please continue** / **AI Pilot** — ``docs/AI_PILOT_AND_CONTINUE.md``."""
    import json as json_mod

    from le_vibe.ai_pilot_paths import H17_MANIFEST, iter_h17_paths
    from le_vibe.qa_scripts import find_monorepo_root

    p = argparse.ArgumentParser(
        prog="lvibe ai-pilot-continue",
        description="List STEP 17 paths (AI Pilot scope, Continue rules, root README §7.1).",
    )
    mode = p.add_mutually_exclusive_group()
    mode.add_argument(
        "--path-only",
        metavar="KEY",
        nargs="?",
        const="doc",
        default=None,
        help="print one path: doc, continue, readme (default key when flag is present: doc)",
    )
    mode.add_argument(
        "--json",
        action="store_true",
        help="print monorepo root and each STEP 17 path with exists flags",
    )
    args = p.parse_args(argv)

    def _emit_json(**payload: object) -> None:
        print(json_mod.dumps(payload, indent=2, ensure_ascii=False), file=sys.stdout)

    root = find_monorepo_root()
    if root is None:
        if args.json:
            _emit_json(
                error="monorepo_not_found",
                hint="docs/PM_STAGE_MAP.md STEP 17 — set LE_VIBE_REPO_ROOT or run from clone",
            )
            return 1
        print(
            "lvibe ai-pilot-continue: could not find monorepo root "
            "(set LE_VIBE_REPO_ROOT or run from a git clone). "
            "See docs/PM_STAGE_MAP.md STEP 17.",
            file=sys.stderr,
        )
        return 1

    key_map = {
        "doc": H17_MANIFEST[0][1],
        "continue": H17_MANIFEST[1][1],
        "readme": H17_MANIFEST[2][1],
    }
    if args.json:
        entries = []
        for label, rel in H17_MANIFEST:
            abs_p = (root / rel).resolve()
            exists = abs_p.is_file()
            entries.append(
                {
                    "label": label,
                    "relative": str(rel).replace("\\", "/"),
                    "path": str(abs_p),
                    "exists": exists,
                }
            )
        all_present = all(e["exists"] for e in entries)
        _emit_json(
            monorepo_root=str(root),
            entries=entries,
            all_present=all_present,
        )
        return 0
    if args.path_only is not None:
        k = args.path_only
        if k not in key_map:
            print(
                f"lvibe ai-pilot-continue: unknown key {k!r} — use: {', '.join(sorted(key_map))}",
                file=sys.stderr,
            )
            return 2
        rel = key_map[k]
        path = (root / rel).resolve()
        if not path.is_file():
            print(f"lvibe ai-pilot-continue: missing {path}", file=sys.stderr)
            return 1
        print(path)
        return 0

    print("Authority: docs/AI_PILOT_AND_CONTINUE.md, docs/PM_STAGE_MAP.md STEP 17")
    for label, path, ok in iter_h17_paths(root):
        status = "OK" if ok else "MISSING"
        print(f"[{status}] {label}: {path}")
    return 0


def _cmd_apply_opening_skip(argv: list[str]) -> int:
    """STEP 2: advance ``opening_intent`` when the user skips — ``SESSION_ORCHESTRATION_SPEC`` §4."""
    from le_vibe.session_orchestrator import apply_opening_skip

    p = argparse.ArgumentParser(
        prog="lvibe apply-opening-skip",
        description=(
            "If session-manifest meta.current_step_id is opening_intent, advance to workspace_scan "
            "or agent_bootstrap per on_skip and workspace contents; may write workspace-scan stub."
        ),
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
            f"lvibe apply-opening-skip: missing {lv} — open this workspace with lvibe after consent "
            "(PRODUCT_SPEC §5.1).",
            file=sys.stderr,
        )
        return 1
    nxt = apply_opening_skip(root, skipped_opening=True)
    if nxt is None:
        print(
            "lvibe apply-opening-skip: no change (not at opening_intent or missing session-manifest.json). "
            "See docs/SESSION_ORCHESTRATION_SPEC.md STEP 2.",
            file=sys.stderr,
        )
        return 1
    print(nxt)
    return 0


def _cmd_continue_rules(argv: list[str]) -> int:
    """STEP 3 (E2): ensure Continue workspace rules anchor ``.lvibe/`` as primary memory."""
    from le_vibe.continue_workspace import (
        LVIBE_CONTINUE_RULE_NAME,
        PRODUCT_WELCOME_RULE_NAME,
        continue_rules_dir,
        ensure_continue_lvibe_rules,
    )

    p = argparse.ArgumentParser(
        prog="lvibe continue-rules",
        description=(
            "Create .continue/rules/*.md when missing so Chat/Agent uses .lvibe/ (session manifest, "
            "agents/*/skill.md). Idempotent — same as workspace prepare."
        ),
    )
    p.add_argument(
        "workspace",
        nargs="?",
        default=".",
        help="workspace root (default: current directory)",
    )
    args = p.parse_args(argv)
    root = Path(args.workspace).resolve()
    written = ensure_continue_lvibe_rules(root)
    written_set = set(written)
    rules = continue_rules_dir(root)
    print("Authority: le_vibe.continue_workspace (STEP 3 / E2), docs/PM_STAGE_MAP.md")
    for fname in (LVIBE_CONTINUE_RULE_NAME, PRODUCT_WELCOME_RULE_NAME):
        path = rules / fname
        tag = "NEW" if path in written_set else "OK"
        print(f"[{tag}] {path.resolve()}")
    return 0


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
    if len(sys.argv) >= 2 and sys.argv[1] == "welcome":
        return _cmd_welcome(sys.argv[2:])
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
    if len(sys.argv) >= 2 and sys.argv[1] == "ci-smoke":
        return _cmd_ci_smoke(sys.argv[2:])
    if len(sys.argv) >= 2 and sys.argv[1] == "ci-editor-gate":
        return _cmd_ci_editor_gate(sys.argv[2:])
    if len(sys.argv) >= 2 and sys.argv[1] == "brand-paths":
        return _cmd_brand_paths(sys.argv[2:])
    if len(sys.argv) >= 2 and sys.argv[1] == "product-surface":
        return _cmd_product_surface(sys.argv[2:])
    if len(sys.argv) >= 2 and sys.argv[1] == "flatpak-appimage":
        return _cmd_flatpak_appimage(sys.argv[2:])
    if len(sys.argv) >= 2 and sys.argv[1] == "ide-prereqs":
        return _cmd_ide_prereqs(sys.argv[2:])
    if len(sys.argv) >= 2 and sys.argv[1] == "workspace-governance":
        return _cmd_workspace_governance(sys.argv[2:])
    if len(sys.argv) >= 2 and sys.argv[1] == "master-orchestrator":
        return _cmd_master_orchestrator(sys.argv[2:])
    if len(sys.argv) >= 2 and sys.argv[1] == "ai-pilot-continue":
        return _cmd_ai_pilot_continue(sys.argv[2:])
    if len(sys.argv) >= 2 and sys.argv[1] == "apply-opening-skip":
        return _cmd_apply_opening_skip(sys.argv[2:])
    if len(sys.argv) >= 2 and sys.argv[1] == "continue-rules":
        return _cmd_continue_rules(sys.argv[2:])

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
