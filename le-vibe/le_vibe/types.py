from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class OSType(str, Enum):
    WINDOWS = "windows"
    MACOS = "macos"
    LINUX = "linux"
    UNKNOWN = "unknown"


@dataclass
class OSInfo:
    os_type: OSType
    name: str
    version: str | None
    arch: str
    release: str | None = None


@dataclass
class GPUInfo:
    vendor: str | None
    model: str | None
    vram_bytes: int | None
    driver_ok: bool | None
    notes: str = ""


@dataclass
class HardwareInfo:
    cpu_model: str
    arch: str
    ram_total_bytes: int
    ram_available_bytes: int
    disk_total_bytes: int
    disk_free_bytes: int
    gpus: list[GPUInfo]
    apple_silicon: bool
    apple_unified_memory_bytes: int | None
    nvidia_present: bool
    acceleration_mode: str  # "gpu", "apple_unified", "cpu_only", "hybrid"
    raw: dict[str, Any] = field(default_factory=dict)


@dataclass
class CheckResult:
    name: str
    ok: bool
    message: str


@dataclass
class TierAssessment:
    tier: str
    rejected_higher: list[tuple[str, str]]  # (tier_name, reason)
    ram_score: float
    vram_score: float
    cpu_score: float
    disk_score: float
    os_score: float
    notes: str


@dataclass
class RejectedCandidate:
    model: str
    reason: str


@dataclass
class ModelDecision:
    selected_model: str
    selected_tier: str
    comfortable: bool
    reason: str
    rejected_candidates: list[RejectedCandidate]


@dataclass
class ServiceResult:
    ok: bool
    message: str
    pid: int | None = None
    method: str | None = None


@dataclass
class BootstrapState:
    os_info: OSInfo
    hardware: HardwareInfo
    prerequisites: list[CheckResult]
    tier_assessment: TierAssessment | None
    model_decision: ModelDecision | None
    ollama_installed: bool
    ollama_version: str | None
    ollama_was_running: bool
    ollama_started_by_script: bool
    port_in_use_before: bool
    host: str
    port: int
    api_verified: bool
    dry_run: bool
    install_log: str = ""
    pull_log: str = ""
