"""STEP 14 / H6: paths for §7.3 IDE packaging — VSCode-linux tree, branding, staging scripts."""

from __future__ import annotations

from pathlib import Path
from typing import Literal

VscodeLinuxBuildStatus = Literal["ready", "partial", "absent"]


def vscode_linux_build_status(root: Path) -> tuple[VscodeLinuxBuildStatus, Path | None]:
    """
    Classify the local VSCode-linux output under ``editor/vscodium/``.

    * **ready** — ``VSCode-linux-*/bin/codium`` exists (14.c complete).
    * **partial** — a ``VSCode-linux-*`` directory exists but ``bin/codium`` is missing
      (incomplete compile; see ``editor/BUILD.md`` *Partial tree*).
    * **absent** — no usable tree (fresh submodule or no build yet).
    """
    vsc = root / "editor" / "vscodium"
    if not vsc.is_dir():
        return "absent", None
    for p in sorted(vsc.glob("VSCode-linux-*")):
        if p.is_dir() and (p / "bin" / "codium").is_file():
            return "ready", p.resolve()
    for p in sorted(vsc.glob("VSCode-linux-*")):
        if p.is_dir():
            return "partial", p.resolve()
    return "absent", None


def find_vscode_linux_tree(root: Path) -> Path | None:
    """Return ``editor/vscodium/VSCode-linux-*`` when it contains ``bin/codium``."""
    st, p = vscode_linux_build_status(root)
    return p if st == "ready" else None


def vscode_linux_bin_filenames(vs_tree: Path | None) -> list[str] | None:
    """
    Filenames in ``VSCode-linux-*/bin`` when a tree path is known (partial or ready).

    ``None`` when there is no ``VSCode-linux-*`` directory; empty list when ``bin/`` is missing
    or empty. Helps diagnose **partial** trees (e.g. only ``codium-tunnel``).
    """
    if vs_tree is None:
        return None
    bin_dir = vs_tree / "bin"
    if not bin_dir.is_dir():
        return []
    return sorted(p.name for p in bin_dir.iterdir() if p.is_file())


def iter_ide_prereq_paths(root: Path) -> list[tuple[str, Path, bool]]:
    """
    Return ``(label, absolute_path, exists)`` for §7.3 packaging touchpoints.

    The VSCode-linux tree is **optional** until ``dev/build.sh`` completes — reported distinctly.
    """
    out: list[tuple[str, Path, bool]] = []

    st, vs = vscode_linux_build_status(root)
    if st == "ready":
        out.append(("VSCode-linux tree (for le-vibe-ide .deb)", vs, True))
    elif st == "partial":
        out.append(
            (
                "VSCode-linux tree — partial (bin/codium missing); editor/BUILD.md *Partial tree* / 14.c",
                vs,
                False,
            )
        )
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

# Keys for ``static_prereq_files_ok`` in ``lvibe ide-prereqs --json``: repo-shipped §7.3 inputs only.
# ``vsc-linux-svg`` is produced by sync-linux-icon-assets.sh before dev/build.sh — omit from the static gate.
IDE_PREREQ_STATIC_OK_KEYS: tuple[str, ...] = (
    "branding",
    "sync-icons",
    "svg",
    "stage",
    "build-ide-deb",
    "build-debs",
    "control",
)


def static_prereq_repo_files_ok(root: Path) -> bool:
    """True when every committed packaging / override file needed for §7.3 automation exists."""
    return all((root / IDE_PREREQ_PATH_ONLY[k]).is_file() for k in IDE_PREREQ_STATIC_OK_KEYS)
