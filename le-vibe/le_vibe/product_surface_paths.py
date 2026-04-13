"""STEP 12 / H8: paths for product-surface / trust files (``docs/PM_STAGE_MAP.md`` STEP 12)."""

from __future__ import annotations

from pathlib import Path

# Same chain as le-vibe/README.md *Trust / H8* and docs/README.md opener.
H8_MANIFEST: tuple[tuple[str, Path], ...] = (
    ("GitHub Actions workflow", Path(".github/workflows/ci.yml")),
    ("Dependabot", Path(".github/dependabot.yml")),
    ("Issue templates (config.yml # H8)", Path(".github/ISSUE_TEMPLATE/config.yml")),
    ("Docs index — product surface", Path("docs/README.md")),
    ("Privacy & telemetry", Path("docs/privacy-and-telemetry.md")),
    ("Security policy", Path("SECURITY.md")),
)


def iter_h8_paths(root: Path) -> list[tuple[str, Path, bool]]:
    """Return ``(label, absolute_path, exists)`` for each H8 path under ``root``."""
    out: list[tuple[str, Path, bool]] = []
    for label, rel in H8_MANIFEST:
        p = (root / rel).resolve()
        out.append((label, p, p.is_file()))
    return out
