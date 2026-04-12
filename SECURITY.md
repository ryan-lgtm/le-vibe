# Security policy (Lé Vibe)

## Scope

This policy applies to **Lé Vibe** code in **this** repository: the **`le-vibe`** Python modules, shell helpers, and **Debian** packaging. Data flows and local logging are summarized in **[`docs/privacy-and-telemetry.md`](docs/privacy-and-telemetry.md)**.

**Upstream** components (**Ollama**, **Continue**, **VSCodium** / **Electron**, kernel, libc) have their own CVE and disclosure processes—report issues there when the defect is not in our launcher or packaged files.

## Reporting

If you find a **security vulnerability** in Lé Vibe–shipped code:

1. **Preferred:** Use **GitHub [private security advisories](https://docs.github.com/en/code-security/security-advisories/about-repository-security-advisories)** for this repository (enable **Security → Private vulnerability reporting** in repository settings when you publish the repo).
2. **Otherwise:** Contact maintainers through a channel they list in the root **`README.md`**, or coordinate with repo owners before posting exploit details in public issues.

Please avoid public issues or discussions that disclose **exploit details** until a fix is agreed.

## Related docs

- **[`docs/PRODUCT_SPEC.md`](docs/PRODUCT_SPEC.md)** §8 — agent **secrets** policy (default deny on `.env` / env files; no secret values in `.lvibe/` RAG)  
- **[`docs/PRODUCT_SPEC.md`](docs/PRODUCT_SPEC.md)** §9 — **Relationship to existing specs** (formal roster of canonical docs, including orchestration and evidence)  
- **[`docs/PM_STAGE_MAP.md`](docs/PM_STAGE_MAP.md)** — orchestrator **STEP** → primary PM doc; **STEPS 13–14** (**H7** / **H6**) align with **[`spec-phase2.md`](spec-phase2.md) §14** when scoping “this repo” vs upstream or out-of-tree bundles  
- **[`docs/README.md`](docs/README.md)** — documentation index; **E1 / pytest** ties **`le-vibe/tests/`** to **`PRODUCT_SPEC_SECTION8_EVIDENCE`** and **`PM_STAGE_MAP` STEP 1**; *Product surface* (**STEP 12**, H8) — **[`.github/workflows/ci.yml`](.github/workflows/ci.yml)**, **[`.github/dependabot.yml`](.github/dependabot.yml)**, **[`.github/ISSUE_TEMPLATE/`](.github/ISSUE_TEMPLATE/)** (**[`config.yml`](.github/ISSUE_TEMPLATE/config.yml)** **`#` H8** maintainer lines; headers / intros cite **`privacy-and-telemetry`** (*E1 contract tests* — root **`README`** *Tests* / **`le-vibe/tests/`**), **`SECURITY`** where relevant, and optional **`docs/rag/le-vibe-phase2-chunks.md`** on **bug** / **feature** / **documentation** forms — *RAG / embeddings*, **`spec-phase2.md` §14*, non-canonical) — refresh E1 evidence when CI / Dependabot / reporter-facing copy changes  
- **[`docs/PRODUCT_SPEC_SECTION8_EVIDENCE.md`](docs/PRODUCT_SPEC_SECTION8_EVIDENCE.md)** — E1 regression evidence (**§1** naming / **H8**, §7 orchestration, §8 secrets policy, §10 acceptance; filename historic); **`le-vibe/tests/`** exercises Continue rules, workspace policy strings tied to **§8**, [**`test_session_orchestrator.py`**](le-vibe/tests/test_session_orchestrator.py) (STEP 2 — manifest ↔ schema), root / package **`README`** E1 roster ([**`test_root_readme_ai_pilot_contract.py`**](le-vibe/tests/test_root_readme_ai_pilot_contract.py), [**`test_le_vibe_readme_e1_contract.py`**](le-vibe/tests/test_le_vibe_readme_e1_contract.py)), and **H8** reporter-YAML substring anchors ([**`test_issue_template_h8_contract.py`](le-vibe/tests/test_issue_template_h8_contract.py)** — not a YAML parse)  
- **[`docs/privacy-and-telemetry.md`](docs/privacy-and-telemetry.md)** — localhost-first behavior, structured logs, third-party policies; *Related documentation* → **E1 contract tests** (root **`README`** *Tests*, **`le-vibe/README`**, **`le-vibe/tests/`** — no network)  
- **[`docs/sbom-signing-audit.md`](docs/sbom-signing-audit.md)** — dependency pins, SBOM, optional package signing  
- **[`CHANGELOG.md`](CHANGELOG.md)** — release notes; cross-check **pip** / supply-chain changes with **`pip-audit`** / **H2** when triaging dependency CVEs  
- **[`debian/le-vibe.README.Debian`](debian/le-vibe.README.Debian)** — shipped as **`/usr/share/doc/le-vibe/README.Debian`** on **`.deb`** installs; operator-facing paths and **§5** consent summary (full agent/secrets policy remains **[`docs/PRODUCT_SPEC.md`](docs/PRODUCT_SPEC.md)** §8)  
- **[`spec-phase2.md`](spec-phase2.md)** §14 — what **this repo** ships vs **deferred** editor fork (**H6**) / alternate bundles (**H7**); scope for vulnerability triage (upstream editor vs launcher)  
- **[`docs/rag/le-vibe-phase2-chunks.md`](docs/rag/le-vibe-phase2-chunks.md)** — optional non-canonical retrieval chunk (`lv-meta-overview`); **`spec-phase2.md`** *RAG / embeddings* (not a second source of truth)  
