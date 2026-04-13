"""STEP 14 / H6: paths for §7.3 IDE packaging — VSCode-linux tree, branding, staging scripts."""

from __future__ import annotations

from pathlib import Path


def find_vscode_linux_tree(root: Path) -> Path | None:
    """Return ``editor/vscodium/VSCode-linux-*`` when it contains ``bin/codium``."""
    vsc = root / "editor" / "vscodium"
    if not vsc.is_dir():
        return None
    for p in sorted(vsc.glob("VSCode-linux-*")):
        if p.is_dir() and (p / "bin" / "codium").is_file():
            return p.resolve()
    return None


def iter_ide_prereq_paths(root: Path) -> list[tuple[str, Path, bool]]:
    """
    Return ``(label, absolute_path, exists)`` for §7.3 packaging touchpoints.

    The VSCode-linux tree is **optional** until ``dev/build.sh`` completes — reported distinctly.
    """
    out: list[tuple[str, Path, bool]] = []

    vs = find_vscode_linux_tree(root)
    if vs is not None:
        out.append(("VSCode-linux tree (for le-vibe-ide .deb)", vs, True))
    else:
        pending = (root / "editor" / "vscodium").resolve()
        out.append(("VSCode-linux tree (for le-vibe-ide .deb) — run editor/BUILD.md", pending, False))

    fixed: tuple[tuple[str, Path], ...] = (
        ("Branding merge (§7.3)", Path("editor/le-vibe-overrides/product-branding-merge.json")),
        ("Linux icon sync", Path("editor/le-vibe-overrides/sync-linux-icon-assets.sh")),
        (
            "VSCodium linux le-vibe.svg (after sync; LEVIBE_EDITOR_GATE_ASSERT_BRAND)",
            Path("editor/vscodium/src/stable/resources/linux/le-vibe.svg"),
        ),
        ("Canonical app icon (stack)", Path("packaging/icons/hicolor/scalable/apps/le-vibe.svg")),
        ("Stage IDE → deb staging", Path("packaging/scripts/stage-le-vibe-ide-deb.sh")),
        ("Build le-vibe-ide .deb", Path("packaging/scripts/build-le-vibe-ide-deb.sh")),
        ("Full-product stack + IDE", Path("packaging/scripts/build-le-vibe-debs.sh")),
        ("IDE debian metadata", Path("packaging/debian-le-vibe-ide/debian/control")),
    )
    for label, rel in fixed:
        p = (root / rel).resolve()
        out.append((label, p, p.is_file()))
    return out


# Relative paths for ``lvibe ide-prereqs --path-only KEY`` (except ``vscode`` — use ``find_vscode_linux_tree``).
IDE_PREREQ_PATH_ONLY: dict[str, Path] = {
    "branding": Path("editor/le-vibe-overrides/product-branding-merge.json"),
    "sync-icons": Path("editor/le-vibe-overrides/sync-linux-icon-assets.sh"),
    "vsc-linux-svg": Path("editor/vscodium/src/stable/resources/linux/le-vibe.svg"),
    "svg": Path("packaging/icons/hicolor/scalable/apps/le-vibe.svg"),
    "stage": Path("packaging/scripts/stage-le-vibe-ide-deb.sh"),
    "build-ide-deb": Path("packaging/scripts/build-le-vibe-ide-deb.sh"),
    "build-debs": Path("packaging/scripts/build-le-vibe-debs.sh"),
    "control": Path("packaging/debian-le-vibe-ide/debian/control"),
}
