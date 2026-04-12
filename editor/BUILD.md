# Building the Lé Vibe IDE (local)

Compile steps are owned by **VSCodium** upstream. In this monorepo:

1. **Toolchain:** **[`.nvmrc`](.nvmrc)** — run **`nvm install` / `nvm use`** from **`editor/`** (matches **`vscodium/.nvmrc`**; see **[`README.md`](README.md)**).
2. **Upstream how-to:** **`vscodium/docs/howto-build.md`** inside the submodule — vscode sources are fetched with **`get_repo.sh`** (and friends) before **`build.sh`**; follow that file, not a duplicate guide here.
3. **Lé Vibe–specific layers:** **[`le-vibe-overrides/README.md`](le-vibe-overrides/README.md)**, **[`../docs/vscodium-fork-le-vibe.md`](../docs/vscodium-fork-le-vibe.md)**, **[`../docs/PRODUCT_SPEC.md`](../docs/PRODUCT_SPEC.md)** §7.2 where branding choices are material.

**CI (smoke only, no full compile yet):** [`.github/workflows/build-le-vibe-ide.yml`](../.github/workflows/build-le-vibe-ide.yml) — see **[`README.md`](README.md)**. **Local:** from the monorepo root, run **`./editor/smoke.sh`** (same gate as CI when **`editor/vscodium`** is present).

## `LE_VIBE_EDITOR` after a local build

The **`le-vibe`** stack discovers the editor via **`LE_VIBE_EDITOR`** (see **[`README.md`](README.md)** *`LE_VIBE_EDITOR`*). After you produce a binary from this tree:

- **Release-style tarball** (`VSCodium-linux-<arch>-<version>.tar.gz`): entry point is **`./bin/codium`** relative to the extracted directory — see **`vscodium/docs/usage.md`** (*From Linux .tar.gz*).
- **`get_repo.sh` / `build.sh` / CI-style builds:** the launcher path depends on arch and packaging; use the **`codium`** (or upstream **`code`**) executable your build emits, then set **`export LE_VIBE_EDITOR=/absolute/path/to/that/binary`** (or put it on **`PATH`** and set **`LE_VIBE_EDITOR=codium`**). When a future **`le-vibe-ide`** `.deb` installs **`/usr/bin/le-vibe-ide`**, point **`LE_VIBE_EDITOR`** there instead.

Until a Lé Vibe–branded install exists, **`/usr/bin/codium`** from **`Recommends: codium`** on the stack package remains the usual default.
