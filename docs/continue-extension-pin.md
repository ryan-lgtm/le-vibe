# Continue extension — Open VSX version pin (Roadmap H4)

Reproducible installs use the Open VSX identifier **`continue.continue`** ([extension page](https://open-vsx.org/extension/Continue/continue)). **`packaging/scripts/install-continue-extension.sh`** passes **`codium --install-extension continue.continue@<version>`** where **`<version>`** comes from **`packaging/continue-openvsx-version`** (one semver per line; comments with **`#`** allowed above the version).

After **`dpkg -i`**, the same pin is installed at **`/usr/share/le-vibe/continue-openvsx-version`**; the script resolves it via **`SCRIPT_DIR/../continue-openvsx-version`** (works for both repo and packaged layouts).

**Product anchor:** [`PRODUCT_SPEC.md`](PRODUCT_SPEC.md) §8–§9. **Roadmap H4** (this doc) is indexed from [`README.md`](README.md) and [`PROMPT_BUILD_LE_VIBE.md`](PROMPT_BUILD_LE_VIBE.md).

**H8 / trust (same repo):** **[`docs/README.md`](README.md)** *Product surface* — **`.github/`** — **`ci.yml`**, **`dependabot.yml`**, **`.github/ISSUE_TEMPLATE/`** + **[`config.yml`](../.github/ISSUE_TEMPLATE/config.yml)** **`#` H8** — plus **[`SECURITY.md`](../SECURITY.md)** *Related docs* (incl. optional [`rag/le-vibe-phase2-chunks.md`](rag/le-vibe-phase2-chunks.md) for *RAG / embeddings*, non-canonical; **`spec-phase2.md`**) and **[`privacy-and-telemetry.md`](privacy-and-telemetry.md)** (*E1 contract tests*).

**`.deb` / `apt`:** The end-to-end steps below match **`/usr/share/doc/le-vibe/README.Debian`** ([`debian/le-vibe.README.Debian`](../debian/le-vibe.README.Debian)) — first-run, **`le-vibe-setup-continue`**, pinned Open VSX install (**§5**/**§8** unchanged).

**Phase 2 scope:** This pin story covers **Continue** on **system VSCodium** (or **`LE_VIBE_EDITOR`**) plus **`le-vibe`** configs — not a **fork-only** IDE binary from **`r-vibe`** alone; see **[`spec-phase2.md`](../spec-phase2.md) §14** (**H6**/**H7**).

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
