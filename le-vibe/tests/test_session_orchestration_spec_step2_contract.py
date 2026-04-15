"""Contract: docs/SESSION_ORCHESTRATION_SPEC.md keeps STEP 2 + session_orchestrator pointer."""

from __future__ import annotations

from pathlib import Path

from workspace_event_contract_utils import FAILURE_MODE_DIAGNOSTIC_GOVERNANCE_INVARIANTS
from workspace_event_contract_utils import PARSE_EXPORTED_HELPER_INDEX_EDGE_CASE_IDS
from workspace_event_contract_utils import PARSE_EXPORTED_HELPER_INDEX_EDGE_CASE_IDS_CANONICAL
from workspace_event_contract_utils import WORKSPACE_EVENT_HELPER_INTERNAL_ONLY_CONSTANT_SYMBOLS
from workspace_event_contract_utils import WORKSPACE_EVENT_HELPER_CALLABLE_SYMBOLS
from workspace_event_contract_utils import WORKSPACE_EVENT_HELPER_CONSTANT_SYMBOLS
from workspace_event_contract_utils import INTERNAL_ONLY_REGISTRY_ORDERING_PAIR
from workspace_event_contract_utils import CALLABLE_PLACEMENT_GUARDED_HELPERS
from workspace_event_contract_utils import HELPER_GOVERNANCE_SPEC_PHRASES
from workspace_event_contract_utils import HELPER_GOVERNANCE_SPEC_FIRST_PHRASE
from workspace_event_contract_utils import HELPER_GOVERNANCE_SPEC_LAST_PHRASE
import workspace_event_contract_utils as workspace_event_utils
from workspace_event_contract_utils import parse_exported_helper_index
from workspace_event_contract_utils import assert_helper_governance_runtime_consistency


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_session_orchestration_spec_section_31_meta_mentions_optional_construction_and_ai_pilot_notes():
    """§3.1 ``meta`` row — optional hints aligned with schemas example + PM_STAGE_MAP STEP 16."""
    text = (_repo_root() / "docs" / "SESSION_ORCHESTRATION_SPEC.md").read_text(encoding="utf-8")
    assert "continue_construction_note" in text
    assert "ai_pilot_note" in text
    assert "AI_PILOT_AND_CONTINUE.md" in text
    assert "PROMPT_BUILD_LE_VIBE.md" in text


def test_session_orchestration_spec_intro_product_authority_cites_product_spec_section9_and_section8_evidence():
    """Intro **Product authority** — PRODUCT_SPEC §9 roster + SECTION8 evidence (STEP 2 authority chain)."""
    text = (_repo_root() / "docs" / "SESSION_ORCHESTRATION_SPEC.md").read_text(encoding="utf-8")
    intro = text.split("**Product authority:**", 1)[1].split("**Maintainer index", 1)[0]
    assert "`docs/PRODUCT_SPEC.md` §9" in intro
    assert "PRODUCT_SPEC_SECTION8_EVIDENCE.md" in intro
    assert "test_session_orchestrator.py" in intro


