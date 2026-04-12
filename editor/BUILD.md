# Building the Lé Vibe IDE (local)

Compile steps are owned by **VSCodium** upstream. In this monorepo:

1. **Toolchain (14.a):** **[`.nvmrc`](.nvmrc)** — run **`nvm install` / `nvm use`** from **`editor/`** (matches **`vscodium/.nvmrc`**; see **[`README.md`](README.md)**). **Canonical helper:** from the repo root, **`source editor/use-node-toolchain.sh`** (or **`./editor/use-node-toolchain.sh node --version`**) — **[`use-node-toolchain.sh`](use-node-toolchain.sh)**. **Sourcing** prints the active **`node`** binary, semver, and **`editor/.nvmrc`** path on **stderr** (quick confirmation you are on the VSCodium pin before **`get_repo`** / build).

   **Compile wrapper vs Node (14.a / 14.e):** **[`packaging/scripts/ci-vscodium-linux-dev-build.sh`](../packaging/scripts/ci-vscodium-linux-dev-build.sh)** (CI **`linux_compile`** and local full builds) compares **`node --version`** to **`editor/.nvmrc`** before **`dev/build.sh`** (CI **`actions/setup-node`** uses the same file). Rare override: **`LEVIBE_SKIP_NODE_VERSION_CHECK=1`**.
2. **Fetch vscode sources (`get_repo`):** upstream’s script is **`vscodium/get_repo.sh`**. It is **cwd-sensitive**: run commands from **`editor/vscodium/`** (the script creates/updates **`vscode/`** next to **`product.json`**). Do not run it from the monorepo root or from **`editor/`** alone. **Monorepo helper (14.b):** from the repository root, **`./editor/fetch-vscode-sources.sh`** **`cd`**s to **`editor/vscodium/`**, sets the same **`VSCODE_QUALITY` / `VSCODE_LATEST` / `CI_BUILD` defaults as **`dev/build.sh`** (the exports **`dev/build.sh`** applies before it **sources** **`get_repo.sh`** when fetching sources), and **sources** **`get_repo.sh`** (no compile). **`vscodium/docs/howto-build.md`** *Build for CI/Downstream* (**`#build-ci`**) adds packaging env (**`SHOULD_BUILD`**, **`OS_NAME`**, …) around **`. get_repo.sh`** — use that full block when reproducing CI, not for a typical local **`vscode/`** fetch. For local iteration, *Build for Development* (**`./dev/build.sh`**) remains the umbrella entrypoint. After a successful fetch, the vscode tree and root **`package.json`** appear per upstream.
3. **Lé Vibe–specific layers:** **[`le-vibe-overrides/README.md`](le-vibe-overrides/README.md)**, **[`../docs/vscodium-fork-le-vibe.md`](../docs/vscodium-fork-le-vibe.md)**, **[`../docs/PRODUCT_SPEC.md`](../docs/PRODUCT_SPEC.md)** §7.3 / §7.2 for branding policy.
4. **Linux icons (§7.3):** **[`packaging/scripts/ci-vscodium-linux-dev-build.sh`](../packaging/scripts/ci-vscodium-linux-dev-build.sh)** runs **[`le-vibe-overrides/sync-linux-icon-assets.sh`](le-vibe-overrides/sync-linux-icon-assets.sh)** before **`dev/build.sh`**, copying **[`packaging/icons/hicolor/scalable/apps/le-vibe.svg`](../packaging/icons/hicolor/scalable/apps/le-vibe.svg)** and emitting **`le-vibe.png`** (needs **`rsvg-convert`** — **`librsvg2-bin`** on Debian, installed in **`build-le-vibe-ide.yml`** **`linux_compile`**). If you call **`./dev/build.sh`** directly, run the sync script first. Generated **`editor/vscodium/src/stable/resources/linux/le-vibe.{svg,png}`** are gitignored. **`product-branding-merge.json`** sets **`linuxIconName`** to **`le-vibe`**. See **[`docs/brand-assets.md`](../docs/brand-assets.md)**.

**Vendoring upstream:** if **`editor/vscodium/`** is not present yet, add it as a **git submodule** and align with CI gates — **[`VENDORING.md`](VENDORING.md)** (**`./editor/smoke.sh`**, pre-binary metadata, optional **`linux_compile`** + **`vscodium-linux-build.tar.gz`** — **14.e / 14.f**).

