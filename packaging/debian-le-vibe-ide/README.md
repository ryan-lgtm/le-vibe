# `le-vibe-ide` — Debian package for the Lé Vibe IDE tree

**Authority:** [`docs/PRODUCT_SPEC.md`](../../docs/PRODUCT_SPEC.md) §7.3 — the stack discovers the editor at **`/usr/lib/le-vibe/bin/codium`** (not a second public **`PATH`** CLI; **`lvibe`** remains the user-facing command).

This directory is a **separate Debian source** (sibling to the root **`debian/`** for the **`le-vibe`** stack package). It **repacks** a local **`VSCode-linux-*/`** tree from **`editor/vscodium/`** produced by **`editor/vscodium/dev/build.sh`** — for **§7.3** layers (merge, icons, defaults), use **`./packaging/scripts/ci-vscodium-linux-dev-build.sh`** from the repo root or repeat those steps manually (**[`editor/BUILD.md`](../../editor/BUILD.md)** *Linux icons*).

**Fresh clone (14.b):** if **`editor/vscodium/`** is empty after **`git clone`**, run **`git submodule update --init editor/vscodium`** from the monorepo root before compiling — **`editor/README.md`** *Fresh clone (14.b)*, **`editor/BUILD.md`**.

## Build steps

1. From the monorepo root, complete an IDE compile per [`editor/BUILD.md`](../../editor/BUILD.md) so **`editor/vscodium/VSCode-linux-*/`** exists. For **§7.3** (merged **`product.json`**, **`sync-linux-icon-assets.sh`**, **`build-env.lvibe-defaults.sh`**) before **`dev/build.sh`**, run **`./packaging/scripts/ci-vscodium-linux-dev-build.sh`** from the repo root; calling **`./dev/build.sh`** only from **`editor/vscodium/`** skips that wrapper unless you repeat those steps manually (**BUILD.md** *Linux icons*).
2. **`./packaging/scripts/stage-le-vibe-ide-deb.sh`** — copies the tree into **`staging/`**, creates **`/usr/lib/le-vibe/bin/codium`** (symlink), and stages **`debian/le-vibe.desktop`** plus **`packaging/icons/.../le-vibe.svg`** for **`/usr/share/applications/`** and **`/usr/share/icons/hicolor/`** (§7.3 Freedesktop integration — no second public CLI; **`Exec=`** uses the internal **`codium`** path). The script **warns** if **`VSCode-linux-*/resources/app/product.json`** lacks **Lé Vibe** strings (upstream-only compile). Set **`LEVIBE_STAGE_IDE_ASSERT_BRAND=1`** to **fail** staging when identity is missing; **`LEVIBE_STAGE_IDE_VERBOSE=1`** prints a line when the check passes.
3. **`./packaging/scripts/build-le-vibe-ide-deb.sh`** — runs **`dpkg-buildpackage`** here; **`*.deb`** artifacts land under **`packaging/`** (gitignored).

**Stack + IDE in one pass (STEP 14 / demo):** from the monorepo root, **`./packaging/scripts/build-le-vibe-debs.sh --with-ide`** builds **`le-vibe_*_all.deb`** (root **`debian/`**) and then this IDE **`.deb`** when **`VSCode-linux-*`** exists; on success it prints **Full-product install** — **[`docs/PM_DEB_BUILD_ITERATION.md`](../../docs/PM_DEB_BUILD_ITERATION.md)** (*Success output (`--with-ide`)*). For releases, attach **`le-vibe_*_all.deb`**, **`le-vibe-ide_*_amd64.deb`**, and **`SHA256SUMS`** — **[`docs/apt-repo-releases.md`](../../docs/apt-repo-releases.md)** (*IDE package*).

## Install both packages (owner / demo)

Use the **same version train** for **`le-vibe`** and **`le-vibe-ide`**. From a directory that contains both **`.deb`** files:

```bash
sudo apt install ./le-vibe_*_all.deb ./le-vibe-ide_*_amd64.deb
```

**`apt`** pulls declared dependencies; if you use **`dpkg -i`** on both files instead, run **`sudo apt -f install`** afterward if the resolver asks.

**After install:** follow the stack post-install flow in **`/usr/share/doc/le-vibe/README.Debian`** (first-run **`lvibe`**, **`le-vibe-setup-continue`**, **§5** **`.lvibe/`** consent). The IDE binary is **`/usr/lib/le-vibe/bin/codium`**; the desktop environment’s **Lé Vibe** menu entry ( **`le-vibe.desktop`**) starts that binary — see also **`debian/le-vibe.README.Debian`** in the monorepo (*Desktop launcher*).

**CI vs maintainer .deb bundles:** Default **`ci.yml`** artifact **`le-vibe-deb`** ships the stack **`le-vibe`** **`.deb`**, SBOM, and **`SHA256SUMS`** for those files — **not** **`le-vibe-ide_*_amd64.deb`**. Honesty — **[`docs/PM_STAGE_MAP.md`](../../docs/PM_STAGE_MAP.md)** (*H1 vs §7.3 .deb bundles*); monorepo table — **[`spec-phase2.md`](../../spec-phase2.md)** *CI `le-vibe-deb` vs maintainer `le-vibe-ide`*.

## Lintian (optional)

**`./packaging/scripts/build-le-vibe-ide-deb.sh`** runs **`lintian`** automatically when it is on **`PATH`** after **`dpkg-buildpackage`**. Tags are **non-fatal** unless **`LEVIBE_IDE_LINTIAN_STRICT=1`** is set in the environment. Manually, from the monorepo root: **`lintian packaging/le-vibe-ide_*_*.deb`**. Use tags as hints — **[`docs/ci-qa-hardening.md`](../../docs/ci-qa-hardening.md)**; the stack **`debian/`** package may run stricter QA in CI (**STEP 10** / **H3**).

The **`le-vibe`** package **`Suggests: le-vibe-ide`** so both can install from the same apt suite when published. This **`le-vibe-ide`** package **`Recommends: le-vibe`** so **`apt install le-vibe-ide`** (from a repo that carries both) pulls the stack—**`lvibe`**, managed Ollama, Continue helpers—for an end-to-end demo without relying on users to discover the sibling **`.deb`** manually.

## Updates (roadmap — PRODUCT_SPEC §7.3)

**v1 / STEP 14:** This **`.deb`** does **not** ship a Lé Vibe–hosted in-app updater. A **Lé Vibe–controlled** update or distribution endpoint remains **roadmap** work (same §7.3 note as the stack package). Until then, refresh the IDE via **`apt`** / your release channel ([`docs/apt-repo-releases.md`](../../docs/apt-repo-releases.md)) or rebuild from the monorepo tag, same as the **`le-vibe`** stack.
