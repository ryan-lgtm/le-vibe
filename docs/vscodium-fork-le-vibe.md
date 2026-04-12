# Lé Vibe IDE — Code OSS desktop shell (`editor/`, monorepo)

**Single project, one repository:** the branded **Lé Vibe IDE** is developed under **`editor/`** in this repo alongside **`le-vibe/`** (Python stack). There is **no** separate “fork repository” product requirement—only this monorepo.

**Also read:** [`spec-phase2.md`](../spec-phase2.md) **§14** (what ships vs **H7** **`packaging/flatpak/`** + **`packaging/appimage/`**). Alternate bundles (**H7**) — [`flatpak-appimage.md`](flatpak-appimage.md) (Flathub-oriented Flatpak).

**Product anchor:** [`PRODUCT_SPEC.md`](PRODUCT_SPEC.md) §7.2 (**`USER RESPONSE REQUIRED`** on material branding/architecture choices), §8–§9.

**H8 baseline:** **[`README.md`](../README.md)** *Product surface* — **`.github/`** (**`ci.yml`**, **`dependabot.yml`**, **`ISSUE_TEMPLATE/`** + **`config.yml`** **`#` H8**), **[`SECURITY.md`](../SECURITY.md)**, **[`privacy-and-telemetry.md`](privacy-and-telemetry.md)** (*E1 contract tests*).

**Bootstrap `.deb` (stack):** [`debian/le-vibe.README.Debian`](../debian/le-vibe.README.Debian) → **`/usr/share/doc/le-vibe/README.Debian`** — install the **`le-vibe`** package for Ollama + `lvibe` + **`.lvibe/`**; wire **`LE_VIBE_EDITOR`** to your **`editor/`** build output when ready.

**Local compile entrypoint (monorepo):** [`editor/BUILD.md`](../editor/BUILD.md) — Node pin, pointer to **`vscodium/docs/howto-build.md`**, overrides, CI.

**E1 (Python / launcher):** **`le-vibe/tests/`** covers launcher and **`LE_VIBE_EDITOR`** wiring. Add **editor-specific** CI and smoke tests under **`editor/`** when the shell sources land (separate job from **`pytest`**).

---

## Why `editor/` lives here

- **One clone** — desktop, scripts, and packaging policy in lockstep.
- **One release train** — tag the monorepo; publish **`le-vibe`** `.deb` + IDE `.deb`/artifact from the same revision when ready.
- **Same governance** — §5 **`.lvibe/`**, §7.2 gates, §8 secrets apply to tooling that touches both trees.

## Layout (inside `editor/` after upstream is vendored)

Exact paths follow the VSCodium / `vscode` tree you import:

| Area | Intent |
|------|--------|
| Application name & id | Desktop `Name=`, Linux `.desktop`, internal app id |
| Icons | `resources/linux`, `hicolor` — align with [`packaging/icons/`](../packaging/icons/) or replace |
| About / credits | “Built on Code - OSS”; Lé Vibe copy; trademark-safe wording |
| Lé Vibe–specific overrides | **[`editor/le-vibe-overrides/`](../editor/le-vibe-overrides/README.md)** — reserved branding/build inputs not shipped by upstream; material choices — **`PRODUCT_SPEC` §7.2** |
| CI | e.g. `.github/workflows/` under repo root or `editor/` — build Linux artifacts on tags |

**Monorepo today:** VSCodium is vendored at **`editor/vscodium/`** (git submodule); Lé Vibe–only layers use **`editor/le-vibe-overrides/`** as above — see **`editor/README.md`**, **`editor/BUILD.md`**, and **[`editor/VENDORING.md`](../editor/VENDORING.md)** (submodule init, **`./editor/smoke.sh`** / CI parity, optional **`linux_compile`** + **`vscodium-linux-build.tar.gz`** — **14.e / 14.f**).

**Fresh clone (14.b):** when **`editor/vscodium/`** is missing or empty after **`git clone`**, run **`git submodule update --init editor/vscodium`** from the repository root — same step as **`editor/README.md`** *Fresh clone (14.b)* before **`get_repo.sh`** / **`fetch-vscode-sources.sh`**.

**Superproject `git status` (§7.3 icons):** **`sync-linux-icon-assets.sh`** writes **`le-vibe.svg`** / **`le-vibe.png`** under **`editor/vscodium/src/stable/resources/linux/`** as **untracked** files. **`.gitmodules`** sets **`ignore = untracked`** for **`editor/vscodium`** so the monorepo root does not show the submodule as modified — **`editor/VENDORING.md`**, **`editor/README.md`**.

