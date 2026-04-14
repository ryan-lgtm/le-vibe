# Full local install (one command)

**Goal:** From a Linux checkout, build the Lé Vibe stack + branded IDE **`.deb`** packages from source, optionally install them locally, and verify the result — **without** an apt repository or external release CDN.

**Canonical entrypoint:** [`packaging/scripts/install-le-vibe-local.sh`](../packaging/scripts/install-le-vibe-local.sh)

| Step | Command |
|------|---------|
| **Preflight only** (deps, disk/RAM hints, VSCode-linux milestone — no compile) | `./packaging/scripts/install-le-vibe-local.sh --preflight-only` |
| **Build `.deb` artifacts** (compile if needed, then package) | `./packaging/scripts/install-le-vibe-local.sh` |
| **Build + non-interactive `sudo apt install` + post-install smoke** | `./packaging/scripts/install-le-vibe-local.sh --install --yes` |

Fresh clone: initialize the editor submodule first — `git submodule update --init editor/vscodium` (**14.b** — [`editor/README.md`](../editor/README.md)).

**Authority:** [`PM_DEB_BUILD_ITERATION.md`](PM_DEB_BUILD_ITERATION.md), [`editor/BUILD.md`](../editor/BUILD.md), STEP **14** close-out — [`verify-step14-closeout.sh`](../packaging/scripts/verify-step14-closeout.sh).

---

## Honest expectations

| Topic | What to expect |
|-------|----------------|
| **Wall time** | Full **`dev/build.sh`** (Electron / VSCodium) is often **1–4+ hours** on a strong workstation; CI-sized runners may OOM or timeout. |
| **Disk** | The **`editor/vscodium/`** tree commonly needs **tens of GB** during compile; keep **≥ ~25 GB** free when possible. |
| **RAM** | Low-RAM hosts may hit **OOM** during `npm` / link steps; add swap or use [`docker-le-vibe-vscodium-linux-compile.sh`](../packaging/scripts/docker-le-vibe-vscodium-linux-compile.sh). |
| **Resume** | If **`VSCode-linux-*/bin/codium`** already exists, the installer **skips** recompiling unless **`--force-editor-build`**. |

---

## Troubleshooting

### Missing host packages (before compile)

- Run **`./packaging/scripts/install-linux-vscodium-build-deps.sh`** (same list as [`linux-vscodium-ci-apt.pkgs`](../packaging/linux-vscodium-ci-apt.pkgs)).
- Print-only: **`./packaging/scripts/install-linux-vscodium-build-deps.sh --print-install-command`**
- Override (risky): **`LEVIBE_SKIP_HOST_DEPS_CHECK=1`** — see [`editor/BUILD.md`](../editor/BUILD.md) **14.e**.

### Node vs `editor/.nvmrc`

- Active Node must match **`editor/.nvmrc`** for **`ci-vscodium-linux-dev-build.sh`**, unless **`LEVIBE_SKIP_NODE_VERSION_CHECK=1`**.
- Helper: **`source editor/use-node-toolchain.sh`**

### Partial **`VSCode-linux-*`** tree (no `bin/codium`)

- Finish **`./packaging/scripts/ci-vscodium-linux-dev-build.sh`** or see **Partial tree** in [`editor/BUILD.md`](../editor/BUILD.md).
- CI tarball path: **`packaging/scripts/install-vscodium-linux-tarball-to-editor-vendor.sh`**

### `sudo` / apt boundaries

- **`--install`** needs **`sudo`** and **`apt-get`** on PATH.
- Build steps do not require root until install.

### STEP 14 verification fails

- Run **`./packaging/scripts/preflight-step14-closeout.sh --require-stack-deb`** for a gap list, then **`./packaging/scripts/verify-step14-closeout.sh --require-stack-deb`**.

---

## Matrix (maintainer environments)

Documented proof targets for the **one-shot** path (script + gates; full compile may be run only on hosts with enough time/disk):

| Environment | Role |
|---------------|------|
| **Ubuntu LTS (e.g. 22.04/24.04) — developer workstation** | Primary: native compile + **`verify-step14-closeout.sh --require-stack-deb`**. |
| **Debian stable / second Ubuntu LTS — Docker or VM** | Secondary: same repo mounted; install [`linux-vscodium-ci-apt.pkgs`](../packaging/linux-vscodium-ci-apt.pkgs) via **`install-linux-vscodium-build-deps.sh`**, then **`install-le-vibe-local.sh --preflight-only`** and contract tests. Full **`dev/build.sh`** in Docker is optional and resource-heavy — see [`docker-le-vibe-vscodium-linux-compile.sh`](../packaging/scripts/docker-le-vibe-vscodium-linux-compile.sh). |

See [`SHIP_REPORT_LOCAL_INSTALL.md`](SHIP_REPORT_LOCAL_INSTALL.md) for the latest recorded matrix results.
