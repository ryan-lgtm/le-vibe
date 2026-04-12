# Lé Vibe — brand assets & screenshot handoff (Roadmap H5)

**STEP 11 / PM map:** [`PM_STAGE_MAP.md`](PM_STAGE_MAP.md) — **H5** row links **`packaging/icons/`** (canonical **`le-vibe.svg`**), [`screenshots/README.md`](screenshots/README.md), and **PRODUCT_SPEC** §1 naming.

This document is the **handoff** for design and marketing: what ships in-repo today, what remains **optional** until a design system lands, and where to add **screenshots** without bloating every clone.

**Product anchor:** [`PRODUCT_SPEC.md`](PRODUCT_SPEC.md) §1 (naming **Lé Vibe**) and §9 (authority roster). **Roadmap H5** (this doc) is indexed from [`README.md`](README.md) and [`PROMPT_BUILD_LE_VIBE.md`](PROMPT_BUILD_LE_VIBE.md).

**H8 / trust (§1 vs `.github/` copy):** **[`docs/README.md`](README.md)** *Product surface* and **[`SECURITY.md`](../SECURITY.md)** *Related docs* (incl. optional [`rag/le-vibe-phase2-chunks.md`](rag/le-vibe-phase2-chunks.md) for *RAG / embeddings*, non-canonical) sit with **[`privacy-and-telemetry.md`](privacy-and-telemetry.md)** (*E1 contract tests*) — keep **§1** / *Naming (must ship)* aligned when **`.github/`** intros or **`SECURITY`** trust lists change.

**Packaged `.deb`:** [`debian/le-vibe.README.Debian`](../debian/le-vibe.README.Debian) → **`/usr/share/doc/le-vibe/README.Debian`** — post-install / Continue steps to mirror in honest marketing and store captures (**§5** **`.lvibe/`** consent applies to real sessions).

**E1 / acceptance:** After changing **`.desktop`** files, **`packaging/icons/`**, or primary **§1** product strings (**Lé Vibe**, é), run **`desktop-file-validate`** on the desktop entries (enforced in **`./packaging/scripts/ci-smoke.sh`** — **[`docs/ci-qa-hardening.md`](ci-qa-hardening.md)**), **`cd le-vibe && python3 -m pytest tests/`** (**H5** — §10 UI/docs + **`desktop-file-validate`** path; full **E1** roster — root [`README.md`](../README.md) *Tests* / **E1 mapping**, **[`spec-phase2.md`](../spec-phase2.md) §14** *Honesty vs CI*), and refresh **[`PRODUCT_SPEC_SECTION8_EVIDENCE.md`](PRODUCT_SPEC_SECTION8_EVIDENCE.md)** if **§10** acceptance moves.

## Current status (baseline shipped)

| Item | State |
|------|--------|
| **App icon (Linux)** | **Scalable SVG** at [`packaging/icons/hicolor/scalable/apps/le-vibe.svg`](../packaging/icons/hicolor/scalable/apps/le-vibe.svg) — Lé Vibe product mark (rounded tile, stylized **L** + curve). Comment in file may still say “swap for final brand guidelines”; functionally it is the **shipping** menu/launcher icon until design replaces it. |
| **Raster PNGs** | **Not** committed — optional for stores/legacy themes (see export checklist below). |
| **README / store screenshots** | **Not** committed by default — use **`docs/screenshots/`** (see [`screenshots/README.md`](screenshots/README.md)) or attach to **GitHub Releases** only. |

**Naming (must ship):** User-facing copy uses **Lé Vibe** (see **[`PRODUCT_SPEC.md`](PRODUCT_SPEC.md)** §1 — including **`.github/`** **H8** surfaces when maintainers or reporters see **`ci.yml`**, **`dependabot.yml`**, **`.github/ISSUE_TEMPLATE/`** intros, or **[`config.yml`](../.github/ISSUE_TEMPLATE/config.yml)** **`#` H8** maintainer lines). Do not use “Visual Studio Code” or Microsoft marks for the product; attribute the editor as **Code - OSS** / **VSCodium** where relevant.

## Canonical icon (Linux)

| Asset | Path |
|-------|------|
| **Scalable (source of truth in this repo)** | [`packaging/icons/hicolor/scalable/apps/le-vibe.svg`](../packaging/icons/hicolor/scalable/apps/le-vibe.svg) |

The **`.desktop`** entry uses **`Icon=le-vibe`**, which resolves via the **hicolor** theme. After editing the SVG, rebuild the **`.deb`** (or refresh your icon cache: **`gtk-update-icon-cache`**, session restart) to verify the launcher and app menu.

### Export checklist (optional PNGs)

If you ship fixed raster sizes (some stores or legacy themes expect them), export from the master art at **128×128** (and optionally **48**, **256**, **512**) into the usual **hicolor** layout, for example:

- `packaging/icons/hicolor/128x128/apps/le-vibe.png`
- `packaging/icons/hicolor/48x48/apps/le-vibe.png`

Then extend **`debian/le-vibe.install`** (or your packaging rules) to install those paths under **`/usr/share/icons/hicolor/...`**. Until PNGs exist, the scalable SVG alone is valid for modern desktops.

### Design constraints

- **Product name in UI/copy:** **Lé Vibe** — not “Visual Studio Code” or Microsoft marks.
- **This repo’s icon:** Lé Vibe–only mark; do not embed third-party logos.
- **Contrast:** Aim for recognizable shape at **22×22** (menu) and **48×48** (grid); test on light and dark panels.

### Presentation palette (diagrams & marketing — reference only)

For **Mermaid diagrams in docs**, slides, or future store art, a consistent accent pairing is **deep purple** (roughly `#4527A0`–`#5E35B1`) and **ruby red** (`#B71C1C`–`#C62828`). This is **not** a guarantee of shipped IDE chrome or themes until the **Lé Vibe** desktop shell (**H6**) defines UI tokens; it keeps diagrams and screenshots visually aligned when useful.

## Screenshots (README / Flatpak / store)

Capture on a **clean** theme at a consistent resolution (e.g. **1920×1080** or **1600×900**). Suggested set (filenames are conventions — adjust to your pipeline):

| Suggested filename | Content |
|---------------------|---------|
| `le-vibe-desktop-menu.png` | App launcher showing **Lé Vibe** entry with icon |
| `le-vibe-first-run.png` | First-run / model flow (no secrets on screen) |
| `le-vibe-continue-chat.png` | VSCodium + **Continue** panel, one turn to **localhost** Ollama (**port 11435**) |

Place files under **`docs/screenshots/`** (see **[`screenshots/README.md`](screenshots/README.md)**) **or** attach only to **GitHub Releases** / marketing CMS — avoid huge binaries on every clone if your team prefers release-only assets. Follow **[`spec-phase2.md`](../spec-phase2.md) §14** so captures do not imply a finished **Lé Vibe–branded** IDE **release** is already published (**H6** sources live under **`editor/vscodium/`**; branding layers use **`editor/le-vibe-overrides/`**).

When adding images to **`README.md`**, use repo-relative paths, for example **`docs/screenshots/le-vibe-continue-chat.png`**.

## Monorepo alignment (H6)

The **Lé Vibe IDE** shell is developed under **`editor/`** in **this** repository (**VSCodium** at **`editor/vscodium/`**, overrides **`editor/le-vibe-overrides/`**) — see **[`vscodium-fork-le-vibe.md`](vscodium-fork-le-vibe.md)**. Keep **`packaging/icons/`** (launcher / **`.deb`**) visually consistent with the IDE branding where possible.
