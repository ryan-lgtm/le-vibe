"""STEP 13 / H7: paths for Flatpak + AppImage templates (``docs/flatpak-appimage.md``)."""

from __future__ import annotations

from pathlib import Path

# Same chain as docs/flatpak-appimage.md *In this repository* table.
H7_MANIFEST: tuple[tuple[str, Path], ...] = (
    ("docs — flatpak-appimage.md", Path("docs/flatpak-appimage.md")),
    ("Flatpak manifest", Path("packaging/flatpak/org.le_vibe.Launcher.yml")),
    ("Flatpak README", Path("packaging/flatpak/README.md")),
    ("AppImage AppRun", Path("packaging/appimage/AppRun")),
    ("AppImage build script", Path("packaging/appimage/build-appimage.sh")),
    ("AppImage README", Path("packaging/appimage/README.md")),
)


def iter_h7_paths(root: Path) -> list[tuple[str, Path, bool]]:
    """Return ``(label, absolute_path, exists)`` for each H7 path under ``root``."""
    out: list[tuple[str, Path, bool]] = []
    for label, rel in H7_MANIFEST:
        p = (root / rel).resolve()
        out.append((label, p, p.is_file()))
    return out
