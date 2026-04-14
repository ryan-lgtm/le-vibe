"""Shared test helpers for workspace-event contract static checks.

Exported helper index:
- parse_exported_helper_index
- workspace_event_static_diagnostics
- discover_workspace_event_emitter_modules
- should_exclude_workspace_event_scan_path
- assert_marker_adjacent_to_target_tests
- assert_safe_update_step_patterns_integrity
- assert_safe_update_procedure_docstring
- assert_internal_only_registry_integrity
- assert_ordering_pair_integrity
- assert_callable_surface_membership
- assert_callable_symbols_resolve
- assert_helper_index_export_and_resolution_consistency
- assert_phrase_bundle_integrity
- assert_phrase_bundle_boundaries_match_constants
- assert_phrase_bundle_full_integrity
- assert_expected_symbol_tuple
- assert_constant_symbol_discoverability
- assert_helper_governance_runtime_consistency
- HELPER_INDEX_GOVERNANCE_ANCHOR_PREFIX
- WORKSPACE_EVENT_HELPER_CALLABLE_SYMBOLS
- WORKSPACE_EVENT_HELPER_CONSTANT_SYMBOLS
- WORKSPACE_EVENT_HELPER_INDEX_SYMBOLS
- SAFE_UPDATE_STEP_PATTERNS
- WORKSPACE_EVENT_SCAN_EXCLUDE_REASONS
- WORKSPACE_EVENT_SCAN_EXCLUDE_PARTS
- WORKSPACE_EVENT_HELPER_INTERNAL_ONLY_CONSTANT_SYMBOLS
- INTERNAL_ONLY_REGISTRY_ORDERING_PAIR
- CALLABLE_PLACEMENT_GUARDED_HELPERS
- HELPER_GOVERNANCE_SPEC_PHRASES
- HELPER_GOVERNANCE_SPEC_FIRST_PHRASE
- HELPER_GOVERNANCE_SPEC_LAST_PHRASE
- FAILURE_MODE_DIAGNOSTIC_GOVERNANCE_INVARIANTS

Safe exclusion update procedure:
1) Update WORKSPACE_EVENT_SCAN_EXCLUDE_REASONS entries (terms + rationale).
2) Confirm WORKSPACE_EVENT_SCAN_EXCLUDE_PARTS remains derived from reason keys.
3) Update docs/SESSION_ORCHESTRATION_SPEC.md exclusion policy text.
4) Update/verify contract assertions in tests/test_session_orchestration_spec_step2_contract.py.
5) Run test_session_orchestrator.py and spec contract tests before merge.
"""

from __future__ import annotations

import ast
import re
from pathlib import Path

