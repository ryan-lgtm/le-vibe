# Lé Vibe — SBOM, vulnerability audit, and `.deb` signing (Roadmap H2)

**STEP 9 / PM map:** [`PM_STAGE_MAP.md`](PM_STAGE_MAP.md) — **H2** row links here, **[`le-vibe/requirements.txt`](../le-vibe/requirements.txt)**, **`pip-audit`** / **`cyclonedx-py`** in **`.github/workflows/ci.yml`**, **`le-vibe-python.cdx.json`**, and **[`.github/dependabot.yml`](../.github/dependabot.yml)** (pip bumps).

Supply-chain practices for the **Python** stack in **`le-vibe/`**, how they connect to **CI artifacts** and **[`docs/apt-repo-releases.md`](apt-repo-releases.md)**, and optional signing of Debian packages.

**CI wiring:** [`.github/workflows/ci.yml`](../.github/workflows/ci.yml) — job step **Python supply chain (H2)** runs **`pip-audit`** and **`cyclonedx-py`** before the `.deb` build; workflow header documents **H8** (**`docs/README`** *Product surface* / **`SECURITY`** / **`privacy-and-telemetry`** *E1*). **[`.github/dependabot.yml`](../.github/dependabot.yml)** header matches the same **H8** chain; **[`.github/ISSUE_TEMPLATE/`](../.github/ISSUE_TEMPLATE/)** (**[`config.yml`](../.github/ISSUE_TEMPLATE/config.yml)** **`#` H8**) completes the reporter-facing slice of that index. Weekly **pip** bump PRs should trigger the **H2** follow-up steps in this doc after merge. See **[`docs/ci-qa-hardening.md`](ci-qa-hardening.md)**. **[`SECURITY.md`](../SECURITY.md)** *Related docs* lists optional **[`rag/le-vibe-phase2-chunks.md`](rag/le-vibe-phase2-chunks.md)** (*RAG / embeddings*, non-canonical) beside the same **H8** roster.

