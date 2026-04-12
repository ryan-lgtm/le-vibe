from __future__ import annotations

from .types import HardwareInfo, TierAssessment

# Tier names must match spec
TIER_70B = "tier_70b_candidate"
TIER_32B_OK = "tier_32b_comfortable"
TIER_32B_SLOW = "tier_32b_possible_but_slow"
TIER_14B = "tier_14b_comfortable"
TIER_8B = "tier_8b_comfortable"
TIER_SMALL = "tier_small_fallback_only"


def _gb(b: int) -> float:
    return b / (1024**3)


def score_model_tier(hw: HardwareInfo) -> TierAssessment:
    """Heuristic tier from RAM, VRAM/unified memory, disk, CPU class."""
    ram_g = _gb(hw.ram_total_bytes)
    free_g = _gb(hw.disk_free_bytes)
    avail_g = _gb(hw.ram_available_bytes)

    max_vram_g = 0.0
    if hw.gpus:
        for g in hw.gpus:
            if g.vram_bytes:
                max_vram_g = max(max_vram_g, _gb(g.vram_bytes))

    effective_mem_g = ram_g
    if hw.apple_silicon and hw.apple_unified_memory_bytes:
        effective_mem_g = _gb(hw.apple_unified_memory_bytes)
        max_vram_g = max(max_vram_g, effective_mem_g * 0.85)

    # Scores 0..1 for logging
    ram_score = min(1.0, ram_g / 128.0)
    vram_score = min(1.0, max_vram_g / 80.0) if max_vram_g else 0.0
    cpu_score = 0.5
    if "xeon" in hw.cpu_model.lower() or "threadripper" in hw.cpu_model.lower():
        cpu_score = 0.85
    elif "i9" in hw.cpu_model or "ryzen 9" in hw.cpu_model.lower():
        cpu_score = 0.75
    disk_score = min(1.0, free_g / 200.0)
    os_score = 1.0

    rejected: list[tuple[str, str]] = []

    def reject(tier: str, reason: str) -> None:
        rejected.append((tier, reason))

    # Minimum disk for large models (~50GB headroom for 70B class)
    if free_g < 15:
        reject(TIER_70B, f"low free disk (~{free_g:.1f} GB); need comfortable headroom for large weights")
        reject(TIER_32B_OK, "insufficient free disk for comfortable 32B")
        reject(TIER_32B_SLOW, "very low disk for 32B weights")

    # 70B: need very strong memory (unified or VRAM + RAM) — conservative
    can_70b = False
    if free_g >= 45 and (max_vram_g >= 42 or (hw.apple_silicon and effective_mem_g >= 64)):
        can_70b = True
    elif free_g >= 45 and ram_g >= 96 and max_vram_g >= 24:
        can_70b = True
    if not can_70b:
        reject(TIER_70B, "insufficient VRAM/unified memory or RAM for 70B-class comfortable run")

    # 32B comfortable: ~24–40GB effective for weights + KV — use unified or 32GB+ class
    can_32_ok = False
    if free_g >= 22:
        if hw.apple_silicon and effective_mem_g >= 36:
            can_32_ok = True
        elif max_vram_g >= 22:
            can_32_ok = True
        elif ram_g >= 48 and max_vram_g >= 12:
            can_32_ok = True
    if not can_32_ok:
        reject(TIER_32B_OK, "not enough comfortable memory headroom for 32B")

    can_32_slow = False
    if free_g >= 20:
        if effective_mem_g >= 28 or max_vram_g >= 16 or ram_g >= 40:
            can_32_slow = True
    if not can_32_slow:
        reject(TIER_32B_SLOW, "below threshold for 32B even as slow tier")

    can_14 = free_g >= 12 and (effective_mem_g >= 18 or max_vram_g >= 10 or ram_g >= 24)
    if not can_14:
        reject(TIER_14B, "insufficient memory for comfortable 14B")

    can_8 = free_g >= 8 and (effective_mem_g >= 10 or max_vram_g >= 6 or ram_g >= 16)
    if not can_8:
        reject(TIER_8B, "insufficient resources for comfortable 8B")

    notes_parts = [
        f"ram={ram_g:.1f}GB avail={avail_g:.1f}GB",
        f"disk_free={free_g:.1f}GB",
        f"max_vram≈{max_vram_g:.1f}GB",
        f"accel={hw.acceleration_mode}",
    ]
    notes = "; ".join(notes_parts)

    if can_70b:
        chosen = TIER_70B
    elif can_32_ok:
        chosen = TIER_32B_OK
    elif can_32_slow:
        chosen = TIER_32B_SLOW
    elif can_14:
        chosen = TIER_14B
    elif can_8:
        chosen = TIER_8B
    else:
        chosen = TIER_SMALL

    return TierAssessment(
        tier=chosen,
        rejected_higher=rejected,
        ram_score=ram_score,
        vram_score=vram_score,
        cpu_score=cpu_score,
        disk_score=disk_score,
        os_score=os_score,
        notes=notes,
    )