WORKSPACE_EVENT_SCAN_EXCLUDE_REASONS: dict[str, str] = {
    "__pycache__": "Python bytecode cache paths are non-source artifacts.",
    "vendor": "Vendored third-party code is not first-party event-emitter surface.",
    "third_party": "Third-party mirrors are external sources, excluded from local contract policy.",
    "generated": "Generated files may be machine-written and unstable for authoring contracts.",
}
WORKSPACE_EVENT_SCAN_EXCLUDE_PARTS: tuple[str, ...] = tuple(WORKSPACE_EVENT_SCAN_EXCLUDE_REASONS.keys())
HELPER_INDEX_GOVERNANCE_ANCHOR_PREFIX = "# HELPER_INDEX_GOVERNANCE:"
EXPORTED_HELPER_INDEX_HEADER = "Exported helper index:"
PARSE_EXPORTED_HELPER_INDEX_EDGE_CASE_IDS_CANONICAL: tuple[str, ...] = (
    "no_header",
    "repeated_header_first_section_wins",
    "empty_section",
)
PARSE_EXPORTED_HELPER_INDEX_EDGE_CASE_IDS: tuple[str, ...] = PARSE_EXPORTED_HELPER_INDEX_EDGE_CASE_IDS_CANONICAL
WORKSPACE_EVENT_HELPER_INTERNAL_ONLY_CONSTANT_SYMBOLS: tuple[str, ...] = (
    "PARSE_EXPORTED_HELPER_INDEX_EDGE_CASE_IDS_CANONICAL",
)
INTERNAL_ONLY_REGISTRY_ORDERING_PAIR: tuple[str, str] = (
    "assert_internal_only_registry_integrity",
    "WORKSPACE_EVENT_HELPER_INTERNAL_ONLY_CONSTANT_SYMBOLS",
)
CALLABLE_PLACEMENT_GUARDED_HELPERS: tuple[str, ...] = (
    "assert_internal_only_registry_integrity",
    "assert_ordering_pair_integrity",
    "assert_phrase_bundle_integrity",
    "assert_helper_governance_runtime_consistency",
)
HELPER_GOVERNANCE_SPEC_FIRST_PHRASE = "Helper internal-only constants registry guard"
HELPER_GOVERNANCE_SPEC_LAST_PHRASE = (
    "Helper-governance runtime consistency checks are centralized in shared helper `assert_helper_governance_runtime_consistency`."
)
HELPER_GOVERNANCE_SPEC_PHRASES: tuple[str, ...] = (
    HELPER_GOVERNANCE_SPEC_FIRST_PHRASE,
    "WORKSPACE_EVENT_HELPER_INTERNAL_ONLY_CONSTANT_SYMBOLS",
    "explicit registry for internal-only helper constants",
    "non-empty, duplicate-free, and in canonical sorted order",
    "registry symbol itself remains discoverable",
    "discoverable in both `WORKSPACE_EVENT_HELPER_CONSTANT_SYMBOLS` and the exported helper docstring index",
    "runtime evidence asserted by parsing `workspace_event_contract_utils` docstring through `parse_exported_helper_index`",
    "runtime exclusion evidence verifies each internal-only member remains absent from parsed exported helper names",
    "non-self-referential",
    "`WORKSPACE_EVENT_HELPER_INTERNAL_ONLY_CONSTANT_SYMBOLS` cannot list itself",
    "each listed symbol must resolve on `workspace_event_contract_utils` (`hasattr`) to prevent stale names",
    "runtime sorted-order evidence keeps the internal-only registry canonical",
    "assert_internal_only_registry_integrity",
    "runtime doc-index ordering evidence keeps `assert_internal_only_registry_integrity` before `WORKSPACE_EVENT_HELPER_INTERNAL_ONLY_CONSTANT_SYMBOLS`",
    "INTERNAL_ONLY_REGISTRY_ORDERING_PAIR",
    "ordering pair remains a 2-tuple with distinct entries and both symbols present in parsed exported helper names",
    "Ordering-pair integrity checks are centralized in shared helper `assert_ordering_pair_integrity`",
    "Placement guard: `assert_ordering_pair_integrity` remains in callable surface (`WORKSPACE_EVENT_HELPER_CALLABLE_SYMBOLS`), excluded from `WORKSPACE_EVENT_HELPER_CONSTANT_SYMBOLS`, and appears before constant section entries in parsed exported helper index.",
    "Callable-surface placement checks are centralized in shared helper `assert_callable_surface_membership`",
    "Callable symbol resolution checks are centralized in shared helper `assert_callable_symbols_resolve`.",
    "Helper-index export coverage + callable resolution checks are centralized in shared helper `assert_helper_index_export_and_resolution_consistency`.",
    "Phrase-bundle integrity guard: `HELPER_GOVERNANCE_SPEC_PHRASES` remains non-empty, duplicate-free, and in canonical order.",
    "Placement guard: `assert_phrase_bundle_integrity` remains in callable surface (`WORKSPACE_EVENT_HELPER_CALLABLE_SYMBOLS`), excluded from `WORKSPACE_EVENT_HELPER_CONSTANT_SYMBOLS`, and appears before constant section entries in helper index.",
    "Callable placement governance source is centralized in `CALLABLE_PLACEMENT_GUARDED_HELPERS`, including `assert_helper_governance_runtime_consistency`.",
    "Expected tuple shape/order checks are centralized in shared helper `assert_expected_symbol_tuple`.",
    "Constant symbol discoverability checks are centralized in shared helper `assert_constant_symbol_discoverability`.",
    "Phrase-bundle boundary checks are centralized in shared helper `assert_phrase_bundle_boundaries_match_constants`.",
    "Placement guard: `assert_helper_governance_runtime_consistency` remains in callable surface (`WORKSPACE_EVENT_HELPER_CALLABLE_SYMBOLS`), excluded from `WORKSPACE_EVENT_HELPER_CONSTANT_SYMBOLS`, and appears before constant section entries in helper index.",
    HELPER_GOVERNANCE_SPEC_LAST_PHRASE,
)
FAILURE_MODE_DIAGNOSTIC_GOVERNANCE_INVARIANTS: tuple[str, ...] = (
    "shape_keys",
    "list_types",
    "sorted_order",
    "source_link_allowed",
    "source_link_used",
    "parity_unknown_unused_empty",
)

