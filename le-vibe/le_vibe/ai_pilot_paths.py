"""STEP 17 / AI Pilot: paths for ``docs/AI_PILOT_AND_CONTINUE.md`` and related contracts."""

from __future__ import annotations

from pathlib import Path

# Same chain as docs/AI_PILOT_AND_CONTINUE.md *Relationship* + le-vibe/README STEP 17.
H17_MANIFEST: tuple[tuple[str, Path], ...] = (
    ("AI Pilot & Continue scope", Path("docs/AI_PILOT_AND_CONTINUE.md")),
    ("Continue workspace rules", Path("le-vibe/le_vibe/continue_workspace.py")),
    ("Root README (§7.1 Please continue / AI Pilot)", Path("README.md")),
)


def iter_h17_paths(root: Path) -> list[tuple[str, Path, bool]]:
    """Return ``(label, absolute_path, exists)`` for each STEP 17 path under ``root``."""
    out: list[tuple[str, Path, bool]] = []
    for label, rel in H17_MANIFEST:
        p = (root / rel).resolve()
        out.append((label, p, p.is_file()))
    return out
