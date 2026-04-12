"""One-time product bootstrap: Ollama + model pull + configs under ~/.config/le-vibe/ (spec-phase2 install/first-run)."""

from __future__ import annotations

import logging
import os
from pathlib import Path

from .api import EnsureBootstrapArgs, ensure_bootstrap
from .models import clear_tag_cache
from .paths import LE_VIBE_MANAGED_OLLAMA_PORT, le_vibe_config_dir
from .structured_log import append_structured_log
from .user_settings import load_user_settings


def first_run_marker_path(config_dir: Path | None = None) -> Path:
    return (config_dir or le_vibe_config_dir()) / ".first-run-complete"


def ensure_product_first_run(
    *,
    yes: bool = True,
    verbose: bool = False,
    force: bool = False,
    config_dir: Path | None = None,
) -> tuple[int, str]:
    """
    Run Phase 1–equivalent bootstrap into the product config dir once.
    Uses managed Ollama on the dedicated port so state matches `le_vibe.launcher`.

    Returns (exit_code, message). Exit codes match ensure_bootstrap; 0 includes skipped.
    """
    if verbose or os.environ.get("LE_VIBE_VERBOSE", "").lower() in ("1", "true", "yes"):
        logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(message)s")
    else:
        logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    clear_tag_cache()
    cfg = config_dir or le_vibe_config_dir()
    us = load_user_settings(config_dir=cfg)
    m = us.get("model") or {}
    model_override: str | None = None
    if not m.get("use_recommended", True):
        raw = m.get("override_tag")
        if isinstance(raw, str) and raw.strip():
            model_override = raw.strip()
    allow_pull = bool(m.get("allow_pull_if_disk_ok", True))
    locked_pol: str | None = "user_settings" if model_override else None
    marker = first_run_marker_path(cfg)

    if force and marker.is_file():
        try:
            marker.unlink()
        except OSError:
            pass

    if not force and marker.is_file() and (cfg / "model-decision.json").is_file():
        append_structured_log("first_run", "skipped", reason="marker_and_model_decision_present")
        return 0, "first-run already completed"

    opts = EnsureBootstrapArgs(
        dry_run=False,
        force_reinstall=False,
        model=model_override,
        allow_slow=False,
        host="127.0.0.1",
        port=LE_VIBE_MANAGED_OLLAMA_PORT,
        yes=yes,
        verbose=verbose,
        config_dir=cfg,
        use_managed_ollama=True,
        allow_pull_if_disk_ok=allow_pull,
        locked_model_policy=locked_pol,
    )
    code, _state = ensure_bootstrap(opts)
    append_structured_log("first_run", "bootstrap_finished", exit_code=code)
    if code == 0:
        try:
            marker.write_text("complete\n", encoding="utf-8")
        except OSError as e:
            logging.warning("could not write first-run marker: %s", e)
        return 0, "first-run bootstrap finished"
    return code, "first-run bootstrap failed; fix errors and retry (or use --force-first-run)"
