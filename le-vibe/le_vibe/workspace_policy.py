"""Persist workspace consent, storage caps, and usage metadata under ``~/.config/le-vibe/`` (PRODUCT_SPEC §5)."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Literal

from .paths import le_vibe_config_dir

ConsentValue = Literal["accepted", "declined"]

DEFAULT_CAP_MB = 50
MIN_CAP_MB = 10
MAX_CAP_MB = 500
POLICY_FILENAME = "workspace-policy.json"


def workspace_key(workspace_root: Path) -> str:
    """Stable key for policy JSON (resolved absolute path)."""
    try:
        return str(workspace_root.resolve())
    except OSError:
        return str(workspace_root)


def policy_path(config_dir: Path | None = None) -> Path:
    return (config_dir or le_vibe_config_dir()) / POLICY_FILENAME


def clamp_cap_mb(raw: int | float | None) -> int:
    if raw is None:
        return DEFAULT_CAP_MB
    try:
        v = int(raw)
    except (TypeError, ValueError):
        return DEFAULT_CAP_MB
    return max(MIN_CAP_MB, min(MAX_CAP_MB, v))


def load_policy(config_dir: Path | None = None) -> dict[str, Any]:
    p = policy_path(config_dir)
    if not p.is_file():
        return {"version": 1, "default_cap_mb": DEFAULT_CAP_MB, "workspaces": {}}
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {"version": 1, "default_cap_mb": DEFAULT_CAP_MB, "workspaces": {}}
    if not isinstance(data, dict):
        return {"version": 1, "default_cap_mb": DEFAULT_CAP_MB, "workspaces": {}}
    ws = data.get("workspaces")
    if not isinstance(ws, dict):
        data["workspaces"] = {}
    data.setdefault("version", 1)
    data.setdefault("default_cap_mb", DEFAULT_CAP_MB)
    data["default_cap_mb"] = clamp_cap_mb(data.get("default_cap_mb"))
    return data


def save_policy(data: dict[str, Any], config_dir: Path | None = None) -> None:
    p = policy_path(config_dir)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(".tmp")
    text = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    tmp.write_text(text, encoding="utf-8")
    tmp.replace(p)


def get_workspace_entry(
    workspace_root: Path,
    *,
    config_dir: Path | None = None,
) -> dict[str, Any] | None:
    key = workspace_key(workspace_root)
    pol = load_policy(config_dir)
    ws = pol.get("workspaces")
    if not isinstance(ws, dict):
        return None
    entry = ws.get(key)
    return entry if isinstance(entry, dict) else None


def get_consent(
    workspace_root: Path,
    *,
    config_dir: Path | None = None,
) -> ConsentValue | None:
    entry = get_workspace_entry(workspace_root, config_dir=config_dir)
    if not entry:
        return None
    c = entry.get("consent")
    if c in ("accepted", "declined"):
        return c  # type: ignore[return-value]
    return None


def set_consent(
    workspace_root: Path,
    consent: ConsentValue,
    *,
    config_dir: Path | None = None,
) -> None:
    key = workspace_key(workspace_root)
    pol = load_policy(config_dir)
    ws = pol.setdefault("workspaces", {})
    if not isinstance(ws, dict):
        ws = {}
        pol["workspaces"] = ws
    cur = ws.get(key)
    if not isinstance(cur, dict):
        cur = {}
    cur["consent"] = consent
    ws[key] = cur
    save_policy(pol, config_dir=config_dir)


def get_cap_mb(workspace_root: Path, *, config_dir: Path | None = None) -> int:
    pol = load_policy(config_dir)
    default = clamp_cap_mb(pol.get("default_cap_mb"))
    entry = get_workspace_entry(workspace_root, config_dir=config_dir)
    if entry and entry.get("cap_mb") is not None:
        return clamp_cap_mb(entry.get("cap_mb"))
    return default


def set_default_cap_mb(mb: int, *, config_dir: Path | None = None) -> None:
    pol = load_policy(config_dir)
    pol["default_cap_mb"] = clamp_cap_mb(mb)
    save_policy(pol, config_dir=config_dir)


def set_workspace_cap_mb(
    workspace_root: Path,
    mb: int,
    *,
    config_dir: Path | None = None,
) -> None:
    key = workspace_key(workspace_root)
    pol = load_policy(config_dir)
    ws = pol.setdefault("workspaces", {})
    if not isinstance(ws, dict):
        ws = {}
        pol["workspaces"] = ws
    cur = ws.get(key)
    if not isinstance(cur, dict):
        cur = {}
    cur["cap_mb"] = clamp_cap_mb(mb)
    ws[key] = cur
    save_policy(pol, config_dir=config_dir)


def cap_mb_from_environ() -> int | None:
    raw = os.environ.get("LE_VIBE_LVIBE_CAP_MB", "").strip()
    if not raw:
        return None
    try:
        return clamp_cap_mb(int(raw))
    except ValueError:
        return None
