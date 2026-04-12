# Vendoring the IDE upstream (Lé Vibe `editor/`)

Keep Lé Vibe docs in **`editor/README.md`** by placing the **VSCodium** tree under **`editor/vscodium/`** (git submodule), not by replacing the whole **`editor/`** directory.

## Submodule (recommended; matches CI `submodules: recursive`)

From the monorepo root (with git initialized):

```bash
git submodule add https://github.com/VSCodium/vscodium.git editor/vscodium
git submodule update --init --recursive
```

Then follow upstream’s **prepare / build** docs from **`editor/vscodium/`** (fetch vscode via **`get_repo.sh`**; root **`package.json`** appears only after that step). Monorepo checklist: **[`BUILD.md`](BUILD.md)**. CI [`.github/workflows/build-le-vibe-ide.yml`](../.github/workflows/build-le-vibe-ide.yml) (or the **`build-linux`** alias [`.github/workflows/build-linux.yml`](../.github/workflows/build-linux.yml)) treats **`editor/package.json`** (flat vscode checkout) or **`editor/vscodium/product.json`** (VSCodium tree) as “sources present.” Verify locally from the repo root with **`./editor/smoke.sh`** (wraps **[`packaging/scripts/ci-editor-gate.sh`](../packaging/scripts/ci-editor-gate.sh)** — **`bash -n`** via **[`packaging/scripts/ci-vscodium-bash-syntax.sh`](../packaging/scripts/ci-vscodium-bash-syntax.sh)** and **`editor/.nvmrc`** parity via **[`packaging/scripts/ci-editor-nvmrc-sync.sh`](../packaging/scripts/ci-editor-nvmrc-sync.sh)** when the submodule is present). On **GitHub Actions**, successful runs also upload pre-binary **`ide-ci-metadata.txt`** (**`le_vibe_editor_docs`**) and write a run **Summary** **Pre-binary artifact** line for the **`LE_VIBE_EDITOR`** docs pointer — see **[`BUILD.md`](BUILD.md)** *CI* and **[`README.md`](README.md)** *CI*.

## Branding & About

After the tree builds, apply Lé Vibe naming, icons, and About copy per **`docs/vscodium-fork-le-vibe.md`** and **`docs/PRODUCT_SPEC.md`** §7.2 where choices are material. Reserved monorepo path: **[`le-vibe-overrides/README.md`](le-vibe-overrides/README.md)** (empty until branding assets or documented patches land).

## `LE_VIBE_EDITOR`

Point **`LE_VIBE_EDITOR`** at your built binary (or packaged **`/usr/bin/...`**). See **`editor/README.md`**.
