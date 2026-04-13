# Lé Vibe — CI and QA hardening (Roadmap H3)

**STEP 10 / PM map:** [`PM_STAGE_MAP.md`](PM_STAGE_MAP.md) — **H3** row links here, **[`packaging/scripts/ci-smoke.sh`](../packaging/scripts/ci-smoke.sh)**, **`packaging/scripts/ci-editor-gate.sh`**, and **`.github/workflows/ci.yml`** **Smoke QA**.

This document describes what **GitHub Actions** enforces, what **`packaging/scripts/ci-smoke.sh`** runs locally, and what remains **manual**.

**Product anchor:** [`PRODUCT_SPEC.md`](PRODUCT_SPEC.md) §8 (secrets / agent policy) and §9 (orchestration + evidence roster). **Roadmap H3** (this doc) is indexed from [`README.md`](README.md) and [`PROMPT_BUILD_LE_VIBE.md`](PROMPT_BUILD_LE_VIBE.md).

**Install UX:** Passing CI does not replace **`/usr/share/doc/le-vibe/README.Debian`** ([`debian/le-vibe.README.Debian`](../debian/le-vibe.README.Debian)) on installed systems — **§5** workspace memory consent before **`.lvibe/`** is created.

**E1 / acceptance:** **`ci-smoke.sh`** runs full **`le-vibe/tests/`** **`pytest`** (incl. **`test_issue_template_h8_contract.py`** — **H8** / **STEP 12**; **`test_product_spec_section8.py`** — **`docs/PRODUCT_SPEC.md`** *Prioritization* (**`linux_compile`**, **`vscodium-linux-build.tar.gz`**, **`actions/cache@v4`**, **`~/.cargo`**, **`spec-phase2.md` §14**; **`./editor/smoke.sh`**); **`test_ci_yml_submodules_contract.py`** — **`ci.yml`** **`submodules: recursive`**; **`test_editor_le_vibe_overrides_readme_contract.py`** — **`editor/le-vibe-overrides/README.md`** **STEP 14** / **H6** strings; **`test_build_le_vibe_ide_workflow_contract.py`** — **`build-le-vibe-ide.yml`** **`ide-ci-metadata`** **`le_vibe_editor_docs`**), then **`ci-editor-gate.sh`** (**H6**), then **`desktop-file-validate`** when installed — full **E1** scope: root **[`README.md`](../README.md)** *Tests* / **E1 mapping** and **[`spec-phase2.md`](../spec-phase2.md) §14** *Honesty vs CI*. For focused Python regression, run **`cd le-vibe && python3 -m pytest tests/`** locally and consult **[`PRODUCT_SPEC_SECTION8_EVIDENCE.md`](PRODUCT_SPEC_SECTION8_EVIDENCE.md)** when behavior under **§1**/**H8** + **§5–§10** changes; see **[H1](apt-repo-releases.md)** / **[H2](sbom-signing-audit.md)** *E1* notes for release-time checks.

## CI workflow (`.github/workflows/ci.yml`)

Order of steps on **`ubuntu-latest`**:

| Step | Purpose |
|------|---------|
| Checkout, pip cache | Reproducible dependency install |
| System packages | **`debhelper`**, **`lintian`**, **`desktop-file-utils`**, etc. |
| **Smoke QA** | **`./packaging/scripts/ci-smoke.sh`** (see below) |
| **Python supply chain (H2)** | **`pip-audit`**, CycloneDX SBOM → **`artifacts/`** |
| **Build `.deb`** | **`dpkg-buildpackage -us -uc -b`** |
| **Checksums (H1)** | **`SHA256SUMS`** over **`.deb`** + SBOM, **`sha256sum -c`** |
| **Lintian** | **`lintian --fail-on error --color never`** — **errors** fail; warnings/info do not |
| **Upload artifact** | **`le-vibe-deb`** — **stack** **`le-vibe`** **`.deb`** + SBOM + **`SHA256SUMS`** (**not** **`le-vibe-ide`**; **§7.3** — [`apt-repo-releases.md`](apt-repo-releases.md) *IDE package*, [`spec-phase2.md`](../spec-phase2.md) *CI `le-vibe-deb` vs maintainer `le-vibe-ide`*, [`PM_STAGE_MAP.md`](PM_STAGE_MAP.md) *H1 vs §7.3 .deb bundles*) |

**Git checkout:** **[`.github/workflows/ci.yml`](../.github/workflows/ci.yml)** uses **`actions/checkout@v4`** with **`submodules: recursive`** so **`editor/vscodium`** is present and **`ci-editor-gate.sh`** runs the **VSCodium** script **`bash -n`** / **`editor/.nvmrc`** checks (not a **layout=none** skip).

**Local clone (14.b):** if **`editor/vscodium/`** is empty after a plain **`git clone`**, run **`git submodule update --init editor/vscodium`** from the repository root before **`./editor/smoke.sh`** / **`ci-editor-gate.sh`** — same as **`editor/README.md`** *Fresh clone (14.b)*.

**Scope:** **[`.github/workflows/ci.yml`](../.github/workflows/ci.yml)** header comments cite **`spec-phase2.md` §14** and **H8** (**`docs/README`** *Product surface* / **`SECURITY`** / **`privacy-and-telemetry`** *E1* — same trust chain as **`packaging/scripts/ci-smoke.sh`**). **[`.github/dependabot.yml`](../.github/dependabot.yml)** and **[`.github/ISSUE_TEMPLATE/`](../.github/ISSUE_TEMPLATE/)** (**[`config.yml`](../.github/ISSUE_TEMPLATE/config.yml)** **`#` H8**) document the same **H8** chain (weekly **pip** + **Actions** bump PRs; reporter-facing template **`#`** lines; **H2** follow-up per **`sbom-signing-audit.md`**). A green **`ci.yml`** run proves **this** tree’s **`.deb`** + Python supply chain and runs **`ci-editor-gate.sh`** (STEP 14 / **H6** — layout, **`bash -n`**, **`editor/.nvmrc`**) after **`pytest`** via **`ci-smoke.sh`** — the same gate as **`./editor/smoke.sh`**. **[`build-le-vibe-ide.yml`](../.github/workflows/build-le-vibe-ide.yml)** is the dedicated **H6** IDE workflow: the **default `linux` job** (**`editor/**`** PR paths, **`ide-v*`** tags, **`workflow_dispatch`**) uploads pre-binary **metadata** (`ide-ci-metadata.txt`, …) — run **Summary** includes **Pre-binary artifact** / **`le_vibe_editor_docs`** ↔ **`LE_VIBE_EDITOR`** (E1 **`test_build_le_vibe_ide_workflow_contract.py`**). Optional job **`linux_compile`** runs **`dev/build.sh`** and uploads **`vscodium-linux-build.tar.gz`** when **`VSCode-linux-*`** exists (**14.e / 14.f** — **not** the default on **`pull_request`**). **[`build-linux.yml`](../.github/workflows/build-linux.yml)** **`uses:`** it (**`workflow_dispatch`** alias). Either way it is **not** the only place the gate runs (**`ci.yml`** also invokes **`ci-editor-gate.sh`** after **`pytest`**). **H7** alternate bundles remain outside default **`ci.yml`**. **[`SECURITY.md`](../SECURITY.md)** *Related docs* lists optional **[`rag/le-vibe-phase2-chunks.md`](rag/le-vibe-phase2-chunks.md)** (*RAG / embeddings*, non-canonical) alongside the same **H8** index — refresh if **`SECURITY`** / trust copy shifts.

**Lintian:** `--color never` keeps logs readable in Actions. To fail on **warnings**, change **`--fail-on`** (expect more noise until maintainer fields and policy tags are clean). See **`man lintian`**.

**IDE `.deb` (`le-vibe-ide`, STEP 14 / §7.3):** **`packaging/scripts/build-le-vibe-ide-deb.sh`** runs **`lintian`** on **`packaging/le-vibe-ide_*.deb`** when **`lintian`** is installed, after **`dpkg-buildpackage`**. Tags are **non-fatal** unless **`LEVIBE_IDE_LINTIAN_STRICT=1`**. Details — **[`packaging/debian-le-vibe-ide/README.md`](../packaging/debian-le-vibe-ide/README.md)**; this path is **not** part of the default **`ci.yml`** **Smoke QA** (that **`lintian`** applies to the **stack** **`.deb`**).

**Maintainer full-product stack + IDE `.deb`:** From the monorepo root, **`packaging/scripts/build-le-vibe-debs.sh --with-ide`** builds both **`le-vibe_*_all.deb`** and **`le-vibe-ide_*_amd64.deb`** when **`editor/vscodium/VSCode-linux-*`** exists and prints **Full-product install** on success — **[`PM_DEB_BUILD_ITERATION.md`](PM_DEB_BUILD_ITERATION.md)** (*Success output (`--with-ide`)*); close-out gate: **`packaging/scripts/verify-step14-closeout.sh --require-stack-deb`** (add **`--apt-sim`** for explicit dependency simulation, **`--json`** for machine-readable close-out output; **`apt_sim_note`** — **[`PM_DEB_BUILD_ITERATION.md`](PM_DEB_BUILD_ITERATION.md)** (*`--json` close-out payload*)); stack **`le-vibe_*.deb`** discovery — **`packaging/scripts/resolve-latest-le-vibe-stack-deb.sh`** (*Output paths* in the same doc); install both — **[`packaging/debian-le-vibe-ide/README.md`](../packaging/debian-le-vibe-ide/README.md)** (*Install both packages*). **Ordering:** **build machine** close-out, **test host** install/smoke — **[`apt-repo-releases.md`](apt-repo-releases.md)** (*IDE package*). **Not** run by default **`ci.yml`**.

## Smoke script (`packaging/scripts/ci-smoke.sh`)

Run from the **repository root**:

```bash
./packaging/scripts/ci-smoke.sh
```

It executes, in order:

1. **`verify-continue-pin.sh`** (H4) — semver in **`packaging/continue-openvsx-version`**
2. **`bash -n`** on **`packaging/bin/*`** — syntax check for **`lvibe`**, **`le-vibe`**, **`le-vibe-setup-continue`**, **`lvibe-hygiene`**
3. **Synthetic workspace hygiene** — **`PYTHONPATH=le-vibe`** Python snippet: **`ensure_lvibe_workspace`** + **`check_lvibe_workspace`** on a temp dir (same checks as **`python -m le_vibe.hygiene`** / **`lvibe-hygiene`**, E4). The subprocess sets **`LE_VIBE_LVIBE_CONSENT=accept`** for that snippet only (matches **`le-vibe/tests/conftest.py`**) so §5 automation intent stays explicit.
4. **`pytest`** for **`le-vibe/tests/`** (installs **`requirements.txt`** + **`pytest`**; full suite — **H8** via **`test_issue_template_h8_contract.py`**; **E1** incl. **`test_product_spec_section8.py`**, **`test_ci_yml_submodules_contract.py`**, **`test_editor_le_vibe_overrides_readme_contract.py`**, **`test_build_le_vibe_ide_workflow_contract.py`** — **`docs/PRODUCT_SPEC.md`** *Prioritization* (**`linux_compile`**, **`vscodium-linux-build.tar.gz`**, **`actions/cache@v4`**, **`~/.cargo`**, **`spec-phase2.md` §14**) / **`ci.yml`** checkout / **`editor/le-vibe-overrides/README.md`** / **`build-le-vibe-ide.yml`**; see root **[`README.md`](../README.md)** *Tests* for **E1** roster)
5. **`ci-editor-gate.sh`** (STEP 14 / **H6**) — same layout / **`bash -n`** / **`editor/.nvmrc`** checks as **`./editor/smoke.sh`** and **[`build-le-vibe-ide.yml`](../.github/workflows/build-le-vibe-ide.yml)** / **[`build-linux.yml`](../.github/workflows/build-linux.yml)** (alias) (no Electron compile)
6. **`desktop-file-validate`** on **`packaging/applications/le-vibe.desktop`**, **`packaging/autostart/le-vibe-continue-setup.desktop`**, and **`packaging/debian-le-vibe-ide/debian/le-vibe.desktop`** (§7.3 **`le-vibe-ide`** menu entry — needs **`desktop-file-utils`**)

On **GitHub Actions**, missing **`desktop-file-validate`** is a **failure**. Locally, it **skips** desktop validation with a notice unless you install **`desktop-file-utils`**.

## IDE smoke (`editor/smoke.sh`, H6)

**`packaging/scripts/ci-smoke.sh`** runs **`ci-editor-gate.sh`** after **`pytest`** (step 5 above) — same gate. To run **only** the IDE checks without pin / wrappers / **`pytest`** / **`.desktop`**, from the **repository root**:

```bash
./editor/smoke.sh
```

That wrapper **`exec`**s **`packaging/scripts/ci-editor-gate.sh`** with the same arguments (**`./editor/smoke.sh --help`** prints **`ci-editor-gate`** usage), matching **[`build-le-vibe-ide.yml`](../.github/workflows/build-le-vibe-ide.yml)** / **[`build-linux.yml`](../.github/workflows/build-linux.yml)** (alias) when sources are present. See **[`editor/README.md`](../editor/README.md)** and **[`docs/vscodium-fork-le-vibe.md`](vscodium-fork-le-vibe.md)**.

**Vendoring + optional full compile (14.e / 14.f):** **`./editor/smoke.sh`** is intentionally the **fast** layout / **`bash -n`** / **`.nvmrc`** gate — it does **not** run upstream **`dev/build.sh`**, run workflow job **`linux_compile`**, or unpack **`vscodium-linux-build.tar.gz`** locally. Submodule setup, optional job **`linux_compile`**, and **`vscodium-linux-build.tar.gz`** / **`print-ci-tarball-codium-path.sh`** are documented under **[`editor/VENDORING.md`](../editor/VENDORING.md)** and **[`editor/BUILD.md`](../editor/BUILD.md)** (**Vendoring upstream**). When **`linux_compile`** runs in **[`build-le-vibe-ide.yml`](../.github/workflows/build-le-vibe-ide.yml)**, it executes **`ci-vscodium-bash-syntax.sh`** + **`ci-editor-nvmrc-sync.sh`** before **`ci-vscodium-linux-dev-build.sh`** (fail fast — same **`bash -n`** / **`.nvmrc`** checks as **`ci-editor-gate`**); **`ci-vscodium-linux-dev-build.sh`** then enforces **`node --version`** vs **`editor/.nvmrc`** before **`dev/build.sh`** (**`LEVIBE_SKIP_NODE_VERSION_CHECK`** — **14.a** / **14.e**, **[`editor/BUILD.md`](../editor/BUILD.md)** *Compile wrapper vs Node*). The job sets **`NODE_OPTIONS=--max-old-space-size=8192`** (same as **`editor/vscodium/dev/build.sh`**) and installs a bounded **apt** set — troubleshooting (**OOM**, missing deps, self-hosted runners) — **[`editor/BUILD.md`](../editor/BUILD.md)** *When full compile fails*.

**Branding (14.d):** this **IDE smoke** path does **not** prove Lé Vibe–visible product identity — only layout / syntax / toolchain parity. Staging map **[`editor/le-vibe-overrides/branding-staging.checklist.md`](../editor/le-vibe-overrides/branding-staging.checklist.md)** — read *PRODUCT_SPEC §7.2 (read before overrides)* first (**14.d**, **`docs/PRODUCT_SPEC.md` §7.2**); see **`editor/README.md`** *14.c vs 14.d*.

## Optional full Linux compile (`linux_compile`, STEP 14.e)

**At a glance:** Merge-quality CI is **`ci.yml`** only — **`linux_compile`** never blocks **`pull_request`** merges (*Honesty vs CI* below). Need **`VSCode-linux-*`** for **`build-le-vibe-ide-deb.sh`** / **`--with-ide`** without a full **`dev/build.sh`**? Prefer **`packaging/scripts/docker-le-vibe-vscodium-prepare-only.sh`** (*Prepare-only* below) before spending runner time on **`linux_compile`**. When you publish **both** **`.deb`** files after any path, use one folder and one regenerated **`SHA256SUMS`** — **[`apt-repo-releases.md`](apt-repo-releases.md)** *Pre-publish artifact checklist* **Checklist shorthand** (*Publishing* below).

**Not a default merge gate:** the fast **`linux`** job runs on **`pull_request`**; job **`linux_compile`** is **opt-in** only — green **`ci.yml`** does **not** depend on it. Same **honesty** bar as **[`spec-phase2.md`](../spec-phase2.md)** §14 *Honesty vs CI* (full Electron compile is **additive**, not implied by stack **`.deb`** CI).

| How to run **`linux_compile`** | Details |
|--------------------------------|---------|
| **Manual dispatch** | GitHub **Actions** → workflow **[`build-le-vibe-ide.yml`](../.github/workflows/build-le-vibe-ide.yml)** → **Run workflow** → enable input **`vscodium_linux_compile`** (**boolean** `true`). |
| **Reusable / alias** | **[`build-linux.yml`](../.github/workflows/build-linux.yml)** **`workflow_dispatch`** forwards **`vscodium_linux_compile`** via **`workflow_call`** — same job definition. |
| **Tag** | Push a tag matching **`ide-v*`** (e.g. **`ide-v0.1.0`**) — **`linux_compile`** **`if:`** includes **`refs/tags/ide-v`** (see workflow file). |

**Artifact:** **`vscodium-linux-build.tar.gz`** (ZIP name like **`le-vibe-vscodium-linux-<run_id>`**). Unpack so **`VSCode-linux-*`** sits under **`editor/vscodium/`**, then **`packaging/scripts/build-le-vibe-ide-deb.sh`** or **`packaging/scripts/build-le-vibe-debs.sh --with-ide`** — full unpack / **`.deb`** flow — **[`editor/BUILD.md`](../editor/BUILD.md)** (*After a successful `linux_compile`*, *14.f*).

**Download shape (14.f):** the workflow **artifact** you get from **Actions → run → Artifacts** (or a CLI download) is a **`.zip`** **around** **`vscodium-linux-build.tar.gz`** — **unzip first**, then pass the **`.tar.gz`** to **`./editor/print-ci-tarball-codium-path.sh`** for a temp **`bin/codium`** / **`LE_VIBE_EDITOR`** path, or unpack into **`editor/vscodium/`** as in **[`editor/BUILD.md`](../editor/BUILD.md)** (*CI artifact → `LE_VIBE_EDITOR`*). Passing the outer **`.zip`** to **`print-ci-tarball-codium-path.sh`** fails by design — same guard as **`editor/BUILD.md`** / **`editor/print-ci-tarball-codium-path.sh`**.

**CLI (`gh`, 14.f):** **`gh run download <RUN_ID> -n le-vibe-vscodium-linux-<RUN_ID> -D ./dir`** pulls the same **`linux_compile`** upload as the Actions UI — **`-n`** must match **`actions/upload-artifact`** in **[`build-le-vibe-ide.yml`](../.github/workflows/build-le-vibe-ide.yml)** (**`le-vibe-vscodium-linux-${{ github.run_id }}`**). You still get the outer **`.zip`** — unzip, then treat the inner **`.tar.gz`** as above (**`print-ci-tarball-codium-path.sh`** / **`BUILD.md`**).

**Finding `RUN_ID`:** The numeric id is in the browser URL (**`/actions/runs/<RUN_ID>`**) for the **`build-le-vibe-ide`** workflow run, or from the CLI: **`gh run list --workflow build-le-vibe-ide.yml --limit 10`** (then **`gh run download <RUN_ID> …`** as above — requires **`gh auth login`**). On a **failed** run, **`gh run view <RUN_ID> --log-failed`** prints failed-step logs without opening the browser (same **`gh`** auth).

**Branch filter (`gh`):** **`gh run list --workflow build-le-vibe-ide.yml --branch main`** (swap **`main`** for your default branch or feature branch) narrows the list when several branches run the same workflow — pick the **`RUN_ID`** from the row you care about, then **`gh run download`** as in *CLI (`gh`, 14.f)* above.

**Runner realism:** Default **GitHub-hosted** images may **OOM** or exceed **time** on a full upstream compile — **[`editor/BUILD.md`](../editor/BUILD.md)** (*When full compile fails* / *Runner realism*). For a repeatable local analogue of the CI environment, **`packaging/scripts/docker-le-vibe-vscodium-linux-compile.sh`** documents the same **`ubuntu:22.04`**-style base as job **`linux_compile`**.

**`NODE_OPTIONS` (heap parity):** Job **`linux_compile`** in **[`build-le-vibe-ide.yml`](../.github/workflows/build-le-vibe-ide.yml)** sets **`NODE_OPTIONS=--max-old-space-size=8192`** (same **heap** intent as **`editor/vscodium/dev/build.sh`**). When you reproduce or bisect **OOM**s locally or in Docker, export the same **`NODE_OPTIONS`** before concluding a CI-only flake — finished runs print a **Job summary — compile** block that echoes the **Toolchain** line (**`env.NODE_OPTIONS`** vs **`dev/build.sh`**).

**Fork / org tuning (optional):** Job **`linux_compile`** in **[`build-le-vibe-ide.yml`](../.github/workflows/build-le-vibe-ide.yml)** defaults to **`ubuntu-latest`** with a bounded **`timeout-minutes`** — if you need routine full Electron compiles in CI, adjust **`runs-on`** (e.g. **self-hosted** or a larger hosted label), raise **`timeout-minutes`**, or maintain a **fork** with those changes. Same **honesty** bar: this does **not** change what default **`ci.yml`** proves — **[`editor/BUILD.md`](../editor/BUILD.md)** *Runner realism*; **[`spec-phase2.md`](../spec-phase2.md)** §14 *Honesty vs CI*.

**Prepare-only (no `dev/build.sh`):** To apply §7.3 branding layers and get a **`VSCode-linux-*`** tree for **`build-le-vibe-ide-deb.sh`** / **`--with-ide`** without waiting on a full Electron compile, **`packaging/scripts/docker-le-vibe-vscodium-prepare-only.sh`** runs the same prepare path as CI inside Docker — **[`editor/BUILD.md`](../editor/BUILD.md)** (*§7.3 prepare-only* / *Preflight*). Still mutates **`editor/vscodium/`**; heavier full compile remains **`docker-le-vibe-vscodium-linux-compile.sh`** above.

### Maintainer triage (`linux_compile` flaky — **not** a merge gate)

Default **`ci.yml`** / **`ci-smoke.sh`** remains the **stack** **`.deb`** + **`pytest`** + **`ci-editor-gate`** bar — optional **`linux_compile`** does **not** block merging (**[`spec-phase2.md`](../spec-phase2.md)** §14 *Honesty vs CI*). When the job **OOM**s, **times out**, or you only need a narrower path to an IDE **`.deb`**:

| Situation | Where to go |
|-----------|-------------|
| **OOM** / process killed on a GitHub-hosted runner | **[`editor/BUILD.md`](../editor/BUILD.md)** *Runner realism* / *When full compile fails*; **`packaging/scripts/docker-le-vibe-vscodium-linux-compile.sh`** (local analogue — *Optional full Linux compile* above) |
| **Timeout** | Same; or **`packaging/scripts/docker-le-vibe-vscodium-prepare-only.sh`** if §7.3 staging + **`build-le-vibe-ide-deb.sh`** is enough without a full **`dev/build.sh`** |
| **Download / unpack mistakes** | *Download shape (14.f)* above — outer Actions **`.zip`** must be unzipped before **`print-ci-tarball-codium-path.sh`** or unpacking **`vscodium-linux-build.tar.gz`** |

**Publishing (H1 / STEP 14):** **`linux_compile`** uploads **`vscodium-linux-build.tar.gz`** — it does **not** replace the stack **`le-vibe`** **`.deb`** from **`ci.yml`** / **`dpkg-buildpackage`**. When you ship **both** **`.deb`** files after staging from a **`linux_compile`** tree, regenerate **`SHA256SUMS`** over **every** **`*.deb`** / SBOM you attach — **[`docs/apt-repo-releases.md`](apt-repo-releases.md)** *Pre-publish artifact checklist* / **Checklist shorthand** (**Integrity**); one-shot maintainer build — **`packaging/scripts/build-le-vibe-debs.sh --with-ide`** — **[`docs/PM_DEB_BUILD_ITERATION.md`](PM_DEB_BUILD_ITERATION.md)** (*Releases & full-product demo*).

## What is not automated here

- **ShellCheck** on every script — optional locally (`shellcheck packaging/scripts/*.sh`); not required in default CI to keep images small.
- **Headless GUI E2E** (full editor + Continue chat) — intentionally out of default CI; use the manual checklist in **[`README.md`](../README.md)** (Release / QA section).

## Related docs

- **[`.github/workflows/ci.yml`](../.github/workflows/ci.yml)** — canonical **stack** **CI** job (artifact **`le-vibe-deb`**)
- **[`editor/VENDORING.md`](../editor/VENDORING.md)** — git submodule at **`editor/vscodium/`**, CI parity, optional **`linux_compile`** + tarball (**14.e / 14.f**)
- **[`editor/README.md`](../editor/README.md)** — *Full Linux compile* (**14.e / 14.f**) + **H3 maintainer index** (opt-in triggers, **`gh run view --log-failed`**, Docker fallbacks — same story as *Optional full Linux compile* above)
- **[`packaging/scripts/docker-le-vibe-vscodium-linux-compile.sh`](../packaging/scripts/docker-le-vibe-vscodium-linux-compile.sh)** — optional **local** full compile in an **`ubuntu:22.04`**-style image (maintainer pain relief when **`linux_compile`** **OOM**/**timeout** on default runners — **14.e**; see *Optional full Linux compile* above)
- **[`packaging/scripts/docker-le-vibe-vscodium-prepare-only.sh`](../packaging/scripts/docker-le-vibe-vscodium-prepare-only.sh)** — §7.3 **prepare-only** in Docker (branding layers + **`VSCode-linux-*`** for IDE **`.deb`** without **`dev/build.sh`** — **14.e**; **[`editor/BUILD.md`](../editor/BUILD.md)** *Preflight*)
- **[`build-le-vibe-ide.yml`](../.github/workflows/build-le-vibe-ide.yml)** — **H6** dedicated IDE workflow (**`editor/**`** PRs, pre-binary metadata artifacts + **`upload-artifact`** **retention-days**, **Summary** **Pre-binary artifact** / **`LE_VIBE_EDITOR`**); optional **`linux_compile`** + **`vscodium-linux-build.tar.gz`** (**14.e**); workflow-level **`permissions:`** **`contents: read`**, **`actions: write`** (checkout + artifacts); same **`ci-editor-gate`** as **`ci-smoke.sh`** / **`./editor/smoke.sh`**
- **[`build-linux.yml`](../.github/workflows/build-linux.yml)** — **`workflow_dispatch`** alias; **`uses:`** **[`build-le-vibe-ide.yml`](../.github/workflows/build-le-vibe-ide.yml)** (same Summary / skip reasons as the reusable workflow)  
- **[`docs/apt-repo-releases.md`](apt-repo-releases.md)** — artifacts, checksums, Releases (H1), **`CHANGELOG.md`** / **`debian/changelog`** when tagging  
- **[`docs/sbom-signing-audit.md`](sbom-signing-audit.md)** — **`pip-audit`**, SBOM (H2)  
- **[`docs/continue-extension-pin.md`](continue-extension-pin.md)** — Open VSX pin verification in smoke (H4)  
- **[`spec-phase2.md`](../spec-phase2.md) §14** — honest split: **`ci.yml`** (via **`ci-smoke.sh`**) = stack **`.deb`** + **`pytest`** + **`ci-editor-gate`** (**H6** gate); **`build-le-vibe-ide.yml`** / **`build-linux.yml`** (alias) = **H6** default **metadata** **`linux`** job + optional **`linux_compile`** tarball + **`editor/**`**-scoped runs; **H7** bundles optional/out-of-tree  
- **[`CHANGELOG.md`](../CHANGELOG.md)** — promote **`[Unreleased]`** when a green CI build becomes a tagged release (same rhythm as **H1**)  
