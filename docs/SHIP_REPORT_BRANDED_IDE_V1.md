# Ship report — Branded Lé Vibe IDE v1 (local self-install + stable orchestration baseline)

**Date:** 2026-04-14  
**Scope:** v1 lock note + branded IDE local flow stability + UX/troubleshooting + orchestrator baseline evidence (Linux local usage).

---

## Acceptance checklist

| Acceptance criterion | Status | Evidence |
|---|---|---|
| 1) `.lvibe` v1 lock note complete | ✅ | [`LVIBE_V1_LOCK_NOTE.md`](LVIBE_V1_LOCK_NOTE.md), [`docs/README.md`](README.md) row, contract test `test_docs_readme_lvibe_v1_lock_note_row_contract.py` |
| 2) Branded IDE end-to-end local path complete | ✅ | [`install-le-vibe-local.sh`](../packaging/scripts/install-le-vibe-local.sh), [`LOCAL_INSTALL_ONE_SHOT.md`](LOCAL_INSTALL_ONE_SHOT.md), `verify-step14-closeout.sh --require-stack-deb` |
| 3) Stability evidence (matrix + deterministic remediation) | ✅ | native + Docker evidence in [`SHIP_REPORT_LOCAL_INSTALL.md`](SHIP_REPORT_LOCAL_INSTALL.md); preflight determinism fields + warnings |
| 4) Orchestrator behavior evidence | ✅ | Continue/workspace/orchestrator tests + user-gate strings (`USER RESPONSE REQUIRED`) in contracts |
| 5) UX/docs coherence | ✅ | root README user-focused; maintainer depth in docs; installer docs updated for preflight JSON and risk signals |
| 6) Regression bar | ✅ | `cd le-vibe && python3 -m pytest tests/` green; STEP 14 close-out green |

---

## Canonical local path

| Action | Command |
|---|---|
| Preflight only | `./packaging/scripts/install-le-vibe-local.sh --preflight-only` |
| Preflight JSON (automation-friendly) | `./packaging/scripts/install-le-vibe-local.sh --preflight-only --json` |
| Build stack + IDE artifacts | `./packaging/scripts/install-le-vibe-local.sh` |
| Build + install + smoke | `./packaging/scripts/install-le-vibe-local.sh --install --yes` |
| STEP 14 strict close-out | `./packaging/scripts/verify-step14-closeout.sh --require-stack-deb` |

---

## Orchestrator baseline evidence (v1)

Representative suites used to keep local orchestrated behavior predictable:

- `python3 -m pytest le-vibe/tests/test_continue_workspace.py -q`
- `python3 -m pytest le-vibe/tests/test_session_orchestrator.py -q`
- `python3 -m pytest le-vibe/tests/test_launcher_master_orchestrator.py -q`
- `python3 -m pytest le-vibe/tests/test_product_spec_section8.py -q`

These guard:

- `.continue/rules` memory/welcome behavior,
- session manifest seeding and epic/task traversal,
- launcher orchestration entry points,
- user-gate and spec-aligned contract text.

---

## Stability / UX hardening notes included

- Installer preflight warns on dirty `editor/vscodium` submodule tree (non-blocking reproducibility signal).
- Preflight JSON now includes `submodule_state`, `node_state`, and `disk_state`.
- Low-disk warning surfaced before long compile runs.
- Existing host dependency and node mismatch messaging retained with actionable next commands.

---

## Known limitations (v1, accepted)

- Default PR CI does not run full Electron compile every time (resource-heavy); installer contracts + close-out gates remain enforced.
- Local host resources still dominate compile reliability (time/disk/RAM), with mitigations documented.
- `.lvibe` is v1-locked (maintenance only); major redesign or new architecture is deferred to explicit v2 authorization.

---

## Statement

**Branded Lé Vibe IDE v1 (local self-install + stable orchestration baseline) is SHIPPED.**
