# Cline extension — Open VSX version pin (Roadmap H4)

Reproducible installs use the Open VSX identifier **`saoudrizwan.claude-dev`** ([extension page](https://open-vsx.org/extension/saoudrizwan/claude-dev)). **`packaging/scripts/install-cline-extension.sh`** passes **`codium --install-extension saoudrizwan.claude-dev@<version>`** where **`<version>`** comes from **`packaging/cline-openvsx-version`** (one semver per line; comments with **`#`** allowed above the version).

The same script installs the companion **`redhat.vscode-yaml`** extension ([Open VSX](https://open-vsx.org/extension/redhat/vscode-yaml)) at **`redhat.vscode-yaml@<version>`** using **`packaging/vscode-yaml-openvsx-version`**, so schema-driven configuration stays consistent in the Cline-first path.

After **`dpkg -i`**, the same pins are installed under **`/usr/share/le-vibe/`** as **`cline-openvsx-version`** and **`vscode-yaml-openvsx-version`**; the script resolves them via **`SCRIPT_DIR/../…`** next to **`install-cline-extension.sh`** (works for both repo and packaged layouts).

**Product anchor:** [`PRODUCT_SPEC.md`](PRODUCT_SPEC.md) §8–§9. **§7.3** fixes the public **`lvibe`** CLI and **`le-vibe-ide`** layout (**`/usr/lib/le-vibe/bin/codium`**) — the Open VSX semver here is unchanged when that shell is present vs a dev-tree **`LE_VIBE_EDITOR`**. **Roadmap H4** (this doc) is indexed from [`README.md`](README.md), [`le-vibe/README.md`](../le-vibe/README.md) *STEP 7*, and [`PROMPT_BUILD_LE_VIBE.md`](PROMPT_BUILD_LE_VIBE.md).

**H8 / trust (same repo):** **[`docs/README.md`](README.md)** *Product surface* — **`.github/`** — **`ci.yml`**, **`dependabot.yml`**, **`.github/ISSUE_TEMPLATE/`** + **[`config.yml`](../.github/ISSUE_TEMPLATE/config.yml)** **`#` H8** — plus **[`SECURITY.md`](../SECURITY.md)** *Related docs* (incl. optional [`rag/le-vibe-phase2-chunks.md`](rag/le-vibe-phase2-chunks.md) for *RAG / embeddings*, non-canonical; **`spec-phase2.md`**) and **[`privacy-and-telemetry.md`](privacy-and-telemetry.md)** (*E1 contract tests*).

**`.deb` / `apt`:** The end-to-end steps below match **`/usr/share/doc/le-vibe/README.Debian`** ([`debian/le-vibe.README.Debian`](../debian/le-vibe.README.Debian)) — first-run, **`le-vibe-setup-cline`**, pinned Open VSX install (**§5**/**§8** unchanged).

**Phase 2 scope:** This pin story covers **Cline** on **system VSCodium** (or **`LE_VIBE_EDITOR`**) plus **`le-vibe`** configs — not a **published** **Lé Vibe–branded** IDE artifact from **`editor/`** until **H6** release work lands (**VSCodium** sources live under **`editor/vscodium/`** in the monorepo); see **[`spec-phase2.md`](../spec-phase2.md) §14** (**H6**/**H7**).

**Fresh clone (14.b):** from the repository root, run **`git submodule update --init editor/vscodium`** when **`editor/vscodium/`** is empty before **`dev/build.sh`**, **`verify-14c-local-binary.sh`**, or the **14.f** path helpers — **[`editor/README.md`](../editor/README.md)** *Fresh clone (14.b)*.

### STEP 14.h — same pin when the editor comes from `editor/`

The **Open VSX semver** in **`packaging/cline-openvsx-version`** is the single source of truth for reproducible installs. It does **not** change when **`LE_VIBE_EDITOR`** points at a **locally built** **`VSCode-linux-*/bin/codium`** or a **CI tarball** instead of **`/usr/bin/codium`** — **`packaging/scripts/install-cline-extension.sh`** always runs **`"$LE_VIBE_EDITOR" --install-extension saoudrizwan.claude-dev@<pin>`** (or override env vars in the table below).

| Concern | Behavior |
|---------|----------|
| **Bundled VSIX in `editor/`** | **Not** shipped in-tree; Cline is installed from the marketplace via the editor CLI (same as stock VSCodium). |
| **First-run vs extension** | **`lvibe`** first-run prepares runtime/config state under **`~/.config/le-vibe/`**; run **`le-vibe-setup-cline`** after that so Cline + YAML install in a deterministic order (see *End-to-end* below). |
| **Editor binary when `LE_VIBE_EDITOR` is unset** | **`packaging/scripts/install-cline-extension.sh`** picks **`/usr/lib/le-vibe/bin/codium`** ( **`le-vibe-ide`** **`.deb`** ), then **`/usr/bin/codium`**, then **`codium`** on **`PATH`** — same order as **`le_vibe.launcher._default_editor`** (**14.g**; **`debian/le-vibe.README.Debian`**). |
| **`LE_VIBE_EDITOR` from `editor/` builds** | After **`dev/build.sh`**, or when you have a **`vscodium-linux-build.tar.gz`** file, set **`LE_VIBE_EDITOR`** via **`editor/print-built-codium-path.sh`**, **`editor/print-vsbuild-codium-path.sh`**, or **`editor/print-ci-tarball-codium-path.sh`** (unpacks to a temp dir — **14.f**) before **`install-cline-extension.sh`** — **[`editor/BUILD.md`](../editor/BUILD.md)** (**14.c** / **14.f**). |
| **Partial `VSCode-linux-*` (no `bin/codium`)** | Finish **`dev/build.sh`** per **[`editor/BUILD.md`](../editor/BUILD.md)** (*Partial tree*, **14.c**) before **`install-cline-extension.sh`**. Triage: **`packaging/scripts/print-step14-vscode-linux-bin-files.sh`** prints **`bin/`** filenames (same as **`lvibe ide-prereqs --json`** **`vscode_linux_bin_files`**); pair with **`packaging/scripts/probe-vscode-linux-build.sh`**. |
| **Confirm built binary (optional)** | **`./editor/verify-14c-local-binary.sh`** (**14.c**) checks **`VSCode-linux-*/bin/codium`** under **`editor/vscodium/`** without **`ollama`**; it does **not** install Cline. Use it before **`install-cline-extension.sh`** when debugging a fresh local compile — then **`export LE_VIBE_EDITOR="$(./editor/print-built-codium-path.sh)"`** (or the **14.f** helpers for CI/unpacked trees). |
| **CI artifact download (`linux_compile`)** | GitHub delivers **`vscodium-linux-build.tar.gz`** inside a **`.zip`** — unzip first, then pass the **`.tar.gz`** to **`print-ci-tarball-codium-path.sh`** (same **14.f** pitfall as **`LE_VIBE_EDITOR`** for **`lvibe`**). |
| **Branding (14.d) vs this pin** | The Open VSX semver is independent of IDE **product identity** (name, About, desktop entry, icons in the Electron tree). Material **Lé Vibe**–visible branding is gated by **`docs/PRODUCT_SPEC.md` §7.2** — maintainer map **[`editor/le-vibe-overrides/branding-staging.checklist.md`](../editor/le-vibe-overrides/branding-staging.checklist.md)** (**14.d**). |
| **Docs** | Tarball paths — **[`editor/BUILD.md`](../editor/BUILD.md)**; IDE packaging story — *14.g* there. |

**E1 / acceptance:** After changing **`packaging/cline-openvsx-version`**, run **`cd le-vibe && python3 -m pytest tests/test_install_cline_extension_script.py tests/test_setup_cline_script.py`**. If Cline install copy or first-run messaging changes, refresh **[`PRODUCT_SPEC_SECTION8_EVIDENCE.md`](PRODUCT_SPEC_SECTION8_EVIDENCE.md)** — same release discipline as **[H1](apt-repo-releases.md)** / **[H2](sbom-signing-audit.md)** / **[H3](ci-qa-hardening.md)** *E1* notes.

## End-to-end (typical)

1. Complete first-run so runtime/model state exists under **`~/.config/le-vibe/`** (launch **`lvibe`** once).
2. On the **next** **`lvibe`** start, the launcher attempts **`le-vibe-setup-cline`** automatically (**`le_vibe.cline_setup_auto`** — **`LE_VIBE_AUTO_CLINE_SETUP=0`** to disable). If that fails, run **`le-vibe-setup-cline`** manually.
3. The editor installs **`saoudrizwan.claude-dev@<pinned-version>`** and **`redhat.vscode-yaml@<pinned-version>`** from your configured marketplace (Open VSX for common VSCodium setups).

Manual install from a dev tree (any cwd; script finds its pin file):

```bash
bash /path/to/r-vibe/packaging/scripts/install-cline-extension.sh
```

## Maintainer workflow

1. Pick a version: browse [Open VSX — Cline](https://open-vsx.org/extension/saoudrizwan/claude-dev) or query latest:  
   `curl -sS 'https://open-vsx.org/api/saoudrizwan/claude-dev/latest' | head -c 400`  
   (inspect **`version`** in the JSON).
2. Set **`packaging/cline-openvsx-version`** to that semver (**one** non-comment line).
3. Set **`packaging/vscode-yaml-openvsx-version`** for **`redhat.vscode-yaml`** (query Open VSX **`/api/redhat/vscode-yaml/latest`** or browse the extension page; one semver line).
4. Run **`cd le-vibe && pytest tests/test_install_cline_extension_script.py tests/test_setup_cline_script.py`**.
5. Rebuild the **`.deb`** and smoke-test **`le-vibe-setup-cline`** with VSCodium.

## CI

**`.github/workflows/ci.yml`** runs **`packaging/scripts/ci-smoke.sh`** before pytest; keep Cline pin/script checks in the Cline installer test contracts.

## Overrides (environment)

| Variable | Effect |
|----------|--------|
| *(unset)* | Read version from the pin file next to the install script (or **`LE_VIBE_CLINE_PIN_FILE`**). |
| **`LE_VIBE_CLINE_OPENVSX_VERSION=latest`** | Install without **`@version`** (marketplace “latest”). |
| **`LE_VIBE_CLINE_OPENVSX_VERSION=1.2.3`** | Pin to that version regardless of the file. |
| **`LE_VIBE_CLINE_EXTENSION`** | Extension id (default **`saoudrizwan.claude-dev`**). Version is still applied as **`id@version`** unless **`latest`**. |
| **`LE_VIBE_CLINE_PIN_FILE`** | Alternate path to a one-line version file. |
| **`LE_VIBE_VSCODE_YAML_OPENVSX_VERSION`** | Same semantics as Continue: unset reads **`packaging/vscode-yaml-openvsx-version`**; **`latest`** installs **`redhat.vscode-yaml`** without **`@version`**. |
| **`LE_VIBE_VSCODE_YAML_PIN_FILE`** | Alternate path for the YAML extension semver file (default next to **`install-cline-extension.sh`**). |
| **`LE_VIBE_VSCODE_YAML_EXTENSION`** | Override extension id (default **`redhat.vscode-yaml`**). |

If a pin file is **missing** and the matching **`LE_VIBE_*_OPENVSX_VERSION`** is unset, the script installs that extension id **without** **`@version`** (whatever the marketplace resolves)—**not** reproducible; keep both pin files in packaging for release builds.

VSIX files are **not** bundled in this repo; **`codium --install-extension id@version`** downloads from the editor’s configured marketplace.