**CI:** [`.github/workflows/build-le-vibe-ide.yml`](../.github/workflows/build-le-vibe-ide.yml) — default **PR** runs match **`./editor/smoke.sh`** (pre-binary **`ide-ci-metadata.txt`**, **`vscode-upstream-stable.json`** when pinned, GitHub Actions **Summary** **Pre-binary artifact** / **`LE_VIBE_EDITOR`** pointer). **Optional full linux compile (14.e):** job **`linux_compile`** sets **`NODE_OPTIONS=--max-old-space-size=8192`** (same as **`editor/vscodium/dev/build.sh`**) on the job environment, then runs **`ci-vscodium-bash-syntax.sh`** + **`ci-editor-nvmrc-sync.sh`** first (same **`bash -n`** / **`.nvmrc`** parity as **`ci-editor-gate`** — fail fast before **`get_repo`** / compile), then **`packaging/scripts/ci-vscodium-linux-dev-build.sh`** → **`editor/vscodium/dev/build.sh`** (same active-**Node** ↔ **`editor/.nvmrc`** rule as *Compile wrapper vs Node* above — **`LEVIBE_SKIP_NODE_VERSION_CHECK`**) when you **manually dispatch** this workflow with **`vscodium_linux_compile`** enabled, or on **`ide-v*`** tag pushes (long run; may fail on undersized runners). The workflow caches **`~/.cargo/registry`** and **`~/.cargo/git`** (**`actions/cache`**) to speed repeat compiles when **`editor/vscodium/product.json`** / **`editor/.nvmrc`** change. If present, **`editor/le-vibe-overrides/build-env.sh`** is sourced after **`build-env.lvibe-defaults.sh`** (see **`build-env.sh.example`**) for extra exports; material branding beyond §7.3 → **`PRODUCT_SPEC` §7.2**. Uploads **`vscodium-linux-build.tar.gz`** as a **`le-vibe-vscodium-linux-*`** artifact when **`VSCode-linux-*`** appears (**`upload-artifact`** **`retention-days: 14`** for that tarball; the default job’s pre-binary **`ide-ci-metadata.txt`** upload uses **`retention-days: 90`**). **[`build-linux.yml`](../.github/workflows/build-linux.yml)** is a **`workflow_dispatch`** alias that **`uses:`** the same workflow and can forward **`vscodium_linux_compile`** via **`workflow_call`** **`inputs`** so **`linux_compile`** runs without opening **`build-le-vibe-ide`** directly. **Local smoke:** **`./editor/smoke.sh`** from the repo root.

### When full compile fails (`linux_compile` / local `dev/build.sh`) — **14.e**

- **Host packages:** **`linux_compile`** installs a **bounded** Debian package set (see **`build-le-vibe-ide.yml`** *Install Linux build dependencies*), including **`jq`**, **`librsvg2-bin`** (§7.3 icon sync), **`dpkg-dev`**, **`rpm`**, and **`python3.11-dev`** alongside the earlier minimal list — closer to **`vscodium/docs/howto-build.md`** *Dependencies* → *Linux* (**`dpkg`** / **`rpm`** / **`rpmbuild`** probes, **Python 3.11** headers for native addons). Upstream’s full list (e.g. **ImageMagick**, **snapcraft**) is still mostly for packaging targets this job does not run by default — if **`dev/build.sh`** fails with missing headers, libraries, or CLI tools, install the matching packages locally or extend the CI job (self-hosted runner image is often easier than guessing every transitive dep on **`ubuntu-latest`** / **`ubuntu-22.04`**).
- **Runner realism:** **`spec-phase2.md` §14** states that a **reproducible green** **`linux_compile`** on default **GitHub-hosted** runners is **not** guaranteed (disk, build time, **OOM**). Prefer a **self-hosted** or larger runner when you need routine full Electron builds until the job is tuned.
- **Fork policy + release smoke:** **[`docs/vscodium-fork-le-vibe.md`](../docs/vscodium-fork-le-vibe.md)** (**14.i**) — use the release checklist after a successful compile.

## `LE_VIBE_EDITOR` after a local build

The **`le-vibe`** stack discovers the editor via **`LE_VIBE_EDITOR`** (see **[`README.md`](README.md)** *`LE_VIBE_EDITOR`*). After you produce a binary from this tree:

