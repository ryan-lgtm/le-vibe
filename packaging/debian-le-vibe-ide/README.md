# `le-vibe-ide` — Debian package for the Lé Vibe IDE tree

**Authority:** [`docs/PRODUCT_SPEC.md`](../../docs/PRODUCT_SPEC.md) §7.3 — the stack discovers the editor at **`/usr/lib/le-vibe/bin/codium`** (not a second public **`PATH`** CLI; **`lvibe`** remains the user-facing command).

This directory is a **separate Debian source** (sibling to the root **`debian/`** for the **`le-vibe`** stack package). It **repacks** a local **`VSCode-linux-*/`** build from **`editor/vscodium/`** after **`./dev/build.sh`**.

## Build steps

1. From the monorepo root, complete an IDE compile per [`editor/BUILD.md`](../../editor/BUILD.md) so **`editor/vscodium/VSCode-linux-*/`** exists.
2. **`./packaging/scripts/stage-le-vibe-ide-deb.sh`** — copies the tree into **`staging/`**, creates **`/usr/lib/le-vibe/bin/codium`** (symlink), and stages **`debian/le-vibe.desktop`** plus **`packaging/icons/.../le-vibe.svg`** for **`/usr/share/applications/`** and **`/usr/share/icons/hicolor/`** (§7.3 Freedesktop integration — no second public CLI; **`Exec=`** uses the internal **`codium`** path).
3. **`./packaging/scripts/build-le-vibe-ide-deb.sh`** — runs **`dpkg-buildpackage`** here; **`*.deb`** artifacts land under **`packaging/`** (gitignored).

The **`le-vibe`** package **`Suggests: le-vibe-ide`** so both can install from the same apt suite when published.

## Updates (roadmap — PRODUCT_SPEC §7.3)

**v1 / STEP 14:** This **`.deb`** does **not** ship a Lé Vibe–hosted in-app updater. A **Lé Vibe–controlled** update or distribution endpoint remains **roadmap** work (same §7.3 note as the stack package). Until then, refresh the IDE via **`apt`** / your release channel ([`docs/apt-repo-releases.md`](../../docs/apt-repo-releases.md)) or rebuild from the monorepo tag, same as the **`le-vibe`** stack.