def test_session_orchestration_spec_documents_step2_and_e1():
    text = (_repo_root() / "docs" / "SESSION_ORCHESTRATION_SPEC.md").read_text(encoding="utf-8")
    assert "STEP 2" in text
    assert "session_orchestrator" in text
    assert "test_session_orchestrator.py" in text
    assert "test_session_orchestration_spec_step2_contract.py" in text
    assert "ensure_pm_session_artifacts" in text
    assert "apply_opening_skip" in text
    assert "session_manifest_example_source_path" in text
    assert "goal_alignment_check.start" in text
    assert "goal_alignment_check.end" in text
    assert "stop_condition_check" in text
    assert "release_readiness_summary" in text
    assert "Release-readiness summary (Task 69)" in text
    assert "CI evidence parser (Task 59)" in text
    assert "meta.ci_failure_log" in text
    assert "meta.ci_failure_logs" in text
    assert "meta.ci_evidence_summary" in text
    assert "subagents reason from actual failures" in text
    assert "CI evidence summary contract" in text
    assert "reported_failed_count" in text
    assert "reported_error_count" in text
    assert "remaining_gaps_report" in text
    assert "Remaining gaps report (Task 66)" in text
    assert "Milestone definition-of-done checks (Task 62)" in text
    assert "meta.milestone_definition_of_done_checks" in text
    assert "Cross-milestone dependency visibility (Task 63)" in text
    assert "meta.milestone_dependency_visibility" in text
    assert "Progress confidence + drift (Task 64)" in text
    assert "meta.progress_confidence_report" in text
    assert "Final milestone lock criteria (Task 65)" in text
    assert "meta.final_milestone_lock_criteria" in text
    assert "Failure-mode cataloging (Task 58)" in text
    assert "meta.failure_mode_catalog" in text
    assert "FAILURE_MODE_SEVERITY_BY_BLOCKER" in text
    assert "FAILURE_MODE_BLOCKER_POLICY" in text
    assert "BLOCKER_GROUP_BASE" in text
    assert "BLOCKER_GROUP_EVIDENCE" in text
    assert "not string heuristics" in text
    assert "Failure-mode policy derivation" in text
    assert "derived from that single policy source" in text
    assert "Failure-mode policy shape guard" in text
    assert "unique blocker ids" in text
    assert "BLOCKER_GROUP_BASE` / `BLOCKER_GROUP_EVIDENCE" in text
    assert "Failure-mode policy tuple schema guard" in text
    assert "strict 3-tuples" in text
    assert "FAILURE_MODE_ALLOWED_SEVERITIES" in text
    assert "`high`, `medium`" in text
    assert "Failure-mode severity taxonomy integrity guard" in text
    assert "non-empty, duplicate-free, and in canonical order" in text
    assert "Failure-mode severity taxonomy parity guard" in text
    assert "failure_mode_severity_taxonomy_diagnostics" in text
    assert "unknown_severities" in text
    assert "unused_allowed_severities" in text
    assert "Failure-mode taxonomy diagnostics schema guard" in text
    assert "allowed_severities" in text
    assert "used_severities" in text
    assert "as list fields" in text
    assert "Failure-mode taxonomy diagnostics ordering guard" in text
    assert "returned in sorted order" in text
    assert "Failure-mode taxonomy source-link guard" in text
    assert "sorted(FAILURE_MODE_ALLOWED_SEVERITIES)" in text
    assert "Failure-mode taxonomy used-source guard" in text
    assert "sorted({severity for _, _, severity in FAILURE_MODE_BLOCKER_POLICY})" in text
    assert "Failure-mode diagnostics governance table" in text
    assert "table-driven test verifies shape, list typing, ordering" in text
    assert "focused tests remain as smoke checks" in text
    assert "Failure-mode diagnostics invariant labels" in text
    for invariant in FAILURE_MODE_DIAGNOSTIC_GOVERNANCE_INVARIANTS:
        assert invariant in text
    assert "Failure-mode severity coverage guard" in text
    assert "every emitted release-readiness blocker id" in text
    assert "RELEASE_READINESS_BASE_BLOCKER_IDS" in text
    assert "RELEASE_READINESS_EVIDENCE_BLOCKER_IDS" in text
    assert "new blockers must declare severity explicitly" in text
    assert "ci_failures_present" in text
    assert "medium" in text
    assert "Evidence provenance validation (Task 59)" in text
    assert "meta.evidence_artifacts" in text
    assert "final_milestone_evidence_untraceable" in text
    assert "Evidence freshness rule (Task 26)" in text
    assert "meta.evidence_artifact_records" in text
    assert "final_milestone_evidence_stale" in text
    assert "Runtime artifact refresh (Task 26 follow-through)" in text
    assert "persist_goal_alignment_check" in text
    assert "persist_stop_condition_check" in text
    assert "Runtime session-id guard" in text
    assert "repair missing/blank `meta.session_id`" in text
    assert "Session-id repair audit logging" in text
    assert "session_id_repaired" in text
    assert "Structured log event contract" in text
    assert "schema_version=workspace_event.v1" in text
    assert "_emit_workspace_event" in text
    assert "WORKSPACE_EVENT_REQUIRED_FIELDS" in text
    assert "test matrix enforces all listed events" in text
    assert "Strict registration rule" in text
    assert "rejects unknown workspace event ids" in text
    assert "Developer checklist when adding a workspace event" in text
    assert "update `WORKSPACE_EVENT_REQUIRED_FIELDS`" in text
    assert "emit through `_emit_workspace_event`" in text
    assert "Static parity guard" in text
    assert "exact set parity with `WORKSPACE_EVENT_REQUIRED_FIELDS`" in text
    assert "shared test utility parses `_emit_workspace_event` callsites" in text
    assert "Event id literals only" in text
    assert "dynamic event-id composition is disallowed" in text
    assert "Static diagnostics quality" in text
    assert "file:line:column" in text
    assert "le_vibe/**/*.py" in text
    assert "Recursive-scan exclusion policy" in text
    assert "generated" in text and "vendor" in text and "third_party" in text
    assert "per-term rationale strings" in text
    assert "Policy-change guard" in text
    assert "exclusion term set is pinned by test" in text
    assert "Safe update procedure" in text
    assert "shared utility docstring lists required exclusion-update steps" in text
    assert "WORKSPACE_EVENT_HELPER_INDEX_SYMBOLS" in text
    assert "HELPER_INDEX_GOVERNANCE_ANCHOR_PREFIX" in text
    assert "Shared docstring index parser" in text
    assert "parse_exported_helper_index" in text
    assert "EXPORTED_HELPER_INDEX_HEADER" in text
    assert "Exported helper index" in text
    assert "without capturing unrelated bullet lists" in text
    assert "table-driven tests with case ids" in text
    assert "PARSE_EXPORTED_HELPER_INDEX_EDGE_CASE_IDS_CANONICAL" in text
    assert "Parser edge-case id integrity guard" in text
    assert "Parser edge-case canonical tuple visibility guard" in text
    assert "Parser edge-case alias identity guard" in text
    for phrase in HELPER_GOVERNANCE_SPEC_PHRASES:
        assert phrase in text
    assert "Phrase-bundle integrity checks are centralized in shared helper `assert_phrase_bundle_integrity`." in text
    assert "Phrase-bundle boundary checks are centralized in shared helper `assert_phrase_bundle_boundaries_match_constants`." in text
    assert "Phrase-bundle full integrity checks are centralized in shared helper `assert_phrase_bundle_full_integrity`." in text
    assert "Expected tuple shape/order checks are centralized in shared helper `assert_expected_symbol_tuple`." in text
    assert "Constant symbol discoverability checks are centralized in shared helper `assert_constant_symbol_discoverability`." in text
    assert "Placement guard: `assert_helper_governance_runtime_consistency` remains in callable surface (`WORKSPACE_EVENT_HELPER_CALLABLE_SYMBOLS`), excluded from `WORKSPACE_EVENT_HELPER_CONSTANT_SYMBOLS`, and appears before constant section entries in helper index." in text
    assert "Helper-governance runtime consistency checks are centralized in shared helper `assert_helper_governance_runtime_consistency`." in text
    assert "must remain in the callable section (`WORKSPACE_EVENT_HELPER_CALLABLE_SYMBOLS`) and out of the constant section" in text
    assert "must remain identity-linked" in text
    assert "(`is`, not copy-equal only)" in text
    assert "internal-only" in text
    assert "must remain excluded from both `WORKSPACE_EVENT_HELPER_CONSTANT_SYMBOLS` and the `Exported helper index` docstring bullets" in text
    assert "non-empty, duplicate-free, and in canonical order" in text
    assert "PARSE_EXPORTED_HELPER_INDEX_EDGE_CASE_IDS" in text
    assert PARSE_EXPORTED_HELPER_INDEX_EDGE_CASE_IDS == PARSE_EXPORTED_HELPER_INDEX_EDGE_CASE_IDS_CANONICAL
    assert PARSE_EXPORTED_HELPER_INDEX_EDGE_CASE_IDS is PARSE_EXPORTED_HELPER_INDEX_EDGE_CASE_IDS_CANONICAL
    assert "PARSE_EXPORTED_HELPER_INDEX_EDGE_CASE_IDS_CANONICAL" in WORKSPACE_EVENT_HELPER_INTERNAL_ONLY_CONSTANT_SYMBOLS
    exported_names = parse_exported_helper_index(workspace_event_utils.__doc__ or "")
    assert_helper_governance_runtime_consistency(
        module=workspace_event_utils,
        exported_names=exported_names,
        helper_governance_spec_phrases=HELPER_GOVERNANCE_SPEC_PHRASES,
        helper_governance_spec_first_phrase=HELPER_GOVERNANCE_SPEC_FIRST_PHRASE,
        helper_governance_spec_last_phrase=HELPER_GOVERNANCE_SPEC_LAST_PHRASE,
        internal_only_constant_symbols=WORKSPACE_EVENT_HELPER_INTERNAL_ONLY_CONSTANT_SYMBOLS,
        helper_constant_symbols=WORKSPACE_EVENT_HELPER_CONSTANT_SYMBOLS,
        internal_only_registry_ordering_pair=INTERNAL_ONLY_REGISTRY_ORDERING_PAIR,
        callable_placement_guarded_helpers=CALLABLE_PLACEMENT_GUARDED_HELPERS,
        helper_callable_symbols=WORKSPACE_EVENT_HELPER_CALLABLE_SYMBOLS,
        helper_index_symbols=workspace_event_utils.WORKSPACE_EVENT_HELPER_INDEX_SYMBOLS,
    )
    assert exported_names.index("assert_ordering_pair_integrity") < exported_names.index(
        "WORKSPACE_EVENT_HELPER_INTERNAL_ONLY_CONSTANT_SYMBOLS"
    )
    for case_id in PARSE_EXPORTED_HELPER_INDEX_EDGE_CASE_IDS:
        assert case_id in text
    assert "Helper-constant index placement" in text
    assert "FAILURE_MODE_DIAGNOSTIC_GOVERNANCE_INVARIANTS" in text
    assert "trailing constant entry" in text
    assert "Helper-docstring index placement" in text
    assert "trailing docstring bullet" in text
    assert "Governance test comment convention" in text
    assert "Guard #N:" in text
    assert "assert_marker_adjacent_to_target_tests" in text
    assert "goal_alignment_check_applied" in text
    assert "stop_condition_check_applied" in text
    assert "Noop events (`*_noop_*`)" in text
    assert "release_readiness_applied" in text
    assert "remaining_gaps_applied" in text
    assert "product.milestones" in text
    assert "objective" in text
    assert "acceptance" in text
    assert "exit_tests" in text
    assert "owners" in text
    assert "Runtime stop condition check" in text
    assert "Task 70" in text
    assert "stays **false** for all partial states" in text
    assert "Runtime alignment checks" in text
    assert "schemas/session-manifest.v1.example.json" in text
    assert "spec-phase2.md" in text and "§14" in text