- **Release-style tarball** (`VSCodium-linux-<arch>-<version>.tar.gz`): entry point is **`./bin/codium`** relative to the extracted directory — see **`vscodium/docs/usage.md`** (*From Linux .tar.gz*).
- **`get_repo.sh` / `build.sh` / CI-style builds:** the launcher path depends on arch and packaging; use the **`codium`** (or upstream **`code`**) executable your build emits, then set **`export LE_VIBE_EDITOR=/absolute/path/to/that/binary`** (or put it on **`PATH`** and set **`LE_VIBE_EDITOR=codium`**). When the **`le-vibe-ide`** **`.deb`** is installed, the stack discovers **`/usr/lib/le-vibe/bin/codium`** automatically (**PRODUCT_SPEC** §7.3 — internal path; **`lvibe`** remains the only public **`PATH`** CLI).

Until a Lé Vibe IDE **`.deb`** is installed, **`/usr/bin/codium`** from **`Recommends: codium`** on the stack package remains the usual default.

## Verify `lvibe` with your editor binary (14.c smoke)

**Built tree present (no Ollama):** from the repo root, **`./editor/verify-14c-local-binary.sh`** prints **`editor/vscodium/VSCode-linux-*/bin/codium`** when **`dev/build.sh`** has succeeded, or exits **`1`** with **`14.a`→`14.c`** remediation (same resolution as **`print-built-codium-path.sh`**, friendlier copy for maintainers).

After a local **VSCodium** build (or with any **`codium`**-compatible binary), point **`LE_VIBE_EDITOR`** at the **`codium`** executable your tree produced. Upstream Linux output is often under a **`VSCode-linux-*`** directory next to **`vscode/`**, or a release-style layout with **`bin/codium`** — see **`vscodium/docs/usage.md`** (*From Linux .tar.gz*) and your **`build.sh`** / **`dev/build.sh`** log lines for the exact path on your machine.

**Discover the built binary (local `VSCode-linux-*` tree):** from the repository root, **`./editor/print-built-codium-path.sh`** prints the absolute path to **`editor/vscodium/VSCode-linux-*/bin/codium`** when present (if several trees exist, picks the newest by file mtime). Use it to set **`LE_VIBE_EDITOR`** before **`smoke-lvibe-editor.sh`** or **`lvibe`**.

**Launcher smoke** (starts managed Ollama, then runs the editor with **`--version`** and exits — requires **`ollama`** on **`PATH`**). **`smoke-lvibe-editor.sh`** checks the **`codium`** path is an executable (absolute/relative file or a name on **`PATH`**) before the launcher runs — use **`./editor/print-built-codium-path.sh`** if you are unsure of the path after **`dev/build.sh`**.

```bash
# from monorepo root
LE_VIBE_EDITOR=/absolute/path/to/codium ./editor/smoke-lvibe-editor.sh
# or pass the binary as the first argument
./editor/smoke-lvibe-editor.sh /absolute/path/to/codium
# after dev/build.sh, if VSCode-linux-* exists — one step (same as print-built + smoke-lvibe-editor):
./editor/smoke-built-codium-lvibe.sh
# or set LE_VIBE_EDITOR explicitly:
LE_VIBE_EDITOR="$(./editor/print-built-codium-path.sh)" ./editor/smoke-lvibe-editor.sh
```

If **`LE_VIBE_EDITOR`** is unset and **`/usr/bin/codium`** exists, the script uses that. This is the same stack path **`lvibe`** uses; it is not a substitute for **`./editor/smoke.sh`** (layout / **`bash -n`** / **`.nvmrc`** gate).

Passing **14.c** smoke only proves the stack can launch your built **`codium`**; it does **not** mean Lé Vibe–visible branding is applied in the Electron tree — see **[`le-vibe-overrides/branding-staging.checklist.md`](le-vibe-overrides/branding-staging.checklist.md)** — read *PRODUCT_SPEC §7.2 (read before overrides)* first (**14.d**, **[`docs/PRODUCT_SPEC.md`](../docs/PRODUCT_SPEC.md)** §7.2).

## Installable layout — tarball + `codium` path (14.f)

The **IDE** **`.deb`** is built from **`packaging/debian-le-vibe-ide/`** after staging a local **`VSCode-linux-*/`** tree (**§7.3** — see *Debian package for the Lé Vibe IDE* below). The **stack** package remains **`le-vibe`** with **`Recommends: codium`** and **`Suggests: le-vibe-ide`**. Use one of the following when you have a **built tree** or a **CI artifact**.

### CI artifact → `LE_VIBE_EDITOR` (14.e output)

After a successful **`linux_compile`** run (**14.e**), GitHub’s artifact UI delivers a **`.zip`** named like **`le-vibe-vscodium-linux-<run_id>`** containing **`vscodium-linux-build.tar.gz`**. From the repository root:

