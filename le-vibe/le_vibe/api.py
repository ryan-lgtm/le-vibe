"""Importable bootstrap API for the Lé Vibe desktop and CLI."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path

from .detect import detect_hardware, detect_os, port_in_use
from .models import choose_best_model, clear_tag_cache, get_available_model_tags
from .ollama_ops import install_ollama, is_ollama_running, pull_model, start_ollama_service, verify_api
from .prereqs import check_prerequisites, ollama_version
from .reporting import generate_continue_config, generate_report, write_model_decision_json
from .managed_ollama import ensure_managed_ollama
from .tier import score_model_tier
from .types import BootstrapState, OSType, ServiceResult


@dataclass
class EnsureBootstrapArgs:
    dry_run: bool = False
    force_reinstall: bool = False
    model: str | None = None
    allow_slow: bool = False
    host: str = "127.0.0.1"
    port: int = 11434
    yes: bool = False
    verbose: bool = False
    # If set, write Continue config, report, and model-decision.json under this directory (e.g. ~/.config/le-vibe/).
    config_dir: Path | None = None
    # When True, start Ollama via ensure_managed_ollama() so PID state matches the launcher (Phase 2 product).
    use_managed_ollama: bool = False


def print_final_instructions(state: BootstrapState, config_hint: Path | None = None) -> None:
    host, port = state.host, state.port
    api = f"http://{host}:{port}"
    print()
    if state.dry_run:
        print("(Dry run — Ollama was not started and models were not pulled.)")
        print("Planned API endpoint:")
        print(api)
    else:
        print("Lé Vibe: local stack is up. Ollama API:")
        print(api)
    print()
    if state.model_decision and state.model_decision.selected_model:
        print("Selected model:")
        print(state.model_decision.selected_model)
        print()
        print("Why this model was chosen:")
        print(state.model_decision.reason)
        print()
    cont = config_hint or Path("(see output/continue-config.yaml)")
    print("To use Continue in Lé Vibe (Code - OSS):")
    print("1. Ensure the Continue extension is installed.")
    print("2. Open Continue config.")
    print("3. Import or paste:")
    print(f"   {cont}")
    print("4. Confirm apiBase is:")
    print(f"   http://localhost:{port}")
    print("5. Choose the local model in Continue.")
    print()
    print("To stop Ollama later (standalone bootstrap, not Lé Vibe managed mode):")
    if state.os_info.os_type == OSType.WINDOWS:
        print("  Run: .\\scripts\\stop_windows.ps1")
    elif state.os_info.os_type == OSType.MACOS:
        print("  Run: bash ./scripts/stop_macos.sh")
    else:
        print("  Run: bash ./scripts/stop_linux.sh")
    print()


def ensure_bootstrap(args: EnsureBootstrapArgs) -> tuple[int, BootstrapState]:
    """
    Phase 1 bootstrap: install Ollama if needed, select model, pull, start service, emit configs.

    Returns (exit_code, state). Exit codes: 0 success, 2 unsupported OS, 3 no model, 4 install fail,
    5 pull fail, 6 start fail, 7 API fail.
    """
    clear_tag_cache()

    os_info = detect_os()
    if os_info.os_type not in (OSType.WINDOWS, OSType.MACOS, OSType.LINUX):
        logging.error("Unsupported OS: %s", os_info.name)
        return 2, BootstrapState(
            os_info=os_info,
            hardware=detect_hardware(),
            prerequisites=[],
            tier_assessment=None,
            model_decision=None,
            ollama_installed=False,
            ollama_version=None,
            ollama_was_running=False,
            ollama_started_by_script=False,
            port_in_use_before=False,
            host=args.host,
            port=args.port,
            api_verified=False,
            dry_run=args.dry_run,
        )

    hw = detect_hardware()
    prereqs = check_prerequisites(os_info)
    port_busy = port_in_use(args.host, args.port)
    ollama_ok, ollama_ver = ollama_version()
    already_running = is_ollama_running(args.host, args.port)

    tier = score_model_tier(hw)
    tags = get_available_model_tags(verbose=args.verbose)
    decision = choose_best_model(
        hw,
        tags,
        tier,
        user_override=args.model,
        allow_slow=args.allow_slow,
    )

    state = BootstrapState(
        os_info=os_info,
        hardware=hw,
        prerequisites=prereqs,
        tier_assessment=tier,
        model_decision=decision,
        ollama_installed=ollama_ok,
        ollama_version=ollama_ver,
        ollama_was_running=already_running,
        ollama_started_by_script=False,
        port_in_use_before=port_busy,
        host=args.host,
        port=args.port,
        api_verified=already_running,
        dry_run=args.dry_run,
    )

    if not decision.selected_model and not args.dry_run:
        logging.error("Could not select a model. See model-decision.json")
        write_model_decision_json(decision, config_dir=args.config_dir)
        generate_report(state, config_dir=args.config_dir)
        return 3, state

    if args.dry_run:
        logging.info("Dry run: skipping install, pull, and start.")
        write_model_decision_json(decision, config_dir=args.config_dir)
        if decision.selected_model:
            generate_continue_config(decision.selected_model, args.host, args.port, config_dir=args.config_dir)
        generate_report(state, config_dir=args.config_dir)
        return 0, state

    if not ollama_ok:
        ok, log_out = install_ollama(os_info, args.force_reinstall, args.yes)
        state.install_log = log_out[:8000]
        if not ok:
            logging.error("Ollama install failed. Log excerpt:\n%s", log_out[:2000])
            write_model_decision_json(decision, config_dir=args.config_dir)
            generate_report(state, config_dir=args.config_dir)
            return 4, state
        ollama_ok, ollama_ver = ollama_version()
        state.ollama_installed = ollama_ok
        state.ollama_version = ollama_ver

    if not decision.selected_model:
        write_model_decision_json(decision, config_dir=args.config_dir)
        generate_report(state, config_dir=args.config_dir)
        return 3, state

    if port_busy and not already_running:
        logging.warning(
            "Port %s is in use but Ollama API did not respond. Stop the other process or use --port.",
            args.port,
        )

    logging.info("Launching local Ollama for Lé Vibe (if not already running)...")
    if args.use_managed_ollama:
        m_ok, m_msg, _st = ensure_managed_ollama(host=args.host, port=args.port)
        sr = ServiceResult(m_ok, m_msg, method="managed" if m_ok else None)
        state.ollama_started_by_script = m_ok
    else:
        sr = start_ollama_service(args.host, args.port, os_info)
        state.ollama_started_by_script = bool(sr.ok and sr.method in ("script", "direct"))
    if not sr.ok:
        logging.error("Could not launch Ollama: %s", sr.message)
        write_model_decision_json(decision, config_dir=args.config_dir)
        generate_report(state, config_dir=args.config_dir)
        return 6, state
    if sr.method == "existing":
        logging.info("Ollama already running on %s:%s", args.host, args.port)
    elif sr.method == "managed":
        logging.info("Ollama ready (managed): %s", sr.message)
    else:
        logging.info("Ollama ready: %s", sr.message)

    logging.info(
        "Pulling model %s — large downloads can take many minutes; progress from ollama follows.",
        decision.selected_model,
    )
    ok, pull_log = pull_model(decision.selected_model)
    state.pull_log = pull_log[-8000:] if len(pull_log) > 8000 else pull_log
    if not ok:
        logging.error("ollama pull failed: %s", pull_log[-2000:])
        write_model_decision_json(decision, config_dir=args.config_dir)
        generate_report(state, config_dir=args.config_dir)
        return 5, state

    state.api_verified = verify_api(args.host, args.port)
    if not state.api_verified:
        logging.error("API check failed at http://%s:%s", args.host, args.port)
        write_model_decision_json(decision, config_dir=args.config_dir)
        generate_report(state, config_dir=args.config_dir)
        return 7, state

    generate_continue_config(decision.selected_model, args.host, args.port, config_dir=args.config_dir)
    write_model_decision_json(decision, config_dir=args.config_dir)
    generate_report(state, config_dir=args.config_dir)
    return 0, state
