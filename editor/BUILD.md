# Building the Lé Vibe IDE (local)

Compile steps are owned by **VSCodium** upstream. In this monorepo:

1. **Toolchain:** **[`.nvmrc`](.nvmrc)** — run **`nvm install` / `nvm use`** from **`editor/`** (matches **`vscodium/.nvmrc`**; see **[`README.md`](README.md)**).
2. **Fetch vscode sources (`get_repo`):** upstream’s script is **`vscodium/get_repo.sh`**. It is **cwd-sensitive**: run commands from **`editor/vscodium/`** (the script creates/updates **`vscode/`** next to **`product.json`**). Do not run it from the monorepo root or from **`editor/`** alone. Full procedure is **`vscodium/docs/howto-build.md`** — use *Build for Development* (**`./dev/build.sh`**) for local iteration, or *Build for CI/Downstream* when you need the **`. get_repo.sh`** / **`build.sh`** sourcing pattern with the documented env vars (avoid inventing a second how-to here). After a successful fetch, the vscode tree and root **`package.json`** appear per upstream.
3. **Lé Vibe–specific layers:** **[`le-vibe-overrides/README.md`](le-vibe-overrides/README.md)**, **[`../docs/vscodium-fork-le-vibe.md`](../docs/vscodium-fork-le-vibe.md)**, **[`../docs/PRODUCT_SPEC.md`](../docs/PRODUCT_SPEC.md)** §7.2 where branding choices are material.

**CI:** [`.github/workflows/build-le-vibe-ide.yml`](../.github/workflows/build-le-vibe-ide.yml) — default **PR** runs match **`./editor/smoke.sh`** (pre-binary **`ide-ci-metadata.txt`**, **`vscode-upstream-stable.json`** when pinned, GitHub Actions **Summary** **Pre-binary artifact** / **`LE_VIBE_EDITOR`** pointer). **Optional full linux compile (14.e):** job **`linux_compile`** runs **`packaging/scripts/ci-vscodium-linux-dev-build.sh`** → **`editor/vscodium/dev/build.sh`** when you **manually dispatch** this workflow with **`vscodium_linux_compile`** enabled, or on **`ide-v*`** tag pushes (long run; may fail on undersized runners). The workflow caches **`~/.cargo/registry`** and **`~/.cargo/git`** (**`actions/cache`**) to speed repeat compiles when **`editor/vscodium/product.json`** / **`editor/.nvmrc`** change. If present, **`editor/le-vibe-overrides/build-env.sh`** is sourced first (see **`editor/le-vibe-overrides/build-env.sh.example`**) so maintainers can export upstream **`APP_NAME`** / **`BINARY_NAME`** / etc. without editing the submodule; material branding → **`PRODUCT_SPEC` §7.2**. Uploads **`vscodium-linux-build.tar.gz`** as a **`le-vibe-vscodium-linux-*`** artifact when **`VSCode-linux-*`** appears. **[`build-linux.yml`](../.github/workflows/build-linux.yml)** is a **`workflow_dispatch`** alias that **`uses:`** the same workflow. **Local smoke:** **`./editor/smoke.sh`** from the repo root.

## `LE_VIBE_EDITOR` after a local build

The **`le-vibe`** stack discovers the editor via **`LE_VIBE_EDITOR`** (see **[`README.md`](README.md)** *`LE_VIBE_EDITOR`*). After you produce a binary from this tree:

- **Release-style tarball** (`VSCodium-linux-<arch>-<version>.tar.gz`): entry point is **`./bin/codium`** relative to the extracted directory — see **`vscodium/docs/usage.md`** (*From Linux .tar.gz*).
- **`get_repo.sh` / `build.sh` / CI-style builds:** the launcher path depends on arch and packaging; use the **`codium`** (or upstream **`code`**) executable your build emits, then set **`export LE_VIBE_EDITOR=/absolute/path/to/that/binary`** (or put it on **`PATH`** and set **`LE_VIBE_EDITOR=codium`**). When a future **`le-vibe-ide`** `.deb` installs **`/usr/bin/le-vibe-ide`**, point **`LE_VIBE_EDITOR`** there instead.

Until a Lé Vibe–branded install exists, **`/usr/bin/codium`** from **`Recommends: codium`** on the stack package remains the usual default.

## Verify `lvibe` with your editor binary (14.c smoke)

After a local **VSCodium** build (or with any **`codium`**-compatible binary), point **`LE_VIBE_EDITOR`** at the **`codium`** executable your tree produced. Upstream Linux output is often under a **`VSCode-linux-*`** directory next to **`vscode/`**, or a release-style layout with **`bin/codium`** — see **`vscodium/docs/usage.md`** (*From Linux .tar.gz*) and your **`build.sh`** / **`dev/build.sh`** log lines for the exact path on your machine.

**Launcher smoke** (starts managed Ollama, then runs the editor with **`--version`** and exits — requires **`ollama`** on **`PATH`**):

