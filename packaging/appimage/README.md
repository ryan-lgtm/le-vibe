# AppImage — Lé Vibe stack (H7)

**Rough target:** self-contained-ish Linux bundle; **production** users should still prefer the **`.deb`** or **[Flatpak](../flatpak/README.md)** (Flathub track) when available.

**Authority:** [`docs/flatpak-appimage.md`](../../docs/flatpak-appimage.md).

## Layout

- **`AppRun`** — sets **`PYTHONPATH`** to the staged **`le-vibe/`** package and pip **`--target`** deps, then runs **`python3 -m le_vibe.launcher`** (same entry as **`lvibe`**).
- **`build-appimage.sh`** — copies **`le-vibe/`**, **`pip install --target`** for [`requirements.txt`](../../le-vibe/requirements.txt), writes **`AppDir/`**, and runs **`appimagetool`** when installed.

This image **expects `python3` on the host PATH** inside the runtime (common AppImage pattern when not embedding CPython). Embedding a full Python prefix is a possible follow-up for stricter portability.

## Build

From the repository root:

```bash
chmod +x packaging/appimage/build-appimage.sh packaging/appimage/AppRun
./packaging/appimage/build-appimage.sh
```

Set **`APPIMAGETOOL`** if the tool is not named **`appimagetool`**.

The IDE binary is **not** bundled; set **`LE_VIBE_EDITOR`** to **VSCodium** / the Lé Vibe IDE **`.deb`** install per [`docs/flatpak-appimage.md`](../../docs/flatpak-appimage.md).
