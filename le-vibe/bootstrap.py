#!/usr/bin/env python3
"""Lé Vibe (le-vibe): cross-platform Ollama bootstrapper with hardware-based model matching."""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

# Allow running as `python bootstrap.py` from le-vibe/
_ROOT = Path(__file__).resolve().parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from le_vibe.api import EnsureBootstrapArgs, ensure_bootstrap, print_final_instructions
from le_vibe.models import clear_tag_cache
from le_vibe.paths import LE_VIBE_MANAGED_OLLAMA_PORT, le_vibe_config_dir


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Lé Vibe (le-vibe): install if needed, launch Ollama, pull a model, emit Continue config.",
    )
    p.add_argument("--dry-run", action="store_true", help="Plan only; no install/pull/start")
    p.add_argument("--force-reinstall", action="store_true", help="Re-run OS installer for Ollama")
    p.add_argument("--model", type=str, default=None, help="Force a specific model tag")
    p.add_argument("--allow-slow", action="store_true", help="Allow possible-but-slow tiers (e.g. 32B)")
    p.add_argument("--host", default="127.0.0.1", help="Ollama bind host (default localhost)")
    p.add_argument(
        "--port",
        type=int,
        default=11434,
        help="Ollama port (use with --le-vibe-product for managed stack default)",
    )
    p.add_argument(
        "--le-vibe-product",
        action="store_true",
        help=f"Write configs under ~/.config/le-vibe/ and use port {LE_VIBE_MANAGED_OLLAMA_PORT} (Phase 2 managed Ollama)",
    )
    p.add_argument("--yes", action="store_true", help="Non-interactive / assume yes")
    p.add_argument("--verbose", "-v", action="store_true", help="Verbose logging")
    return p


def main() -> int:
    args = build_arg_parser().parse_args()
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s: %(message)s",
    )
    clear_tag_cache()

    config_dir: Path | None = None
    host = args.host
    port = args.port
    if args.le_vibe_product:
        config_dir = le_vibe_config_dir()
        port = LE_VIBE_MANAGED_OLLAMA_PORT

    opts = EnsureBootstrapArgs(
        dry_run=args.dry_run,
        force_reinstall=args.force_reinstall,
        model=args.model,
        allow_slow=args.allow_slow,
        host=host,
        port=port,
        yes=args.yes,
        verbose=args.verbose,
        config_dir=config_dir,
        use_managed_ollama=bool(args.le_vibe_product),
        allow_pull_if_disk_ok=True,
        locked_model_policy=("cli_override" if args.model else None),
    )
    code, state = ensure_bootstrap(opts)

    cont_hint: Path | None = None
    if config_dir is not None:
        cont_hint = config_dir / "continue-config.yaml"
    elif code == 0 or args.dry_run:
        cont_hint = _ROOT / "output" / "continue-config.yaml"

    if code == 0:
        print_final_instructions(state, config_hint=cont_hint)
    return code


if __name__ == "__main__":
    sys.exit(main())
