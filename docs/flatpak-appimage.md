# Lé Vibe — Flatpak & AppImage (Roadmap H7)

**STEP 13 / PM map:** [`PM_STAGE_MAP.md`](PM_STAGE_MAP.md) — **H7** ships **in-tree** packaging templates for **Flatpak** (Flathub-oriented) and **AppImage** under **`packaging/`** — see **[`spec-phase2.md`](../spec-phase2.md) §14** vs **H6** **`editor/`**.

## In this repository

| Path | Role |
|------|------|
| **[`packaging/flatpak/org.le_vibe.Launcher.yml`](../packaging/flatpak/org.le_vibe.Launcher.yml)** | **`flatpak-builder`** manifest for the **Python stack** + **`lvibe`** (same rough role as the **`.deb`**). |
| **[`packaging/flatpak/README.md`](../packaging/flatpak/README.md)** | Local build commands; **Flathub** submission notes (separate `flathub` git repo, AppStream, **`flatpak-builder-lint`**). |
| **[`packaging/appimage/`](../packaging/appimage/)** | **`AppRun`**, **`build-appimage.sh`**, **[`README.md`](../packaging/appimage/README.md)** — stages **`AppDir/`** and runs **`appimagetool`** when available. |

**Rough target — Flathub:** Use this manifest as the **upstream** source for a Flathub submission (typically a dedicated repo under **`github.com/flathub`**, per Flathub’s workflow). Rename **`app-id`** if required for **reverse-DNS** verification (e.g. **`io.github.<org>.<name>`** once the GitHub namespace is fixed).

**Supported baseline Linux install** remains the **native `.deb`** ([`apt-repo-releases.md`](apt-repo-releases.md), [`sbom-signing-audit.md`](sbom-signing-audit.md)). Flatpak/AppImage are **additional** channels for the **stack**; they do **not** replace the **`.deb`** story for maintainer CI in this repo.

**Product anchor:** [`PRODUCT_SPEC.md`](PRODUCT_SPEC.md) §8–§9. **H8** (trust) — [`README.md`](README.md) *Product surface* — **`.github/`** (**`ci.yml`**, **`dependabot.yml`**, **`ISSUE_TEMPLATE/`** + [`config.yml`](../.github/ISSUE_TEMPLATE/config.yml) **`#` H8**).

**E1 (this repository):** There is still **no** CI job that **builds** Flatpak/AppImage on every PR (clone size, runner time). **`pytest`** locks docs + paths via [`test_flatpak_appimage_doc_h7_contract.py`](../le-vibe/tests/test_flatpak_appimage_doc_h7_contract.py). **Native** acceptance remains **`le-vibe/tests/`** + **`.deb`** + [`PRODUCT_SPEC_SECTION8_EVIDENCE.md`](PRODUCT_SPEC_SECTION8_EVIDENCE.md) — compare **[H1](apt-repo-releases.md)** / **[H2](sbom-signing-audit.md)** *E1*.

**Native `.deb` baseline:** [`debian/le-vibe.README.Debian`](../debian/le-vibe.README.Debian) — **§5** **`.lvibe/`** consent; compare alternate-bundle UX (sandbox, **`ollama`**) against this.

## Ollama, editor, sandbox

- **Ollama:** Lé Vibe expects **`ollama`** reachable (managed or system). Sandboxed Flatpak apps need explicit **`finish-args`** (e.g. **`--share=network`**, **`--filesystem`** for model paths) — tighten beyond the template as you harden the product.
- **Editor:** The **Electron IDE** is **not** compiled inside these H7 templates; users install **VSCodium** / **[`com.vscodium.VSCodium`](https://flathub.org/apps/com.vscodium.codium)** on the host or set **`LE_VIBE_EDITOR`** to a reachable binary (same story as [`debian/le-vibe.README.Debian`](../debian/le-vibe.README.Debian) **14.g**).
- **Autostart / Zenity:** Paths differ under sandbox; re-validate **G-A2** / **G-A3** if you ship those entry points inside a bundle.

## Flatpak (Flathub track)

1. Build locally — [`packaging/flatpak/README.md`](../packaging/flatpak/README.md).
2. Add **AppStream** **`metainfo.xml`** for Flathub PRs.
3. Run **`flatpak-builder-lint`** before publishing.

## AppImage

1. Run **`./packaging/appimage/build-appimage.sh`** from the repo root (see [`packaging/appimage/README.md`](../packaging/appimage/README.md)).
2. The current **`AppRun`** uses the **host `python3`**; embedding CPython in **`AppDir`** is optional follow-up for stricter portability.

## Coordination

- **Versioning:** Align bundle versions with **`debian/changelog`** / public release story ([`apt-repo-releases.md`](apt-repo-releases.md)).
- **SBOM / audit:** Python deps follow [`sbom-signing-audit.md`](sbom-signing-audit.md); Flatpak modules add their own graph.
- **Releases:** Attach **`.zsync`** / Flatpak **refs** alongside **`SHA256SUMS`** where applicable.
