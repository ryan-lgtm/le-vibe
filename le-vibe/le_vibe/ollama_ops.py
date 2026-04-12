from __future__ import annotations

import os
import shutil
import subprocess
import time
from pathlib import Path

import requests

from .types import OSInfo, OSType, ServiceResult


def is_ollama_running(host: str, port: int) -> bool:
    try:
        r = requests.get(f"http://{host}:{port}/api/tags", timeout=3)
        return r.status_code == 200
    except requests.RequestException:
        return False


def pull_model(model_tag: str) -> tuple[bool, str]:
    """
    Run `ollama pull` with output on the TTY so progress is visible (capturing looked like a hang).
    """
    try:
        p = subprocess.run(
            ["ollama", "pull", model_tag],
            timeout=7200,
        )
        ok = p.returncode == 0
        note = "ok" if ok else f"exit {p.returncode}"
        return ok, note
    except subprocess.TimeoutExpired:
        return False, "pull timed out"
    except FileNotFoundError:
        return False, "ollama binary not found"


def _scripts_dir() -> Path:
    return Path(__file__).resolve().parent.parent / "scripts"


def install_ollama(os_info: OSInfo, force: bool, non_interactive: bool) -> tuple[bool, str]:
    script_dir = _scripts_dir()
    env = os.environ.copy()
    if non_interactive:
        env["BOOTSTRAP_YES"] = "1"

    if os_info.os_type == OSType.WINDOWS:
        ps1 = script_dir / "install_windows.ps1"
        cmd = [
            "powershell.exe",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            str(ps1),
        ]
        if force:
            cmd.append("-Force")
    elif os_info.os_type == OSType.MACOS:
        sh = script_dir / "install_macos.sh"
        cmd = ["bash", str(sh)] + (["--force"] if force else [])
    elif os_info.os_type == OSType.LINUX:
        sh = script_dir / "install_linux.sh"
        cmd = ["bash", str(sh)] + (["--force"] if force else [])
    else:
        return False, "unsupported OS for install"

    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=600, env=env)
        out = (r.stdout or "") + (r.stderr or "")
        return r.returncode == 0, out
    except Exception as e:
        return False, str(e)


def start_ollama_service(host: str, port: int, os_info: OSInfo) -> ServiceResult:
    """
    Launch le-vibe's local stack: ensure Ollama is listening on host:port.
    Runs before model pull so the daemon is explicitly started, not only implied by `ollama pull`.
    """
    if is_ollama_running(host, port):
        return ServiceResult(True, "Ollama API already responding", method="existing")

    ollama_bin = shutil.which("ollama")
    if not ollama_bin:
        return ServiceResult(False, "ollama not in PATH after install")

    script_dir = _scripts_dir()
    if os_info.os_type == OSType.WINDOWS:
        ps1 = script_dir / "start_windows.ps1"
        cmd = ["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(ps1)]
    elif os_info.os_type == OSType.MACOS:
        cmd = ["bash", str(script_dir / "start_macos.sh")]
    else:
        cmd = ["bash", str(script_dir / "start_linux.sh")]

    env = {**os.environ, "OLLAMA_HOST": f"{host}:{port}"}
    try:
        subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            env=env,
            start_new_session=True,
        )
    except Exception as e:
        return ServiceResult(False, f"start script failed: {e}")

    if _wait_for_api(host, port, seconds=30):
        return ServiceResult(True, "Ollama launched via platform start script", method="script")

    # Fallback: run `ollama serve` directly (same as scripts, but guaranteed from this process tree)
    try:
        subprocess.Popen(
            [ollama_bin, "serve"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            env=env,
            start_new_session=True,
        )
    except OSError as e:
        return ServiceResult(False, f"ollama serve fallback failed: {e}")

    if _wait_for_api(host, port, seconds=45):
        return ServiceResult(True, "Ollama launched via `ollama serve`", method="direct")

    return ServiceResult(False, "Ollama did not become ready after script and direct serve")


def _wait_for_api(host: str, port: int, seconds: int) -> bool:
    for _ in range(seconds):
        time.sleep(1)
        if is_ollama_running(host, port):
            return True
    return False


def verify_api(host: str, port: int) -> bool:
    return is_ollama_running(host, port)
