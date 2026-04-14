# Agent Orchestration Session Playbook

Purpose: provide a repeatable, one-chat-per-task progression to harden orchestration between the operator chat agent and subagents, including structured debate, cross-agent communication, design tradeoffs, and code-delivery prioritization.

Use this as a sequential backlog for 70 engineering chat sessions. Each task is scoped so a Cursor engineering agent can complete it in one focused session.

## Working principles

- One session, one shippable increment.
- Every session must end with updated tests or explicit test evidence.
- Operator agent owns goals, constraints, and acceptance criteria.
- Subagents must provide evidence, not opinions, when debating.
- Disagreements resolve through documented decision records and scorecards.

## Canonical subagent roster (SaaS personas)

Use these roles as the canonical specialist roster for orchestration debates, handoffs, and execution support:

- Subject Matter/Industry Expert (`@sme`)
- Senior Product Operations (`@props`)
- Senior Product Management (`@prod`)
- Senior Backend Engineer (`@be-eng`)
- Senior Frontend Engineer (`@fe-eng`)
- Senior DevOps Engineer (`@do-eng`)
- Senior Marketing (`@marketing`)
- Senior Customer Success (`@cs`)
- Senior Revenue (`@rev`)

Persona behavior should follow general SaaS industry responsibilities and skillsets for each role.

## Session backlog (70 tasks)

### Phase 1 - Foundations and contracts (1-10)

1. Define operator-to-subagent message envelope schema (goal, constraints, inputs, success metrics).
2. Define subagent-to-operator response schema (result, evidence, confidence, blockers, next action).
3. Add explicit `decision_request` and `decision_response` payload types.
4. Add `assumption_log` field and require it on every non-trivial response.
5. Add a canonical severity taxonomy (`critical`, `high`, `medium`, `low`, `info`) for findings.
6. Add explicit delivery priority labels (`ship-now`, `next`, `later`, `parked`) to each task.
7. Create an orchestration glossary (operator, subagent, arbiter, critic, implementer, reviewer).
8. Add a schema validator utility and failing tests for malformed orchestration payloads.
9. Add a compatibility/version field for orchestration protocol evolution.
10. Publish orchestration contract examples in docs and templates.

### Phase 2 - Subagent role specialization (11-20)

11. Define role cards for the canonical roster (`@sme`, `@props`, `@prod`, `@be-eng`, `@fe-eng`, `@do-eng`, `@marketing`, `@cs`, `@rev`).
12. Add capability declarations per subagent (what each role can and cannot decide).
13. Add a role-based route planner that maps task type to default subagent mix from the canonical roster.
14. Add fallback routing when preferred role is unavailable.
15. Add conflict-of-interest rule (implementer cannot be sole approver of own design).
16. Add escalation rule when risk score exceeds threshold (default to `@prod` + `@props` + relevant engineering role).
17. Add quality gate definitions for code, integration, packaging, and go-to-market readiness (`@marketing`, `@cs`, `@rev`).
18. Add explicit timebox policy per role to avoid infinite analysis loops.
19. Add operator override mechanism with audit note requirements.
20. Add tests confirming correct role assignment for representative task categories.

### Phase 3 - Debate and argumentation loop (21-30)

21. Implement structured debate prompt format (`position`, `evidence`, `risks`, `rebuttal`).
22. Require at least two distinct solution proposals for high-impact tasks.
23. Add an arbiter scoring rubric (complexity, risk, reversibility, user impact, delivery speed).
24. Add tie-break rule preferring reversible and testable options.
25. Add a max rounds setting for debate (`N` rounds before forced decision).
26. Add “evidence freshness” rule; stale claims must be revalidated.
27. Add `counterexample_required` flag for architecture debates.
28. Add a “steelman opponent” step before final recommendation.
29. Capture debate transcripts into concise decision records.
30. Add tests for debate loop termination and deterministic winner selection.

### Phase 4 - Cross-subagent communication (31-40)

31. Define subagent-to-subagent handoff packet format.
32. Add shared context IDs so parallel subagents reference same work unit.
33. Add deduplication guard so two subagents do not redo identical tasks.
34. Add stale-context detection when upstream assumptions change.
35. Add explicit dependency graph field in handoff packets.
36. Add “request clarification” channel between subagents before escalation.
37. Add operator-visible trace of subagent handoffs and decision points.
38. Add handoff quality checks (missing acceptance criteria should fail handoff).
39. Add timeout + retry semantics for unanswered inter-subagent requests.
40. Add tests for parallel subagent convergence and consistent merged outputs.

