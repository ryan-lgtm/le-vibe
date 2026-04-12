# Continue extension — Open VSX version pin (Roadmap H4)

Reproducible installs use the Open VSX identifier **`continue.continue`** ([extension page](https://open-vsx.org/extension/Continue/continue)). **`packaging/scripts/install-continue-extension.sh`** passes **`codium --install-extension continue.continue@<version>`** where **`<version>`** comes from **`packaging/continue-openvsx-version`** (one semver per line; comments with **`#`** allowed above the version).

After **`dpkg -i`**, the same pin is installed at **`/usr/share/le-vibe/continue-openvsx-version`**; the script resolves it via **`SCRIPT_DIR/../continue-openvsx-version`** (works for both repo and packaged layouts).

**Product anchor:** [`PRODUCT_SPEC.md`](PRODUCT_SPEC.md) §8–§9. **§7.3** fixes the public **`lvibe`** CLI and **`le-vibe-ide`** layout (**`/usr/lib/le-vibe/bin/codium`**) — the Open VSX semver here is unchanged when that shell is present vs a dev-tree **`LE_VIBE_EDITOR`**. **Roadmap H4** (this doc) is indexed from [`README.md`](README.md), [`le-vibe/README.md`](../le-vibe/README.md) *STEP 7*, and [`PROMPT_BUILD_LE_VIBE.md`](PROMPT_BUILD_LE_VIBE.md).

**H8 / trust (same repo):** **[`docs/README.md`](README.md)** *Product surface* — **`.github/`** — **`ci.yml`**, **`dependabot.yml`**, **`.github/ISSUE_TEMPLATE/`** + **[`config.yml`](../.github/ISSUE_TEMPLATE/config.yml)** **`#` H8** — plus **[`SECURITY.md`](../SECURITY.md)** *Related docs* (incl. optional [`rag/le-vibe-phase2-chunks.md`](rag/le-vibe-phase2-chunks.md) for *RAG / embeddings*, non-canonical; **`spec-phase2.md`**) and **[`privacy-and-telemetry.md`](privacy-and-telemetry.md)** (*E1 contract tests*).

**`.deb` / `apt`:** The end-to-end steps below match **`/usr/share/doc/le-vibe/README.Debian`** ([`debian/le-vibe.README.Debian`](../debian/le-vibe.README.Debian)) — first-run, **`le-vibe-setup-continue`**, pinned Open VSX install (**§5**/**§8** unchanged).

**Phase 2 scope:** This pin story covers **Continue** on **system VSCodium** (or **`LE_VIBE_EDITOR`**) plus **`le-vibe`** configs — not a **published** **Lé Vibe–branded** IDE artifact from **`editor/`** until **H6** release work lands (**VSCodium** sources live under **`editor/vscodium/`** in the monorepo); see **[`spec-phase2.md`](../spec-phase2.md) §14** (**H6**/**H7**).

**Fresh clone (14.b):** from the repository root, run **`git submodule update --init editor/vscodium`** when **`editor/vscodium/`** is empty before **`dev/build.sh`**, **`verify-14c-local-binary.sh`**, or the **14.f** path helpers — **[`editor/README.md`](../editor/README.md)** *Fresh clone (14.b)*.

### STEP 14.h — same pin when the editor comes from `editor/`

The **Open VSX semver** in **`packaging/continue-openvsx-version`** is the single source of truth for reproducible installs. It does **not** change when **`LE_VIBE_EDITOR`** points at a **locally built** **`VSCode-linux-*/bin/codium`** or a **CI tarball** instead of **`/usr/bin/codium`** — **`packaging/scripts/install-continue-extension.sh`** always runs **`"$LE_VIBE_EDITOR" --install-extension continue.continue@<pin>`** (or override env vars in the table below).

| Concern | Behavior |
|---------|----------|
| **Bundled VSIX in `editor/`** | **Not** shipped in-tree; Continue is installed from the marketplace via the editor CLI (same as stock VSCodium). |
| **First-run vs extension** | **`lvibe`** first-run creates stack config under **`~/.config/le-vibe/`**; run **`le-vibe-setup-continue`** after that so **`sync-continue-config.sh`** + **`install-continue-extension.sh`** run in order (see *End-to-end* above). **`./editor/smoke-lvibe-editor.sh`** only checks launcher ↔ binary — it does **not** install Continue. |
| **Editor binary when `LE_VIBE_EDITOR` is unset** | **`packaging/scripts/install-continue-extension.sh`** picks **`/usr/lib/le-vibe/bin/codium`** ( **`le-vibe-ide`** **`.deb`** ), then **`/usr/bin/codium`**, then **`codium`** on **`PATH`** — same order as **`le_vibe.launcher._default_editor`** (**14.g**; **`debian/le-vibe.README.Debian`**). |
| **`LE_VIBE_EDITOR` from `editor/` builds** | After **`dev/build.sh`**, or when you have a **`vscodium-linux-build.tar.gz`** file, set **`LE_VIBE_EDITOR`** via **`editor/print-built-codium-path.sh`**, **`editor/print-vsbuild-codium-path.sh`**, or **`editor/print-ci-tarball-codium-path.sh`** (unpacks to a temp dir — **14.f**) before **`install-continue-extension.sh`** — **[`editor/BUILD.md`](../editor/BUILD.md)** (**14.c** / **14.f**). |
| **Confirm built binary (optional)** | **`./editor/verify-14c-local-binary.sh`** (**14.c**) checks **`VSCode-linux-*/bin/codium`** under **`editor/vscodium/`** without **`ollama`**; it does **not** install Continue. Use it before **`install-continue-extension.sh`** when debugging a fresh local compile — then **`export LE_VIBE_EDITOR="$(./editor/print-built-codium-path.sh)"`** (or the **14.f** helpers for CI/unpacked trees). |
| **CI artifact download (`linux_compile`)** | GitHub delivers **`vscodium-linux-build.tar.gz`** inside a **`.zip`** — unzip first, then pass the **`.tar.gz`** to **`print-ci-tarball-codium-path.sh`** (same **14.f** pitfall as **`LE_VIBE_EDITOR`** for **`lvibe`**). |
| **Branding (14.d) vs this pin** | The Open VSX semver is independent of IDE **product identity** (name, About, desktop entry, icons in the Electron tree). Material **Lé Vibe**–visible branding is gated by **`docs/PRODUCT_SPEC.md` §7.2** — maintainer map **[`editor/le-vibe-overrides/branding-staging.checklist.md`](../editor/le-vibe-overrides/branding-staging.checklist.md)** (**14.d**). |
| **Docs** | Tarball paths — **[`editor/BUILD.md`](../editor/BUILD.md)**; IDE packaging story — *14.g* there. |

**E1 / acceptance:** After changing **`packaging/continue-openvsx-version`**, run **`./packaging/scripts/verify-continue-pin.sh`** and **`cd le-vibe && python3 -m pytest tests/`** (**H4** — **[`test_continue_openvsx_pin.py`](../le-vibe/tests/test_continue_openvsx_pin.py)**; full **E1** roster — root [`README.md`](../README.md) *Tests* / **E1 mapping**, **[`spec-phase2.md`](../spec-phase2.md) §14** *Honesty vs CI*). If Continue install copy or first-run messaging changes, refresh **[`PRODUCT_SPEC_SECTION8_EVIDENCE.md`](PRODUCT_SPEC_SECTION8_EVIDENCE.md)** — same release discipline as **[H1](apt-repo-releases.md)** / **[H2](sbom-signing-audit.md)** / **[H3](ci-qa-hardening.md)** *E1* notes.

## End-to-end (typical)

1. Complete first-run so **`~/.config/le-vibe/continue-config.yaml`** exists (launch **`lvibe`** once).
2. Run **`le-vibe-setup-continue`** (or **`--gui`**), which runs **`sync-continue-config.sh`** then **`install-continue-extension.sh`**.
3. The editor installs **`continue.continue@<pinned-version>`** from your configured marketplace (Open VSX for common VSCodium setups).

Manual install from a dev tree (any cwd; script finds its pin file):

```bash
bash /path/to/r-vibe/packaging/scripts/install-continue-extension.sh
```

## Maintainer workflow

1. Pick a version: browse [Open VSX — Continue](https://open-vsx.org/extension/Continue/continue) or query latest:  
   `curl -sS 'https://open-vsx.org/api/Continue/continue/latest' | head -c 400`  
   (inspect **`version`** in the JSON).
2. Set **`packaging/continue-openvsx-version`** to that semver (**one** non-comment line).
3. Run **`./packaging/scripts/verify-continue-pin.sh`** (and **`cd le-vibe && pytest`** — includes **`test_continue_openvsx_pin`**).
4. Rebuild the **`.deb`** and smoke-test **`le-vibe-setup-continue`** with VSCodium.

## CI

**`.github/workflows/ci.yml`** runs **`packaging/scripts/ci-smoke.sh`**, which invokes **`verify-continue-pin.sh`** before pytest so a bad or empty pin fails the job.

## Overrides (environment)

| Variable | Effect |
|----------|--------|
| *(unset)* | Read version from the pin file next to the install script (or **`LE_VIBE_CONTINUE_PIN_FILE`**). |
| **`LE_VIBE_CONTINUE_OPENVSX_VERSION=latest`** | Install without **`@version`** (marketplace “latest”). |
| **`LE_VIBE_CONTINUE_OPENVSX_VERSION=1.2.3`** | Pin to that version regardless of the file. |
| **`LE_VIBE_CONTINUE_EXTENSION`** | Extension id (default **`continue.continue`**). Version is still applied as **`id@version`** unless **`latest`**. |
| **`LE_VIBE_CONTINUE_PIN_FILE`** | Alternate path to a one-line version file. |

If the pin file is **missing** and **`LE_VIBE_CONTINUE_OPENVSX_VERSION`** is unset, the script installs **`continue.continue`** with **no** **`@version`** (whatever the marketplace resolves)—**not** reproducible; keep the pin file in packaging for release builds.

VSIX files are **not** bundled in this repo; **`codium --install-extension id@version`** downloads from the editor’s configured marketplace.
