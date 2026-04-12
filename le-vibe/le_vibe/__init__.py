"""le-vibe: hardware-aware local Ollama model setup for Continue + Code - OSS (Lé Vibe)."""

from .api import EnsureBootstrapArgs, ensure_bootstrap, print_final_instructions
from .first_run import ensure_product_first_run, first_run_marker_path
from .managed_ollama import (
    ManagedOllamaState,
    ensure_managed_ollama,
    stop_managed_ollama,
)
from .paths import LE_VIBE_MANAGED_OLLAMA_PORT, le_vibe_config_dir
from .reporting import LOCKED_MODEL_FILENAME
from .continue_workspace import (
    LVIBE_CONTINUE_RULE_NAME,
    PRODUCT_WELCOME_RULE_NAME,
    ensure_continue_lvibe_rules,
)
from .editor_welcome import WELCOME_MD_NAME, ensure_lvibe_welcome_md
from .session_orchestrator import (
    apply_opening_skip,
    ensure_pm_session_artifacts,
    iter_tasks_in_epic_order,
    load_session_manifest,
)
from .welcome import maybe_print_welcome, welcome_marker_path
from .workspace_hub import (
    ensure_gitignore_has_lvibe,
    ensure_lvibe_workspace,
    prepare_workspaces_for_editor_args,
    workspace_roots_from_editor_args,
)

__version__ = "1.0.0"

__all__ = [
    "EnsureBootstrapArgs",
    "LE_VIBE_MANAGED_OLLAMA_PORT",
    "LOCKED_MODEL_FILENAME",
    "LVIBE_CONTINUE_RULE_NAME",
    "PRODUCT_WELCOME_RULE_NAME",
    "WELCOME_MD_NAME",
    "ManagedOllamaState",
    "apply_opening_skip",
    "ensure_continue_lvibe_rules",
    "ensure_lvibe_welcome_md",
    "ensure_bootstrap",
    "ensure_gitignore_has_lvibe",
    "ensure_lvibe_workspace",
    "ensure_managed_ollama",
    "ensure_pm_session_artifacts",
    "ensure_product_first_run",
    "first_run_marker_path",
    "iter_tasks_in_epic_order",
    "le_vibe_config_dir",
    "load_session_manifest",
    "maybe_print_welcome",
    "prepare_workspaces_for_editor_args",
    "print_final_instructions",
    "stop_managed_ollama",
    "welcome_marker_path",
    "workspace_roots_from_editor_args",
]