```bash
# from monorepo root
LE_VIBE_EDITOR=/absolute/path/to/codium ./editor/smoke-lvibe-editor.sh
# or pass the binary as the first argument
./editor/smoke-lvibe-editor.sh /absolute/path/to/codium
```

If **`LE_VIBE_EDITOR`** is unset and **`/usr/bin/codium`** exists, the script uses that. This is the same stack path **`lvibe`** uses; it is not a substitute for **`./editor/smoke.sh`** (layout / **`bash -n`** / **`.nvmrc`** gate).

## Installable layout — tarball + `codium` path (14.f)

There is **no** **`le-vibe-ide`** `.deb` in this repository yet; the **stack** package remains **`le-vibe`** with **`Recommends: codium`**. Use one of the following when you have a **built tree** or a **CI artifact**.

### Local or CI compile output (`VSCode-linux-*`)

After **`./dev/build.sh`** (or CI job **`linux_compile`**), upstream emits a directory **`editor/vscodium/VSCode-linux-<arch>/`** (e.g. **`x64`**). The desktop entrypoint is:

```text
editor/vscodium/VSCode-linux-<arch>/bin/codium
```

Set **`LE_VIBE_EDITOR`** to that **absolute** path (or add **`.../bin`** to **`PATH`** and use **`LE_VIBE_EDITOR=codium`** only if that **`codium`** resolves to this binary).

### GitHub Actions artifact **`vscodium-linux-build.tar.gz`**

Successful **`linux_compile`** runs upload **`vscodium-linux-build.tar.gz`** (artifact name **`le-vibe-vscodium-linux-<run_id>`**). It contains a **single** top-level directory (**`VSCode-linux-<arch>/`**) produced by the build.

```bash
tar -xzf vscodium-linux-build.tar.gz
realpath VSCode-linux-*/bin/codium   # use this for LE_VIBE_EDITOR
```

This is **not** byte-identical to upstream’s release-named **`VSCodium-linux-<arch>-<version>.tar.gz`** archives, but the **per-directory** layout matches the same **`bin/codium`** pattern — see **`vscodium/docs/usage.md`** (*From Linux .tar.gz*) for portable-mode and PATH notes.

### Upstream release `.tar.gz` (reference)

Official **VSCodium** Linux tarballs use **`./bin/codium`** relative to the extract root (**`VSCodium-linux-…`**). Prefer that flow when you consume upstream binaries; prefer **`VSCode-linux-*`** paths above when you build from **this** monorepo or CI.

## Default `LE_VIBE_EDITOR` / packaging story when the IDE ships (14.g)

**Today:** the **`le-vibe`** stack **`.deb`** does **not** ship the IDE binary. Launcher resolution (**`le_vibe.launcher`**, **`_default_editor`**) is: **`$LE_VIBE_EDITOR`** if set; else **`/usr/bin/le-vibe-ide`** if that path is executable; else **`/usr/bin/codium`** if that path is executable; else the bare command **`codium`** on **`PATH`**. **`debian/control`** uses **`Recommends: codium`** so a normal **`apt install`** usually yields an editor without extra configuration.

**When a packaged Lé Vibe IDE exists** (expected separate source/binary package, e.g. **`le-vibe-ide`**, not yet in this repository): the **intended** integration is:

| Piece | Intent |
|--------|--------|
| **Binary on disk** | Install **`/usr/bin/le-vibe-ide`** (name is illustrative—**`PRODUCT_SPEC`** §7.2 if renaming is material). |
| **Stack package** | **`le-vibe`** gains **`Recommends:`** or **`Suggests:`** **`le-vibe-ide`** (or the chosen package name) so **`apt`** pulls the branded shell alongside the Python stack. |
| **Default without user env** | Prefer shipping a **system default** users can override: e.g. **`/usr/bin/le-vibe-ide`** if present in the same resolution order **before** stock **`codium`**, *or* a small **`/etc/profile.d/`** snippet that sets **`LE_VIBE_EDITOR=/usr/bin/le-vibe-ide`** for login shells—**exact mechanism is a §7.2 / maintainer choice**, not fixed here. |
| **Overrides** | Users and distros always win via **`export LE_VIBE_EDITOR=...`** (profile, systemd user environment, or session). |

Until that package lands, keep using **`LE_VIBE_EDITOR`** pointing at a **`VSCode-linux-*/bin/codium`** build, CI tarball, or **`/usr/bin/codium`** as documented above.

## Continue extension pin — Open VSX (14.h)

**Continue** installs use the same pinned Open VSX version as the stack (**`packaging/continue-openvsx-version`**) whether **`LE_VIBE_EDITOR`** is system **`codium`** or a **`VSCode-linux-*/bin/codium`** build from this tree — **`packaging/scripts/install-continue-extension.sh`** respects **`LE_VIBE_EDITOR`**. Run **`le-vibe-setup-continue`** after first-run so **`sync-continue-config.sh`** + extension install follow **`docs/continue-extension-pin.md`** (not bundled VSIX under **`editor/`**). After changing the pin file, run **`./packaging/scripts/verify-continue-pin.sh`** (CI runs it via **`ci-smoke.sh`**).
