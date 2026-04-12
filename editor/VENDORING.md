# Vendoring the IDE upstream (Lé Vibe `editor/`)

Keep Lé Vibe docs in **`editor/README.md`** by placing the **VSCodium** tree under **`editor/vscodium/`** (git submodule), not by replacing the whole **`editor/`** directory.

## Submodule (recommended; matches CI `submodules: recursive`)

From the monorepo root (with git initialized):

```bash
git submodule add https://github.com/VSCodium/vscodium.git editor/vscodium
git submodule update --init --recursive
```

**Already cloned** (submodule declared in **`.gitmodules`**): from the monorepo root run **`git submodule update --init editor/vscodium`** when **`editor/vscodium/`** is empty — same as **`editor/README.md`** *Fresh clone (14.b)* and **`docs/vscodium-fork-le-vibe.md`**.

**Untracked Linux icons (§7.3):** **`.gitmodules`** sets **`ignore = untracked`** for **`editor/vscodium`**. Generated **`le-vibe.svg`** / **`le-vibe.png`** under **`editor/vscodium/src/stable/resources/linux/`** (from **`le-vibe-overrides/sync-linux-icon-assets.sh`**) stay **untracked** in the submodule and do **not** mark the superproject submodule as “modified” in **`git status`** — they are not committed to upstream VSCodium.

Then follow upstream’s **prepare / build** docs from **`editor/vscodium/`** — authoritative reference: **`docs/howto-build.md`** (*Build for Development* — **`./dev/build.sh`**; *Build for CI/Downstream* — **`. get_repo.sh`** pattern). Fetch vscode via **`get_repo.sh`** (cwd **`editor/vscodium/`**); root **`package.json`** appears only after that step. **Monorepo fetch-only entrypoint (14.b):** from the repository root, **`./editor/fetch-vscode-sources.sh`** — **[`BUILD.md`](BUILD.md)**. Monorepo checklist: **[`BUILD.md`](BUILD.md)**. CI [`.github/workflows/build-le-vibe-ide.yml`](../.github/workflows/build-le-vibe-ide.yml) (or the **`build-linux`** alias [`.github/workflows/build-linux.yml`](../.github/workflows/build-linux.yml)) treats **`editor/package.json`** (flat vscode checkout) or **`editor/vscodium/product.json`** (VSCodium tree) as “sources present.” Verify locally from the repo root with **`./editor/smoke.sh`** (wraps **[`packaging/scripts/ci-editor-gate.sh`](../packaging/scripts/ci-editor-gate.sh)** — **`bash -n`** via **[`packaging/scripts/ci-vscodium-bash-syntax.sh`](../packaging/scripts/ci-vscodium-bash-syntax.sh)** and **`editor/.nvmrc`** parity via **[`packaging/scripts/ci-editor-nvmrc-sync.sh`](../packaging/scripts/ci-editor-nvmrc-sync.sh)** when the submodule is present). On **GitHub Actions**, successful runs also upload pre-binary **`ide-ci-metadata.txt`** (**`le_vibe_editor_docs`**) via **`upload-artifact`** with **`retention-days`** (bounded pre-binary retention; see the workflow YAML) and write a run **Summary** **Pre-binary artifact** line for the **`LE_VIBE_EDITOR`** docs pointer — see **[`BUILD.md`](BUILD.md)** *CI* and **[`README.md`](README.md)** *CI*.

**Optional full compile + tarball (14.e / 14.f):** the same workflow defines job **`linux_compile`** (opt-in — **`workflow_dispatch`** **`vscodium_linux_compile`**, **`workflow_call`**, or **`ide-v*`** tag; not the default **`pull_request`** path). That job runs **`ci-vscodium-bash-syntax.sh`** + **`ci-editor-nvmrc-sync.sh`** before **`ci-vscodium-linux-dev-build.sh`** (fail fast — same gates as **`ci-editor-gate`**); **`ci-vscodium-linux-dev-build.sh`** enforces **`node --version`** vs **`editor/.nvmrc`** before **`dev/build.sh`** (**`LEVIBE_SKIP_NODE_VERSION_CHECK`** — **14.a** / **14.e**; **[`BUILD.md`](BUILD.md)** *Compile wrapper vs Node*). The job sets **`NODE_OPTIONS=--max-old-space-size=8192`** (same as **`editor/vscodium/dev/build.sh`**) and a bounded **apt** install — details + when compiles fail — **[`BUILD.md`](BUILD.md)** *CI* / *When full compile fails*. On success it may upload **`vscodium-linux-build.tar.gz`**; resolve **`bin/codium`** for **`LE_VIBE_EDITOR`** with **`./editor/print-ci-tarball-codium-path.sh`** — see **[`BUILD.md`](BUILD.md)** *Installable layout* and **[`README.md`](README.md)** *Full Linux compile*.

**Release bundles (H1 vs §7.3):** Default **`ci.yml`** artifact **`le-vibe-deb`** is **stack-only**; **`le-vibe-ide_*_amd64.deb`** repacks **`VSCode-linux-*`** after a full build — **[`../docs/apt-repo-releases.md`](../docs/apt-repo-releases.md)** (*IDE package*); **[`../docs/PM_STAGE_MAP.md`](../docs/PM_STAGE_MAP.md)** (*H1 vs §7.3 .deb bundles*); **[`../docs/PRODUCT_SPEC.md`](../docs/PRODUCT_SPEC.md)** § *Prioritization* — **Release bundles (H1 / STEP 8 vs STEP 14 / §7.3)**.

**Full-product build (`--with-ide`):** From the repository root, **`./packaging/scripts/build-le-vibe-debs.sh --with-ide`** builds the stack **`le-vibe`** **`.deb`** and **`le-vibe-ide_*_amd64.deb`** when **`VSCode-linux-*`** exists, then prints **Full-product install** on success — **[`../docs/PM_DEB_BUILD_ITERATION.md`](../docs/PM_DEB_BUILD_ITERATION.md)** (*Success output (`--with-ide`)*); step-by-step packaging — **[`BUILD.md`](BUILD.md)** *Debian package for the Lé Vibe IDE*; install both **`.deb`** files — **[`../packaging/debian-le-vibe-ide/README.md`](../packaging/debian-le-vibe-ide/README.md)** (*Install both packages*).

## Branding & About

**14.c** launcher smoke and an optional **14.e** **`linux_compile`** tarball prove the **`codium`** path — not Lé Vibe–visible product branding. Read **[`le-vibe-overrides/branding-staging.checklist.md`](le-vibe-overrides/branding-staging.checklist.md)** *PRODUCT_SPEC §7.2 (read before overrides)* first, then the rest of the checklist (**14.d**), before claiming shipped identity; policy shell **`docs/vscodium-fork-le-vibe.md`**, **`docs/PRODUCT_SPEC.md`** §7.2. Reserved inputs: **[`le-vibe-overrides/README.md`](le-vibe-overrides/README.md)**.

## `LE_VIBE_EDITOR`

Point **`LE_VIBE_EDITOR`** at your built binary (or packaged **`/usr/bin/...`**). See **`editor/README.md`**.
