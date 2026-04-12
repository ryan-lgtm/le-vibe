from __future__ import annotations

import logging
import re
import subprocess
from typing import Callable

from .tier import (
    TIER_70B,
    TIER_32B_OK,
    TIER_32B_SLOW,
    TIER_14B,
    TIER_8B,
    TIER_SMALL,
)
from .types import HardwareInfo, ModelDecision, RejectedCandidate, TierAssessment

log = logging.getLogger(__name__)

# Ordered fallback ladder (spec): try first successful tag in this order
PRIMARY_LADDER = [
    "deepseek-r1:70b",
    "deepseek-r1:32b",
    "deepseek-r1:14b",
    "deepseek-r1:8b",
    "deepseek-r1:7b",
    "deepseek-r1:1.5b",
]

SECONDARY_LADDER = [
    "qwen2.5-coder:7b",
    "qwen2.5-coder:3b",
    "qwen2.5-coder:1.5b",
]

KNOWN_LIBRARY_TAGS = set(PRIMARY_LADDER + SECONDARY_LADDER)

TAG_CACHE: list[str] | None = None


def _run(cmd: list[str], timeout: float = 120.0) -> tuple[int, str]:
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return r.returncode, (r.stdout or "") + (r.stderr or "")
    except Exception as e:
        return -1, str(e)


def tag_exists_in_registry(model_tag: str) -> bool:
    """Prefer `ollama show` when installed; else trust known library tags (pull validates)."""
    code, out = _run(["ollama", "show", model_tag], timeout=60)
    if code == 0 and "Error" not in out[:200]:
        return True

    # Registry endpoints vary; trust canonical Ollama library names so install can proceed
    # before `ollama` exists — `ollama pull` remains the real validation.
    if model_tag in KNOWN_LIBRARY_TAGS:
        log.debug(
            "Unverified online; treating %s as a known Ollama library tag (pull will confirm).",
            model_tag,
        )
        return True
    return False


def get_available_model_tags(verbose: bool = False) -> list[str]:
    """Local `ollama list` plus verified ladder tags."""
    global TAG_CACHE
    if TAG_CACHE is not None:
        return TAG_CACHE

    found: set[str] = set()
    code, out = _run(["ollama", "list"], timeout=30)
    if code == 0:
        for line in out.splitlines()[1:]:
            parts = line.split()
            if parts:
                found.add(parts[0].strip())

    for model in PRIMARY_LADDER + SECONDARY_LADDER:
        if tag_exists_in_registry(model):
            found.add(model)
            if verbose:
                log.debug("tag ok: %s", model)

    TAG_CACHE = sorted(found)
    return TAG_CACHE


def clear_tag_cache() -> None:
    global TAG_CACHE
    TAG_CACHE = None


def model_eligible_for_tier(model_tag: str, machine_tier: str, allow_slow: bool) -> tuple[bool, str]:
    """Whether this machine tier may select this model as a comfortable (or allowed slow) default."""
    mt = machine_tier
    t = model_tag.lower()

    if "70b" in t or ":70b" in t:
        ok = mt == TIER_70B
        return ok, "" if ok else "70B requires tier_70b_candidate"

    if "32b" in t:
        if mt in (TIER_70B, TIER_32B_OK):
            return True, ""
        if mt == TIER_32B_SLOW:
            if allow_slow:
                return True, ""
            return False, "32B is possible-but-slow on this machine; use --allow-slow for 32B"
        return False, "insufficient tier for comfortable 32B"

    if "14b" in t:
        ok = mt in (TIER_70B, TIER_32B_OK, TIER_32B_SLOW, TIER_14B)
        return ok, "" if ok else "insufficient tier for 14B"

    if "8b" in t:
        ok = mt in (TIER_70B, TIER_32B_OK, TIER_32B_SLOW, TIER_14B, TIER_8B)
        return ok, "" if ok else "insufficient tier for 8B class"

    if "7b" in t:
        ok = mt in (TIER_70B, TIER_32B_OK, TIER_32B_SLOW, TIER_14B, TIER_8B, TIER_SMALL)
        return ok, "" if ok else "insufficient tier for 7B class"

    if "3b" in t or "1.5b" in t:
        return True, ""

    return True, ""


