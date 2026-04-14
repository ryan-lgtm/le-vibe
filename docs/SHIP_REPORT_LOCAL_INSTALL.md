# Ship report — comfortable one-shot local install (editor + stack)

**Date:** 2026-04-13  
**Scope:** Canonical bash installer, preflight UX, documentation, contract tests, STEP **14** gates — **no** apt repo hosting.

---

## Canonical commands

| Action | Command |
|--------|---------|
| Preflight (check-only) | `./packaging/scripts/install-le-vibe-local.sh --preflight-only` |
| Full build (artifacts; no `sudo` unless `--install`) | `./packaging/scripts/install-le-vibe-local.sh` |
| Full build + install + smoke | `./packaging/scripts/install-le-vibe-local.sh --install --yes` |
| STEP **14** close-out (maintainer) | `./packaging/scripts/verify-step14-closeout.sh --require-stack-deb` |

---

## Matrix results

| Host | What we ran | Result |
|------|-------------|--------|
| **A — Native Linux (workspace)** | `bash -n install-le-vibe-local.sh`; `pytest tests/test_install_le_vibe_local_script_contract.py`; `./packaging/scripts/verify-step14-closeout.sh --require-stack-deb`; `./packaging/scripts/install-le-vibe-local.sh --preflight-only` | **Pass** — verifier OK; preflight exit **0** (deps check warned while `vscode_linux_build` already **ready**). |
| **B — Docker `ubuntu:22.04`** (bind-mount repo) | `apt-get install` minimal toolchain + `install-linux-vscodium-build-deps.sh` (root); `bash -n`; `pytest tests/test_install_le_vibe_local_script_contract.py`; `install-le-vibe-local.sh --preflight-only` | **Pass** (2026-04-13: ~66s wall after image warm; **10** installer contract tests; preflight exit **0**; VSCode probe may show `unknown` in minimal containers without Node on `PATH` — deps check still runs). |

**Docker proof (template):**

```bash
docker run --rm -v "$(pwd)":/r -w /r ubuntu:22.04 bash -lc '
  set -euo pipefail
  export DEBIAN_FRONTEND=noninteractive
  apt-get update -qq
  apt-get install -y -qq git ca-certificates python3 python3-pip debhelper dpkg-dev build-essential coreutils findutils
  python3 -m pip install -q pytest
  ./packaging/scripts/install-linux-vscodium-build-deps.sh
  bash -n packaging/scripts/install-le-vibe-local.sh
  cd le-vibe && python3 -m pytest tests/test_install_le_vibe_local_script_contract.py -q
  cd /r && ./packaging/scripts/install-le-vibe-local.sh --preflight-only
'
```

---

## Time / disk (honest ranges)

- **Editor compile:** often **1–4+ hours**; may **OOM** on small RAM or tight disk.
- **Disk:** plan for **tens of GB** under **`editor/vscodium/`**; **≥ ~25 GB** free recommended before a from-scratch compile.

---

## Tests + gates

| Check | Result |
|-------|--------|
| `pytest tests/test_install_le_vibe_local_script_contract.py` + related docs/BUILD contracts | **621 passed** (`./packaging/scripts/ci-smoke.sh` full `le-vibe` suite) |
| `verify-step14-closeout.sh --require-stack-deb` | **OK** |

**Last verification (2026-04-13):** `bash -n packaging/scripts/install-le-vibe-local.sh`; `pytest` installer + `test_docs_readme_local_install_one_shot_row_contract` (**11** passed); `verify-step14-closeout.sh --require-stack-deb` **OK**; `ci-smoke.sh` **621** passed; `test_verify_step14_closeout_contract.py` stubs aligned with `dpkg-deb --fsys-tarfile | tar -xOf` + packaged `desktop-file-validate` path (real **`/usr/bin/tar`** via stub `exec`); Docker `ubuntu:22.04` matrix template (**~70s**, installer contracts + `--preflight-only` **OK**).

---

## Known limitations

- Full **`dev/build.sh`** is **not** run on every PR in default **`ci.yml`** (too heavy); contract tests + **`bash -n`** guard the installer script.
- **Two distinct “clean” full compiles** are operator-expensive; matrix **B** validates **preflight + deps + contracts** in Docker; full Electron compile in Docker remains optional via existing Docker scripts.
- **Minimal Docker** may lack Node on `PATH`; `probe-vscode-linux-build.sh` can report `unknown` while the bind-mounted tree still contains `bin/codium` — use **`editor/use-node-toolchain.sh`** or install Node per **`editor/.nvmrc`** before a real compile in that environment.

---

## Statement

**Comfortable one-shot self-installed editor experience (as defined in-repo: one canonical script, preflight, docs, tests, STEP 14 gates): SHIPPED.**

Further work (apt repos, `.lvibe/` governance, etc.) requires **explicit product authorization**.
