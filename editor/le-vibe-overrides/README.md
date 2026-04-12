# Lé Vibe overrides (placeholder)

**Material product naming, icons, desktop id, and About copy** follow **`docs/PRODUCT_SPEC.md`** §7.2. If the orchestrator cannot pick a safe default from the specs, **halt** and print **`USER RESPONSE REQUIRED`** (numbered questions)—do not guess Lé Vibe–visible branding.

This directory is reserved for **Lé Vibe–only** inputs that upstream **VSCodium** does not ship: documented deltas against **`editor/vscodium/product.json`**, Linux **`.desktop`** / app-id notes, icon sources aligned with **[`packaging/icons/`](../../packaging/icons/)**, and maintainer patch notes—policy shell in **`docs/vscodium-fork-le-vibe.md`**.

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
