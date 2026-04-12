# Building the Lé Vibe IDE (local)

Compile steps are owned by **VSCodium** upstream. In this monorepo:

1. **Toolchain:** **[`.nvmrc`](.nvmrc)** — run **`nvm install` / `nvm use`** from **`editor/`** (matches **`vscodium/.nvmrc`**; see **[`README.md`](README.md)**).
2. **Upstream how-to:** **`vscodium/docs/howto-build.md`** inside the submodule — vscode sources are fetched with **`get_repo.sh`** (and friends) before **`build.sh`**; follow that file, not a duplicate guide here.
3. **Lé Vibe–specific layers:** **[`le-vibe-overrides/README.md`](le-vibe-overrides/README.md)**, **[`../docs/vscodium-fork-le-vibe.md`](../docs/vscodium-fork-le-vibe.md)**, **[`../docs/PRODUCT_SPEC.md`](../docs/PRODUCT_SPEC.md)** §7.2 where branding choices are material.

**CI (smoke only, no full compile yet):** [`.github/workflows/build-le-vibe-ide.yml`](../.github/workflows/build-le-vibe-ide.yml) — see **[`README.md`](README.md)**.
