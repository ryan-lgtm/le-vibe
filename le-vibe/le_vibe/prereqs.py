from __future__ import annotations

import shutil
import subprocess
import urllib.request

from .types import CheckResult, OSInfo, OSType


def check_prerequisites(os_info: OSInfo) -> list[CheckResult]:
    results: list[CheckResult] = []

    # Internet
    try:
        urllib.request.urlopen("https://ollama.com", timeout=8)
        results.append(CheckResult("internet", True, "reachable https://ollama.com"))
    except OSError as e:
        results.append(CheckResult("internet", False, str(e)))

    for tool in ("curl", "tar"):
        p = shutil.which(tool)
        results.append(CheckResult(tool, p is not None, p or f"missing {tool}"))

    if os_info.os_type == OSType.LINUX:
        if shutil.which("systemctl"):
            results.append(CheckResult("systemctl", True, "present"))
        else:
            results.append(CheckResult("systemctl", False, "optional; user-session start fallback"))

    return results


def ollama_version() -> tuple[bool, str | None]:
    try:
        r = subprocess.run(
            ["ollama", "--version"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if r.returncode == 0:
            return True, (r.stdout or r.stderr or "").strip().splitlines()[0]
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
        pass
    return False, None
