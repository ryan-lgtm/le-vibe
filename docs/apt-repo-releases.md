# Lé Vibe — releases, checksums, and apt hosting (Roadmap H1)

**STEP 8 / PM map:** [`PM_STAGE_MAP.md`](PM_STAGE_MAP.md) — **H1** row links here, **`debian/changelog`**, **`CHANGELOG.md`**, and **`.github/workflows/ci.yml`** artifact **`le-vibe-deb`**.

**CI vs IDE bundle:** Default **`ci.yml`** **`le-vibe-deb`** contains the **stack** **`le-vibe`** **`.deb`** + SBOM + **`SHA256SUMS`** — **not** **`le-vibe-ide_*_amd64.deb`** (**§7.3**). Full-product releases attach both — *IDE package* below; monorepo honesty — **[`spec-phase2.md`](../spec-phase2.md)** *CI `le-vibe-deb` vs maintainer `le-vibe-ide`*.

This document is for **maintainers** who publish the **`.deb`** beyond ad-hoc copies: **GitHub Actions** artifacts, **checksum files**, **GitHub Releases**, and optional **apt** repositories.

**Product anchor:** [`PRODUCT_SPEC.md`](PRODUCT_SPEC.md) §8–§9 — agent/secrets policy and the orchestration roster. **Roadmap H1** (this doc) is indexed from [`README.md`](README.md) and [`PROMPT_BUILD_LE_VIBE.md`](PROMPT_BUILD_LE_VIBE.md); see also [`sbom-signing-audit.md`](sbom-signing-audit.md) (**H2**).

**E1 / acceptance:** After changing launcher or packaging behavior, re-verify **[`PRODUCT_SPEC_SECTION8_EVIDENCE.md`](PRODUCT_SPEC_SECTION8_EVIDENCE.md)** and run **`cd le-vibe && python3 -m pytest tests/`** (full suite — **H8** / **STEP 12** via **`test_issue_template_h8_contract.py`**; see root **[`README.md`](../README.md)** *Tests* / **E1 mapping** and **`spec-phase2.md` §14** *Honesty vs CI* for the rest) in a source tree — same bar as CI (**[`ci-qa-hardening.md`](ci-qa-hardening.md)**). **[`.github/workflows/ci.yml`](../.github/workflows/ci.yml)**, **[`.github/dependabot.yml`](../.github/dependabot.yml)**, and **[`.github/ISSUE_TEMPLATE/`](../.github/ISSUE_TEMPLATE/)** (**[`config.yml`](../.github/ISSUE_TEMPLATE/config.yml)** **`#` H8** maintainer lines) sit in the same **H8** index as **`docs/README`** *Product surface* / **`SECURITY`** / **`privacy-and-telemetry`** *E1 contract tests* — workflow and Dependabot headers record that chain alongside **§14** scope (**H2** bump PRs → **`sbom-signing-audit.md`** follow-up). **[`SECURITY.md`](../SECURITY.md)** *Related docs* lists optional **[`rag/le-vibe-phase2-chunks.md`](rag/le-vibe-phase2-chunks.md)** (*RAG / embeddings*, non-canonical) in the same **H8** index — refresh when trust or **`SECURITY`** copy shifts.

