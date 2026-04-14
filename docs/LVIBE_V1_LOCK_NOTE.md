# Lé Vibe `.lvibe/` v1 Lock Note

This note freezes the `.lvibe/` workspace-memory concept for **v1**.

## Decision

`.lvibe/` hardening is accepted and **v1-locked**.

## In scope for maintenance (v1)

- Bug fixes and regressions only.
- Security/privacy fixes (especially §8 secrets handling).
- Contract-test/doc drift fixes needed to keep accepted behavior stable.

## Out of scope for this phase

- Broad `.lvibe/` redesign.
- New storage architecture or major schema migration.
- New vector database / hosted embedding architecture as a prerequisite for v1.

## Authority and expected behavior

- Consent-gated creation and decline persistence: [`PRODUCT_SPEC.md`](PRODUCT_SPEC.md) §5.1
- Storage cap + compaction policy: [`PRODUCT_SPEC.md`](PRODUCT_SPEC.md) §5.4–§5.5
- Git hygiene, user gate, and secrets policy: [`PRODUCT_SPEC.md`](PRODUCT_SPEC.md) §6–§8
- Runtime/session coordination anchors: [`SESSION_ORCHESTRATION_SPEC.md`](SESSION_ORCHESTRATION_SPEC.md), [`PM_STAGE_MAP.md`](PM_STAGE_MAP.md)

## v2 parking lot (future, explicit authorization required)

If product chooses to evolve `.lvibe/` beyond v1 stability, queue those ideas under a dedicated v2 prompt and approval cycle (examples: richer retrieval indexing, expanded observability surfaces, major schema evolution).

Until then, engineers should prioritize the next pillar: **stable, user-friendly, orchestrated, locally self-installable branded IDE v1**.