1. Unzip the download; note the path to **`vscodium-linux-build.tar.gz`**.
2. **`export LE_VIBE_EDITOR="$(./editor/print-ci-tarball-codium-path.sh /path/to/vscodium-linux-build.tar.gz)"`** — prints **`VSCode-linux-<arch>/bin/codium`** inside a temp extract (see **`editor/print-ci-tarball-codium-path.sh`**).
3. Optional launcher smoke: **`./editor/smoke-lvibe-editor.sh`** (requires **`ollama`** on **`PATH`** — **14.c**).

This is the supported **installable tree** path from CI when you have not yet built the **`le-vibe-ide`** **`.deb`** (**14.g**).

### Local or CI compile output (`VSCode-linux-*`)

After **`./dev/build.sh`** (or CI job **`linux_compile`**), upstream emits a directory **`editor/vscodium/VSCode-linux-<arch>/`** (e.g. **`x64`**). The desktop entrypoint is:

```text
editor/vscodium/VSCode-linux-<arch>/bin/codium
```

Set **`LE_VIBE_EDITOR`** to that **absolute** path (or add **`.../bin`** to **`PATH`** and use **`LE_VIBE_EDITOR=codium`** only if that **`codium`** resolves to this binary).

### GitHub Actions artifact **`vscodium-linux-build.tar.gz`**

Successful **`linux_compile`** runs upload **`vscodium-linux-build.tar.gz`** (artifact name **`le-vibe-vscodium-linux-<run_id>`**). It contains a **single** top-level directory (**`VSCode-linux-<arch>/`**) produced by the build.

**GitHub’s download is a `.zip`** wrapping that tarball — unzip it, then pass the path to **`vscodium-linux-build.tar.gz`** into **`print-ci-tarball-codium-path.sh`** (or extract the tarball yourself and use **`print-vsbuild-codium-path.sh`** on the unpack directory).

```bash
tar -xzf vscodium-linux-build.tar.gz
# from repo root, pass the directory that contains VSCode-linux-* (often the unpack cwd):
LE_VIBE_EDITOR="$(./editor/print-vsbuild-codium-path.sh "$PWD")"   # or: realpath VSCode-linux-*/bin/codium
```

**Without unpacking into your cwd:** from the repo root, **`./editor/print-ci-tarball-codium-path.sh /path/to/vscodium-linux-build.tar.gz`** extracts to a **temp** directory, then prints the same **`bin/codium`** absolute path (**14.f**).

**`./editor/print-vsbuild-codium-path.sh`** (**14.f**) resolves **`VSCode-linux-*/bin/codium`** under any **absolute or relative** unpack root (same discovery logic as **`print-built-codium-path.sh`**, which only searches **`editor/vscodium/`** — **14.c**).

This is **not** byte-identical to upstream’s release-named **`VSCodium-linux-<arch>-<version>.tar.gz`** archives, but the **per-directory** layout matches the same **`bin/codium`** pattern — see **`vscodium/docs/usage.md`** (*From Linux .tar.gz*) for portable-mode and PATH notes.

### Upstream release `.tar.gz` (reference)

Official **VSCodium** Linux tarballs use **`./bin/codium`** relative to the extract root (**`VSCodium-linux-…`**). Prefer that flow when you consume upstream binaries; prefer **`VSCode-linux-*`** paths above when you build from **this** monorepo or CI.

## Default `LE_VIBE_EDITOR` / packaging story when the IDE ships (14.g)

**Stack package:** the **`le-vibe`** **`.deb`** does **not** embed the Electron tree; it ships Python + wrappers. Launcher resolution (**`le_vibe.launcher._default_editor`** in **`le-vibe/le_vibe/launcher.py`**) is: **`$LE_VIBE_EDITOR`** if set; else **`/usr/lib/le-vibe/bin/codium`** if that path is executable; else **`/usr/bin/codium`** if that path is executable; else the bare command **`codium`** on **`PATH`**. End-user copy: **`debian/le-vibe.README.Debian`** (*Default editor when `LE_VIBE_EDITOR` is unset*). **`debian/control`** uses **`Recommends: codium`** and **`Suggests: le-vibe-ide`**.

