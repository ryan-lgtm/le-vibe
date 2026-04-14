# Agent skill templates

These files are copied to **`.lvibe/agents/<agent_id>/skill.md`** when missing (workspace prepare or **`lvibe sync-agent-skills`**). Keep each skill **bounded**—short persona and priorities, not unbounded logs.

Under storage pressure, **compaction** trims shared **`rag/`** / **`chunks/`** and incremental memory **before** shortening per-agent `skill.md` (see **PRODUCT_SPEC §5.5**).

## Canonical SaaS role roster and aliases

Use this role set for orchestration and subagent debate:

- Subject Matter/Industry Expert (`@sme`) → `subject-matter-industry-expert.md`
- Senior Product Operations (`@props`) → `senior-product-operations.md`
- Senior Product Management (`@prod`) → `senior-product-management.md`
- Senior Backend Engineer (`@be-eng`) → `senior-backend-engineer.md`
- Senior Frontend Engineer (`@fe-eng`) → `senior-frontend-engineer.md`
- Senior DevOps Engineer (`@do-eng`) → `senior-devops-engineer.md`
- Senior Marketing (`@marketing`) → `senior-marketing.md`
- Senior Customer Success (`@cs`) → `senior-customer-success.md`
- Senior Revenue (`@rev`) → `senior-revenue.md`

## Legacy template compatibility (deprecated names)

These legacy files remain for backward compatibility and migration:

- `product-manager.md` → use `senior-product-management.md` (`@prod`)
- `project-manager.md` → use `senior-product-operations.md` (`@props`)
- `senior-industry-advisor.md` → use `subject-matter-industry-expert.md` (`@sme`)
- `senior-qa-engineer.md` → quality responsibilities are now shared across engineering + product ops with customer-facing readiness from `@marketing`, `@cs`, and `@rev`
- `user.md` → explicit user authority remains at orchestration gate (`USER RESPONSE REQUIRED`); not part of canonical specialist roster