def test_session_orchestration_spec_lists_maintainer_full_product_deb_step14():
    """STEP 14: session spec names PM deb doc + Full-product install vs default ci.yml le-vibe-deb."""
    text = (_repo_root() / "docs" / "SESSION_ORCHESTRATION_SPEC.md").read_text(encoding="utf-8")
    assert "Maintainer full-product" in text
    assert "PM_DEB_BUILD_ITERATION.md" in text
    assert "build-le-vibe-debs.sh --with-ide" in text
    assert "Full-product install" in text
    assert "verify-step14-closeout.sh --require-stack-deb" in text
    assert "preflight-step14-closeout.sh" in text
    assert "ide-prereqs --print-closeout-commands" in text
    assert "--apt-sim" in text
    assert "--json" in text
    assert "apt_sim_note" in text
    assert "le-vibe-deb" in text
    assert "apt-repo-releases.md" in text
    assert "H1 vs §7.3 .deb bundles" in text
    assert "build machine" in text
    assert "test host" in text
    assert "Compile fail-fast" in text
    assert "packaging/scripts/ci-vscodium-bash-syntax.sh" in text
    assert "packaging/scripts/ci-editor-nvmrc-sync.sh" in text
    assert "packaging/scripts/ci-vscodium-linux-dev-build.sh" in text
    assert "./editor/smoke.sh" in text
    assert "linux_compile" in text
    assert "Partial VSCode-linux" in text
    assert "print-built-codium-path" in text
    assert "print-vsbuild-codium-path" in text
    assert "print-step14-vscode-linux-bin-files.sh" in text
    assert "build-le-vibe-ide-deb.sh --help" in text
    assert "manual-step14-install-smoke.sh --verify-only" in text
    assert "manual-step14-install-smoke.sh --json" in text
    assert "desktop_file_validate_on_path" in text
    assert "desktop_file_validate" in text
    assert "desktop-file-validate" in text


