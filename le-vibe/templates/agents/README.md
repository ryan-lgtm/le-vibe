# Agent skill templates

These files are copied to **`.lvibe/agents/<agent_id>/skill.md`** when missing (workspace prepare or **`lvibe sync-agent-skills`**). Keep each skill **bounded**—short persona and priorities, not unbounded logs.

Under storage pressure, **compaction** trims shared **`rag/`** / **`chunks/`** and incremental memory **before** shortening per-agent `skill.md` (see **PRODUCT_SPEC §5.5**).