### Phase 5 - Prioritization and execution governance (41-50)

41. Add objective scorecard model (value, urgency, risk reduction, effort).
42. Add weighted prioritization function configurable by operator.
43. Add “must-ship first” policy for security, data-loss, and install regressions.
44. Add WIP cap policy to enforce finish-before-start behavior.
45. Add “execution lane” model (`hotfix`, `feature`, `hardening`, `debt`).
46. Add automatic demotion of speculative work when blockers exist on critical path.
47. Add queue aging rules so important work cannot starve.
48. Add milestone-based batching that maps tasks to release checkpoints.
49. Add scorecard explanation output (why chosen, why deferred).
50. Add tests validating prioritization ordering under different weights.

### Phase 6 - Delivery controls and safety (51-60)

51. Add pre-implementation checklist gate (requirements, constraints, rollback plan).
52. Add post-implementation checklist gate (tests, docs, migration notes, risk review).
53. Add mandatory rollback strategy field for high-risk changes.
54. Add uncertainty threshold that forces clarification before coding.
55. Add protected-file policy requiring higher confidence for critical scripts.
56. Add explicit “no-destructive-actions” guard in orchestration templates.
57. Add red-team subagent pass for security-sensitive change sets.
58. Add failure-mode cataloging to decision records.
59. Add CI evidence parser so subagents reason from actual failures.
60. Add tests ensuring unsafe actions are blocked and escalated.

### Phase 7 - Product-goal closure and milestone completion (61-70)

61. Define formal milestone schema (objective, acceptance, exit tests, owners).
62. Add per-milestone “definition of done” checks consumed by operator agent.
63. Add cross-milestone dependency visibility in orchestration outputs.
64. Add progress confidence scoring with drift detection.
65. Add final-milestone lock criteria requiring complete acceptance evidence.
66. Add explicit “remaining gaps” report before milestone close.
67. Add `goal_alignment_check` at start and end of each session.
68. Add `stop_condition_check` that only allows completion at final milestone.
69. Add release-readiness summary generated from all session records.
70. Add tests proving stop condition stays false until product goals and final milestone are complete.

## Copy/paste repeatable prompt (engineering agent)

Use this prompt at the start of each session. Replace bracketed placeholders.

```text
You are the ENGINEERING AGENT for Lé Vibe.

Mission:
- Execute exactly one session task from the Agent Orchestration Session Playbook.
- Deliver code, tests, and documentation evidence for the selected task.
- Prioritize execution quality and shipping momentum over speculative expansion.

Session context:
- Session number: [NN]
- Task title: [TASK TITLE]
- Product goal: [GOAL]
- Current milestone: [MILESTONE NAME]
- Final milestone: [FINAL MILESTONE NAME]
- Constraints/non-goals: [CONSTRAINTS]

Operating directives:
1) Treat operator goals as highest priority.
2) Use only the canonical subagent roster: `@sme`, `@props`, `@prod`, `@be-eng`, `@fe-eng`, `@do-eng`, `@marketing`, `@cs`, `@rev`.
3) If multiple approaches exist, run a brief evidence-based debate and choose the best path via explicit scorecard.
4) Keep scope to one-session completion; avoid unrelated refactors.
5) Implement changes directly, then run/extend tests.
6) Update documentation for behavior changes.
7) Provide concise “what changed, why, evidence” summary.

Stop/continue rule (strict):
- Do NOT stop because a local subtask is done.
- Continue working this prompt directive until BOTH conditions are true:
  A) Product goals for this session are satisfied with evidence.
  B) The final milestone has been achieved and verified.
- If either A or B is false, output: PASTE SAME AGAIN and the next highest-impact action.
- Only output: LÉ VIBE SESSION COMPLETE when A and B are both true.
- If blocked by missing product decision, output: USER RESPONSE REQUIRED with numbered questions.

Required output sections:
1) Plan
2) Implementation
3) Tests/Evidence
4) Docs updated
5) Risks/Follow-ups
6) Continuation line (PASTE SAME AGAIN / USER RESPONSE REQUIRED / LÉ VIBE SESSION COMPLETE)
```

## Suggested execution cadence

- Sessions 1-20: protocol and role contracts.
- Sessions 21-40: debate + communication reliability.
- Sessions 41-60: prioritization and safety controls.
- Sessions 61-70: milestone closure logic and release readiness.