**Packaged Lé Vibe IDE (`le-vibe-ide`):** Debian source **`packaging/debian-le-vibe-ide/`** (see **`README.md`** there). After **`dev/build.sh`** produces **`editor/vscodium/VSCode-linux-*/`**, run **`packaging/scripts/stage-le-vibe-ide-deb.sh`** from the repository root, then **`packaging/scripts/build-le-vibe-ide-deb.sh`** (or **`dpkg-buildpackage`** from **`packaging/debian-le-vibe-ide/`**). That installs the tree under **`/usr/lib/le-vibe/ide/`** and **`/usr/lib/le-vibe/bin/codium`**, plus **`/usr/share/applications/le-vibe.desktop`** and the **`hicolor`** app icon (**PRODUCT_SPEC** §7.3 — no second public CLI name such as **`/usr/bin/le-vibe-ide`**; **`lvibe`** only; menu **`Exec=`** is the internal **`codium`** path).

| Piece | Intent |
|--------|--------|
| **Binary on disk** | **`/usr/lib/le-vibe/bin/codium`** → packaged **`VSCode-linux-*/bin/codium`** (upstream binary filename is an implementation detail). |
| **Stack package** | **`Suggests: le-vibe-ide`** so **`apt`** can install the IDE alongside the Python stack when both are published. |
| **Overrides** | Users and distros always win via **`export LE_VIBE_EDITOR=...`** (profile, systemd user environment, or session). |

Until **`le-vibe-ide`** is installed, keep using **`LE_VIBE_EDITOR`** pointing at a **`VSCode-linux-*/bin/codium`** build, CI tarball, or **`/usr/bin/codium`** as documented above.

### Debian package for the Lé Vibe IDE (§7.3)

1. Build: from repo root **`./packaging/scripts/ci-vscodium-linux-dev-build.sh`** (after **`fetch-vscode-sources.sh`** / toolchain — **14.a–14.b**), or **`cd editor/vscodium && ./dev/build.sh`** only if you already ran **`./editor/le-vibe-overrides/sync-linux-icon-assets.sh`** and merged **`product-branding-merge.json`** (use the wrapper unless you know upstream’s expectations).
2. Stage: **`./packaging/scripts/stage-le-vibe-ide-deb.sh`** (optional argument: path to **`VSCode-linux-*`**; default: discover under **`editor/vscodium/`**).
3. Package: **`./packaging/scripts/build-le-vibe-ide-deb.sh`** — produces **`le-vibe-ide_*.deb`** next to **`packaging/debian-le-vibe-ide/`** (ignored by git as **`*.deb`**).

### Unpacked trees and **`_default_editor`** (14.f → 14.g)

**`le_vibe.launcher._default_editor`** probes **`/usr/lib/le-vibe/bin/codium`**, then **`/usr/bin/codium`**, then falls back to the bare command **`codium`** on **`PATH`**. A **`VSCode-linux-*`** directory from **14.f** (local build, CI tarball extract, or upstream archive) at **`$HOME/opt/…`**, under the repo’s **`editor/vscodium/`**, or anywhere else **is not auto-discovered** unless installed via **`le-vibe-ide`** or **`LE_VIBE_EDITOR`**. Set **`LE_VIBE_EDITOR`** to the **`bin/codium`** absolute path (or add a symlink under **`/usr/local/bin`** / **`~/bin`** on **`PATH`**) — same persistence options as **`editor/README.md`** *Persisting `LE_VIBE_EDITOR`* (**systemd** **`environment.d`**, **`~/.profile`**, etc.).

## Continue extension pin — Open VSX (14.h)

**Continue** installs use the same pinned Open VSX version as the stack (**`packaging/continue-openvsx-version`**) whether **`LE_VIBE_EDITOR`** is system **`codium`** or a **`VSCode-linux-*/bin/codium`** from a local build, unpack dir, or **`vscodium-linux-build.tar.gz`** (**`print-ci-tarball-codium-path.sh`** — **14.f**) — **`packaging/scripts/install-continue-extension.sh`** respects **`LE_VIBE_EDITOR`**. When **`LE_VIBE_EDITOR`** is unset, that script uses the same **`/usr/lib/le-vibe/bin/codium` → `/usr/bin/codium`** resolution order as **`le_vibe.launcher._default_editor`** (**14.g**). After a local **`dev/build.sh`**, optional **`./editor/verify-14c-local-binary.sh`** (**14.c**) confirms the tree exists before you **`export LE_VIBE_EDITOR=…`** and run **`le-vibe-setup-continue`**. Run **`le-vibe-setup-continue`** after first-run so **`sync-continue-config.sh`** + extension install follow **`docs/continue-extension-pin.md`** (not bundled VSIX under **`editor/`**). After changing the pin file, run **`./packaging/scripts/verify-continue-pin.sh`** (CI runs it via **`ci-smoke.sh`**).