def test_session_orchestration_spec_phase2_paragraph_lists_linux_compile_tarball():
    """STEP 14.e / 14.j: Phase 2 vs this tree paragraph stays honest vs build-le-vibe-ide.yml."""
    text = (_repo_root() / "docs" / "SESSION_ORCHESTRATION_SPEC.md").read_text(encoding="utf-8")
    assert "linux_compile" in text
    assert "vscodium-linux-build.tar.gz" in text
    assert "ci-vscodium-bash-syntax.sh" in text
    assert "ci-editor-nvmrc-sync.sh" in text
    assert "ci-vscodium-linux-dev-build.sh" in text
    assert "node --version" in text
    assert "LEVIBE_SKIP_NODE_VERSION_CHECK" in text
    assert "fail fast" in text


def test_session_orchestration_spec_phase2_paragraph_lists_14d_branding_honesty():
    """STEP 14.d: SESSION_ORCHESTRATION_SPEC separates PM session work from IDE branding staging."""
    text = (_repo_root() / "docs" / "SESSION_ORCHESTRATION_SPEC.md").read_text(encoding="utf-8")
    assert "14.d" in text
    assert "branding-staging.checklist.md" in text
    assert "read before overrides" in text
    assert "14.c vs 14.d" in text


def test_session_orchestration_spec_lists_step14_closeout_manifest_and_runbook():
    """STEP 14: optional session-manifest seed + autonomous engineer runbook stay linked."""
    text = (_repo_root() / "docs" / "SESSION_ORCHESTRATION_SPEC.md").read_text(encoding="utf-8")
    assert "schemas/session-manifest.step14-closeout.v1.example.json" in text
    assert "STEP14_AUTONOMOUS_ENGINEER_RUNBOOK.md" in text
