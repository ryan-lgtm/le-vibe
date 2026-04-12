from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from .types import BootstrapState, ModelDecision

LOCKED_MODEL_FILENAME = "locked-model.json"


def _project_root() -> Path:
    return Path(__file__).resolve().parent.parent


def _templates_dir() -> Path:
    return _project_root() / "templates"


def _output_dir() -> Path:
    out = _project_root() / "output"
    out.mkdir(parents=True, exist_ok=True)
    return out


def _resolve_output_dir(config_dir: Path | None) -> Path:
    if config_dir is not None:
        config_dir.mkdir(parents=True, exist_ok=True)
        return config_dir
    return _output_dir()


def generate_continue_config(
    model_tag: str,
    host: str,
    port: int,
    *,
    config_dir: Path | None = None,
) -> Path:
    env = Environment(
        loader=FileSystemLoader(str(_templates_dir())),
        autoescape=select_autoescape(enabled_extensions=()),
    )
    tpl = env.get_template("continue-config.yaml.j2")
    text = tpl.render(selected_model=model_tag, host=host, port=port)

    out_dir = _resolve_output_dir(config_dir)
    dest = out_dir / "continue-config.yaml"
    if dest.exists():
        bak = out_dir / "continue-config.yaml.bak"
        shutil.copy2(dest, bak)

    dest.write_text(text, encoding="utf-8")
    return dest


def generate_report(state: BootstrapState, *, config_dir: Path | None = None) -> Path:
    env = Environment(
        loader=FileSystemLoader(str(_templates_dir())),
        autoescape=select_autoescape(enabled_extensions=("html", "xml")),
    )
    tpl = env.get_template("report.md.j2")
    hw = state.hardware
    decision = state.model_decision

    text = tpl.render(
        generated_at=datetime.now(timezone.utc).isoformat(),
        os_info=state.os_info,
        hardware=hw,
        prerequisites=state.prerequisites,
        tier=state.tier_assessment,
        decision=decision,
        ollama_installed=state.ollama_installed,
        ollama_version=state.ollama_version,
        ollama_was_running=state.ollama_was_running,
        ollama_started_by_script=state.ollama_started_by_script,
        host=state.host,
        port=state.port,
        api_verified=state.api_verified,
        dry_run=state.dry_run,
        install_log=state.install_log,
        pull_log=state.pull_log,
    )

    out_dir = _resolve_output_dir(config_dir)
    dest = out_dir / "bootstrap-report.md"
    dest.write_text(text, encoding="utf-8")
    return dest


def write_locked_model_json(
    model_tag: str,
    *,
    reason_excerpt: str = "",
    policy: str = "hardware_tier_best_fit",
    config_dir: Path | None = None,
) -> Path:
    """
    Persist the concrete Ollama model tag under ~/.config/le-vibe/ (never AUTODETECT as sole stored value).
    Inspect `locked-model.json` for the machine-local lock; upgrades do not silently drift without a new bootstrap.
    """
    out_dir = _resolve_output_dir(config_dir)
    dest = out_dir / LOCKED_MODEL_FILENAME
    payload = {
        "ollama_model": model_tag.strip(),
        "locked_at_utc": datetime.now(timezone.utc).isoformat(),
        "policy": policy,
        "selection_reason_excerpt": (reason_excerpt or "")[:2000],
    }
    dest.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return dest


def write_model_decision_json(
    decision: ModelDecision | None,
    *,
    config_dir: Path | None = None,
    locked_policy: str | None = None,
) -> Path:
    out_dir = _resolve_output_dir(config_dir)
    dest = out_dir / "model-decision.json"
    if decision is None:
        dest.write_text("{}", encoding="utf-8")
        return dest
    from .models import model_decision_to_json

    dest.write_text(json.dumps(model_decision_to_json(decision), indent=2), encoding="utf-8")
    policy = locked_policy or "hardware_tier_best_fit"
    if decision.selected_model and decision.selected_model.strip():
        write_locked_model_json(
            decision.selected_model,
            reason_excerpt=decision.reason,
            config_dir=config_dir,
            policy=policy,
        )
    return dest
