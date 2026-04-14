"""Append-safe, optionally idempotent writes to ``memory/incremental.md`` (PRODUCT_SPEC §5.3)."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path


def append_incremental_fact(
    workspace_root: Path,
    text: str,
    *,
    idempotent_id: str | None = None,
) -> tuple[bool, Path]:
    """
    Append a short dated line to ``.lvibe/memory/incremental.md``.

    If ``idempotent_id`` is set and a matching ``lvibe:fact`` block already exists, returns
    ``(False, path)`` without writing. Otherwise returns ``(True, path)``.

    Raises:
        FileNotFoundError: if ``.lvibe/memory/incremental.md`` is missing.
        ValueError: if ``text`` is empty or ``idempotent_id`` is invalid.
    """
    inc = workspace_root / ".lvibe" / "memory" / "incremental.md"
    if not inc.is_file():
        raise FileNotFoundError(str(inc))
    body = text.strip()
    if not body:
        raise ValueError("text must be non-empty")
    if idempotent_id is not None:
        tid = idempotent_id.strip()
        if not tid or "\n" in tid or "-->" in tid or "<!--" in tid:
            raise ValueError("idempotent_id must be a short single-line token")
        idempotent_id = tid

    existing = inc.read_text(encoding="utf-8", errors="replace")
    if idempotent_id:
        marker = f"<!-- lvibe:fact id={idempotent_id} -->"
        if marker in existing:
            return False, inc

    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    line = f"- {stamp} — {body}\n"
    if idempotent_id:
        block = (
            f"<!-- lvibe:fact id={idempotent_id} -->\n"
            f"{line}"
            "<!-- /lvibe:fact -->\n"
        )
    else:
        block = line

    with inc.open("a", encoding="utf-8") as f:
        if existing and not existing.endswith("\n"):
            f.write("\n")
        f.write(block)
    return True, inc
