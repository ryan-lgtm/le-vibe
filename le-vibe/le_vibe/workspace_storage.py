"""Usage metering, persistence, and compaction for ``.lvibe/`` (PRODUCT_SPEC §5.4–5.5)."""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .structured_log import append_structured_log
from .workspace_policy import cap_mb_from_environ, get_cap_mb

_LVIBE = ".lvibe"

# Re-export for callers that import size of tree
def _dir_size_bytes(root: Path) -> int:
    total = 0
    try:
        for p in root.rglob("*"):
            if p.is_file():
                total += p.stat().st_size
    except OSError as e:
        logging.debug("workspace_storage: size walk failed: %s", e)
    return total


def write_storage_state(
    workspace_root: Path,
    *,
    cap_mb: int,
    usage_bytes: int,
) -> Path:
    """Write ``.lvibe/storage-state.json`` with usage vs cap (PRODUCT_SPEC §5.4)."""
    lv = workspace_root / _LVIBE
    out = lv / "storage-state.json"
    payload: dict[str, Any] = {
        "schema": "lvibe-storage-state.v1",
        "cap_mb": cap_mb,
        "usage_bytes": usage_bytes,
        "usage_human": _format_mb(usage_bytes),
        "cap_human": f"{cap_mb} MB",
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return out


def _format_mb(nbytes: int) -> str:
    mb = nbytes / (1024 * 1024)
    return f"{mb:.2f} MB"


def compact_lvibe_tree(workspace_root: Path, cap_mb: int) -> list[str]:
    """
    Deterministic compaction when usage exceeds cap (PRODUCT_SPEC §5.5).

    Order: shared RAG/chunks first, then trim incremental memory, then round-robin among
    per-agent files. Does not remove ``session-manifest.json``; if still over cap, logs only.
    """
    lvibe = workspace_root / _LVIBE
    if not lvibe.is_dir():
        return []
    cap_bytes = cap_mb * 1024 * 1024
    actions: list[str] = []

    def over() -> bool:
        return _dir_size_bytes(lvibe) > cap_bytes

    if not over():
        return []

    # 1) RAG + legacy chunks: remove oldest files by mtime (refs only)
    for tree_name in ("rag", "chunks"):
        sub = lvibe / tree_name
        if not sub.is_dir():
            continue
        files = [p for p in sub.rglob("*") if p.is_file()]
        files.sort(key=lambda p: p.stat().st_mtime)
        for f in files:
            if not over():
                break
            try:
                rel = f.relative_to(lvibe)
                f.unlink()
                actions.append(f"removed {rel}")
            except OSError:
                continue

    # 2) Per-agent: trim largest skill.md files last — remove oldest small sidecars first
    agents = lvibe / "agents"
    if agents.is_dir() and over():
        sidecars: list[Path] = []
        for agent_dir in sorted(agents.iterdir()):
            if not agent_dir.is_dir():
                continue
            for f in agent_dir.iterdir():
                if f.is_file() and f.name not in ("skill.md",):
                    sidecars.append(f)
        sidecars.sort(key=lambda p: p.stat().st_mtime)
        for f in sidecars:
            if not over():
                break
            try:
                rel = f.relative_to(lvibe)
                f.unlink()
                actions.append(f"removed {rel}")
            except OSError:
                continue

    # 3) memory/incremental.md — truncate from the top (keep tail) if still over
    inc = lvibe / "memory" / "incremental.md"
    if inc.is_file() and over():
        try:
            text = inc.read_text(encoding="utf-8", errors="replace")
            if len(text) > 800:
                tail = text[-400:]
                inc.write_text(
                    "# Incremental memory (bounded)\n\n"
                    "_Truncated by Lé Vibe storage compaction (PRODUCT_SPEC §5.5)._\n\n"
                    + tail,
                    encoding="utf-8",
                )
                actions.append("truncated memory/incremental.md")
        except OSError:
            pass

    # 4) Round-robin among agents/*/skill.md — shorten files (never delete manifest)
    if over() and agents.is_dir():
        agent_dirs = sorted([p for p in agents.iterdir() if p.is_dir()])
        round_idx = 0
        safety = 400
        while over() and safety > 0 and agent_dirs:
            safety -= 1
            d = agent_dirs[round_idx % len(agent_dirs)]
            round_idx += 1
            skill = d / "skill.md"
            if not skill.is_file():
                continue
            try:
                st = skill.read_text(encoding="utf-8", errors="replace")
                if len(st) < 400:
                    continue
                skill.write_text(st[: len(st) // 2] + "\n\n_…compacted…_\n", encoding="utf-8")
                actions.append(f"compacted {skill.relative_to(lvibe)}")
            except OSError:
                continue

    if over():
        actions.append(
            f"warning: still over cap after compaction ({_format_mb(_dir_size_bytes(lvibe))} / {cap_mb} MB)"
        )

    return actions


def refresh_storage_metadata(workspace_root: Path, *, config_dir: Path | None = None) -> tuple[int, int]:
    """Recompute usage, optionally compact, write ``storage-state.json``. Returns (usage_bytes, cap_mb)."""
    lvibe = workspace_root / _LVIBE
    env_cap = cap_mb_from_environ()
    cap = env_cap if env_cap is not None else get_cap_mb(workspace_root, config_dir=config_dir)
    if not lvibe.is_dir():
        return 0, cap
    usage = _dir_size_bytes(lvibe)
    if usage > cap * 1024 * 1024:
        actions = compact_lvibe_tree(workspace_root, cap)
        if actions:
            append_structured_log(
                "workspace",
                "lvibe_compaction",
                workspace=str(workspace_root.resolve()),
                actions=actions[:40],
            )
        usage = _dir_size_bytes(lvibe)
    write_storage_state(workspace_root, cap_mb=cap, usage_bytes=usage)
    return usage, cap
