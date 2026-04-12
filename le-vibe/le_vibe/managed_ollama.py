"""Start/stop Lé Vibe–managed `ollama serve` with a dedicated host:port (spec-phase2 §7.1–7.2-A)."""

from __future__ import annotations

import json
import os
import shutil
import signal
import subprocess
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .ollama_ops import is_ollama_running
from .paths import LE_VIBE_MANAGED_OLLAMA_PORT, managed_ollama_state_path
from .structured_log import append_structured_log

SIGTERM_WAIT_SEC = 12.0
SIGKILL_WAIT_SEC = 3.0


@dataclass
class ManagedOllamaState:
    """Persisted under ~/.config/le-vibe/managed_ollama.json."""

    pid: int
    host: str
    port: int
    session_id: str
    started_at_unix: float

    def to_json(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> ManagedOllamaState:
        return cls(
            pid=int(data["pid"]),
            host=str(data["host"]),
            port=int(data["port"]),
            session_id=str(data["session_id"]),
            started_at_unix=float(data["started_at_unix"]),
        )


def _read_state(path: Path) -> ManagedOllamaState | None:
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return ManagedOllamaState.from_json(data)
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError):
        return None


def _write_state(path: Path, state: ManagedOllamaState) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state.to_json(), indent=2), encoding="utf-8")


def _pid_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    return True


def _is_our_port_responding(host: str, port: int, expected_pid: int) -> bool:
    if not is_ollama_running(host, port):
        return False
    # Best-effort: API up and PID still alive (dedicated port ⇒ should be our serve).
    return _pid_alive(expected_pid)


def ensure_managed_ollama(
    host: str = "127.0.0.1",
    port: int | None = None,
    state_path: Path | None = None,
    session_id: str = "default",
) -> tuple[bool, str, ManagedOllamaState | None]:
    """
    Start `ollama serve` bound to OLLAMA_HOST=host:port, new session, record PID.

    If the same state already matches a live API on that port, returns success without spawning.

    If the port answers but the recorded PID is stale or missing, returns failure (do not kill strangers).
    """
    if port is None:
        port = LE_VIBE_MANAGED_OLLAMA_PORT
    path = state_path or managed_ollama_state_path()
    ollama_bin = shutil.which("ollama")
    if not ollama_bin:
        append_structured_log(
            "managed_ollama",
            "ensure_failed",
            reason="ollama_not_in_path",
            host=host,
            port=port,
        )
        return False, "ollama binary not in PATH", None

    existing = _read_state(path)
    if existing and (existing.host != host or existing.port != port):
        existing = None
    if existing and existing.host == host and existing.port == port:
        if _is_our_port_responding(host, port, existing.pid):
            append_structured_log(
                "managed_ollama",
                "ensure_ok",
                detail="already_running",
                host=host,
                port=port,
                pid=existing.pid,
            )
            return True, "managed Ollama already running for this session", existing
        # Stale file
        try:
            path.unlink(missing_ok=True)
        except OSError:
            pass

    if is_ollama_running(host, port):
        append_structured_log(
            "managed_ollama",
            "ensure_failed",
            reason="port_in_use_not_managed",
            host=host,
            port=port,
        )
        return (
            False,
            f"port {port} already serves an HTTP API but is not Lé Vibe–managed "
            f"(or stale state was cleared). Choose another port or free {host}:{port}.",
            None,
        )

    env = {**os.environ, "OLLAMA_HOST": f"{host}:{port}"}
    try:
        proc = subprocess.Popen(
            [ollama_bin, "serve"],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            env=env,
            start_new_session=True,
        )
    except OSError as e:
        append_structured_log(
            "managed_ollama",
            "ensure_failed",
            reason="spawn_error",
            host=host,
            port=port,
            error=str(e),
        )
        return False, f"failed to spawn ollama serve: {e}", None

    pid = proc.pid
    started = time.time()
    state = ManagedOllamaState(
        pid=pid,
        host=host,
        port=port,
        session_id=session_id,
        started_at_unix=started,
    )
    _write_state(path, state)

    deadline = time.time() + 45
    while time.time() < deadline:
        if is_ollama_running(host, port):
            append_structured_log(
                "managed_ollama",
                "ensure_ok",
                detail="started",
                host=host,
                port=port,
                pid=pid,
            )
            return True, f"started managed Ollama pid={pid} on {host}:{port}", state
        if proc.poll() is not None:
            try:
                path.unlink(missing_ok=True)
            except OSError:
                pass
            append_structured_log(
                "managed_ollama",
                "ensure_failed",
                reason="serve_exited_early",
                host=host,
                port=port,
                exit_code=proc.returncode,
            )
            return False, f"ollama serve exited early (code {proc.returncode})", None
        time.sleep(0.25)

    try:
        path.unlink(missing_ok=True)
    except OSError:
        pass
    _terminate_tree(pid)
    append_structured_log(
        "managed_ollama",
        "ensure_failed",
        reason="ready_timeout",
        host=host,
        port=port,
        pid=pid,
    )
    return False, "managed Ollama did not become ready in time", None


def stop_managed_ollama(state_path: Path | None = None) -> tuple[bool, str]:
    """SIGTERM managed process group, wait, then SIGKILL. Removes state file on success."""
    path = state_path or managed_ollama_state_path()
    state = _read_state(path)
    if state is None:
        append_structured_log("managed_ollama", "stop_ok", detail="no_state")
        return True, "no managed Ollama state (nothing to stop)"

    pid = state.pid
    if not _pid_alive(pid):
        try:
            path.unlink(missing_ok=True)
        except OSError:
            pass
        append_structured_log("managed_ollama", "stop_ok", detail="process_already_gone", pid=pid)
        return True, "managed process already gone"

    _terminate_tree(pid)
    t0 = time.time()
    while time.time() - t0 < SIGKILL_WAIT_SEC:
        if not _pid_alive(pid):
            try:
                path.unlink(missing_ok=True)
            except OSError:
                pass
            append_structured_log("managed_ollama", "stop_ok", detail="sigterm", pid=pid)
            return True, "stopped managed Ollama"
        time.sleep(0.1)

    try:
        path.unlink(missing_ok=True)
    except OSError:
        pass
    append_structured_log("managed_ollama", "stop_uncertain", pid=pid)
    return False, f"could not confirm stop for pid {pid}"


def _terminate_tree(pid: int) -> None:
    if os.name == "nt":
        # Launcher milestone targets Linux; keep a safe no-op path.
        try:
            os.kill(pid, signal.SIGTERM)
        except OSError:
            pass
        return
    try:
        os.killpg(pid, signal.SIGTERM)
    except OSError:
        try:
            os.kill(pid, signal.SIGTERM)
        except OSError:
            pass
    t0 = time.time()
    while time.time() - t0 < SIGTERM_WAIT_SEC:
        if not _pid_alive(pid):
            return
        time.sleep(0.1)
    try:
        os.killpg(pid, signal.SIGKILL)
    except OSError:
        try:
            os.kill(pid, signal.SIGKILL)
        except OSError:
            pass
