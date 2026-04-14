# Flatpak — Lé Vibe stack (`org.le_vibe.Launcher`)

Welcome — this is the Flatpak packaging entry point for the Lé Vibe stack.

**Roadmap H7 / STEP 13.** **Rough target:** [Flathub](https://flathub.org/) (submit a dedicated repo under `github.com/flathub` per Flathub workflow; this file is the **upstream manifest** in the monorepo).

**Authority:** [`docs/flatpak-appimage.md`](../../docs/flatpak-appimage.md), [`docs/PRODUCT_SPEC.md`](../../docs/PRODUCT_SPEC.md) §8–§9.

## What this bundles

The manifest installs the **Python `le-vibe/` stack** and **`lvibe`** wrappers (same layout idea as the **`.deb`**). It does **not** compile the **Lé Vibe IDE** Electron shell from **`editor/`**; users still point **`LE_VIBE_EDITOR`** at **VSCodium** / **`com.vscodium.VSCodium`** on the host or a separate Flatpak. See **Ollama / sandbox** notes in [`docs/flatpak-appimage.md`](../../docs/flatpak-appimage.md).

## Build (local)

From the **repository root** (full monorepo checkout; `flatpak` + `flatpak-builder` installed):

```bash
flatpak install -y flathub org.freedesktop.Platform//24.08 org.freedesktop.Sdk//24.08
flatpak-builder --user --install --force-clean flatpak-build-dir packaging/flatpak/org.le_vibe.Launcher.yml
```

`flatpak-builder` copies the repo root (`path: ../..` in the manifest). A populated **`editor/vscodium`** submodule increases clone size; for a slimmer working tree, skip or deinit that submodule before building if you do not need it.

## Flathub submission

1. Use or rename **`app-id`** to match Flathub naming / domain verification (often **`io.github.<org>.<app>`** once the GitHub org/repo is known).
2. Add **`metainfo.xml`** (AppStream) in a Flathub PR per [Flathub requirements](https://github.com/flathub/flathub/wiki/App-Requirements).
3. Run **`flatpak-builder-lint`** on the manifest and the built Flatpak.
