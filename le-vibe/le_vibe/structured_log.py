"""Append-only JSON lines log under ``~/.config/le-vibe/`` — local only; no third-party telemetry."""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .paths import le_vibe_config_dir

STRUCTURED_LOG_FILENAME = "le-vibe.log.jsonl"


def structured_log_path() -> Path:
    return le_vibe_config_dir() / STRUCTURED_LOG_FILENAME


def structured_log_enabled() -> bool:
    return os.environ.get("LE_VIBE_STRUCTURED_LOG", "1").strip().lower() not in (
        "0",
        "false",
        "no",
        "off",
    )


def append_structured_log(component: str, event: str, **fields: Any) -> None:
    """
    Append one JSON object per line (UTC ``ts``, ``component``, ``event``, optional fields).
    Fails silently if the config dir is not writable (launcher must stay robust).
    """
    if not structured_log_enabled():
        return
    record: dict[str, Any] = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "component": component,
        "event": event,
    }
    for k, v in fields.items():
        if v is not None:
            record[k] = v
    path = structured_log_path()
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False, default=str) + "\n")
    except OSError:
        return