# Step-intent patterns for the safe exclusion update procedure.
SAFE_UPDATE_STEP_PATTERNS: tuple[str, ...] = (
    # Step 1: exclusion terms/rationale map update is explicitly documented.
    r"1\)\s+.*EXCLUDE_REASONS",
    # Step 2: derived parts list remains mechanically tied to reasons keys.
    r"2\)\s+.*EXCLUDE_PARTS.*derived",
    # Step 3: spec text is synced when policy changes.
    r"3\)\s+.*SESSION_ORCHESTRATION_SPEC\.md",
    # Step 4: contract assertion updates remain mandatory.
    r"4\)\s+.*contract assertions",
    # Step 5: targeted orchestrator/spec test run remains required.
    r"5\)\s+.*test_session_orchestrator\.py.*spec contract tests",
)

WORKSPACE_EVENT_HELPER_CALLABLE_SYMBOLS: tuple[str, ...] = (
    "parse_exported_helper_index",
    "workspace_event_static_diagnostics",
    "discover_workspace_event_emitter_modules",
    "should_exclude_workspace_event_scan_path",
    "assert_safe_update_step_patterns_integrity",
    "assert_safe_update_procedure_docstring",
    "assert_internal_only_registry_integrity",
    "assert_ordering_pair_integrity",
    "assert_callable_surface_membership",
    "assert_callable_symbols_resolve",
    "assert_helper_index_export_and_resolution_consistency",
    "assert_phrase_bundle_integrity",
    "assert_phrase_bundle_boundaries_match_constants",
    "assert_phrase_bundle_full_integrity",
    "assert_expected_symbol_tuple",
    "assert_constant_symbol_discoverability",
    "assert_helper_governance_runtime_consistency",
)

WORKSPACE_EVENT_HELPER_CONSTANT_SYMBOLS: tuple[str, ...] = (
    "HELPER_INDEX_GOVERNANCE_ANCHOR_PREFIX",
    "WORKSPACE_EVENT_HELPER_INDEX_SYMBOLS",
    "SAFE_UPDATE_STEP_PATTERNS",
    "WORKSPACE_EVENT_SCAN_EXCLUDE_REASONS",
    "WORKSPACE_EVENT_SCAN_EXCLUDE_PARTS",
    "WORKSPACE_EVENT_HELPER_INTERNAL_ONLY_CONSTANT_SYMBOLS",
    "INTERNAL_ONLY_REGISTRY_ORDERING_PAIR",
    "CALLABLE_PLACEMENT_GUARDED_HELPERS",
    "HELPER_GOVERNANCE_SPEC_PHRASES",
    "HELPER_GOVERNANCE_SPEC_FIRST_PHRASE",
    "HELPER_GOVERNANCE_SPEC_LAST_PHRASE",
    "FAILURE_MODE_DIAGNOSTIC_GOVERNANCE_INVARIANTS",
)

WORKSPACE_EVENT_HELPER_INDEX_SYMBOLS: tuple[str, ...] = (
    WORKSPACE_EVENT_HELPER_CALLABLE_SYMBOLS + WORKSPACE_EVENT_HELPER_CONSTANT_SYMBOLS
)


def should_exclude_workspace_event_scan_path(path: Path) -> bool:
    """True when a path should be excluded from workspace-event static scans."""
    return any(part in WORKSPACE_EVENT_SCAN_EXCLUDE_PARTS for part in path.parts)


def parse_exported_helper_index(doc: str) -> list[str]:
    """Return helper names from the ``Exported helper index`` section only."""
    in_index = False
    out: list[str] = []
    for raw_line in doc.splitlines():
        stripped = raw_line.strip()
        if stripped == EXPORTED_HELPER_INDEX_HEADER:
            in_index = True
            continue
        if not in_index:
            continue
        # End the section on the next non-bullet non-empty line (typically next header).
        if stripped and not stripped.startswith("- "):
            break
        if stripped.startswith("- "):
            out.append(stripped[2:])
    return out


def discover_workspace_event_emitter_modules(package_root: Path) -> list[Path]:
    """
    Discover Python modules under package_root containing _emit_workspace_event callsites.
    """
    modules: list[Path] = []
    for py_file in sorted(package_root.glob("**/*.py")):
        if should_exclude_workspace_event_scan_path(py_file):
            continue
        text = py_file.read_text(encoding="utf-8")
        if "_emit_workspace_event(" not in text:
            continue
        modules.append(py_file)
    return modules


