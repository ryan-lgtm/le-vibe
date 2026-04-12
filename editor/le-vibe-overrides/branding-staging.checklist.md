# Lé Vibe IDE — branding staging checklist (14.d)

Use this **before** changing **user-visible** IDE identity (name, binary, About, desktop entry, icons inside the Electron tree). **Authority:** [`docs/PRODUCT_SPEC.md`](../../docs/PRODUCT_SPEC.md) **§7.3** (resolved IDE decisions for STEP 14) and **PRODUCT_SPEC §7.2** for anything **outside** §7.3. Do not ship guessed strings that contradict **§7.3** in CI or **`build-env.sh`**.

### PRODUCT_SPEC §7.3 + §7.2 (read before overrides)

- **§7.3** — *Material Lé Vibe IDE (H6 / STEP 14) — **resolved** product decisions* in **[`docs/PRODUCT_SPEC.md`](../../docs/PRODUCT_SPEC.md)** — unified **Lé Vibe** identity, **`lvibe`-only** public CLI, **full** v1 branding, **Debian IDE package**, local-first CI policy.
- **§7.2** — *User gate* — for choices **not** fixed in **§7.3**, halt with **`USER RESPONSE REQUIRED`** (numbered questions).
- **§7.3 (2026-04-12):** **`packaging/scripts/ci-vscodium-linux-dev-build.sh`** merges **`product-branding-merge.json`** into **`editor/vscodium/product.json`**, patches **`dev/build.sh`** so **`APP_NAME`** / **`ORG_NAME`** / … honor the environment, and sources **`build-env.lvibe-defaults.sh`** — **Lé Vibe** short/long names and **`APP_NAME`** for **`!!APP_NAME!!`** patches. Optional gitignored **`build-env.sh`** still layers local overrides (e.g. **`SKIP_ASSETS`**).
- **Honesty:** **`sync-linux-icon-assets.sh`** + **`linuxIconName`** **`le-vibe`** ship the menu/launcher icon path for §7.3; desktop **`Keywords=`** / URL protocol / **`Exec=`** packaging polish may still need maintainer passes — **[`spec-phase2.md`](../../spec-phase2.md) §14** (*Gap*) where relevant; window title / About track **`nameShort`** / merge above.

**Fresh clone (14.b):** **`git submodule update --init editor/vscodium`** from the monorepo root when **`editor/vscodium/`** is empty — **[`../README.md`](../README.md)** *Fresh clone (14.b)* — before **`fetch-vscode-sources.sh`** in *Build / verify order* below.

## Upstream knobs (verify after every `editor/vscodium` submodule bump)

| Layer | Where | Notes |
|-------|--------|--------|
| **Compile-time env** | [`build-env.sh.example`](build-env.sh.example) → optional **`build-env.sh`** (gitignored locally) | Sourced by [`packaging/scripts/ci-vscodium-linux-dev-build.sh`](../../packaging/scripts/ci-vscodium-linux-dev-build.sh) before **`dev/build.sh`**. Commented defaults in the example mirror upstream **VSCodium** — honest baseline until §7.2-approved overrides. |
| **Product metadata** | **`editor/vscodium/product.json`**, generated vscode **`product.json`** under fetched **`vscode/`** | Read map: [`README.md`](README.md) *Upstream touchpoints (14.d)*. Patches belong in maintainer workflow or fork notes — not committed as “done” until applied in the build. |
| **Linux desktop** | **`src/stable/resources/linux/*.desktop`** (paths vary by quality) | Coordinate app id / **`Exec=`** with the Debian **`le-vibe-ide`** package (internal **`codium`** path under **`/usr/lib/le-vibe/`** — not a second public **`PATH`** CLI; **`lvibe`** only per §7.3) — [`docs/vscodium-fork-le-vibe.md`](../../docs/vscodium-fork-le-vibe.md) *Branding & overrides*. |
| **Icons (stack vs IDE)** | [`packaging/icons/`](../../packaging/icons/) → **[`sync-linux-icon-assets.sh`](sync-linux-icon-assets.sh)** → **`editor/vscodium/src/stable/resources/linux/le-vibe.{svg,png}`** (untracked; superproject **`.gitmodules`** **`ignore = untracked`**) | [`docs/brand-assets.md`](../../docs/brand-assets.md); **`product-branding-merge.json`** **`linuxIconName`**. |

## Build / verify order

1. **14.a** — [`../use-node-toolchain.sh`](../use-node-toolchain.sh) (or **`nvm`** from **`editor/`**).
2. **14.b** — [`../fetch-vscode-sources.sh`](../fetch-vscode-sources.sh).
3. **14.c** — [`../verify-14c-local-binary.sh`](../verify-14c-local-binary.sh) (binary present) / [`../print-built-codium-path.sh`](../print-built-codium-path.sh) / [`../smoke-built-codium-lvibe.sh`](../smoke-built-codium-lvibe.sh) with **`LE_VIBE_EDITOR`** after **`dev/build.sh`**.
4. **14.e / 14.f** — optional CI **`linux_compile`** tarball — [`../BUILD.md`](../BUILD.md) *CI* / *Installable layout*.

**E1:** [`test_build_env_example_step14_contract.py`](../../le-vibe/tests/test_build_env_example_step14_contract.py), [`test_editor_le_vibe_overrides_readme_contract.py`](../../le-vibe/tests/test_editor_le_vibe_overrides_readme_contract.py), [`test_vscodium_fork_le_vibe_branding_contract.py`](../../le-vibe/tests/test_vscodium_fork_le_vibe_branding_contract.py).
