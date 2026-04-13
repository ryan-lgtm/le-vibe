"""One-time terminal welcome for Lé Vibe (OSS / local-first positioning)."""

from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path


def welcome_marker_path(config_dir: Path) -> Path:
    return config_dir / ".welcome-shown"


WELCOME_BANNER = """
╔══════════════════════════════════════════════════════════════════╗
║  Welcome to Lé Vibe                                              ║
╠══════════════════════════════════════════════════════════════════╣
║  Lé Vibe is a free, open source, local-first coding environment  ║
║  — an alternative to Cursor (AI-assisted coding; not the same     ║
║  feature set). Models run on your hardware via Ollama.           ║
╚══════════════════════════════════════════════════════════════════╝

  Tip: In a project folder, `lvibe welcome` prints section-4 workspace copy; `lvibe open-welcome`
  opens `.lvibe/WELCOME.md` in your editor (PRODUCT_SPEC section 4 / STEP 4).

  First-run / logs: `lvibe --skip-first-run` / `--force-first-run`, `LE_VIBE_VERBOSE=1` — see `le-vibe/README.md`
  (*First-run (launcher)*); structured log path: `lvibe logs --path-only` (STEP 6).
""".strip()


def maybe_print_welcome(config_dir: Path, *, force: bool = False) -> None:
    """Print the welcome banner once per machine unless force=True."""
    cfg = Path(config_dir)
    marker = welcome_marker_path(cfg)
    if not force and marker.is_file():
        return
    print(WELCOME_BANNER, file=sys.stdout)
    try:
        cfg.mkdir(parents=True, exist_ok=True)
        marker.write_text(
            f"shown_at_utc={datetime.now(timezone.utc).isoformat()}\n",
            encoding="utf-8",
        )
    except OSError:
        pass