def assert_marker_adjacent_to_target_tests(
    lines: list[str],
    expected_pairs: tuple[tuple[str, str], ...],
) -> None:
    """Shared assertion for comment-marker adjacency to target test defs."""
    for guard_prefix, fn_def_prefix in expected_pairs:
        fn_idx = next(
            (idx for idx, line in enumerate(lines) if line.strip().startswith(fn_def_prefix)),
            -1,
        )
        assert fn_idx >= 0, fn_def_prefix
        guard_idx = -1
        for idx in range(fn_idx - 1, -1, -1):
            stripped = lines[idx].strip()
            if not stripped:
                continue
            if stripped.startswith("#"):
                guard_idx = idx
                break
            break
        assert guard_idx >= 0, guard_prefix
        assert lines[guard_idx].strip().startswith(guard_prefix), (guard_prefix, lines[guard_idx].strip())
        # Allow one blank spacer line for readability.
        assert fn_idx - guard_idx in (1, 2), (guard_prefix, fn_def_prefix, guard_idx, fn_idx)


def assert_safe_update_step_patterns_integrity(patterns: tuple[str, ...]) -> None:
    """Shared integrity guard for step-pattern checklist semantics."""
    assert len(patterns) == 5
    required_step_tokens = [f"{idx}\\)" for idx in range(1, 6)]
    for token in required_step_tokens:
        matches = [pattern for pattern in patterns if token in pattern]
        assert len(matches) == 1, f"expected exactly one pattern for {token}, got {len(matches)}"
    for idx, pattern in enumerate(patterns, start=1):
        assert f"{idx}\\)" in pattern, f"pattern at index {idx - 1} must correspond to step {idx}"


def assert_safe_update_procedure_docstring(doc: str, patterns: tuple[str, ...]) -> None:
    """Shared docstring guard for safe exclusion update procedure wording."""
    assert "Safe exclusion update procedure" in doc
    assert "WORKSPACE_EVENT_SCAN_EXCLUDE_REASONS" in doc
    assert "SESSION_ORCHESTRATION_SPEC.md" in doc
    assert "test_session_orchestration_spec_step2_contract.py" in doc
    for step in ("1)", "2)", "3)", "4)", "5)"):
        assert step in doc
    for pattern in patterns:
        assert re.search(pattern, doc), pattern


def assert_internal_only_registry_integrity(
    names: tuple[str, ...],
    *,
    module: object,
    exported_names: list[str],
    constant_symbols: tuple[str, ...],
    registry_symbol: str = "WORKSPACE_EVENT_HELPER_INTERNAL_ONLY_CONSTANT_SYMBOLS",
) -> None:
    """Shared integrity guard for internal-only helper constant symbol registry."""
    assert len(names) > 0
    assert len(names) == len(set(names))
    assert names == tuple(sorted(names))
    assert registry_symbol not in names
    for name in names:
        assert hasattr(module, name), name
        assert name not in constant_symbols
        assert name not in exported_names


def assert_ordering_pair_integrity(pair: tuple[str, str], exported_names: list[str]) -> None:
    """Shared integrity guard for before/after symbol ordering pairs."""
    assert len(pair) == 2
    before_symbol, after_symbol = pair
    assert before_symbol != after_symbol
    assert before_symbol in exported_names
    assert after_symbol in exported_names
    assert exported_names.index(before_symbol) < exported_names.index(after_symbol)


def assert_callable_surface_membership(
    symbol: str,
    *,
    callable_symbols: tuple[str, ...],
    constant_symbols: tuple[str, ...],
    index_symbols: tuple[str, ...],
) -> None:
    """Shared guard that a helper symbol stays in callable surface only."""
    assert symbol in callable_symbols
    assert symbol not in constant_symbols
    callable_count = len(callable_symbols)
    callable_slice = index_symbols[:callable_count]
    constant_slice = index_symbols[callable_count:]
    assert symbol in callable_slice
    assert symbol not in constant_slice


def assert_callable_symbols_resolve(symbols: tuple[str, ...], module: object) -> None:
    """Shared guard that callable symbol names resolve on module."""
    for symbol in symbols:
        assert hasattr(module, symbol), symbol


def assert_helper_index_export_and_resolution_consistency(
    index_symbols: tuple[str, ...],
    callable_symbols: tuple[str, ...],
    module: object,
    exported_names: list[str],
) -> None:
    """Shared guard for helper-index export coverage and callable resolution."""
    for symbol in index_symbols:
        assert symbol in exported_names
    assert_callable_symbols_resolve(callable_symbols, module)


def assert_phrase_bundle_integrity(
    phrases: tuple[str, ...],
    *,
    first_phrase: str,
    last_phrase: str,
) -> None:
    """Shared integrity guard for ordered phrase bundles."""
    assert len(phrases) > 0
    assert len(phrases) == len(set(phrases))
    assert phrases[0] == first_phrase
    assert phrases[-1] == last_phrase


