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