Upstream VSCodium prepare/build scripts remain the source of truth for **how** to compile; this doc stays a **pointer** and policy shell, not a full upstream mirror.

## Branding & overrides (**14.d** — **`PRODUCT_SPEC`** §7.2)

**Build-applied identity (§7.3):** **`packaging/scripts/ci-vscodium-linux-dev-build.sh`** merges **`editor/le-vibe-overrides/product-branding-merge.json`**, patches **`dev/build.sh`** so **`APP_NAME`** / **`ORG_NAME`** honor the environment, and sources **`build-env.lvibe-defaults.sh`** before **`dev/build.sh`** — **Lé Vibe** product strings and **`APP_NAME`** for **`!!APP_NAME!!`** substitution in upstream patches. Interim **`LE_VIBE_EDITOR`** → stock **VSCodium** remains valid when you skip a full compile; optional **`build-env.sh`** (from **`build-env.sh.example`**) layers local overrides. **Installable IDE `.deb` (same §7.3):** sibling Debian source **[`packaging/debian-le-vibe-ide/`](../packaging/debian-le-vibe-ide/README.md)** repacks **`VSCode-linux-*`**, ships **`le-vibe.desktop`** + **`hicolor`** icon, and states **roadmap** in-app **Lé Vibe–hosted** updates vs **`apt`** upgrades ([`apt-repo-releases.md`](../apt-repo-releases.md)) — public **`PATH`** CLI remains **`lvibe`** only.

When implementation starts, **material** visible branding (product string, icon set, update channel, bundled extensions) is gated by **`docs/PRODUCT_SPEC.md` §7.2**—use **`USER RESPONSE REQUIRED`** when specs do not uniquely decide. **Staging + notes** live under **[`editor/le-vibe-overrides/README.md`](../editor/le-vibe-overrides/README.md)**; maintainer touchpoint table **[`editor/le-vibe-overrides/branding-staging.checklist.md`](../editor/le-vibe-overrides/branding-staging.checklist.md)** (**14.d**) opens with *PRODUCT_SPEC §7.2 (read before overrides)* — read that before **`build-env.sh.example`** → **`build-env.sh`** or claiming shipped identity; see **Upstream touchpoints (14.d)** in the README for a path map (**`product.json`**, **`src/stable/resources/linux/`** `.desktop` templates, **`vscode/`** after fetch, **`packaging/icons/`**). **Related (not duplicate):** **[`docs/brand-assets.md`](brand-assets.md)** (**H5** / **STEP 11**) covers stack **README / marketing** icons and screenshots; **`14.d`** is the **desktop IDE** identity layer in **`editor/`**—coordinate §1 naming across both. The build pipeline must **not** claim Lé Vibe product completion until those layers are actually applied—keep **`CHANGELOG.md`** and **§14** honesty in sync when behavior changes.

**Monorepo order of operations (before / alongside overrides):** **[`editor/fetch-vscode-sources.sh`](../editor/fetch-vscode-sources.sh)** (fetch **`vscode/`**) → **`editor/vscodium/dev/build.sh`** (optional **[`editor/le-vibe-overrides/build-env.sh`](../editor/le-vibe-overrides/build-env.sh.example)** for upstream env experiments) → confirm **`VSCode-linux-*/bin/codium`** (**[`editor/verify-14c-local-binary.sh`](../editor/verify-14c-local-binary.sh)** — **14.c**, no Ollama) → **`LE_VIBE_EDITOR`** smoke (**[`editor/smoke-built-codium-lvibe.sh`](../editor/smoke-built-codium-lvibe.sh)** from repo root, or **[`editor/print-built-codium-path.sh`](../editor/print-built-codium-path.sh)** + **[`editor/smoke-lvibe-editor.sh`](../editor/smoke-lvibe-editor.sh)**). **14.c** proves launcher ↔ upstream **`codium`** only. **§7.3** visible identity is applied when **`dev/build.sh`** is run **after** **`packaging/scripts/ci-vscodium-linux-dev-build.sh`** (merge **`product-branding-merge.json`**, **`sync-linux-icon-assets.sh`**, **`build-env.lvibe-defaults.sh`**, **`dev/build.sh`** env patch) — same path as optional **`linux_compile`** (**14.e**). Invoking **`dev/build.sh`** alone without that wrapper still yields **VSCodium**-default product strings until you replicate those steps; material choices **outside** **§7.3** remain **§7.2** / **`USER RESPONSE REQUIRED`**. Full detail **[`editor/BUILD.md`](../editor/BUILD.md)** (**14.b–14.c**).