def assert_phrase_bundle_boundaries_match_constants(
    phrases: tuple[str, ...],
    *,
    first_phrase: str,
    last_phrase: str,
) -> None:
    """Shared guard that phrase bundle boundaries match canonical constants."""
    assert phrases[0] == first_phrase
    assert phrases[-1] == last_phrase


def assert_phrase_bundle_full_integrity(
    phrases: tuple[str, ...],
    *,
    first_phrase: str,
    last_phrase: str,
) -> None:
    """Shared guard combining phrase bundle integrity and boundary checks."""
    assert_phrase_bundle_integrity(
        phrases,
        first_phrase=first_phrase,
        last_phrase=last_phrase,
    )
    assert_phrase_bundle_boundaries_match_constants(
        phrases,
        first_phrase=first_phrase,
        last_phrase=last_phrase,
    )


def assert_expected_symbol_tuple(
    symbols: tuple[str, ...],
    expected: tuple[str, ...],
) -> None:
    """Shared guard for non-empty, duplicate-free, exact canonical symbol tuples."""
    assert len(symbols) > 0
    assert len(symbols) == len(set(symbols))
    assert symbols == expected


def assert_constant_symbol_discoverability(
    symbol: str,
    *,
    constant_symbols: tuple[str, ...],
    exported_names: list[str],
) -> None:
    """Shared guard that a constant symbol remains discoverable."""
    assert symbol in constant_symbols
    assert symbol in exported_names


def assert_helper_governance_runtime_consistency(
    *,
    module: object,
    exported_names: list[str],
    helper_governance_spec_phrases: tuple[str, ...],
    helper_governance_spec_first_phrase: str,
    helper_governance_spec_last_phrase: str,
    internal_only_constant_symbols: tuple[str, ...],
    helper_constant_symbols: tuple[str, ...],
    internal_only_registry_ordering_pair: tuple[str, str],
    callable_placement_guarded_helpers: tuple[str, ...],
    helper_callable_symbols: tuple[str, ...],
    helper_index_symbols: tuple[str, ...],
) -> None:
    """Shared runtime governance check for helper-index policy invariants."""
    assert_phrase_bundle_full_integrity(
        helper_governance_spec_phrases,
        first_phrase=helper_governance_spec_first_phrase,
        last_phrase=helper_governance_spec_last_phrase,
    )
    assert_constant_symbol_discoverability(
        "WORKSPACE_EVENT_HELPER_INTERNAL_ONLY_CONSTANT_SYMBOLS",
        constant_symbols=helper_constant_symbols,
        exported_names=exported_names,
    )
    assert (
        "WORKSPACE_EVENT_HELPER_INTERNAL_ONLY_CONSTANT_SYMBOLS"
        not in internal_only_constant_symbols
    )
    assert_internal_only_registry_integrity(
        internal_only_constant_symbols,
        module=module,
        exported_names=exported_names,
        constant_symbols=helper_constant_symbols,
    )
    assert_ordering_pair_integrity(internal_only_registry_ordering_pair, exported_names)
    assert_expected_symbol_tuple(
        callable_placement_guarded_helpers,
        (
            "assert_internal_only_registry_integrity",
            "assert_ordering_pair_integrity",
            "assert_phrase_bundle_integrity",
            "assert_helper_governance_runtime_consistency",
        ),
    )
    for helper_symbol in callable_placement_guarded_helpers:
        assert_callable_surface_membership(
            helper_symbol,
            callable_symbols=helper_callable_symbols,
            constant_symbols=helper_constant_symbols,
            index_symbols=helper_index_symbols,
        )
    assert_callable_symbols_resolve(helper_callable_symbols, module)
    assert_helper_index_export_and_resolution_consistency(
        helper_index_symbols,
        helper_callable_symbols,
        module,
        exported_names,
    )


def workspace_event_static_diagnostics(source_path: Path) -> tuple[set[str], list[str]]:
    """
    Return emitted literal event ids and non-literal callsite diagnostics.
    """
    tree = ast.parse(source_path.read_text(encoding="utf-8"))
    emitted: set[str] = set()
    errors: list[str] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if not isinstance(node.func, ast.Name) or node.func.id != "_emit_workspace_event":
            continue
        if len(node.args) < 2:
            errors.append(f"{source_path}:{node.lineno}:{node.col_offset} missing event argument")
            continue
        event_arg = node.args[1]
        if isinstance(event_arg, ast.Constant) and isinstance(event_arg.value, str):
            emitted.add(event_arg.value)
            continue
        errors.append(f"{source_path}:{node.lineno}:{node.col_offset} event id must be string literal")
    return emitted, errors

