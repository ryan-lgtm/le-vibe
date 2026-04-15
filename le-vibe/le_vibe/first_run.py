"""One-time product bootstrap: Ollama + model pull + configs under ~/.config/le-vibe/ (spec-phase2 install/first-run)."""

from __future__ import annotations

import json
import logging
import os
import subprocess
from pathlib import Path

from .api import EnsureBootstrapArgs, ensure_bootstrap
from .models import clear_tag_cache
from .ollama_ops import list_local_model_names, model_tag_present_locally, verify_api
from .paths import LE_VIBE_MANAGED_OLLAMA_PORT, le_vibe_config_dir
from .structured_log import append_structured_log
from .user_settings import load_user_settings

_DISALLOWED_EXTENSION_IDS: tuple[str, ...] = ("continue.continue",)


def first_run_marker_path(config_dir: Path | None = None) -> Path:
    return (config_dir or le_vibe_config_dir()) / ".first-run-complete"


def _default_editor_for_readiness() -> str:
    env = os.environ.get("LE_VIBE_EDITOR")
    if env:
        return env
    lv_ide = "/usr/lib/le-vibe/bin/codium"
    if os.path.isfile(lv_ide) and os.access(lv_ide, os.X_OK):
        return lv_ide
    if os.path.isfile("/usr/bin/codium") and os.access("/usr/bin/codium", os.X_OK):
        return "/usr/bin/codium"
    return "codium"


def _disallowed_extension_remediation(editor: str, extension_id: str) -> str:
    return (
        f"Lé Vibe: disallowed extension `{extension_id}` is active in the selected editor. "
        "Continue must be removed for a Cline-only runtime. "
        f"Run `{editor} --uninstall-extension {extension_id}` and retry `lvibe`."
    )


def evaluate_first_run_agent_readiness(
    *,
    config_dir: Path | None = None,
    host: str = "127.0.0.1",
    port: int = LE_VIBE_MANAGED_OLLAMA_PORT,
) -> tuple[bool, str]:
    """
    C2 readiness gate:
    - managed Ollama API responds,
    - selected model exists on the managed API,
    - Cline extension is active in the target editor binary.
    """
    cfg = config_dir or le_vibe_config_dir()
    if not verify_api(host, port):
        return (
            False,
            f"Lé Vibe: Ollama API is not reachable at http://{host}:{port}. "
            "Run `lvibe --force-first-run` and retry.",
        )

    model_decision = cfg / "model-decision.json"
    if not model_decision.is_file():
        return (
            False,
            "Lé Vibe: missing model decision state (~/.config/le-vibe/model-decision.json). "
            "Run `lvibe --force-first-run` to regenerate first-run state.",
        )
    try:
        payload = json.loads(model_decision.read_text(encoding="utf-8"))
        selected_model = str(payload.get("selected_model") or "").strip()
    except (OSError, json.JSONDecodeError):
        return (
            False,
            "Lé Vibe: model decision state is unreadable. "
            "Run `lvibe --force-first-run` to repair configuration state.",
        )
    if not selected_model:
        return (
            False,
            "Lé Vibe: no selected model is recorded. "
            "Run `lvibe --force-first-run` and choose/allow a model.",
        )
    names = list_local_model_names(host, port)
    if not model_tag_present_locally(selected_model, names):
        return (
            False,
            f"Lé Vibe: selected model `{selected_model}` is missing on managed Ollama ({host}:{port}). "
            "Enable pull in user settings or run `lvibe --force-first-run` to repair.",
        )

    editor = _default_editor_for_readiness()
    try:
        out = subprocess.check_output([editor, "--list-extensions"], text=True, stderr=subprocess.STDOUT)
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        return (
            False,
            f"Lé Vibe: cannot inspect editor extensions via `{editor} --list-extensions`. "
            "Install/configure the Lé Vibe editor binary and rerun `lvibe`.",
        )
    exts = {ln.strip().lower() for ln in out.splitlines() if ln.strip()}
    for ext_id in _DISALLOWED_EXTENSION_IDS:
        if ext_id in exts:
            return False, _disallowed_extension_remediation(editor, ext_id)
    if "saoudrizwan.claude-dev" not in exts:
        return (
            False,
            "Lé Vibe: Cline extension is not active in the selected editor. "
            "Run `le-vibe-setup-cline` and retry.",
        )
    return True, "agent-ready"


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
    return (
        code,
        "first-run bootstrap failed; fix errors above and retry, or use --force-first-run. "
        "Set LE_VIBE_VERBOSE=1 for more detail. "
        "`lvibe --help` lists --skip-first-run / --force-first-run (STEP 6). "
        "Inspect logs: `lvibe logs` prints the path and `Live: tail -f …` lines (same as the command); "
        "`lvibe logs --path-only`, or `lvibe logs --tail 50` (adjust N; STEP 6).",
    )