**Install UX:** Each **`.deb`** ships **`/usr/share/doc/le-vibe/README.Debian`** (source [`debian/le-vibe.README.Debian`](../debian/le-vibe.README.Debian)) — post-install steps, **§5** **`.lvibe/`** workspace consent, pointers to **`PRODUCT_SPEC`** / the docs index, and an on-disk **Phase 2 scope** line (**`docs/spec-phase2.md` §14**, **H6**/**H7** vs this package). Mention it in **GitHub Releases** copy when you publish binaries so users land on the same authority chain as the source tree. **Release/marketing copy** should stay aligned with **[`spec-phase2.md`](../spec-phase2.md) §14** — **`editor/`** (**H6**) and optional **H7** bundles ship per policy; stack **`le-vibe`** **`.deb`** may publish separately from IDE artifacts until unified releases exist.

## Versioned changelog

Package version and per-release notes live in **`debian/changelog`** (Debian policy format). For **GitHub Releases** body text, also update the root **[`CHANGELOG.md`](../CHANGELOG.md)** (Keep a Changelog style) so users see the same story without reading Debian policy formatting. Between tags, **`[Unreleased]`** may hold **Documentation** / trust-alignment bullets (e.g. **`spec-phase2.md` §14** cross-links) — fold them into a dated **`[x.y.z]`** section when you bump **`debian/changelog`**.

**Dual changelog discipline:** **`debian/changelog`** is authoritative for the **stack** **`.deb`** version (**`dpkg -l le-vibe`** after install). **`CHANGELOG.md`** is the **Keep a Changelog** narrative you paste into **GitHub Releases** — both must describe the **same** **`x.y.z`** before you run the **stack-only** checklist (*Checklist — stack-only GitHub Release* below).

**IDE `le-vibe-ide` changelog:** The **branded IDE** **`.deb`** is versioned from **[`packaging/debian-le-vibe-ide/debian/changelog`](../packaging/debian-le-vibe-ide/debian/changelog)** (separate file at **`dpkg-buildpackage`** time under **`packaging/debian-le-vibe-ide/`**). Bump it when you ship a new **`le-vibe-ide_*_amd64.deb`**; user-facing **root** **`CHANGELOG.md`** entries often emphasize the **stack** story — add IDE packaging notes there when maintainers need the same **Release** narrative for both packages. **`ide-v*`** git tags still **only** opt into **`linux_compile`** — they do **not** replace stack **`debian/changelog`** / **`v…`** tags (*Tagging discipline* below).

Bump before tagging a release, for example:

```bash
cd /path/to/r-vibe
dch -v 0.1.1 "Describe user-visible changes."
# edit the entry if needed, then build
dpkg-buildpackage -us -uc -b
```

The first line (`le-vibe (0.1.1) unstable; urgency=…`) must match the version users see after **`apt install`** / **`dpkg -l le-vibe`**.

**Before a stack tag / Release:** **`dpkg-parsechangelog -S Version -l debian/changelog`** (from **`dpkg-dev`**) prints the **semver** in the top stanza — it should match the dated section you folded into **[`CHANGELOG.md`](../CHANGELOG.md)** and the **`v…`** tag you intend for **`gh release create`** (*Tagging discipline* / *Stack release tags vs `ide-v`* below).

### Tagging discipline (stack vs `ide-v*` compile tags)

**Stack `le-vibe` .deb:** Keep **`debian/changelog`**, root **[`CHANGELOG.md`](../CHANGELOG.md)**, and your **Git tag** / **GitHub Release** aligned — that is the primary **H1** version story for the Python stack **`.deb`**.

**`ide-v*` tags:** Pushing a tag like **`ide-v0.1.0`** opts into job **`linux_compile`** in **[`build-le-vibe-ide.yml`](../.github/workflows/build-le-vibe-ide.yml)** (STEP **14.e**) — it does **not** replace bumping **`debian/changelog`** for the stack package. Treat IDE compile tags as an **additive** maintainer/CI track, not the same release lever as **`le-vibe`** versioning — **[`spec-phase2.md`](../spec-phase2.md)** *Honesty vs CI*; triggers — **[`docs/ci-qa-hardening.md`](ci-qa-hardening.md)** *Optional full Linux compile*.

### Stack release tags vs `ide-v*` (publishing)

**Stack `le-vibe` .deb + GitHub Release:** After **`debian/changelog`** / **`CHANGELOG.md`** match the version you are shipping, tag **`main`** with a **stack** version tag aligned with that story (common pattern: **`v`** plus the same **semver** as **`dpkg -l le-vibe`** — e.g. **`v0.1.1`** when the package is **`0.1.1`**). Use that tag with **`gh release create <tag>`** / attach **`le-vibe-deb`** artifacts — *GitHub Releases + checksums* below. **`ide-v*`** tags **only** drive optional **`linux_compile`**; they do **not** replace a **`debian/changelog`** bump or a **stack** release tag for the Python **`.deb`**.

### Checklist — stack-only GitHub Release (H1)

Use this as a **minimal ordered path**; supporting detail spans *Versioned changelog* (above) and *Pre-publish artifact checklist*, *Minimum directory layout*, and *GitHub Releases + checksums* (below).

1. **Bump** **`debian/changelog`** and fold **`CHANGELOG.md`** **`[Unreleased]`** into a dated **`[x.y.z]`** section (*Versioned changelog*).
2. **Confirm version** — **`dpkg-parsechangelog -S Version -l debian/changelog`** matches the **`v…`** tag you will use (*Before a stack tag / Release* above).
3. **Green build** — a successful **`.github/workflows/ci.yml`** run on **`main`** (artifact **`le-vibe-deb`**) or a local **`dpkg-buildpackage -us -uc -b`** with the same tree.
4. **Download** the **`le-vibe-deb`** artifact, unzip, and run **`sha256sum -c SHA256SUMS`** in that directory (*CI artifacts* / *Minimum directory layout*).
5. **Publish** — push the **stack** tag, then **`gh release create`** (or the UI) with **`*.deb`**, **`SHA256SUMS`**, and **`le-vibe-python.cdx.json`** as needed — paste **`CHANGELOG.md`** for that version into the Release body (*GitHub Releases + checksums*). **IDE** **`.deb`** is **not** in **`le-vibe-deb`** — *Combined drop* / *Artifact sources at a glance* if you attach **`le-vibe-ide_*_amd64.deb`** too.

### Checklist — full-product GitHub Release (stack + IDE, H1 / STEP 14 / §7.3)

Use when you attach **both** **`le-vibe_*_all.deb`** and **`le-vibe-ide_*_amd64.deb`** to the **same** Release (full Lé Vibe install — **[`packaging/debian-le-vibe-ide/README.md`](../packaging/debian-le-vibe-ide/README.md)** *Install both packages*).

1. **Stack version story** — complete *Dual changelog discipline* and steps **1–2** of the **stack-only** checklist above ( **`debian/changelog`** / **`CHANGELOG.md`** / intended **`v…`** tag). **`ide-v*`** tags are **not** a substitute — *Tagging discipline* / *Stack release tags vs `ide-v`*.
2. **Produce IDE** **`.deb`** — confirm the version you intend: **`dpkg-parsechangelog -S Version -l packaging/debian-le-vibe-ide/debian/changelog`** (from the repo root; **`dpkg-dev`**) prints the top stanza’s semver — it should match **[`packaging/debian-le-vibe-ide/debian/changelog`](../packaging/debian-le-vibe-ide/debian/changelog)** and the story in *IDE `le-vibe-ide` changelog* above (parallel cue to **`dpkg-parsechangelog -S Version -l debian/changelog`** for the stack — *Before a stack tag / Release*); then build **`packaging/le-vibe-ide_*.deb`** via **`build-le-vibe-ide-deb.sh`** or **`build-le-vibe-debs.sh --with-ide`** when **`VSCode-linux-*`** exists — **[`docs/PM_DEB_BUILD_ITERATION.md`](PM_DEB_BUILD_ITERATION.md)** (*Success output (`--with-ide`)*); local close-out check: **`packaging/scripts/verify-step14-closeout.sh --require-stack-deb`** (gate + built **`codium`** + both **`.deb`** artifacts; add **`--apt-sim`** for explicit **`apt-get -s install`** simulation; add **`--json`** for machine-readable success output; **`apt_sim_note`** — **[`docs/PM_DEB_BUILD_ITERATION.md`](PM_DEB_BUILD_ITERATION.md)** (*`--json` close-out payload*)); paths — *Artifact sources at a glance*.
3. **One release directory** — copy the **`le-vibe-deb`** tree (stack **`*.deb`**, **`le-vibe-python.cdx.json`**, **`SHA256SUMS`**) **and** the IDE **`.deb`** into **one** folder, then **regenerate** **`SHA256SUMS`** so it lists **every** shipped **`*.deb`** **and** **`le-vibe-python.cdx.json`** (*Pre-publish* **Combined drop** / **Integrity**).
4. **Verify** — **`sha256sum -c SHA256SUMS`** (or **`lvibe verify-checksums`**) before **`gh release create`** — *GitHub Releases + checksums*.

## CI artifacts (what ships from each green run)

Workflow **`.github/workflows/ci.yml`** uploads a single artifact bundle **`le-vibe-deb`** containing:

| File | Role |
|------|------|
| **`le-vibe_<version>_all.deb`** | Installable package |
| **`SHA256SUMS`** | **`sha256sum`** lines for **each** `*.deb` **and** **`le-vibe-python.cdx.json`** (CycloneDX SBOM from **`pip-audit` / `cyclonedx-bom`** — see **[`docs/sbom-signing-audit.md`](sbom-signing-audit.md)**) |
| **`le-vibe-python.cdx.json`** | Python dependency SBOM for supply-chain review |

CI runs **`sha256sum -c SHA256SUMS`** after generating the manifest so a corrupted or mismatched tree fails the job.

### Artifact sources at a glance (CI vs maintainer output)

Use this when you know **which** **`.deb`** you have but not **where** it was produced — then align with *Pre-publish artifact checklist* and *Minimum directory layout*.

| Artifact | Default source |
|----------|----------------|
| **`le-vibe_*_all.deb`** | **CI:** artifact **`le-vibe-deb`** (unzip). **Maintainer:** sibling **`../le-vibe_*_all.deb`** after **`dpkg-buildpackage -us -uc -b`** from the repo root — **[`PM_DEB_BUILD_ITERATION.md`](PM_DEB_BUILD_ITERATION.md)** *Output paths (from repo root)*. |
| **`le-vibe-python.cdx.json`**, **`SHA256SUMS`** | **CI:** inside **`le-vibe-deb`**. **Local** stack-only builds: regenerate **`SHA256SUMS`** per *Manual checksums* — do not assume the CI manifest without downloading CI. |
| **`le-vibe-ide_*_amd64.deb`** | **Not** in default **`ci.yml`**. **Maintainer:** **`packaging/le-vibe-ide_*.deb`** after **`build-le-vibe-ide-deb.sh`** or **`build-le-vibe-debs.sh --with-ide`** — same *Output paths* table in **`PM_DEB_BUILD_ITERATION.md`**. |

**Stack `.deb` path (close-out / Full-product install line):** **`packaging/scripts/resolve-latest-le-vibe-stack-deb.sh`** implements discovery (newest **`le-vibe_*.deb`** beside the clone, then under the **repo root**). **`verify-step14-closeout.sh --require-stack-deb`**, **`build-le-vibe-debs.sh`**, and **`manual-step14-install-smoke.sh`** (default **`STACK_DEB`**) use it — **[`PM_DEB_BUILD_ITERATION.md`](PM_DEB_BUILD_ITERATION.md)** *Output paths (from repo root)*. **STEP 14 preflight:** **`packaging/scripts/preflight-step14-closeout.sh`** reports **`[ok]`** / **`[missing]`** for the editor gate, **14.c** **`codium`**, IDE **`.deb`**, and (with **`--require-stack-deb`**) stack **`le-vibe_*.deb`** before the strict **`verify-step14-closeout.sh`** — same *Output paths* / *Preflight (all gaps)* in **`PM_DEB_BUILD_ITERATION.md`**.

Before a **Combined drop**, copy every shipped **`*.deb`** (and SBOM if you attach it) into **one** directory, then **regenerate** **`SHA256SUMS`** (*Integrity* / *Combined drop* rows below).

### Pre-publish artifact checklist (CI vs maintainer)

Use this when deciding what to attach to **GitHub Releases** or copy into an **apt** pool — same files as **[`ci.yml`](../.github/workflows/ci.yml)** vs a **full-product** drop built off-CI.

**Integrity:** Regenerate **`SHA256SUMS`** whenever you add, replace, or combine **`*.deb`** / SBOM files from more than one directory or build step — the manifest must list **every** file you attach (same command family as *Manual checksums* below).

| Scenario | What to publish | Verify before users install |
|----------|-----------------|----------------------------|
| **Stack only** (default PR CI) | Download artifact **`le-vibe-deb`**: **`le-vibe_*_all.deb`**, **`SHA256SUMS`**, **`le-vibe-python.cdx.json`** | In the extracted folder: **`sha256sum -c SHA256SUMS`** |
| **Stack + IDE** (maintainer **§7.3**) | **`le-vibe_*_all.deb`** and **`le-vibe-ide_*_amd64.deb`**, one **`SHA256SUMS`** covering **every** `*.deb` and the SBOM line you ship | **`sha256sum -c SHA256SUMS`**; build both with **`packaging/scripts/build-le-vibe-debs.sh --with-ide`** — **Full-product install** on success — **[`PM_DEB_BUILD_ITERATION.md`](PM_DEB_BUILD_ITERATION.md)** (*Success output (`--with-ide`)*); install order — *Install both packages* in **[`packaging/debian-le-vibe-ide/README.md`](../packaging/debian-le-vibe-ide/README.md)** |
| **Combined drop** (CI stack artifact + **IDE** built separately) | Download **`le-vibe-deb`** for the stack **`.deb`**, **`le-vibe-python.cdx.json`**, and the CI **`SHA256SUMS`**; add **`le-vibe-ide_*_amd64.deb`** from **`build-le-vibe-ide-deb.sh`** (or a prior **`--with-ide`** run) into the **same** directory — then **regenerate** **`SHA256SUMS`** so it lists **every** shipped **`*.deb`** **and** the SBOM (**Integrity** above). The CI manifest alone is **not** valid after you add the second **`.deb`**. | **`sha256sum -c SHA256SUMS`** or **`lvibe verify-checksums`**; same **Publishing** / **Integrity** story as **[`ci-qa-hardening.md`](ci-qa-hardening.md)** *Optional full Linux compile* |

**Checklist shorthand (what lands in one release directory / GitHub Release):**

- **Stack only** — from **`le-vibe-deb`**: **`le-vibe_*_all.deb`**, **`le-vibe-python.cdx.json`**, **`SHA256SUMS`** (CI manifest already consistent).
- **Stack + IDE (one maintainer run)** — **`build-le-vibe-debs.sh --with-ide`**: both **`*.deb`** files **plus** **`le-vibe-python.cdx.json`** if you ship it, **one** **`SHA256SUMS`** covering everything you attach (*Integrity*).
- **Combined drop** — start from the CI **`le-vibe-deb`** tree, add **`le-vibe-ide_*_amd64.deb`**, **regenerate** **`SHA256SUMS`** before **`sha256sum -c`** / **`gh release create`**.

### Minimum directory layout (readiness gate)

Use this **before** **`sha256sum -c SHA256SUMS`**, **`lvibe verify-checksums`**, or **`gh release create`** attachments:

- **Stack-only (matches default CI):** one directory containing **`le-vibe_*_all.deb`**, **`le-vibe-python.cdx.json`**, and **`SHA256SUMS`** — the manifest must list **every** blob you ship (same three path families **[`.github/workflows/ci.yml`](../.github/workflows/ci.yml)** uploads as **`le-vibe-deb`**).
- **Stack + IDE:** same folder **plus** **`le-vibe-ide_*_amd64.deb`**, then **rewrite** **`SHA256SUMS`** (do **not** reuse the CI file unchanged after adding the IDE **`.deb`** — *Combined drop* row above).

**Fetch CI artifacts:** **`gh run download <RUN_ID> -n le-vibe-deb -D ./release-dir`** or **Actions → workflow run → Artifacts** — unzip so **`SHA256SUMS`** and the files it names sit together (*GitHub Releases + checksums*).

**Versioning:** bump **`debian/changelog`** and fold **`CHANGELOG.md`** **`[Unreleased]`** into a dated section before tagging — see *Versioned changelog* above. **Hosted apt** server layout stays out of this repo (secrets, DNS, TLS) — use *Private or team apt repo* for tooling only.

### IDE package (`le-vibe-ide`, STEP 14 / §7.3)

**Engineering queue:** The Master orchestrator runs **0 → 1 → 14 → 2–13 → 15–17** — **STEP 14** (**§7.3** IDE **`.deb`**) is **next after baseline regression**, not a late add-on. See **[`PROMPT_BUILD_LE_VIBE.md`](PROMPT_BUILD_LE_VIBE.md)** (*ORDERED WORK QUEUE*, *Rolling iteration — prefer continuation*) and **[`PM_STAGE_MAP.md`](PM_STAGE_MAP.md)** *Execution order* / **STEP 16**. This H1 document covers **publishing** the IDE **`.deb`** once it exists.

**Compile fail-fast (STEP 14, same as `./editor/smoke.sh` / `build-le-vibe-ide.yml` *linux_compile*):** **`packaging/scripts/ci-vscodium-bash-syntax.sh`** → **`packaging/scripts/ci-editor-nvmrc-sync.sh`** → **`packaging/scripts/ci-vscodium-linux-dev-build.sh`** (→ **`editor/vscodium/dev/build.sh`**) — **[`PRODUCT_SPEC.md`](PRODUCT_SPEC.md)** *Prioritization*; **[`editor/BUILD.md`](../editor/BUILD.md)** (*CI*).

Default **`ci.yml`** artifacts ship the **stack** **`le-vibe`** **`.deb`** only. The **Lé Vibe IDE** is a **sibling** Debian source under **`packaging/debian-le-vibe-ide/`**: after **`editor/vscodium/VSCode-linux-*`** exists, run **`packaging/scripts/build-le-vibe-ide-deb.sh`** (or **`packaging/scripts/build-le-vibe-debs.sh --with-ide`** with the stack — **[`docs/PM_DEB_BUILD_ITERATION.md`](PM_DEB_BUILD_ITERATION.md)**). Full story — **[`packaging/debian-le-vibe-ide/README.md`](../packaging/debian-le-vibe-ide/README.md)**, **[`editor/BUILD.md`](../editor/BUILD.md)**. **Incomplete Linux build:** if **`VSCode-linux-*/bin/codium`** is missing, finish **`dev/build.sh`** — **[`editor/BUILD.md`](../editor/BUILD.md)** (*Partial tree*, **14.c**); **[`docs/PM_DEB_BUILD_ITERATION.md`](PM_DEB_BUILD_ITERATION.md)** (*Partial VSCode-linux tree*); **`./editor/print-built-codium-path.sh`**, **`./editor/print-vsbuild-codium-path.sh`** (and **`packaging/scripts/stage-le-vibe-ide-deb.sh`**) surface the same failure mode before **`dpkg-buildpackage`**. **`packaging/scripts/build-le-vibe-ide-deb.sh --help`** lists the same triage and **`verify-step14-closeout.sh`** pointers as the other STEP 14 scripts.

**Maintainer build output:** Successful **`build-le-vibe-debs.sh --with-ide`** prints a **Full-product install** line (**`sudo apt install`** with both resolved **`.deb`** paths) — **[`docs/PM_DEB_BUILD_ITERATION.md`](PM_DEB_BUILD_ITERATION.md)** (*Success output (`--with-ide`)*). Installing both from one directory (or equivalent) — **[`packaging/debian-le-vibe-ide/README.md`](../packaging/debian-le-vibe-ide/README.md)** (*Install both packages*). Local close-out gate: **`packaging/scripts/verify-step14-closeout.sh --require-stack-deb`** (add **`--apt-sim`** for explicit dependency simulation, **`--json`** for machine-readable success output; **`apt_sim_note`** — **[`docs/PM_DEB_BUILD_ITERATION.md`](PM_DEB_BUILD_ITERATION.md)** (*`--json` close-out payload*)). For the remaining maintainer-host install/launch smoke, run **`packaging/scripts/manual-step14-install-smoke.sh`** (or **`--print-install-cmd`** to emit an exact install command, **`--json`** for machine-readable paths/install command). The smoke helper’s **`--help`** and checklist assume **`verify-step14-closeout.sh --require-stack-deb`** already passed on the **build machine** where the **`.deb`** files were produced; perform **`sudo apt install`** and follow-up checks on a **test host** — same ordering as **`packaging/debian-le-vibe-ide/README.md`** (*Install both packages*).

**Release QA (optional):** **`LEVIBE_EDITOR_GATE_ASSERT_BRAND=1 packaging/scripts/build-le-vibe-debs.sh --with-ide`** runs **`ci-editor-gate.sh`** before IDE staging (§7.3 **`product.json`** identity) — **[`docs/PM_DEB_BUILD_ITERATION.md`](PM_DEB_BUILD_ITERATION.md)** (*Pre-staging gate*); **[`editor/BUILD.md`](../editor/BUILD.md)** (*Debian package for the Lé Vibe IDE*).

For a **release** that demos the **full** stack + branded editor, attach **`le-vibe-ide_*_amd64.deb`** alongside **`le-vibe_*_all.deb`** when both exist; add both **`*.deb`** lines to **`SHA256SUMS`** and run **`sha256sum -c SHA256SUMS`** before publishing.

## GitHub Releases + checksums

> **H1 quick pointer:** Use the ordered checklists *Checklist — stack-only GitHub Release* and *Checklist — full-product GitHub Release* (above) before you **`gh release create`** — same *Dual changelog discipline* / *Pre-publish* / **Combined drop** story as the sections above.

**Combined drop (same as *Pre-publish* above):** If the stack **`le-vibe_*_all.deb`** comes from downloading CI **`le-vibe-deb`** and **`le-vibe-ide_*_amd64.deb`** from a **separate** maintainer build, **regenerate** **`SHA256SUMS`** in your release directory **before** **`sha256sum -c`**, **`lvibe verify-checksums`**, or **`gh release create`** — the CI **`SHA256SUMS`** alone is wrong once the second **`*.deb`** is present (*Pre-publish artifact checklist* — **Combined drop**).

When you cut a **release** (tag + GitHub Release):

1. Pick a **green** workflow run on **`main`** / **`master`** (or build locally with **`dpkg-buildpackage -us -uc -b`** and regenerate checksums as below).
2. Download artifact **`le-vibe-deb`** (ZIP from **Actions → workflow run → Artifacts**), or use the **`gh`** CLI:  
   `gh run download <run-id> -n le-vibe-deb -D ./release-dir`  
   Unzip the bundle so **`SHA256SUMS`**, **`*.deb`**, and **`le-vibe-python.cdx.json`** sit in one directory (same layout after **`gh run download`** — the artifact is a **`.zip`** wrapper around those files).
3. Attach to the GitHub Release: **`*.deb`**, **`SHA256SUMS`**, and optionally **`le-vibe-python.cdx.json`** (already listed in **`SHA256SUMS`**).
4. Paste **`CHANGELOG.md`** section for that version into the Release description.
5. **Optional (`gh` CLI):** after you push a **version tag** that matches **`debian/changelog`** / **`CHANGELOG.md`** (see *Tagging discipline* above), you can attach the same files in one step, for example:  
   `gh release create v0.1.0 ./le-vibe_*_all.deb ./SHA256SUMS ./le-vibe-python.cdx.json --notes-file CHANGELOG-snippet.md`  
   (paths relative to your release directory; **`gh`** must be authenticated — `gh auth login`. Full-product drops add **`le-vibe-ide_*_amd64.deb`** to the file list.)

**Verify before install** (run inside the directory that contains **`SHA256SUMS`** and the files named on the right-hand side of each line — typically the extracted artifact folder):

```bash
sha256sum -c SHA256SUMS
```

Same check via the **`le-vibe`** CLI after the stack **`.deb`** is installed: **`lvibe verify-checksums -C .`** (or **`-C /path/to/extracted-artifact`**); **`--json`** for scripts — **[`le-vibe/README.md`](../le-vibe/README.md)** *Release channel / checksums (STEP 8 / H1)*.

### Release assets vs `SHA256SUMS` (sanity)

Every file named on the **right-hand side** of **`SHA256SUMS`** must exist **beside** **`SHA256SUMS`** in the release directory before **`sha256sum -c`** (or **`lvibe verify-checksums`**) succeeds. If you **omit** an optional attachment (e.g. **`le-vibe-python.cdx.json`**) from a GitHub Release, **regenerate** **`SHA256SUMS`** so it does not reference a missing path — same **Integrity** rule as *Pre-publish* above.

Then install the **`.deb`**:

```bash
sudo apt install ./le-vibe_*_all.deb
```

(`apt install ./file.deb` resolves dependencies from configured apt sources.)

**Manual checksums** (e.g. local build without SBOM path):

```bash
sha256sum le-vibe_*_all.deb le-vibe-python.cdx.json > SHA256SUMS
sha256sum -c SHA256SUMS
```

Optional: sign **`SHA256SUMS`** with **`gpg --clearsign`** and publish **`SHA256SUMS.asc`**; users verify with **`gpg --verify`**. Key handling is described in **[`docs/sbom-signing-audit.md`](sbom-signing-audit.md)**.

## Private or team apt repo (overview)

Hosting a real **apt** repository usually means: a web root (or object storage) with **`Packages`**, **`Release`**, and **`InRelease`** (or **`Release.gpg`**), plus a **pool/** of **`*.deb`** files. Two common toolchains:

### reprepro

- One-off imports: **`reprepro includedeb suite /path/to/package.deb`**
- Typical layout: a single directory holding **`conf/distributions`**, **`conf/options`**, **`db/`**, **`dists/`**, **`pool/`**
- Signing: set **`SignWith: default`** (or a key id) in **`conf/distributions`** so **`Release`** is signed; clients need your **GPG** key in **`apt-key`** / **`signed-by=`** (modern apt prefers a keyring file under **`/etc/apt/trusted.gpg.d/`** or **`Signed-By`** in the source line)

See **`man reprepro`** and Debian wiki “LocalAPTRepository” for full examples.

### aptly

- **`aptly repo create -distribution=…`** then **`aptly repo add …`**, **`aptly publish repo …`**
- Publishes a **`public/`** tree you sync to HTTPS; supports signing on publish

See **`https://www.aptly.info/`** for CLI details.

### Client snippet (after you publish)

Users add something like:

```text
deb [signed-by=/usr/share/keyrings/le-vibe-archive-keyring.gpg] https://releases.example.com/le-vibe/apt stable main
```

Exact **`signed-by`** and URL depend on how you host keys and the repository. Do not ship private keys in this repo; use CI secrets or offline signing.

## What stays in this repository

- **Source:** `debian/`, `packaging/`, CI that builds, verifies checksums, and uploads artifacts.
- **Not required in-tree:** full **reprepro**/**aptly** config for your domain — that is org-specific (DNS, TLS, signing keys, mirror layout).

For product positioning and **`editor/`** / IDE shell notes, see **`README.md`** and **`docs/vscodium-fork-le-vibe.md`**.

## Related docs

| Doc | Role |
|-----|------|
| [`PRODUCT_SPEC_SECTION8_EVIDENCE.md`](PRODUCT_SPEC_SECTION8_EVIDENCE.md) | **E1** regression audit + *Last verified* — refresh when **H1** release / packaging copy shifts (same **`pytest`** bar as *E1 / acceptance* above) |
| [`ci-qa-hardening.md`](ci-qa-hardening.md) | Smoke script, **lintian**, CI step order (H3); **optional `linux_compile`** (*Optional full Linux compile*, STEP 14.e) — opt-in CI **`vscodium-linux-build.tar.gz`** / unpack **`VSCode-linux-*`** before **`le-vibe-ide`** **`.deb`** (not default PR CI). *Related docs* in the same file lists **[`editor/README.md`](../editor/README.md)** (*Full Linux compile* / **H3** maintainer index). |
| [`sbom-signing-audit.md`](sbom-signing-audit.md) | **`pip-audit`**, CycloneDX SBOM next to **`.deb`** (H2) |
| [`CHANGELOG.md`](../CHANGELOG.md) | **Keep a Changelog** narrative for GitHub Release bodies — same **`x.y.z`** as **`debian/changelog`** before you tag (*Dual changelog discipline* above) |
| [`PM_DEB_BUILD_ITERATION.md`](PM_DEB_BUILD_ITERATION.md) | Maintainer **`packaging/scripts/build-le-vibe-debs.sh`** — stack + optional **`--with-ide`** (STEP 14 / §7.3); **Compile fail-fast:** **`ci-vscodium-bash-syntax.sh`** → **`ci-editor-nvmrc-sync.sh`** → **`ci-vscodium-linux-dev-build.sh`** (same as **`./editor/smoke.sh`** / **`linux_compile`**) — *IDE package* above; **Publishing** / **`DEB_BUILD_OPTIONS`** — pairs with *Pre-publish* / **Combined drop** / **`dpkg-parsechangelog`** above |
| [`PM_STAGE_MAP.md`](PM_STAGE_MAP.md) | Roadmap **H1** (STEP 8) vs §7.3 **`.deb`** bundles (STEP 14) — same honesty bar as **[`spec-phase2.md`](../spec-phase2.md)** *CI `le-vibe-deb` vs maintainer `le-vibe-ide`* |
| [`.github/workflows/ci.yml`](../.github/workflows/ci.yml) | Canonical workflow; artifact bundle **`le-vibe-deb`** |
