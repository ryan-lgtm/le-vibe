#!/usr/bin/env python3
"""CLI for probe-vscode-linux-build.sh — classifier + weighted compile-gate progress.

Pytest: le-vibe/tests/test_probe_vscode_linux_build_script_contract.py; verify JSON stubs —
  le-vibe/tests/test_verify_step14_closeout_contract.py (fcntl lock; .gitignore: le-vibe/.pytest-verify-step14-contract.lock).
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path


def _ascii_progress_bar(pct: int, width: int = 32) -> str:
    pct = max(0, min(100, pct))
    filled = round(width * pct / 100)
    bar = "#" * filled + "-" * (width - filled)
    return f"[{bar}] {pct}%"


_RECOVERY_EPILOG = """When partial — recover toward bin/codium (linux_compile tarball or local dev/build.sh):
  packaging/scripts/print-github-linux-compile-artifact-hint.sh
  packaging/scripts/trigger-le-vibe-ide-linux-compile.sh
  packaging/scripts/download-vscodium-linux-compile-artifact.sh  (--install)
  packaging/scripts/install-vscodium-linux-tarball-to-editor-vendor.sh
Also: print-step14-vscode-linux-bin-files.sh (bin/ inventory); editor/BUILD.md (Partial tree, 14.f);
lvibe ide-prereqs --print-closeout-commands; packaging/scripts/preflight-step14-closeout.sh.
Same classifier as le_vibe.ide_packaging_paths.vscode_linux_build_status()."""


def main() -> int:
    p = argparse.ArgumentParser(
        description="Classify editor/vscodium VSCode-linux-* build state (STEP 14).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=_RECOVERY_EPILOG,
    )
    p.add_argument(
        "repo_root",
        nargs="?",
        default=os.environ.get("REPO_ROOT", "."),
        help="Monorepo root (default: cwd or REPO_ROOT)",
    )
    mode = p.add_mutually_exclusive_group()
    mode.add_argument(
        "--progress",
        action="store_true",
        help="Print 0–100 compile progress, bar, checklist with running /100, compile_gate_pct (human-readable)",
    )
    mode.add_argument(
        "--json",
        action="store_true",
        help="Print JSON: vscode_linux_build, compile_gate_pct, milestones, paths",
    )
    args = p.parse_args()
    root = Path(args.repo_root).resolve()

    from le_vibe.ide_packaging_paths import vscode_linux_compile_gate_progress

    data = vscode_linux_compile_gate_progress(root)
    st = str(data["vscode_linux_build"])

    if args.json:
        print(json.dumps(data, indent=2, ensure_ascii=False))
        return 0
    if args.progress:
        pct = int(data["compile_gate_pct"])
        remaining = max(0, 100 - pct)
        milestones = data["compile_gate_milestones"]
        print("STEP 14 — Linux compile gate (toward VSCode-linux-*/bin/codium only; not .deb packaging)")
        print("")
        print(f"Compile gate progress: {pct}/100 ({pct}% complete)")
        print(_ascii_progress_bar(pct))
        if remaining:
            print(f"Remaining to compile gate: {remaining}/100 ({remaining}% left)")
        else:
            print("Remaining to compile gate: 0/100 (compile gate satisfied)")
        print("")
        print("Checklist (running total is sum of completed rows, top to bottom):")
        running = 0
        for m in milestones:
            mark = "x" if m["done"] else " "
            w = int(m["weight"])
            if m["done"]:
                running += w
            print(f"  [{mark}] {running:>3}/100  (+{w}% this row)  {m['label']}")
        if running != pct:
            print(f"  (note: order-independent total is {pct}/100 — see compile_gate_pct below)")
        print("")
        print(
            "Weights (reference, sum 100): vscodium/ 10 + product.json 15 + VSCode-linux-* 35 + "
            "bin/ ≥1 file 10 + bin/codium 30"
        )
        print("")
        print(f"compile_gate_pct: {pct}")
        print(f"vscode_linux_build: {st}")
        vp = data.get("vscode_linux_path")
        if vp:
            print(f"vscode_linux_path: {vp}")
        return 0

    print(st)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
