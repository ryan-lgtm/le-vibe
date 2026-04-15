# Edit proposal contract (v1)

Epic **N9** — assistant output that drives **preview → apply** flows must validate before any workspace mutation.

## Machine-readable schema

- **JSON Schema:** [`schemas/levibe.edit-proposal.v1.json`](schemas/levibe.edit-proposal.v1.json) (Draft 2020-12; `$id` for stable reference).

## Runtime validation

- **Module:** [`edit-proposal.js`](edit-proposal.js) exports `validateEditProposal(raw)` — same rules as the schema, implemented without extra npm dependencies.

## Shape (summary)

| Field | Required | Notes |
|--------|----------|--------|
| `kind` | yes | Must be exactly `levibe.edit_proposal.v1`. |
| `proposals` | yes | Non-empty array of per-file edits. |
| `rationale` | no | Human-readable reason; max 16000 chars. |
| `confidence` | no | Optional `score` (0–1) and/or `flags` (snake_case tokens). |

Each **proposal** has:

- `targetUri` — `file://` URI for the workspace file.
- `edit` — either:
  - **`range_replace`:** VS Code–style 0-based `range` (`start` / `end` positions) + `newText`, or
  - **`full_file`:** `content` string replacing the entire file.

Malformed payloads must be rejected by `validateEditProposal` before UI apply (see `test/edit-proposal.test.js`).

**Preview before write (Epic N9):** the panel can show a unified diff (`edit-preview.js`) and gate applies with **`leVibeNative.requireEditPreviewBeforeApply`** — see **`README.md`** *Edit preview before apply*.

**Apply:** validated proposals are written with **`workspace-edit-apply.js`** (`applyEditProposalBatchAsWorkspaceEdit`) — one **`WorkspaceEdit`** per accepted batch for editor-friendly undo.
