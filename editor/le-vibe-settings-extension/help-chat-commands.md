# Lé Vibe — Chat commands & mentions (help)

Static copy aligned with **docs/PM_IDE_SETTINGS_AND_WORKFLOWS.md** §1 (product goal table).

## Settings (overview)

| Area | Behavior |
|------|----------|
| **`.lvibe/` size cap** | **10–500 MB**, default **50 MB**; global default may live in **`~/.config/le-vibe/user-settings.json`**; per-workspace overrides stay in **`workspace-policy.json`** when set at consent. |
| **Model** | **Recommended** (hardware tier in **`locked-model.json`**) vs **override tag** (e.g. `mistral:latest`). Optional **pull if disk OK** — stack checks free disk before pulling. |
| **New workspace defaults** | Toggle hints for first open (welcome, workflow pointers). |
| **Help — mentions & commands** | This panel: **`/setup-workspace`**, **`/agent <role_id>`**, **`@<role>`** → **`.lvibe/agents/<id>/skill.md`**. |

## Commands

- **`/setup-workspace`** — Walks the onboarding Q&A. Completion: empty **`.lvibe/.workspace-context-seeded`**. Until then, Continue rules may append a short footer pointing to the workflow file.
- **`/agent <role_id>`** — Steer using **`.lvibe/agents/<role_id>/skill.md`** (example: **`/agent product_manager`**).

## Mentions

- **`@<role>`** — Same idea as **`/agent`**; maps to **`.lvibe/agents/<id>/skill.md`**.

## Workflow file (setup-workspace)

In your **open workspace folder**, after Lé Vibe has prepared **`.lvibe/`**:

**`.lvibe/workflows/setup-workspace.md`**

Upstream template in the Lé Vibe product repo: **`le-vibe/templates/workflows/setup-workspace.md`**.

Use the button in this panel to open the file when it exists.
