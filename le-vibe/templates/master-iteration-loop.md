# Master iteration loop — template pointer

**Canonical source:** [`docs/MASTER_ITERATION_LOOP.md`](../../docs/MASTER_ITERATION_LOOP.md) (spec + paste block). **Mode semantics (ENGINEER / PRODUCT_MANAGER / PROJECT, OWNER_DIRECTIVES, when the loop may stop):** [`docs/AGENT_MODE_ORCHESTRATION.md`](../../docs/AGENT_MODE_ORCHESTRATION.md).

**Paste-ready prompt (repo root):** `python3 packaging/scripts/print-master-iteration-loop-prompt.py` — copy **stdout** into Cursor. Same prompt for every hat; set `MODE:`, optional `OWNER_DIRECTIVES:`, and optional `CONTINUATION:` per [`docs/MASTER_ITERATION_LOOP.md`](../../docs/MASTER_ITERATION_LOOP.md) *Human workflow*.

**Engineering workflow:** After each **major track** or **milestone**, run **`git add`**, **`git commit`**, and **`git push`** — see **Git checkpoints** in [`docs/PROMPT_BUILD_LE_VIBE.md`](../../docs/PROMPT_BUILD_LE_VIBE.md) (Master orchestrator global rules) and [`docs/MASTER_ITERATION_LOOP.md`](../../docs/MASTER_ITERATION_LOOP.md).

This file exists so workspace seeds and docs can point at one stable path alongside `le-vibe/templates/agents/*.md`.