**Product anchor:** [`PRODUCT_SPEC.md`](PRODUCT_SPEC.md) §8–§9 — must-ship secrets posture and the orchestration roster. **Roadmap H2** (this file) is indexed from [`README.md`](README.md) and [`PROMPT_BUILD_LE_VIBE.md`](PROMPT_BUILD_LE_VIBE.md) alongside **H1**/**H3** guides.

**Install UX:** **`apt install`** / **`.deb`** users should read **`/usr/share/doc/le-vibe/README.Debian`** (source [`debian/le-vibe.README.Debian`](../debian/le-vibe.README.Debian)) for post-install steps and **§5** **`.lvibe/`** consent; **[H1](apt-repo-releases.md)** covers release artifacts, checksums, and apt hosting.

**E1 / acceptance:** Changing **`le-vibe/requirements.txt`**, SBOM tooling, or **`pip-audit`** policy can shift §8–§10 posture — re-run **`cd le-vibe && python3 -m pytest tests/`** (full suite — **H8** / **STEP 12** via **`test_issue_template_h8_contract.py`**; see root **[`README.md`](../README.md)** *Tests* / **E1 mapping** and **[`spec-phase2.md`](../spec-phase2.md) §14** *Honesty vs CI* for the rest), **`pip-audit`**, and refresh **[`PRODUCT_SPEC_SECTION8_EVIDENCE.md`](PRODUCT_SPEC_SECTION8_EVIDENCE.md)** / **[`CHANGELOG.md`](../CHANGELOG.md)** when deps change materially (same rhythm as **[H1](apt-repo-releases.md)** *E1 / acceptance*).

**Supply-chain scope:** **`cyclonedx-py`** / **`pip-audit`** here apply to **`le-vibe/requirements.txt`** in **this** repository only. A branded editor fork (**H6**) or Flatpak/AppImage pipeline (**H7**) needs its **own** SBOM and audit story — see **[`spec-phase2.md`](../spec-phase2.md) §14**.

## SBOM (CycloneDX)

CI runs **`cyclonedx-py requirements`** against **`le-vibe/requirements.txt`** and writes **`le-vibe-python.cdx.json`** (JSON CycloneDX) into **`artifacts/`**. That file is included in **`SHA256SUMS`** next to the **`.deb`** (see **H1** in **[`docs/apt-repo-releases.md`](apt-repo-releases.md)**).

**`requirements.txt`** uses **exact version pins** (`==`) so SBOM components carry **resolved** versions and **`pip-audit`** checks match what reproducible installs resolve.

Regenerate locally:

```bash
cd le-vibe
python3 -m pip install cyclonedx-bom
cyclonedx-py requirements requirements.txt -o le-vibe-python.cdx.json --of JSON
```

## Vulnerability audit (`pip-audit`)

CI installs **`pip-audit`** (not listed in **`requirements.txt`** — it is a **CI/dev tool**) and runs **`pip-audit -r requirements.txt`** from **`le-vibe/`**. The job **fails** if [OSV](https://osv.dev/) reports known vulnerabilities for pinned dependencies.

Local check (match CI):

```bash
cd le-vibe
python3 -m pip install pip-audit
pip-audit -r requirements.txt
```

To inspect a specific advisory without changing files: **`pip-audit -r requirements.txt --desc on`**.

## Dependabot (Python)

[`.github/dependabot.yml`](../.github/dependabot.yml) includes **`package-ecosystem: pip`** for **`/le-vibe`** so GitHub can open PRs to bump pins in **`requirements.txt`**. The file header restates **§8–§9**, **`CHANGELOG.md`**, and this doc for maintainers. After merging bumps, run **`pip-audit`** locally and refresh SBOM expectations if you commit generated JSON anywhere.

## Signing the `.deb` (maintainer — offline or CI secrets)

CI builds **unsigned** packages (**`dpkg-buildpackage -us -uc`**) and uploads the **`.deb`** plus SBOM and checksums. For a **trusted apt channel**, you typically sign **repository metadata** (**`Release` / `InRelease`**) with **reprepro** or **aptly** (see **[`docs/apt-repo-releases.md`](apt-repo-releases.md)**), and optionally sign **individual `.deb`** files.

| Approach | Use case |
|----------|----------|
| **Repository signing** (`Release`, `InRelease`) | Users trust **`apt update`** from your apt repo; most common for team/internal mirrors. |
| **`debsign`** / **`dpkg-sig`** | Sign the **`.deb`** binary; users verify out-of-band or via a keyring you publish. |

**Rules of thumb**

- Keep **private keys** in **GitHub Environments**, **OIDC**-backed signing, or **offline** hardware; **never** commit keys to this repository.
- Publish a **GPG** public key or **keyring** (`.gpg`) for **`signed-by=`** in **`sources.list`** / **`.sources`** — same trust model as **[`docs/apt-repo-releases.md`](apt-repo-releases.md)**.
- For **checksum-only** releases (no apt repo), **`SHA256SUMS`** + optional **`gpg --clearsign`** on that file is enough for many users (also covered under **H1**).

## Alignment with CI artifacts

| Output | Purpose |
|--------|---------|
| **`le-vibe-python.cdx.json`** | CycloneDX SBOM for the pinned **`requirements.txt`** |
| **`pip-audit`** (exit non-zero on vulns) | Blocks merges with known vulnerable deps |
| **`SHA256SUMS`** | Integrity over **`.deb`** + SBOM (see **H1**) |

## Related docs

- **[`docs/apt-repo-releases.md`](apt-repo-releases.md)** — checksums, GitHub Releases, apt layout, **`CHANGELOG.md`** / **`debian/changelog`** when versioning  
- **[`CHANGELOG.md`](../CHANGELOG.md)** — user-facing notes; mention **`pip-audit`** / SBOM-affecting dep bumps when they are user-visible  
- **[`docs/continue-extension-pin.md`](continue-extension-pin.md)** — Open VSX pin (H4), separate from Python SBOM
