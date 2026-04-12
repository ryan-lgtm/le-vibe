# Lé Vibe — CI and QA hardening (Roadmap H3)

This document describes what **GitHub Actions** enforces, what **`packaging/scripts/ci-smoke.sh`** runs locally, and what remains **manual**.

**Product anchor:** [`PRODUCT_SPEC.md`](PRODUCT_SPEC.md) §8 (secrets / agent policy) and §9 (orchestration + evidence roster). **Roadmap H3** (this doc) is indexed from [`README.md`](README.md) and [`PROMPT_BUILD_LE_VIBE.md`](PROMPT_BUILD_LE_VIBE.md).

**Install UX:** Passing CI does not replace **`/usr/share/doc/le-vibe/README.Debian`** ([`debian/le-vibe.README.Debian`](../debian/le-vibe.README.Debian)) on installed systems — **§5** workspace memory consent before **`.lvibe/`** is created.

**E1 / acceptance:** **`ci-smoke.sh`** runs full **`le-vibe/tests/`** **`pytest`** (incl. **`test_issue_template_h8_contract.py`** — **H8** / **STEP 12**; **`test_product_spec_section8.py`** — **`docs/PRODUCT_SPEC.md`** *Prioritization* / **`./editor/smoke.sh`**), then **`ci-editor-gate.sh`** (**H6**), then **`desktop-file-validate`** when installed — full **E1** scope: root **[`README.md`](../README.md)** *Tests* / **E1 mapping** and **[`spec-phase2.md`](../spec-phase2.md) §14** *Honesty vs CI*. For focused Python regression, run **`cd le-vibe && python3 -m pytest tests/`** locally and consult **[`PRODUCT_SPEC_SECTION8_EVIDENCE.md`](PRODUCT_SPEC_SECTION8_EVIDENCE.md)** when behavior under **§1**/**H8** + **§5–§10** changes; see **[H1](apt-repo-releases.md)** / **[H2](sbom-signing-audit.md)** *E1* notes for release-time checks.

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
| **Upload artifact** | **`le-vibe-deb`** bundle |

**Scope:** **[`.github/workflows/ci.yml`](../.github/workflows/ci.yml)** header comments cite **`spec-phase2.md` §14** and **H8** (**`docs/README`** *Product surface* / **`SECURITY`** / **`privacy-and-telemetry`** *E1* — same trust chain as **`packaging/scripts/ci-smoke.sh`**). **[`.github/dependabot.yml`](../.github/dependabot.yml)** and **[`.github/ISSUE_TEMPLATE/`](../.github/ISSUE_TEMPLATE/)** (**[`config.yml`](../.github/ISSUE_TEMPLATE/config.yml)** **`#` H8**) document the same **H8** chain (weekly **pip** + **Actions** bump PRs; reporter-facing template **`#`** lines; **H2** follow-up per **`sbom-signing-audit.md`**). A green **`ci.yml`** run proves **this** tree’s **`.deb`** + Python supply chain and runs **`ci-editor-gate.sh`** (STEP 14 / **H6** — layout, **`bash -n`**, **`editor/.nvmrc`**) after **`pytest`** via **`ci-smoke.sh`** — the same gate as **`./editor/smoke.sh`**. **[`build-le-vibe-ide.yml`](../.github/workflows/build-le-vibe-ide.yml)** is the dedicated **H6** workflow (**`editor/**`** PR paths, **`ide-v*`** tags, **`workflow_dispatch`**, **metadata** artifact upload); it is **not** the only place the gate runs. **H7** alternate bundles remain outside default **`ci.yml`**. **[`SECURITY.md`](../SECURITY.md)** *Related docs* lists optional **[`rag/le-vibe-phase2-chunks.md`](rag/le-vibe-phase2-chunks.md)** (*RAG / embeddings*, non-canonical) alongside the same **H8** index — refresh if **`SECURITY`** / trust copy shifts.

**Lintian:** `--color never` keeps logs readable in Actions. To fail on **warnings**, change **`--fail-on`** (expect more noise until maintainer fields and policy tags are clean). See **`man lintian`**.

## Smoke script (`packaging/scripts/ci-smoke.sh`)

Run from the **repository root**:

```bash
./packaging/scripts/ci-smoke.sh
```

It executes, in order:

1. **`verify-continue-pin.sh`** (H4) — semver in **`packaging/continue-openvsx-version`**
2. **`bash -n`** on **`packaging/bin/*`** — syntax check for **`lvibe`**, **`le-vibe`**, **`le-vibe-setup-continue`**, **`lvibe-hygiene`**
3. **Synthetic workspace hygiene** — **`PYTHONPATH=le-vibe`** Python snippet: **`ensure_lvibe_workspace`** + **`check_lvibe_workspace`** on a temp dir (same checks as **`python -m le_vibe.hygiene`** / **`lvibe-hygiene`**, E4). The subprocess sets **`LE_VIBE_LVIBE_CONSENT=accept`** for that snippet only (matches **`le-vibe/tests/conftest.py`**) so §5 automation intent stays explicit.
4. **`pytest`** for **`le-vibe/tests/`** (installs **`requirements.txt`** + **`pytest`**; full suite — **H8** via **`test_issue_template_h8_contract.py`**; **E1** incl. **`test_product_spec_section8.py`** — **`docs/PRODUCT_SPEC.md`** *Prioritization* / **`./editor/smoke.sh`**; see root **[`README.md`](../README.md)** *Tests* for **E1** roster)
5. **`ci-editor-gate.sh`** (STEP 14 / **H6**) — same layout / **`bash -n`** / **`editor/.nvmrc`** checks as **`./editor/smoke.sh`** and **[`build-le-vibe-ide.yml`](../.github/workflows/build-le-vibe-ide.yml)** (no Electron compile)
6. **`desktop-file-validate`** on **`packaging/applications/le-vibe.desktop`** and **`packaging/autostart/le-vibe-continue-setup.desktop`** (needs **`desktop-file-utils`**)

On **GitHub Actions**, missing **`desktop-file-validate`** is a **failure**. Locally, it **skips** desktop validation with a notice unless you install **`desktop-file-utils`**.

## IDE smoke (`editor/smoke.sh`, H6)

**`packaging/scripts/ci-smoke.sh`** runs **`ci-editor-gate.sh`** after **`pytest`** (step 5 above) — same gate. To run **only** the IDE checks without pin / wrappers / **`pytest`** / **`.desktop`**, from the **repository root**:

```bash
./editor/smoke.sh
```

That wrapper **`exec`**s **`packaging/scripts/ci-editor-gate.sh`**, matching **[`build-le-vibe-ide.yml`](../.github/workflows/build-le-vibe-ide.yml)** when sources are present. See **[`editor/README.md`](../editor/README.md)** and **[`docs/vscodium-fork-le-vibe.md`](vscodium-fork-le-vibe.md)**.

## What is not automated here

- **ShellCheck** on every script — optional locally (`shellcheck packaging/scripts/*.sh`); not required in default CI to keep images small.
- **Headless GUI E2E** (full editor + Continue chat) — intentionally out of default CI; use the manual checklist in **[`README.md`](../README.md)** (Release / QA section).

## Related docs

- **[`.github/workflows/ci.yml`](../.github/workflows/ci.yml)** — canonical **stack** **CI** job (artifact **`le-vibe-deb`**)  
- **[`build-le-vibe-ide.yml`](../.github/workflows/build-le-vibe-ide.yml)** — **H6** dedicated workflow (**`editor/**`** PRs, metadata artifacts); same **`ci-editor-gate`** as **`ci-smoke.sh`** / **`./editor/smoke.sh`**  
- **[`docs/apt-repo-releases.md`](apt-repo-releases.md)** — artifacts, checksums, Releases (H1), **`CHANGELOG.md`** / **`debian/changelog`** when tagging  
- **[`docs/sbom-signing-audit.md`](sbom-signing-audit.md)** — **`pip-audit`**, SBOM (H2)  
- **[`docs/continue-extension-pin.md`](continue-extension-pin.md)** — Open VSX pin verification in smoke (H4)  
- **[`spec-phase2.md`](../spec-phase2.md) §14** — honest split: **`ci.yml`** (via **`ci-smoke.sh`**) = stack **`.deb`** + **`pytest`** + **`ci-editor-gate`** (**H6** gate); **`build-le-vibe-ide.yml`** = **H6** **metadata** + **`editor/**`**-scoped runs; **H7** bundles optional/out-of-tree  
- **[`CHANGELOG.md`](../CHANGELOG.md)** — promote **`[Unreleased]`** when a green CI build becomes a tagged release (same rhythm as **H1**)  
