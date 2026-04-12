# Lé Vibe IDE — desktop shell (monorepo)

**Lé Vibe is one repository.** This directory is the **canonical home** for the **Code - OSS–based desktop application** (branded binary, icons, About, Linux packaging of the editor itself). **Engineering and PM tracks treat `editor/` as P0** after baseline must-ship checks—see **`docs/PROMPT_BUILD_LE_VIBE.md`** (Master orchestrator **STEP 14**, **editor-first** order).

| Path | Role |
|------|------|
| **`editor/`** (here) | Lé Vibe IDE — VSCodium/Code OSS sources, branding, build scripts, CI for the Electron app |
| **`editor/le-vibe-overrides/`** | Reserved for Lé Vibe–specific branding/overrides (see **`README.md`** there); §7.2 for material choices |
| **`editor/vscodium/`** | **VSCodium** upstream (recommended git submodule); **`product.json`**, **`get_repo.sh`** / **`build.sh`** per **`BUILD.md`** and upstream **`docs/howto-build.md`** |
| **`editor/smoke.sh`** | Local **H6** gate — runs **`packaging/scripts/ci-editor-gate.sh`** (layout, **`bash -n`** on upstream scripts, **`editor/.nvmrc`** sync) |
| **`editor/smoke-lvibe-editor.sh`** | Optional **launcher ↔ binary** check — runs **`lvibe`** stack with **`--editor`** and **`-- --version`** (needs **`ollama`** on **`PATH`**); see **`BUILD.md`** *Verify `lvibe`* |
| **`le-vibe/`** | Python bootstrap, `lvibe` launcher, managed Ollama, `.lvibe/` workspace hub, **`le-vibe`** `.deb` |
| **`debian/`**, **`packaging/`** | Debian packaging and PATH wrappers for the **stack** package |

**Product intent (aligned with earlier designs):** Local-first **Linux IDE** with managed Ollama lifecycle, **Continue**-oriented agent defaults, honest hardware tiering, and **Lé Vibe** naming—see **`spec-phase2.md` §2** (product definition), **`PRODUCT_SPEC.md`** (must-ship), and **`docs/vscodium-fork-le-vibe.md`**. Session/epic work under **`.lvibe/`** coordinates **delivery of this shell** plus the stack, not parallel products.

Populate **`editor/`** by vendoring upstream (e.g. [VSCodium](https://github.com/VSCodium/vscodium)) via **git submodule**, **subtree**, or a tracked import—see **`docs/vscodium-fork-le-vibe.md`** and **[`VENDORING.md`](VENDORING.md)** (recommended: submodule at **`editor/vscodium/`** so this README stays in-tree). Until sources exist here, developers may point **`LE_VIBE_EDITOR`** at system **VSCodium**; production intent remains **one tree**, one product.

**Node:** match VSCodium’s toolchain — **[`.nvmrc`](.nvmrc)** mirrors **`vscodium/.nvmrc`** (run **`nvm install`** / **`nvm use`** from **`editor/`** before upstream **`get_repo` / build** steps).

## `LE_VIBE_EDITOR` (launcher ↔ IDE binary)

The Python stack (`lvibe`, `le-vibe` wrappers) resolves the desktop editor in this order (see `le-vibe/le_vibe/launcher.py`):

1. **`LE_VIBE_EDITOR`** if set in the environment (absolute path or executable name on `PATH`).
2. Else **`/usr/bin/le-vibe-ide`** if that file exists and is executable (future packaged Lé Vibe IDE — **14.g**).
3. Else **`/usr/bin/codium`** if that file exists and is executable.
4. Else the bare command **`codium`** (must be on `PATH`).

**Packaging:** the **`le-vibe`** `.deb` sets a default of `/usr/bin/codium` in its launcher scripts and **Recommends: codium** in `debian/control` so a typical install gets an editor without extra flags. **When a future `le-vibe-ide` `.deb` ships** the branded binary, the stack should **`Recommends:`** it and define how **`LE_VIBE_EDITOR`** defaults (profile.d vs launcher order)—see **[`BUILD.md`](BUILD.md)** *Default `LE_VIBE_EDITOR` / packaging story when the IDE ships* (**14.g**). Until then, set **`LE_VIBE_EDITOR`** to your build path, symlink, or **`/usr/bin/codium`**, and keep CI smoke aligned.

**CI:** [`.github/workflows/build-le-vibe-ide.yml`](../.github/workflows/build-le-vibe-ide.yml) runs on `workflow_dispatch`, **`workflow_call`**, **`pull_request`** (paths under **`editor/`**, IDE workflows, **`ci-editor-gate`**, **`ci-editor-nvmrc-sync`**, **`ci-vscodium-bash-syntax`**), and tags `ide-v*`. [`.github/workflows/build-linux.yml`](../.github/workflows/build-linux.yml) is a **`build-linux`** label that dispatches the same job (manual only). When upstream is missing, the job **passes** with a skip notice; with the VSCodium submodule, smoke includes **`bash -n`** via [`ci-vscodium-bash-syntax.sh`](../packaging/scripts/ci-vscodium-bash-syntax.sh) and **`editor/.nvmrc`** parity via [`ci-editor-nvmrc-sync.sh`](../packaging/scripts/ci-editor-nvmrc-sync.sh). Extend the workflow with the real Linux build and **`.deb`/bundle** upload per **`docs/vscodium-fork-le-vibe.md`**; today the job uploads a small **metadata** artifact (`ide-ci-metadata.txt` — layout/ref/sha/run_id plus **`le_vibe_editor_docs=editor/README.md`** for **`LE_VIBE_EDITOR`**; pinned **`vscode-upstream-stable.json`** when the submodule is present) so the artifact path is wired before binaries exist — **`upload-artifact`** sets **retention-days** (bounded pre-binary store; see workflow YAML); the workflow sets **`permissions:`** **`contents: read`**, **`actions: write`** (checkout + artifact upload). On **GitHub Actions**, the run **Summary** tab echoes the same **`LE_VIBE_EDITOR`** pointer (**Pre-binary artifact** line) for quick verification. **Local check:** [`./editor/smoke.sh`](smoke.sh) from the repo root (wraps **[`packaging/scripts/ci-editor-gate.sh`](../packaging/scripts/ci-editor-gate.sh)**; also run via **[`packaging/scripts/ci-smoke.sh`](../packaging/scripts/ci-smoke.sh)**).

**Build (local):** **[`BUILD.md`](BUILD.md)** — pointers to **`vscodium/docs/howto-build.md`**, Node, overrides, **`LE_VIBE_EDITOR`** after a successful build, CI, and **tarball / `bin/codium` paths** (14.f — **`VSCode-linux-*`** vs release **`VSCodium-linux-*.tar.gz`**).

**Authority:** [`docs/PRODUCT_SPEC.md`](../docs/PRODUCT_SPEC.md) (naming, §7.2 user gate on material IDE choices), [`spec-phase2.md`](../spec-phase2.md) §2 and §14.
