"""Unit tests for tier scoring and model ladder selection."""

from __future__ import annotations

import pytest

from le_vibe.models import choose_best_model, model_eligible_for_tier
from le_vibe.tier import (
    TIER_14B,
    TIER_32B_OK,
    TIER_32B_SLOW,
    TIER_70B,
    TIER_8B,
    TIER_SMALL,
    score_model_tier,
)
from le_vibe.types import GPUInfo, HardwareInfo, TierAssessment


def _hw(
    ram_gb: float,
    disk_free_gb: float,
    vram_gb: float | None = None,
    apple: bool = False,
) -> HardwareInfo:
    gb = 1024**3
    gpus = []
    if vram_gb is not None:
        gpus.append(GPUInfo("NVIDIA", "Test", int(vram_gb * gb), True))
    return HardwareInfo(
        cpu_model="Test CPU",
        arch="x86_64",
        ram_total_bytes=int(ram_gb * gb),
        ram_available_bytes=int(ram_gb * 0.5 * gb),
        disk_total_bytes=int(500 * gb),
        disk_free_bytes=int(disk_free_gb * gb),
        gpus=gpus,
        apple_silicon=apple,
        apple_unified_memory_bytes=int(ram_gb * gb) if apple else None,
        nvidia_present=bool(vram_gb),
        acceleration_mode="apple_unified" if apple else ("gpu" if vram_gb else "cpu_only"),
    )


def test_tier_strong_gpu_32b_comfortable():
    t = score_model_tier(_hw(ram_gb=64, disk_free_gb=80, vram_gb=24))
    assert t.tier in (TIER_32B_OK, TIER_70B, TIER_32B_SLOW)


def test_tier_laptop_14b():
    t = score_model_tier(_hw(ram_gb=32, disk_free_gb=60, vram_gb=8))
    assert t.tier in (TIER_14B, TIER_32B_SLOW, TIER_32B_OK)


def test_tier_small_fallback():
    t = score_model_tier(_hw(ram_gb=8, disk_free_gb=20, vram_gb=None))
    assert t.tier == TIER_SMALL


def test_choose_prefers_14b_when_32b_slow_without_allow_slow():
    hw = _hw(ram_gb=32, disk_free_gb=60, vram_gb=8)
    ta = TierAssessment(
        tier=TIER_32B_SLOW,
        rejected_higher=[],
        ram_score=0.5,
        vram_score=0.5,
        cpu_score=0.5,
        disk_score=0.5,
        os_score=1.0,
        notes="test",
    )
    d = choose_best_model(hw, [], ta, allow_slow=False, tag_check=lambda m: True)
    assert d.selected_model == "deepseek-r1:14b"


def test_choose_32b_when_slow_allowed():
    hw = _hw(ram_gb=64, disk_free_gb=80, vram_gb=24)
    ta = TierAssessment(
        tier=TIER_32B_SLOW,
        rejected_higher=[],
        ram_score=0.5,
        vram_score=0.5,
        cpu_score=0.5,
        disk_score=0.5,
        os_score=1.0,
        notes="test",
    )
    d = choose_best_model(hw, [], ta, allow_slow=True, tag_check=lambda m: True)
    assert d.selected_model == "deepseek-r1:32b"


def test_model_eligible_32b_slow():
    ok, _ = model_eligible_for_tier("deepseek-r1:32b", TIER_32B_SLOW, allow_slow=False)
    assert ok is False
    ok2, _ = model_eligible_for_tier("deepseek-r1:32b", TIER_32B_SLOW, allow_slow=True)
    assert ok2 is True
