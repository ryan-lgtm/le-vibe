# Lé Vibe overrides

**Fine-grain STEP 14.d:** policy and cross-links live in **`docs/vscodium-fork-le-vibe.md`** (*Branding & overrides*). **§7.3** fixes material IDE naming for v1 — **`product-branding-merge.json`**, **`build-env.lvibe-defaults.sh`**, **`sync-linux-icon-assets.sh`**, and **`ci-vscodium-linux-dev-build.sh`** apply **Lé Vibe** name + Linux icon wiring on every full compile path; deeper desktop/About polish still tracks **`branding-staging.checklist.md`**. Choices **outside** §7.3 follow **`docs/PRODUCT_SPEC.md`** §7.2 — **halt** with **`USER RESPONSE REQUIRED`** when specs do not decide.

**Master orchestrator order:** **0 → 1 → 14 → 2–13 → 15–17** — branding work here serves **STEP 14** immediately after baseline **STEP 0–1**, not as a backlog tail. See **`docs/PROMPT_BUILD_LE_VIBE.md`** (*ORDERED WORK QUEUE*, *Rolling iteration — prefer continuation*) and **`docs/PM_STAGE_MAP.md`** *Execution order* / **STEP 16** (same pointer as **`editor/README.md`** *Master orchestrator order*).

This directory is reserved for **Lé Vibe–only** inputs that upstream **VSCodium** does not ship: documented deltas against **`editor/vscodium/product.json`**, Linux **`.desktop`** / app-id notes, **Electron / desktop** icon targets under upstream **`resources/linux`** / **`hicolor`** (coordinate with **`packaging/icons/`** when reusing stack art), and maintainer patch notes—policy shell in **`docs/vscodium-fork-le-vibe.md`**.

**Do not confuse with Roadmap H5:** **[`docs/brand-assets.md`](../../docs/brand-assets.md)** (**`PM_STAGE_MAP.md` STEP 11**) and **[`docs/screenshots/README.md`](../../docs/screenshots/README.md)** own **README / store / `.deb`** icon + screenshot handoff; **`14.d`** here is the **IDE binary** shell (Code OSS + desktop file + app metadata), still gated by **`PRODUCT_SPEC` §7.2** for anything user-visible.

**Release bundles (H1 vs §7.3):** Default **`ci.yml`** artifact **`le-vibe-deb`** is **stack-only**; the sibling **`le-vibe-ide_*_amd64.deb`** repacks the **`VSCode-linux-*`** tree you brand here — **[`docs/apt-repo-releases.md`](../../docs/apt-repo-releases.md)** (*IDE package*); **[`docs/PM_STAGE_MAP.md`](../../docs/PM_STAGE_MAP.md)** (*H1 vs §7.3 .deb bundles*); **[`docs/PRODUCT_SPEC.md`](../../docs/PRODUCT_SPEC.md)** § *Prioritization* — **Release bundles (H1 / STEP 8 vs STEP 14 / §7.3)**.

**Packaged full product (`--with-ide`):** From the repository root, **`./packaging/scripts/build-le-vibe-debs.sh --with-ide`** builds the stack **`le-vibe`** **`.deb`** and **`le-vibe-ide_*_amd64.deb`** when **`VSCode-linux-*`** exists, then prints **Full-product install** on success — **[`docs/PM_DEB_BUILD_ITERATION.md`](../../docs/PM_DEB_BUILD_ITERATION.md)** (*Success output (`--with-ide`)*); install both **`.deb`** files — **[`packaging/debian-le-vibe-ide/README.md`](../../packaging/debian-le-vibe-ide/README.md)** (*Install both packages*).

**Staging checklist:** **[`branding-staging.checklist.md`](branding-staging.checklist.md)** — upstream **`product.json`** / desktop / icon touchpoints and **§7.2** gate in one place (**14.d**). Read the checklist section **PRODUCT_SPEC §7.2 (read before overrides)** first; it restates **`docs/PRODUCT_SPEC.md`** §7.2 (*User gate*) and **`spec-phase2.md` §14** honesty—do not treat **`build-env.sh.example`** → **`build-env.sh`** exports or committed patch notes as shipped Lé Vibe identity until that gate is satisfied.

**Fresh clone (14.b):** **`editor/vscodium/`** must exist before **14.a** / **`fetch-vscode-sources.sh`** — run **`git submodule update --init editor/vscodium`** from the monorepo root when the tree is empty — **[`../README.md`](../README.md)** *Fresh clone (14.b)*.

## Build flow vs branding layers (14.d)

Use this order so **overrides** stay tied to a reproducible tree (**§7.3** applies **`product-branding-merge.json`**, **`build-env.lvibe-defaults.sh`**, and a **`dev/build.sh`** patch via **`ci-vscodium-linux-dev-build.sh`**; upstream binary name stays **`codium`**):

