# Vendoring the IDE upstream (Lé Vibe `editor/`)

Keep Lé Vibe docs in **`editor/README.md`** by placing the **VSCodium** tree under **`editor/vscodium/`** (git submodule), not by replacing the whole **`editor/`** directory.

## Submodule (recommended; matches CI `submodules: recursive`)

From the monorepo root (with git initialized):

```bash
git submodule add https://github.com/VSCodium/vscodium.git editor/vscodium
git submodule update --init --recursive
```

Then follow upstream’s **prepare / build** docs from **`editor/vscodium/`**. CI [`.github/workflows/build-le-vibe-ide.yml`](../.github/workflows/build-le-vibe-ide.yml) (or the **`build-linux`** alias [`.github/workflows/build-linux.yml`](../.github/workflows/build-linux.yml)) treats either **`editor/package.json`** (flat checkout) or **`editor/vscodium/package.json`** (submodule layout) as “sources present.” Verify locally with **[`packaging/scripts/ci-editor-gate.sh`](../packaging/scripts/ci-editor-gate.sh)**.

## Branding & About

After the tree builds, apply Lé Vibe naming, icons, and About copy per **`docs/vscodium-fork-le-vibe.md`** and **`docs/PRODUCT_SPEC.md`** §7.2 where choices are material.

## `LE_VIBE_EDITOR`

Point **`LE_VIBE_EDITOR`** at your built binary (or packaged **`/usr/bin/...`**). See **`editor/README.md`**.
