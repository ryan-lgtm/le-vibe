"""STEP 11 / H5: canonical brand asset paths (``docs/brand-assets.md``)."""

from __future__ import annotations

from pathlib import Path

# Relative to monorepo root — same table as docs/brand-assets.md.
SCALABLE_SVG_REL = Path("packaging") / "icons" / "hicolor" / "scalable" / "apps" / "le-vibe.svg"

# Installed by debian/le-vibe.install (hicolor theme).
PACKAGED_ICON_SVG = Path("/usr/share/icons/hicolor/scalable/apps/le-vibe.svg")


def resolve_scalable_icon_paths() -> tuple[Path | None, Path | None]:
    """
    Return ``(monorepo_svg, packaged_svg)`` — either may be ``None`` if that layout is absent.

    Monorepo path uses :func:`le_vibe.qa_scripts.find_monorepo_root`.
    """
    from le_vibe.qa_scripts import find_monorepo_root

    mono: Path | None = None
    root = find_monorepo_root()
    if root is not None:
        p = root / SCALABLE_SVG_REL
        if p.is_file():
            mono = p
    pkg: Path | None = None
    if PACKAGED_ICON_SVG.is_file():
        pkg = PACKAGED_ICON_SVG
    return mono, pkg