1. **Toolchain + fetch vscode:** activate Node (**14.a**) — **`source ../use-node-toolchain.sh`** from repo root (or manual **`nvm`** from **`editor/`**). Then from repo root, **[`../fetch-vscode-sources.sh`](../fetch-vscode-sources.sh)** (**14.b**) — creates **`editor/vscodium/vscode/`**.
2. **Compile:** from repo root, **`packaging/scripts/ci-vscodium-linux-dev-build.sh`** → **`editor/vscodium/dev/build.sh`** — see **[`../BUILD.md`](../BUILD.md)** (or run **`dev/build.sh`** directly only if you accept **VSCodium** defaults). Optional **[`build-env.sh`](build-env.sh.example)** (copy from **`build-env.sh.example`**) layers local exports **after** **`build-env.lvibe-defaults.sh`**.
3. **Verify launcher ↔ binary (14.c):** **[`../verify-14c-local-binary.sh`](../verify-14c-local-binary.sh)** (built **`codium`** present, no Ollama) — then **[`../smoke-built-codium-lvibe.sh`](../smoke-built-codium-lvibe.sh)** from repo root after **`dev/build.sh`**, or **[`../print-built-codium-path.sh`](../print-built-codium-path.sh)** then **[`../smoke-lvibe-editor.sh`](../smoke-lvibe-editor.sh)** with **`LE_VIBE_EDITOR`**.

**What “Lé Vibe branding” means here:** committed **`product.json`** merge inputs, icon sync, and CI/local compile hooks under this directory — **§7.3** applies on **`ci-vscodium-linux-dev-build.sh`** runs; optional **`build-env.sh`** layers experiments **after** **`build-env.lvibe-defaults.sh`**. **`docs/vscodium-fork-le-vibe.md`** (*Branding & overrides*) is the policy shell.

## Upstream touchpoints (14.d)

Use this as a **read map** before editing upstream or recording patch notes—paths are under **`editor/vscodium/`** unless noted. Upstream moves files between releases; re-verify after a submodule bump. **§7.3** v1 identity ships via the **merge + env + icon sync** pipeline (not hand-edited committed **`product.json`** in **`vscodium/`**); material changes **beyond** §7.3 still follow **§7.2**.

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
| **Optional compile env (CI + local full build)** | Copy **`build-env.sh.example`** → **`build-env.sh`** (gitignored locally if you prefer). **`packaging/scripts/ci-vscodium-linux-dev-build.sh`** sources it before **`dev/build.sh`** so you can export upstream **`APP_NAME`**, **`BINARY_NAME`**, etc. Material identity changes follow **`PRODUCT_SPEC` §7.2**. **E1:** **[`../../le-vibe/tests/test_build_env_example_step14_contract.py`](../../le-vibe/tests/test_build_env_example_step14_contract.py)** locks the example file vs **H6** honesty. |

**CI:** optional job **`linux_compile`** runs **`ci-vscodium-bash-syntax.sh`** + **`ci-editor-nvmrc-sync.sh`** before **`ci-vscodium-linux-dev-build.sh`** → **`dev/build.sh`** (fail fast — **`../BUILD.md`** *CI*; **`ci-vscodium-linux-dev-build.sh`** enforces **`node --version`** vs **`editor/.nvmrc`** — **14.a** / **14.e**; **`LEVIBE_SKIP_NODE_VERSION_CHECK`**). Without **`build-env.sh`**, upstream **`dev/build.sh`** defaults apply. Pre-binary PR metadata and **`./editor/smoke.sh`** are unchanged.

**Launcher:** after a successful build, point **`LE_VIBE_EDITOR`** at the binary your tree emits — see **[`../README.md`](../README.md)** (*`LE_VIBE_EDITOR`*) and **[`../BUILD.md`](../BUILD.md)**.

**CI (STEP 14 / H6):** the vendoring smoke gate matches **[`.github/workflows/build-le-vibe-ide.yml`](../../.github/workflows/build-le-vibe-ide.yml)** and the manual **[`build-linux.yml`](../../.github/workflows/build-linux.yml)** alias; local parity: **`./editor/smoke.sh`** from the repository root — **[`docs/ci-qa-hardening.md`](../../docs/ci-qa-hardening.md)** (*IDE smoke*). Pre-binary CI uploads **`ide-ci-metadata.txt`** with **`le_vibe_editor_docs=editor/README.md`** (stack **`LE_VIBE_EDITOR`** pointer to **[`../README.md`](../README.md)**); the workflow sets **`upload-artifact`** **`retention-days`** and **`permissions:`** **`contents: read`**, **`actions: write`** — substring-locked by **`test_build_le_vibe_ide_workflow_contract.py`** under **`le-vibe/tests/`**. Optional job **`linux_compile`** uses the same fail-fast scripts and **`ci-vscodium-linux-dev-build.sh`** **`node --version`** vs **`editor/.nvmrc`** check (**`LEVIBE_SKIP_NODE_VERSION_CHECK`**) as **`../BUILD.md`** *CI* before **`dev/build.sh`**, then may upload **`vscodium-linux-build.tar.gz`** when opt-in (**14.e / 14.f** — see **[`../BUILD.md`](../BUILD.md)** *CI*).
