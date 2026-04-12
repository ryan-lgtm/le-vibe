# `le-vibe-ide` — Debian package for the Lé Vibe IDE tree

**Authority:** [`docs/PRODUCT_SPEC.md`](../../docs/PRODUCT_SPEC.md) §7.3 — the stack discovers the editor at **`/usr/lib/le-vibe/bin/codium`** (not a second public **`PATH`** CLI; **`lvibe`** remains the user-facing command).

This directory is a **separate Debian source** (sibling to the root **`debian/`** for the **`le-vibe`** stack package). It **repacks** a local **`VSCode-linux-*/`** tree from **`editor/vscodium/`** produced by **`editor/vscodium/dev/build.sh`** — for **§7.3** layers (merge, icons, defaults), use **`./packaging/scripts/ci-vscodium-linux-dev-build.sh`** from the repo root or repeat those steps manually (**[`editor/BUILD.md`](../../editor/BUILD.md)** *Linux icons*).

**Fresh clone (14.b):** if **`editor/vscodium/`** is empty after **`git clone`**, run **`git submodule update --init editor/vscodium`** from the monorepo root before compiling — **`editor/README.md`** *Fresh clone (14.b)*, **`editor/BUILD.md`**.

## Build steps

1. From the monorepo root, complete an IDE compile per [`editor/BUILD.md`](../../editor/BUILD.md) so **`editor/vscodium/VSCode-linux-*/`** exists. For **§7.3** (merged **`product.json`**, **`sync-linux-icon-assets.sh`**, **`build-env.lvibe-defaults.sh`**) before **`dev/build.sh`**, run **`./packaging/scripts/ci-vscodium-linux-dev-build.sh`** from the repo root; calling **`./dev/build.sh`** only from **`editor/vscodium/`** skips that wrapper unless you repeat those steps manually (**BUILD.md** *Linux icons*).
2. **`./packaging/scripts/stage-le-vibe-ide-deb.sh`** — copies the tree into **`staging/`**, creates **`/usr/lib/le-vibe/bin/codium`** (symlink), and stages **`debian/le-vibe.desktop`** plus **`packaging/icons/.../le-vibe.svg`** for **`/usr/share/applications/`** and **`/usr/share/icons/hicolor/`** (§7.3 Freedesktop integration — no second public CLI; **`Exec=`** uses the internal **`codium`** path).
3. **`./packaging/scripts/build-le-vibe-ide-deb.sh`** — runs **`dpkg-buildpackage`** here; **`*.deb`** artifacts land under **`packaging/`** (gitignored).

**Stack + IDE in one pass (STEP 14 / demo):** from the monorepo root, **`./packaging/scripts/build-le-vibe-debs.sh --with-ide`** builds **`le-vibe_*_all.deb`** (root **`debian/`**) and then this IDE **`.deb`** when **`VSCode-linux-*`** exists — **[`docs/PM_DEB_BUILD_ITERATION.md`](../../docs/PM_DEB_BUILD_ITERATION.md)**. For releases, attach **`le-vibe_*_all.deb`**, **`le-vibe-ide_*_amd64.deb`**, and **`SHA256SUMS`** — **[`docs/apt-repo-releases.md`](../../docs/apt-repo-releases.md)** (*IDE package*).

## Lintian (optional)

**`./packaging/scripts/build-le-vibe-ide-deb.sh`** runs **`lintian`** automatically when it is on **`PATH`** after **`dpkg-buildpackage`**. Tags are **non-fatal** unless **`LEVIBE_IDE_LINTIAN_STRICT=1`** is set in the environment. Manually, from the monorepo root: **`lintian packaging/le-vibe-ide_*_*.deb`**. Use tags as hints — **[`docs/ci-qa-hardening.md`](../../docs/ci-qa-hardening.md)**; the stack **`debian/`** package may run stricter QA in CI (**STEP 10** / **H3**).

The **`le-vibe`** package **`Suggests: le-vibe-ide`** so both can install from the same apt suite when published.

## Updates (roadmap — PRODUCT_SPEC §7.3)

**v1 / STEP 14:** This **`.deb`** does **not** ship a Lé Vibe–hosted in-app updater. A **Lé Vibe–controlled** update or distribution endpoint remains **roadmap** work (same §7.3 note as the stack package). Until then, refresh the IDE via **`apt`** / your release channel ([`docs/apt-repo-releases.md`](../../docs/apt-repo-releases.md)) or rebuild from the monorepo tag, same as the **`le-vibe`** stack.
