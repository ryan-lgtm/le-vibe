# CP6 end-to-end acceptance (Lé Vibe Chat)

**Purpose:** one place to record whether Lé Vibe Chat is shippable for a given build: **automated gate** (machine) + **manual checklist** (human). Product track: **task-cp6-1**.

## Automated gate (exit code)

From **`editor/le-vibe-native-extension/`**:

```bash
npm run e2e-acceptance
```

- **Exit `0`** → **`e2e-acceptance: RESULT=PASS`** (runs **`npm run verify`**: unit tests + integration smoke).
- **Exit non-zero** → **`e2e-acceptance: RESULT=FAIL`**.

**Strict local Ollama (optional release sign-off):** when Ollama must be up on the same machine:

```bash
LEVIBE_E2E_ACCEPTANCE_STRICT_OLLAMA=1 npm run e2e-acceptance
```

This runs **`npm run verify`**, then **`node ./scripts/smoke-integration.js`** with **`LEVIBE_NATIVE_SMOKE_STRICT_OLLAMA=1`** so a failed Ollama probe fails the gate.

**Monorepo one-liner** (from repository root):

```bash
./packaging/scripts/levibe-chat-e2e-acceptance.sh
```

## Manual checklist (required for full CP6 sign-off)

Complete **after** the automated gate is **PASS**. Mark each row **PASS** or **FAIL**; any **FAIL** blocks release until remediated or explicitly waived by product.

| # | Area | What to verify | Result |
|---|------|----------------|--------|
| M1 | Chat + **Ollama** | Open **Lé Vibe Chat: Open Agent Surface**, send a short prompt with a live model; stream completes or surfaces a clear error (no stuck spinner). | |
| M2 | **Create / edit / delete** | In a folder workspace, use chat/panel flows (e.g. scaffold create, sample plan) so files under the workspace change as expected; no silent destructive writes outside the confirmed paths. | |
| M3 | **Preview → apply → undo** | Follow **`OPERATOR.md`** *E2E agentic editor release checklist* section **A — Preview → accept → apply → undo*. | |
| M4 | **Plan + cancel** | Same doc, section **B — Multi-step workspace plan → cancel mid-flight**. | |
| M5 | **Conflict / stale file** | Trigger an edit proposal apply when the file changed on disk after preview; expect deterministic conflict remediation (no blind overwrite). Regression coverage also runs under **`npm run verify`**. | |
| M6 | **Inline suggestions (optional)** | With **`leVibeNative.inlineSuggestionsEnabled`** **true**, confirm inline completions appear or fail gracefully; with **false**, confirm **Quick Fix** / selection assist still works (task-cp4-3). | |

**Sign-off**

| Build (tag / VSIX / git sha) | Date (YYYY-MM-DD) | Automated (`e2e-acceptance`) | Manual table | Sign-off |
|------------------------------|-------------------|-------------------------------|--------------|----------|
| | | PASS / FAIL | PASS / FAIL | |

## Related runbooks

- **`OPERATOR.md`** — *E2E agentic editor release checklist (Epic N15)* (preview, plan, cancel).
- **`OPERATOR.md`** — *Verify (canonical)* for **`npm run verify`** and smoke env vars.
