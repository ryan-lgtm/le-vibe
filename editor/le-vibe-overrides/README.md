# Lé Vibe overrides (placeholder)

**Material product naming, icons, and About copy** follow **`docs/PRODUCT_SPEC.md`** §7.2. This directory is reserved for **Lé Vibe–specific** build inputs that are not part of upstream **VSCodium** (e.g. documented **`product.json`** deltas, icon assets, or patch notes)—see **`docs/vscodium-fork-le-vibe.md`** and **`editor/README.md`**.

Nothing is wired here yet; the **VSCodium** submodule under **`editor/vscodium/`** remains the compile entrypoint.

**Launcher:** after a successful build, point **`LE_VIBE_EDITOR`** at the binary your tree emits — see **[`../README.md`](../README.md)** (*`LE_VIBE_EDITOR`*) and **[`../BUILD.md`](../BUILD.md)**.

**CI (STEP 14 / H6):** the vendoring smoke gate matches **[`.github/workflows/build-le-vibe-ide.yml`](../../.github/workflows/build-le-vibe-ide.yml)** and the manual **[`build-linux.yml`](../../.github/workflows/build-linux.yml)** alias; local parity: **`./editor/smoke.sh`** from the repository root — **[`docs/ci-qa-hardening.md`](../../docs/ci-qa-hardening.md)** (*IDE smoke*). Pre-binary CI uploads **`ide-ci-metadata.txt`** with **`le_vibe_editor_docs=editor/README.md`** (stack **`LE_VIBE_EDITOR`** pointer to **[`../README.md`](../README.md)**); the workflow sets **`upload-artifact`** **`retention-days`** and **`permissions:`** **`contents: read`**, **`actions: write`** — substring-locked by **`test_build_le_vibe_ide_workflow_contract.py`** under **`le-vibe/tests/`**.
