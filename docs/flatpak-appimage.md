# Lé Vibe — Flatpak & AppImage (Roadmap H7)

## Scope status (this repository)

**Deliverable for H7 here:** this document only — **rationale**, **host/sandbox constraints**, **coordination** with the **`.deb`** and **[`apt-repo-releases.md`](apt-repo-releases.md)** / **[`sbom-signing-audit.md`](sbom-signing-audit.md)**. **Flatpak manifests** and **AppImage** build recipes are **intentionally not** shipped in this tree (keeps CI and clone size small); add them in a **separate** manifest repo or workflow when you productize those channels.

**SKIPPED (in-repo manifests):** No `*.yml` / `flatpak-builder` / `AppRun` definitions live under this repo by policy above — not a gap to “fix” in-tree unless the product owner moves packaging here.

The **supported** Linux package in this repository is the **native `.deb`** built with **`dpkg-buildpackage`** (see root **`README.md`**). **Flatpak** and **AppImage** are **optional** distribution shapes.

**Product anchor:** [`PRODUCT_SPEC.md`](PRODUCT_SPEC.md) §8–§9 (secrets + orchestration roster). **H7** stays coordination-only here — [`spec-phase2.md`](../spec-phase2.md) **§14** (*in-repo vs deferred*); **H6** — [`vscodium-fork-le-vibe.md`](vscodium-fork-le-vibe.md), [`editor/README.md`](../editor/README.md) (monorepo **`editor/`**).

**`.github/` trust (native tree, H8):** **[`README.md`](README.md)** *Product surface* lists **`.github/`** — **`ci.yml`**, **`dependabot.yml`**, **`.github/ISSUE_TEMPLATE/`** + **[`config.yml`](../.github/ISSUE_TEMPLATE/config.yml)** **`#` H8** maintainer lines — plus **[`SECURITY.md`](../SECURITY.md)** (*Related docs* incl. optional **[`rag/le-vibe-phase2-chunks.md`](rag/le-vibe-phase2-chunks.md)** — *RAG / embeddings*, non-canonical) and **[`privacy-and-telemetry.md`](privacy-and-telemetry.md)** (*E1 contract tests*). A **separate** Flatpak/AppImage pipeline should document how it stays comparable on supply chain and reporting.

**E1 (this repository):** There is **no** in-tree Flatpak/AppImage build to **`pytest`** — acceptance for Linux shipping remains the **`.deb`** + **`le-vibe/tests/`** + **[`PRODUCT_SPEC_SECTION8_EVIDENCE.md`](PRODUCT_SPEC_SECTION8_EVIDENCE.md)** (compare **[H1](apt-repo-releases.md)** / **[H2](sbom-signing-audit.md)** *E1*). **Native-tree full E1 roster** — root **[`README.md`](../README.md)** *Tests* / **E1 mapping**; **[`spec-phase2.md`](../spec-phase2.md) §14** *Honesty vs CI*. A downstream bundle repo needs its own SBOM, **`pip-audit`**, and release checks.

**Native `.deb` baseline:** [`debian/le-vibe.README.Debian`](../debian/le-vibe.README.Debian) / **`/usr/share/doc/le-vibe/README.Debian`** documents the supported install path (post-install, **§5** **`.lvibe/`** consent) — compare Flatpak/AppImage UX gaps against this, not an imagined shortcut.

## Why a separate pipeline

- **Ollama:** Lé Vibe expects **`ollama`** on the host (or an install path the bootstrap can use). Sandboxed Flatpak apps need explicit **`--filesystem`** / **`--talk-name`** (or similar) permissions so **`ollama serve`** on **localhost:11435** and model storage remain usable — document every hole you punch.
- **Editor:** VSCodium / Code OSS is **not** bundled in the `.deb`; the same applies here: either depend on **`com.vscodium.VSCodium`** from Flathub as a **runtime extension** / side-install, or tell users to install the editor on the host and set **`LE_VIBE_EDITOR`** to the binary inside the sandbox if exposed.
- **Autostart / Zenity:** **`/etc/xdg/autostart`** and **`zenity`** behave differently under sandbox; re-test **G-A2** / **G-A3** UX if you port those entry points.

## Flatpak (outline)

Typical ingredients:

1. **`org.example.LeVibe.yml`** (or JSON) with **`io.github.flatpak.BaseApp`** / **`org.freedesktop.Platform`** + **`org.freedesktop.Sdk`** matching your Python version.
2. **Module** that installs **`le-vibe/`** (e.g. **`pip install .`** or copy the tree) and **`/app/bin/le-vibe`** launcher.
3. **`finish-args`:** **`--share=network`**, **`--socket=fallback-x11`**, **`--socket=wayland`**, **`--filesystem=home`** (narrow as far as possible), plus whatever is required for **`~/.config/le-vibe`** and talking to **Ollama**.
4. **Desktop file** and **icons** from **`packaging/`**, validated with **`desktop-file-validate`**.

Publish via **Flathub** or a private **flatpak** remote; signing and **`flatpak-builder-lint`** are part of that process.

## AppImage (outline)

1. Build a minimal prefix (or use **linuxdeploy** / **appimagetool**) containing Python, **`le-vibe`** deps, and wrapper scripts.
2. Ship the same **`AppRun`** pattern: invoke **`python3 -m le_vibe.launcher`** or **`/usr/bin/le-vibe`** equivalent with **`PYTHONPATH`** set inside the image.
3. **FUSE** / **libfuse** requirements on user systems — document clearly.

## Coordination with this repo

- **Versioning:** Align AppImage / Flatpak **release tags** with **`debian/changelog`** or your public version story when you announce a drop.
- **SBOM / audit:** Reuse **[`docs/sbom-signing-audit.md`](sbom-signing-audit.md)** ideas for Python deps; Flatpak has its own module graph.
- **Releases:** **[`docs/apt-repo-releases.md`](apt-repo-releases.md)** describes checksums and apt hosting; attach AppImage **`.zsync`** or Flatpak **refs** the same way you would other binaries.