## CI sketch (monorepo)

Shipped workflows: **[`.github/workflows/build-le-vibe-ide.yml`](../.github/workflows/build-le-vibe-ide.yml)** (`workflow_dispatch`, **`pull_request`** on `editor/**` + related paths, tags `ide-v*`, **`workflow_call`**) and **[`.github/workflows/build-linux.yml`](../.github/workflows/build-linux.yml)** (manual **`build-linux`** alias). Local parity: **[`editor/smoke.sh`](../editor/smoke.sh)** (repo root) or **[`packaging/scripts/ci-editor-gate.sh`](../packaging/scripts/ci-editor-gate.sh)** (orchestrates layout + **`ci-vscodium-bash-syntax.sh`** + **`ci-editor-nvmrc-sync.sh`** when the submodule is present; also invoked from **[`packaging/scripts/ci-smoke.sh`](../packaging/scripts/ci-smoke.sh)**). Successful runs append a **GitHub Actions job summary** (**Summary** tab) with the same **`./editor/smoke.sh`** pointer and doc links, plus a **Pre-binary artifact** line echoing **`ide-ci-metadata.txt`**’s **`le_vibe_editor_docs=editor/README.md`** (**`LE_VIBE_EDITOR`** stack pointer to **[`editor/README.md`](../editor/README.md)**); the metadata upload uses **`retention-days`** on **`upload-artifact`** (bounded retention until real binaries ship). The workflow declares **`permissions:`** **`contents: read`**, **`actions: write`** for checkout + artifacts. When the layout gate skips, the summary states why.

Prefer a **dedicated workflow** (e.g. `.github/workflows/build-le-vibe-ide.yml`) that:

1. **Checkout** this repo (optionally with submodules if **`editor/`** uses them).
2. **cd editor/** (or run upstream’s entrypoint from that path).
3. **Cache** Node / compiler deps per upstream docs (the shipped workflow caches **`~/.cargo`** on **`linux_compile`** — see **[`build-le-vibe-ide.yml`](../.github/workflows/build-le-vibe-ide.yml)**).
4. **Default `linux` job:** layout gate + smoke (**`ci-vscodium-bash-syntax.sh`**, **`ci-editor-nvmrc-sync.sh`**) — uploads **pre-binary** **`ide-ci-metadata.txt`** (**`le_vibe_editor_docs=editor/README.md`**) + **`vscode-upstream-stable.json`** when vendored (**`upload-artifact`** **`retention-days`**). **`pull_request`** uses this path only — **no** full upstream compile.
5. **Optional `linux_compile` job (14.e):** **`workflow_dispatch`** **`vscodium_linux_compile`**, **`workflow_call`** (e.g. **`build-linux.yml`** **`with:`**), or **`ide-v*`** tag push — **`ci-vscodium-bash-syntax.sh`** + **`ci-editor-nvmrc-sync.sh`** first (fail fast — same gates as **`ci-editor-gate`**), then **`packaging/scripts/ci-vscodium-linux-dev-build.sh`** → **`editor/vscodium/dev/build.sh`**; uploads **`vscodium-linux-build.tar.gz`** when **`VSCode-linux-*`** exists (**`upload-artifact`** **`retention-days: 14`** on that tarball). GitHub’s artifact UI wraps downloads in a **`.zip`** around that file (**14.f**). That compile path applies **§7.3** (merged **`product.json`**, Linux icon sync, **`APP_NAME`/`ORG_NAME`** defaults) before the Electron build; the on-disk binary name may remain **`codium`** while the **built shell** shows **Lé Vibe** — **`spec-phase2.md` §14** / **H6** honesty. Default **`linux`** (PR) jobs do **not** run this compile.
6. **Smoke / QA:** parity with **`./editor/smoke.sh`**; optional post-build checks (`desktop-file-validate`, **`LE_VIBE_EDITOR`** **`--version`** via **`./editor/smoke-lvibe-editor.sh`** with **`ollama`**) — root **[`README.md`](../README.md)** (managed Ollama **11435**).

Keep signing tokens in GitHub Environments.

Example shape (adapt paths when **`editor/`** is populated):

```yaml
# .github/workflows/build-le-vibe-ide.yml  (monorepo root)
on:
  workflow_dispatch:
  push:
    tags: ["ide-v*"]

jobs:
  linux:
    runs-on: ubuntu-latest
    timeout-minutes: 120
    steps:
      - uses: actions/checkout@v4
      # with: submodules: true   # if editor/ uses submodules
      # run upstream prepare + build from editor/
```

## Wiring the IDE build to the Lé Vibe stack

- **`LE_VIBE_EDITOR`** — set to the built binary, or rely on **`/usr/lib/le-vibe/bin/codium`** when the **`le-vibe-ide`** **`.deb`** is installed (**`packaging/debian-le-vibe-ide/`** — **PRODUCT_SPEC** §7.3).
- **Tarball / installable tree (14.f)** — **`VSCode-linux-<arch>/bin/codium`** from a local or CI build, **`vscodium-linux-build.tar.gz`** from **`linux_compile`**, vs upstream **`VSCodium-linux-*.tar.gz`** — see **[`editor/BUILD.md`](../editor/BUILD.md)** *Installable layout — tarball + `codium` path*; **IDE `.deb`** — **`editor/BUILD.md`** *Debian package for the Lé Vibe IDE*.
- **Default editor when the IDE package is installed (14.g)** — launcher order matches **`le_vibe.launcher._default_editor`** (E1 **`le-vibe/tests/test_launcher_default_editor.py`**): **`/usr/lib/le-vibe/bin/codium`** before **`/usr/bin/codium`**. **`le-vibe`** **`Suggests: le-vibe-ide`** — **[`editor/BUILD.md`](../editor/BUILD.md)** *Default `LE_VIBE_EDITOR`*; **`debian/le-vibe.README.Debian`**; **[`editor/README.md`](../editor/README.md)** (*Persisting `LE_VIBE_EDITOR`*).
- **`~/.config/le-vibe/`** — unchanged; Continue + managed Ollama stay in the Python stack.
- **Debian** — optional future **`debian/`** package for the IDE alone, or bundle; **`Recommends:`** the **`le-vibe`** stack package when both ship together.

## Release checklist (IDE maintainer)

- [ ] Legal: MIT / third-party notices preserved; no “Visual Studio Code” as product name.
- [ ] Version string matches release channel.
- [ ] Smoke: open editor, Continue, one chat to local Ollama on **11435** (see root **`README.md`**).
- [ ] Monorepo: same tag documents **`le-vibe/`** + **`editor/`** state when coordinating drops.

### Release smoke checklist (14.i)

Use this **before** tagging or publishing IDE-related artifacts; it complements the short list above and **[`editor/BUILD.md`](../editor/BUILD.md)** (**14.f–14.h**). Order is **1 → 9** for a full maintainer pass; skip **5** when you only validate pre-binary gates + docs. **PM / queue:** **[`docs/PM_STAGE_MAP.md`](../docs/PM_STAGE_MAP.md)** STEP **14** *Also read* (**`build-le-vibe-ide.yml`**, **`14.g`**, related E1) and STEP **10** (**H3** QA CI — **`test_docs_readme_ci_qa_hardening_row_contract.py`**, **14.e / 14.f** per row **1c** below) — open when this checklist or **`spec-phase2.md` §14** *Honesty vs CI* changes.

| Step | Command / artifact | Pass criteria |
|------|---------------------|---------------|
| **1. Layout + toolchain gate** | From repo root: **`./editor/smoke.sh`** | **`ci-editor-gate`** reports **`layout=vscodium`** (or your supported layout); **`bash -n`** on upstream scripts + monorepo helpers (**`use-node-toolchain.sh`**, **`fetch-vscode-sources.sh`**, **`print-built-codium-path.sh`**, **`verify-14c-local-binary.sh`**, **`print-vsbuild-codium-path.sh`**, **`print-ci-tarball-codium-path.sh`**, **`smoke-built-codium-lvibe.sh`**, **`ci-vscodium-linux-dev-build.sh`**) OK; **`editor/.nvmrc`** matches **`editor/vscodium/.nvmrc`**. |
| **1b. Compile hook + branding staging (14.d / H6 honesty)** | **`editor/le-vibe-overrides/build-env.sh.example`** — E1 **`test_build_env_example_step14_contract.py`**; touchpoint map **`editor/le-vibe-overrides/branding-staging.checklist.md`** — E1 **`test_branding_staging_checklist_14d_contract`** | **`build-env.sh.example`** still lists **`dev/build.sh`** env surface + **§7.2** / **`USER RESPONSE REQUIRED`** for visible renames; **`branding-staging.checklist.md`** maps **`product.json`** / desktop / icons before claiming shipped Lé Vibe identity. Default CI/local compiles stay **VSCodium-named** until **`build-env.sh`** (gitignored copy) exports Lé Vibe–approved identity. |
| **1c. Docs index (H3 / STEP 10 — 14.e / 14.f)** | E1 **`test_docs_readme_ci_qa_hardening_row_contract.py`** — **[`docs/README.md`](../docs/README.md)** *Roadmap H* **`ci-qa-hardening.md`** row | Matches **`docs/ci-qa-hardening.md`** *IDE smoke*: fast **`./editor/smoke.sh`** vs optional **`linux_compile`** / **`vscodium-linux-build.tar.gz`** (see **[`docs/PM_STAGE_MAP.md`](../docs/PM_STAGE_MAP.md)** STEP **10** *Also read*). |
| **2. Python E1** | **`cd le-vibe && python3 -m pytest tests/`** | Green — locks launcher, workflows, pin docs. |
| **3. Continue pin (H4)** | **`./packaging/scripts/verify-continue-pin.sh`** | Semver line in **`packaging/continue-openvsx-version`**. |
| **4. Stack `.deb` (when packaging changed)** | **`dpkg-buildpackage -us -uc -b`** from repo root | **`le-vibe`** package builds; see **`debian/changelog`**. |
| **5. Optional full IDE compile** | **`build-le-vibe-ide`**: **`workflow_dispatch`** **`vscodium_linux_compile`**, tag **`ide-v*`**, or **`build-linux.yml`** **`workflow_dispatch`** with the same flag (**`workflow_call`** **`inputs`** → **`linux_compile`**) — job runs **`ci-vscodium-bash-syntax.sh`** + **`ci-editor-nvmrc-sync.sh`** before **`ci-vscodium-linux-dev-build.sh`**; that wrapper also requires active **`node`** = **`editor/.nvmrc`** before **`dev/build.sh`** (**[`editor/BUILD.md`](../editor/BUILD.md)** *Compile wrapper vs Node*, **`LEVIBE_SKIP_NODE_VERSION_CHECK`**) | Job **`linux_compile`** finishes; artifact **`vscodium-linux-build.tar.gz`** present when **`VSCode-linux-*`** was produced — may fail on undersized runners (**[`editor/BUILD.md`](../editor/BUILD.md)** *CI*, **14.e**). |
| **6. Launcher ↔ binary** | **`LE_VIBE_EDITOR=<path/to/codium> ./editor/smoke-lvibe-editor.sh`**, or after a local build **`./editor/smoke-built-codium-lvibe.sh`** (or **`LE_VIBE_EDITOR="$(./editor/print-built-codium-path.sh)" ./editor/smoke-lvibe-editor.sh`**) | Optional preflight (local **`editor/vscodium/`** tree only, no Ollama): **`./editor/verify-14c-local-binary.sh`** (**14.c**) before **`smoke-*`**. **`smoke-lvibe-editor`** / **`smoke-built-codium-lvibe`** need **`ollama`** on **`PATH`**; editor prints **`--version`** and exits. For **`vscodium-linux-build.tar.gz`**, **`LE_VIBE_EDITOR="$(./editor/print-ci-tarball-codium-path.sh …)"`** or unpack and **`./editor/print-vsbuild-codium-path.sh`** (**14.f**). If the tarball came from **GitHub Actions**, the download is a **`.zip`** around that file — unzip first, then pass the **`.tar.gz`** to the helper (passing the outer **`.zip`** to **`print-ci-tarball-codium-path.sh`** fails with exit code **`2`** and **unzip first** — **14.f**, E1 **`test_print_paths_14f_contract.py`**). |
| **7. Product path** | First-run **`lvibe`**, then **`le-vibe-setup-continue`** | **`~/.config/le-vibe/continue-config.yaml`**; pinned Continue per **`docs/continue-extension-pin.md`** (**14.h**). |
| **8. End-to-end agent** | Open workspace, Continue chat to **managed Ollama** **11435** | Matches root **`README.md`** QA expectations. |
| **9. §14 honesty gate (14.j prep)** | After IDE-doc / §14 table edits: **`cd le-vibe && python3 -m pytest tests/test_spec_phase2_section14_snapshot_contract.py`** | **`spec-phase2.md` §14** IDE row + *Honesty vs CI* stay aligned with root **`CHANGELOG.md`** **[Unreleased]** — same discipline as **STEP 14.j** (full suite still **`pytest tests/`**). |

Roadmap references: **G-B3**, **H6** in [`PROMPT_BUILD_LE_VIBE.md`](PROMPT_BUILD_LE_VIBE.md).