def choose_best_model(
    hardware: HardwareInfo,
    available_tags: list[str],
    assessment: TierAssessment,
    user_override: str | None = None,
    allow_slow: bool = False,
    tag_check: Callable[[str], bool] | None = None,
) -> ModelDecision:
    check = tag_check or tag_exists_in_registry
    rejected: list[RejectedCandidate] = []
    avail_set = set(available_tags)
    mt = assessment.tier

    if user_override:
        u = user_override.strip()
        practical = _override_practical(u, assessment, allow_slow)
        if not practical.ok:
            return ModelDecision(
                selected_model=u,
                selected_tier=mt,
                comfortable=False,
                reason=practical.reason,
                rejected_candidates=[RejectedCandidate(u, practical.reason)],
            )
        if check(u):
            return ModelDecision(
                selected_model=u,
                selected_tier=mt,
                comfortable=practical.comfortable,
                reason="User-requested model; hardware check passed and tag is available.",
                rejected_candidates=[],
            )
        rejected.append(RejectedCandidate(u, "tag not found in registry / ollama show failed"))
        return ModelDecision(
            selected_model="",
            selected_tier=mt,
            comfortable=False,
            reason="Forced model not available.",
            rejected_candidates=rejected,
        )

    for ladder_name, ladder in (("deepseek-r1", PRIMARY_LADDER), ("fallback", SECONDARY_LADDER)):
        for model_tag in ladder:
            elig, why = model_eligible_for_tier(model_tag, mt, allow_slow)
            if not elig:
                rejected.append(RejectedCandidate(model_tag, why or "not eligible for this hardware tier"))
                continue

            exists = check(model_tag) or model_tag in avail_set
            if not exists:
                rejected.append(RejectedCandidate(model_tag, "not available from registry / local list"))
                continue

            comfortable = not ("32b" in model_tag.lower() and mt == TIER_32B_SLOW and not allow_slow)
            if mt == TIER_SMALL:
                comfortable = False

            reason = (
                f"First available model in {ladder_name} ladder matching tier {mt}. "
                f"{assessment.notes}"
            )
            return ModelDecision(
                selected_model=model_tag,
                selected_tier=mt,
                comfortable=comfortable,
                reason=reason,
                rejected_candidates=rejected,
            )

    return ModelDecision(
        selected_model="",
        selected_tier=mt,
        comfortable=False,
        reason="No suitable model found in fallback ladders.",
        rejected_candidates=rejected,
    )


class _OverrideCheck:
    def __init__(self, ok: bool, reason: str, comfortable: bool):
        self.ok = ok
        self.reason = reason
        self.comfortable = comfortable


def _override_practical(model_tag: str, assessment: TierAssessment, allow_slow: bool) -> _OverrideCheck:
    m = re.search(r":(\d+)b", model_tag.lower())
    if not m:
        return _OverrideCheck(True, "", True)
    b = int(m.group(1))
    if b >= 70 and assessment.tier != TIER_70B:
        return _OverrideCheck(False, "70B not practical for this machine's tier", False)
    if b >= 32 and assessment.tier in (TIER_14B, TIER_8B, TIER_SMALL):
        if not allow_slow:
            return _OverrideCheck(False, "32B not comfortable for this hardware; pass --allow-slow to force", False)
    if b >= 32 and assessment.tier == TIER_32B_SLOW and not allow_slow:
        return _OverrideCheck(False, "32B is only 'possible but slow'; use --allow-slow", False)
    return _OverrideCheck(True, "", True)


def model_decision_to_json(decision: ModelDecision) -> dict:
    return {
        "selected_model": decision.selected_model,
        "selected_tier": decision.selected_tier,
        "comfortable": decision.comfortable,
        "reason": decision.reason,
        "rejected_candidates": [{"model": r.model, "reason": r.reason} for r in decision.rejected_candidates],
    }
