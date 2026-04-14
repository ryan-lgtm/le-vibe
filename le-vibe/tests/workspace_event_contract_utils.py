"""Shared test helpers for workspace-event contract static checks.

Exported helper index:
- workspace_event_static_diagnostics
- discover_workspace_event_emitter_modules
- should_exclude_workspace_event_scan_path
- assert_safe_update_step_patterns_integrity
- assert_safe_update_procedure_docstring
- HELPER_INDEX_GOVERNANCE_ANCHOR_PREFIX
- WORKSPACE_EVENT_HELPER_CALLABLE_SYMBOLS
- WORKSPACE_EVENT_HELPER_CONSTANT_SYMBOLS
- WORKSPACE_EVENT_HELPER_INDEX_SYMBOLS
- SAFE_UPDATE_STEP_PATTERNS
- WORKSPACE_EVENT_SCAN_EXCLUDE_REASONS
- WORKSPACE_EVENT_SCAN_EXCLUDE_PARTS

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
    "workspace_event_static_diagnostics",
    "discover_workspace_event_emitter_modules",
    "should_exclude_workspace_event_scan_path",
    "assert_safe_update_step_patterns_integrity",
    "assert_safe_update_procedure_docstring",
)

WORKSPACE_EVENT_HELPER_CONSTANT_SYMBOLS: tuple[str, ...] = (
    "HELPER_INDEX_GOVERNANCE_ANCHOR_PREFIX",
    "WORKSPACE_EVENT_HELPER_INDEX_SYMBOLS",
    "SAFE_UPDATE_STEP_PATTERNS",
    "WORKSPACE_EVENT_SCAN_EXCLUDE_REASONS",
    "WORKSPACE_EVENT_SCAN_EXCLUDE_PARTS",
)

WORKSPACE_EVENT_HELPER_INDEX_SYMBOLS: tuple[str, ...] = (
    WORKSPACE_EVENT_HELPER_CALLABLE_SYMBOLS + WORKSPACE_EVENT_HELPER_CONSTANT_SYMBOLS
)


def should_exclude_workspace_event_scan_path(path: Path) -> bool:
    """True when a path should be excluded from workspace-event static scans."""
    return any(part in WORKSPACE_EVENT_SCAN_EXCLUDE_PARTS for part in path.parts)


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

