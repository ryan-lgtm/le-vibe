# Lé Vibe IDE — Code OSS desktop shell (`editor/`, monorepo)

**Single project, one repository:** the branded **Lé Vibe IDE** is developed under **`editor/`** in this repo alongside **`le-vibe/`** (Python stack). There is **no** separate “fork repository” product requirement—only this monorepo.

**Also read:** [`spec-phase2.md`](../spec-phase2.md) **§14** (what ships vs **H7** Flatpak deferral). Optional alternate bundles (**H7**) — [`flatpak-appimage.md`](flatpak-appimage.md).

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

**Monorepo today:** VSCodium is vendored at **`editor/vscodium/`** (git submodule); Lé Vibe–only layers use **`editor/le-vibe-overrides/`** as above — see **`editor/README.md`** and **`editor/BUILD.md`**.

Upstream VSCodium prepare/build scripts remain the source of truth for **how** to compile; this doc stays a **pointer** and policy shell, not a full upstream mirror.

## CI sketch (monorepo)

Shipped workflows: **[`.github/workflows/build-le-vibe-ide.yml`](../.github/workflows/build-le-vibe-ide.yml)** (`workflow_dispatch`, **`pull_request`** on `editor/**` + related paths, tags `ide-v*`, **`workflow_call`**) and **[`.github/workflows/build-linux.yml`](../.github/workflows/build-linux.yml)** (manual **`build-linux`** alias). Local parity: **[`editor/smoke.sh`](../editor/smoke.sh)** (repo root) or **[`packaging/scripts/ci-editor-gate.sh`](../packaging/scripts/ci-editor-gate.sh)** (orchestrates layout + **`ci-vscodium-bash-syntax.sh`** + **`ci-editor-nvmrc-sync.sh`** when the submodule is present; also invoked from **[`packaging/scripts/ci-smoke.sh`](../packaging/scripts/ci-smoke.sh)**).

Prefer a **dedicated workflow** (e.g. `.github/workflows/build-le-vibe-ide.yml`) that:

1. **Checkout** this repo (optionally with submodules if **`editor/`** uses them).
2. **cd editor/** (or run upstream’s entrypoint from that path).
3. **Cache** Node / compiler deps per upstream docs.
4. **Build** Linux `.deb` / AppImage / artifact and upload as release assets (today **`build-le-vibe-ide`** uploads **metadata** only — `ide-ci-metadata.txt` + pinned **`vscode-upstream-stable.json`** when vendored — as a hook for the real binary drop).
5. **Smoke:** `desktop-file-validate`, launch binary, Continue + managed Ollama **11435** per root **[`README.md`](../README.md)**.

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

- **`LE_VIBE_EDITOR`** — set to the built binary (e.g. `/usr/bin/le-vibe-ide`) for launcher discovery.
- **`~/.config/le-vibe/`** — unchanged; Continue + managed Ollama stay in the Python stack.
- **Debian** — optional future **`debian/`** package for the IDE alone, or bundle; **`Recommends:`** the **`le-vibe`** stack package when both ship together.

## Release checklist (IDE maintainer)

- [ ] Legal: MIT / third-party notices preserved; no “Visual Studio Code” as product name.
- [ ] Version string matches release channel.
- [ ] Smoke: open editor, Continue, one chat to local Ollama on **11435** (see root **`README.md`**).
- [ ] Monorepo: same tag documents **`le-vibe/`** + **`editor/`** state when coordinating drops.

Roadmap references: **G-B3**, **H6** in [`PROMPT_BUILD_LE_VIBE.md`](PROMPT_BUILD_LE_VIBE.md).
