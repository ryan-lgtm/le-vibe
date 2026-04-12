from __future__ import annotations

import os
import platform
import re
import shutil
import socket
import subprocess
from pathlib import Path
from typing import Any

import psutil

from .types import GPUInfo, HardwareInfo, OSInfo, OSType


def detect_os() -> OSInfo:
    system = platform.system().lower()
    release = platform.release()
    ver = platform.version()
    arch = platform.machine().lower()

    if system == "windows":
        return OSInfo(
            os_type=OSType.WINDOWS,
            name="Windows",
            version=release,
            arch=arch,
            release=ver,
        )
    if system == "darwin":
        mac_ver = platform.mac_ver()[0] or None
        return OSInfo(
            os_type=OSType.MACOS,
            name="macOS",
            version=mac_ver,
            arch=arch,
            release=release,
        )
    if system == "linux":
        return OSInfo(
            os_type=OSType.LINUX,
            name="Linux",
            version=release,
            arch=arch,
            release=ver,
        )
    return OSInfo(os_type=OSType.UNKNOWN, name=platform.system(), version=None, arch=arch)


def _run_capture(cmd: list[str], timeout: float = 8.0) -> tuple[int, str]:
    try:
        r = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            env={**os.environ, "LC_ALL": "C"},
        )
        out = (r.stdout or "") + (r.stderr or "")
        return r.returncode, out.strip()
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
        return -1, ""


def _parse_nvidia_smi() -> tuple[list[GPUInfo], bool]:
    gpus: list[GPUInfo] = []
    code, out = _run_capture(["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader,nounits"])
    if code != 0 or not out:
        return gpus, False
    driver_ok = True
    for line in out.splitlines():
        line = line.strip()
        if not line:
            continue
        parts = [p.strip() for p in line.split(",")]
        if len(parts) >= 2:
            name = parts[0]
            try:
                mib = int(float(parts[1]))
                vram = mib * 1024 * 1024
            except ValueError:
                vram = None
            gpus.append(
                GPUInfo(
                    vendor="NVIDIA",
                    model=name,
                    vram_bytes=vram,
                    driver_ok=driver_ok,
                )
            )
    return gpus, bool(gpus)


def _apple_silicon_info() -> tuple[bool, int | None, str]:
    if platform.system() != "Darwin":
        return False, None, ""
    arch = platform.machine().lower()
    if arch != "arm64":
        return False, None, ""
    vm = psutil.virtual_memory()
    return True, vm.total, "Apple Silicon unified memory (total RAM used for GPU)"


def _rocm_gpu() -> list[GPUInfo]:
    code, out = _run_capture(["rocm-smi", "--showmeminfo", "vram"])
    if code != 0:
        return []
    gpus: list[GPUInfo] = []
    for m in re.finditer(r"(\d+)\s*MiB", out):
        try:
            mib = int(m.group(1))
            vram = mib * 1024 * 1024
        except ValueError:
            continue
        gpus.append(GPUInfo(vendor="AMD", model="ROCm GPU", vram_bytes=vram, driver_ok=True))
    if not gpus and "GPU" in out:
        gpus.append(GPUInfo(vendor="AMD", model="ROCm", vram_bytes=None, driver_ok=True))
    return gpus


def detect_hardware() -> HardwareInfo:
    cpu_model = platform.processor() or "unknown"
    try:
        if Path("/proc/cpuinfo").is_file():
            with open("/proc/cpuinfo", encoding="utf-8", errors="replace") as f:
                for line in f:
                    if line.startswith("model name"):
                        cpu_model = line.split(":", 1)[1].strip()
                        break
    except OSError:
        pass

    arch = platform.machine().lower()
    vm = psutil.virtual_memory()
    du = shutil.disk_usage(Path.cwd())

    apple_si, unified, apple_note = _apple_silicon_info()
    nvidia_gpus, nvidia_ok = _parse_nvidia_smi()
    rocm = _rocm_gpu()
    gpus = nvidia_gpus + rocm

    if apple_si:
        acceleration_mode = "apple_unified"
    elif nvidia_gpus:
        acceleration_mode = "hybrid" if vm.total < 16 * 1024**3 else "gpu"
    elif rocm:
        acceleration_mode = "hybrid"
    else:
        acceleration_mode = "cpu_only"

    raw: dict[str, Any] = {"apple_note": apple_note}
    return HardwareInfo(
        cpu_model=cpu_model,
        arch=arch,
        ram_total_bytes=vm.total,
        ram_available_bytes=vm.available,
        disk_total_bytes=du.total,
        disk_free_bytes=du.free,
        gpus=gpus,
        apple_silicon=apple_si,
        apple_unified_memory_bytes=unified if apple_si else None,
        nvidia_present=bool(nvidia_gpus),
        acceleration_mode=acceleration_mode,
        raw=raw,
    )


def is_port_open(host: str, port: int, timeout: float = 0.5) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


def port_in_use(host: str, port: int) -> bool:
    return is_port_open(host, port)
