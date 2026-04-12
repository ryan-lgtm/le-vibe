# Lé Vibe — CI and QA hardening (Roadmap H3)

This document describes what **GitHub Actions** enforces, what **`packaging/scripts/ci-smoke.sh`** runs locally, and what remains **manual**.

**Product anchor:** [`PRODUCT_SPEC.md`](PRODUCT_SPEC.md) §8 (secrets / agent policy) and §9 (orchestration + evidence roster). **Roadmap H3** (this doc) is indexed from [`README.md`](README.md) and [`PROMPT_BUILD_LE_VIBE.md`](PROMPT_BUILD_LE_VIBE.md).

**Install UX:** Passing CI does not replace **`/usr/share/doc/le-vibe/README.Debian`** ([`debian/le-vibe.README.Debian`](../debian/le-vibe.README.Debian)) on installed systems — **§5** workspace memory consent before **`.lvibe/`** is created.

**E1 / acceptance:** **`ci-smoke.sh`** ends with **`pytest`** (full **`le-vibe/tests/`**, incl. **`test_issue_template_h8_contract.py`** — **H8** / **STEP 12** substring anchors for **`.github/ISSUE_TEMPLATE/*.yml`**; full **E1** scope — root **[`README.md`](../README.md)** *Tests* / **E1 mapping** and **[`spec-phase2.md`](../spec-phase2.md) §14** *Honesty vs CI*) — for full product regression (not only CI parity), run **`cd le-vibe && python3 -m pytest tests/`** locally and consult **[`PRODUCT_SPEC_SECTION8_EVIDENCE.md`](PRODUCT_SPEC_SECTION8_EVIDENCE.md)** when behavior under **§1**/**H8** + **§5–§10** changes; see **[H1](apt-repo-releases.md)** / **[H2](sbom-signing-audit.md)** *E1* notes for release-time checks.

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

**Scope:** **[`.github/workflows/ci.yml`](../.github/workflows/ci.yml)** header comments cite **`spec-phase2.md` §14** and **H8** (**`docs/README`** *Product surface* / **`SECURITY`** / **`privacy-and-telemetry`** *E1* — same trust chain as **`packaging/scripts/ci-smoke.sh`**). **[`.github/dependabot.yml`](../.github/dependabot.yml)** and **[`.github/ISSUE_TEMPLATE/`](../.github/ISSUE_TEMPLATE/)** (**[`config.yml`](../.github/ISSUE_TEMPLATE/config.yml)** **`#` H8**) document the same **H8** chain (weekly **pip** + **Actions** bump PRs; reporter-facing template **`#`** lines; **H2** follow-up per **`sbom-signing-audit.md`**). A green CI run proves **this** tree’s **`.deb`** + Python supply chain, not a separate **H6** editor build or **H7** alternate bundle. **[`SECURITY.md`](../SECURITY.md)** *Related docs* lists optional **[`rag/le-vibe-phase2-chunks.md`](rag/le-vibe-phase2-chunks.md)** (*RAG / embeddings*, non-canonical) alongside the same **H8** index — refresh if **`SECURITY`** / trust copy shifts.

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
4. **`pytest`** for **`le-vibe/tests/`** (installs **`requirements.txt`** + **`pytest`**; full suite — **H8** via **`test_issue_template_h8_contract.py`**; see root **[`README.md`](../README.md)** *Tests* for **E1** roster)
5. **`desktop-file-validate`** on **`packaging/applications/le-vibe.desktop`** and **`packaging/autostart/le-vibe-continue-setup.desktop`** (needs **`desktop-file-utils`**)

On **GitHub Actions**, missing **`desktop-file-validate`** is a **failure**. Locally, it **skips** desktop validation with a notice unless you install **`desktop-file-utils`**.

## What is not automated here

- **ShellCheck** on every script — optional locally (`shellcheck packaging/scripts/*.sh`); not required in default CI to keep images small.
- **Headless GUI E2E** (full editor + Continue chat) — intentionally out of default CI; use the manual checklist in **[`README.md`](../README.md)** (Release / QA section).

## Related docs

- **[`.github/workflows/ci.yml`](../.github/workflows/ci.yml)** — canonical **CI** job (artifact **`le-vibe-deb`**)  
- **[`docs/apt-repo-releases.md`](apt-repo-releases.md)** — artifacts, checksums, Releases (H1), **`CHANGELOG.md`** / **`debian/changelog`** when tagging  
- **[`docs/sbom-signing-audit.md`](sbom-signing-audit.md)** — **`pip-audit`**, SBOM (H2)  
- **[`docs/continue-extension-pin.md`](continue-extension-pin.md)** — Open VSX pin verification in smoke (H4)  
- **[`spec-phase2.md`](../spec-phase2.md) §14** — honest split: default CI validates **this** tree’s **`.deb`** + Python stack, not **H6**/**H7** bundles  
- **[`CHANGELOG.md`](../CHANGELOG.md)** — promote **`[Unreleased]`** when a green CI build becomes a tagged release (same rhythm as **H1**)  
