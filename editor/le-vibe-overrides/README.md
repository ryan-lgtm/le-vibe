# Lé Vibe overrides (placeholder)

**Fine-grain STEP 14.d:** policy and cross-links live in **`docs/vscodium-fork-le-vibe.md`** (*Branding & overrides*). **Material product naming, icons, desktop id, and About copy** follow **`docs/PRODUCT_SPEC.md`** §7.2. If the orchestrator cannot pick a safe default from the specs, **halt** and print **`USER RESPONSE REQUIRED`** (numbered questions)—do not guess Lé Vibe–visible branding.

This directory is reserved for **Lé Vibe–only** inputs that upstream **VSCodium** does not ship: documented deltas against **`editor/vscodium/product.json`**, Linux **`.desktop`** / app-id notes, icon sources aligned with **[`packaging/icons/`](../../packaging/icons/)**, and maintainer patch notes—policy shell in **`docs/vscodium-fork-le-vibe.md`**.

## Build flow vs branding layers (14.d)

Use this order so **overrides** stay tied to a reproducible tree (upstream defaults remain **VSCodium** / **`codium`** until patches and **`build-env.sh`** exports intentionally change visible identity — **§7.2**):

1. **Toolchain + fetch vscode:** activate Node (**14.a**) — **`source ../use-node-toolchain.sh`** from repo root (or manual **`nvm`** from **`editor/`**). Then from repo root, **[`../fetch-vscode-sources.sh`](../fetch-vscode-sources.sh)** (**14.b**) — creates **`editor/vscodium/vscode/`**.
2. **Compile:** **`cd editor/vscodium && ./dev/build.sh`** — see **[`../BUILD.md`](../BUILD.md)**. Optional **[`build-env.sh`](build-env.sh.example)** (copy from **`build-env.sh.example`**) is sourced by **[`../../packaging/scripts/ci-vscodium-linux-dev-build.sh`](../../packaging/scripts/ci-vscodium-linux-dev-build.sh)** before **`dev/build.sh`** in CI and for local full builds; use for upstream **`APP_NAME`**, **`BINARY_NAME`**, etc. only when **§7.2** allows.
3. **Verify launcher ↔ binary (14.c):** **[`../smoke-built-codium-lvibe.sh`](../smoke-built-codium-lvibe.sh)** from repo root after **`dev/build.sh`**, or **[`../print-built-codium-path.sh`](../print-built-codium-path.sh)** then **[`../smoke-lvibe-editor.sh`](../smoke-lvibe-editor.sh)** with **`LE_VIBE_EDITOR`**.

**What “Lé Vibe branding” means here:** staged **`product.json`** diffs, icons, desktop metadata, and patch notes under this directory—**not** automatic renames until maintainers apply them. **`docs/vscodium-fork-le-vibe.md`** (*Branding & overrides*) is the policy shell.

## Upstream touchpoints (14.d)

Use this as a **read map** before editing upstream or recording patch notes—paths are under **`editor/vscodium/`** unless noted. Upstream moves files between releases; re-verify after a submodule bump. **Do not** commit modified **`product.json`** / desktop templates here as “done branding” until **`build-env.sh`** or forked upstream steps apply them (**§7.2**).

| Area | Where to look |
|------|----------------|
| **Prepare / build entrypoints** | **`product.json`**, **`prepare_src.sh`**, **`prepare_vscode.sh`**, **`dev/build.sh`**, **`build.sh`** — see **`docs/howto-build.md`** |
| **Linux `.desktop` templates** | e.g. **`src/stable/resources/linux/code.desktop`**, **`code-url-handler.desktop`** (Insider vs stable under **`src/insider/`**) |
| **Fetched vscode tree** | After **`fetch-vscode-sources.sh`**, **`editor/vscodium/vscode/`** — merged **Code - OSS** product metadata used at compile time |
| **Icons vs stack** | Ship art in **[`packaging/icons/`](../../packaging/icons/)**; install targets follow upstream **`resources/linux`** / **`hicolor`** layout — **`docs/vscodium-fork-le-vibe.md`** (*Branding & overrides*) |

## What to stage here (checklist)

| Concern | Notes |
|--------|--------|
| **Product / application name** | VSCodium uses **`product.json`** + generated vscode **`product.json`**; Lé Vibe user-visible name stays **Lé Vibe** (é)—see **`PRODUCT_SPEC`**. |
| **Icons** | Prefer exports under **`packaging/icons/`**; install paths under upstream **`resources/linux`** / **`hicolor`** follow **`docs/vscodium-fork-le-vibe.md`**. |
| **About / credits** | “Built on Code - OSS”; no “Visual Studio Code” as the product name—see fork doc release checklist. |
| **Optional compile env (CI + local full build)** | Copy **`build-env.sh.example`** → **`build-env.sh`** (gitignored locally if you prefer). **`packaging/scripts/ci-vscodium-linux-dev-build.sh`** sources it before **`dev/build.sh`** so you can export upstream **`APP_NAME`**, **`BINARY_NAME`**, etc. Material identity changes follow **`PRODUCT_SPEC` §7.2**. |

**CI:** optional **`linux_compile`** still runs upstream **`dev/build.sh`**; without **`build-env.sh`** the defaults from that script apply. Pre-binary PR metadata and **`./editor/smoke.sh`** are unchanged.

**Launcher:** after a successful build, point **`LE_VIBE_EDITOR`** at the binary your tree emits — see **[`../README.md`](../README.md)** (*`LE_VIBE_EDITOR`*) and **[`../BUILD.md`](../BUILD.md)**.

**CI (STEP 14 / H6):** the vendoring smoke gate matches **[`.github/workflows/build-le-vibe-ide.yml`](../../.github/workflows/build-le-vibe-ide.yml)** and the manual **[`build-linux.yml`](../../.github/workflows/build-linux.yml)** alias; local parity: **`./editor/smoke.sh`** from the repository root — **[`docs/ci-qa-hardening.md`](../../docs/ci-qa-hardening.md)** (*IDE smoke*). Pre-binary CI uploads **`ide-ci-metadata.txt`** with **`le_vibe_editor_docs=editor/README.md`** (stack **`LE_VIBE_EDITOR`** pointer to **[`../README.md`](../README.md)**); the workflow sets **`upload-artifact`** **`retention-days`** and **`permissions:`** **`contents: read`**, **`actions: write`** — substring-locked by **`test_build_le_vibe_ide_workflow_contract.py`** under **`le-vibe/tests/`**.
