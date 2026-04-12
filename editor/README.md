# Lé Vibe IDE — desktop shell (monorepo)

**Lé Vibe is one repository.** This directory is the **canonical home** for the **Code - OSS–based desktop application** (branded binary, icons, About, Linux packaging of the editor itself). **Engineering and PM tracks treat `editor/` as P0** after baseline must-ship checks—see **`docs/PROMPT_BUILD_LE_VIBE.md`** (Master orchestrator **STEP 14**, **editor-first** order).

| Path | Role |
|------|------|
| **`editor/`** (here) | Lé Vibe IDE — VSCodium/Code OSS sources, branding, build scripts, CI for the Electron app |
| **`le-vibe/`** | Python bootstrap, `lvibe` launcher, managed Ollama, `.lvibe/` workspace hub, **`le-vibe`** `.deb` |
| **`debian/`**, **`packaging/`** | Debian packaging and PATH wrappers for the **stack** package |

**Product intent (aligned with earlier designs):** Local-first **Linux IDE** with managed Ollama lifecycle, **Continue**-oriented agent defaults, honest hardware tiering, and **Lé Vibe** naming—see **`spec-phase2.md` §2** (product definition), **`PRODUCT_SPEC.md`** (must-ship), and **`docs/vscodium-fork-le-vibe.md`**. Session/epic work under **`.lvibe/`** coordinates **delivery of this shell** plus the stack, not parallel products.

Populate **`editor/`** by vendoring upstream (e.g. [VSCodium](https://github.com/VSCodium/vscodium)) via **git submodule**, **subtree**, or a tracked import—see **`docs/vscodium-fork-le-vibe.md`** and **[`VENDORING.md`](VENDORING.md)** (recommended: submodule at **`editor/vscodium/`** so this README stays in-tree). Until sources exist here, developers may point **`LE_VIBE_EDITOR`** at system **VSCodium**; production intent remains **one tree**, one product.

## `LE_VIBE_EDITOR` (launcher ↔ IDE binary)

The Python stack (`lvibe`, `le-vibe` wrappers) resolves the desktop editor in this order (see `le-vibe/le_vibe/launcher.py`):

1. **`LE_VIBE_EDITOR`** if set in the environment (absolute path or executable name on `PATH`).
2. Else **`/usr/bin/codium`** if that file exists and is executable.
3. Else the bare command **`codium`** (must be on `PATH`).

**Packaging:** the **`le-vibe`** `.deb` sets a default of `/usr/bin/codium` in its launcher scripts and **Recommends: codium** in `debian/control` so a typical install gets an editor without extra flags. When this directory ships a branded binary (e.g. `/usr/bin/le-vibe-ide`), set **`LE_VIBE_EDITOR`** to that path—or install a symlink/name your package provides—and update CI smoke accordingly.

**CI:** [`.github/workflows/build-le-vibe-ide.yml`](../.github/workflows/build-le-vibe-ide.yml) runs on `workflow_dispatch` and tags `ide-v*`. Until **`editor/package.json`** or **`editor/vscodium/package.json`** exists (upstream vendored), the job **passes** with a skip notice; after vendoring, extend the workflow with the real Linux build and artifact upload per **`docs/vscodium-fork-le-vibe.md`**.

**Authority:** [`docs/PRODUCT_SPEC.md`](../docs/PRODUCT_SPEC.md) (naming, §7.2 user gate on material IDE choices), [`spec-phase2.md`](../spec-phase2.md) §2 and §14.
