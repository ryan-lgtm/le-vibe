# Workspace plan contract (v1)

Epic **N10** — ordered multi-file operations produced by a model or orchestrator must validate before any disk write.

## Machine-readable schema

- [`schemas/levibe.workspace-plan.v1.json`](schemas/levibe.workspace-plan.v1.json)

## Runtime validation

- [`workspace-plan.js`](workspace-plan.js) — `validateWorkspacePlan(raw)` and `formatPlanValidationForUser(errors)` (same rules; no extra npm deps).

## Shape

| Field | Required | Notes |
|--------|----------|--------|
| `kind` | yes | Exactly `levibe.workspace_plan.v1`. |
| `steps` | yes | Non-empty array; each step has unique `id`. |

### Step kinds (`op`)

| `op` | Required fields |
|-----|------------------|
| `create_file` | `targetUri` (`file://`), optional `content` |
| `apply_edit` | `targetUri`, `edit` (same shape as **`levibe.edit_proposal.v1`** per-file edit: `full_file` or `range_replace`) |
| `delete_file` | `targetUri` |
| `move_file` | `fromUri`, `toUri` |

Invalid plans return a single **`userMessage`** string suitable for `showErrorMessage` / panel status — no partial execution in consumers that call `validateWorkspacePlan` first.

## Rollback after mid-plan failure (Epic N10)

When **`executeValidatedWorkspacePlan`** stops on a **failed** step after one or more steps completed successfully:

1. **User-visible:** the panel chat stream includes an explicit partial-state line and offers **Undo completed steps** (enabled only when there is something to revert).
2. **Semantics:** inverses are derived from snapshots taken **immediately before** each step (file bytes / existence). The extension applies those inverses **in reverse order** via `WorkspaceEdit` (same undo-friendly path as forward edits — not raw shell `rm`).
3. **Best-effort:** if the workspace changed again before rollback (conflicts, external edits), a rollback step may fail; the panel reports how many inverse steps ran before the error.
4. **Cancel:** stopping a run with **Cancel plan run** does **not** auto-undo completed steps (user may keep partial work); only **failure** arms the rollback affordance for the completed prefix in the current implementation.

Structured audit: `workspace_plan_rollback` events in **`workspace-plan-audit.jsonl`** record how many inverse steps completed.

## Dry-run (Epic N10)

**`dryRunValidatedWorkspacePlan`** (see [`workspace-plan-dry-run.js`](workspace-plan-dry-run.js)) walks a **validated** plan and prints per-step **rough** byte/token estimates **without** applying `WorkspaceEdit`s. Reads are allowed only to measure existing files (capped read size for very large files). Token figures are a **bounded heuristic** (UTF-8 bytes ÷ 4), not a real tokenizer. Panel demo: **Dry-run sample plan** before **Run sample workspace plan**.
