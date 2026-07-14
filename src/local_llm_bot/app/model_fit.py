# src/local_llm_bot/app/model_fit.py
# Version: 1.0.0
# Changelog: 1.0.0 — AIStudio_1020: shared model-memory-fit service. ONE policy, imported by the API
#   preflight (/ask), the model list (/models `fit` field), and bench.py (--fit-policy) so no surface
#   re-implements the arithmetic (the _967 UI heuristic drifted from reality precisely because it did).
#   Converts the silent 27b-on-24GB wedge — loads → HTTP blocks → tiny RSS → no error → looks hung —
#   into an explicit BLOCK + recommended-tier at every entry point. Anti-silent-failure by construction
#   (NOTES - urc - Silent Failure Antipattern - 2026-06-25). Thresholds live in config.ModelFitConfig
#   and are PROVISIONAL pending 24GB-tier ESEF calibration (design note §3).
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

# Verdict constants — the three fit bands.
FIT = "FIT"      # dispatch normally
WARN = "WARN"    # dispatch, but surface the risk loudly
BLOCK = "BLOCK"  # refuse; recommend the largest model that fits

# When a model's footprint estimates to Q4 weights and disk size is unknown, approximate weight bytes
# per parameter. Q4_K_M is ~0.6-0.7 bytes/param; use the conservative upper end so we under-promise fit.
_BYTES_PER_PARAM_Q4 = 0.7


@dataclass(frozen=True)
class FitVerdict:
    """The fit decision for one model on this machine, plus the data behind it."""
    verdict: str                      # FIT | WARN | BLOCK
    footprint_bytes: int              # estimated runtime footprint (weights + KV + overhead)
    available_bytes: int              # available RAM after the reserve
    headroom_frac: float | None       # footprint / available (None when either is unknown)
    recommendation: str | None = None # id of the largest model that DOES fit (set on WARN/BLOCK)
    reason: str = ""                  # short human string for the API/UI/bench message

    def to_dict(self) -> dict[str, Any]:
        return {
            "verdict": self.verdict,
            "footprint_bytes": self.footprint_bytes,
            "available_bytes": self.available_bytes,
            "headroom_frac": round(self.headroom_frac, 3) if self.headroom_frac is not None else None,
            "recommendation": self.recommendation,
            "reason": self.reason,
        }


def estimate_footprint_bytes(*, size_bytes: int | None, param_count: int | None, mult: float) -> int:
    """Estimated RUNTIME footprint, not raw disk size.

    Ollama's on-disk quant (`size_bytes`) understates what inference actually holds: weights + the KV
    cache (grows with num_ctx) + runtime overhead. Phase 1 folds all of that into one calibrated
    scalar `mult` over the disk size. Falls back to a param-count estimate when disk size is missing.
    Returns 0 when neither input is known (caller treats 0 as 'unknown → do not block').
    """
    if size_bytes:
        return int(size_bytes * mult)
    if param_count:
        return int(param_count * _BYTES_PER_PARAM_Q4 * mult)
    return 0


def fit_verdict(
    *,
    footprint_bytes: int,
    available_bytes: int,
    warn_frac: float,
    block_frac: float,
    recommendation: str | None = None,
) -> FitVerdict:
    """Classify a single model's footprint against post-reserve available memory.

    Bands: frac < warn_frac → FIT; warn_frac ≤ frac < block_frac → WARN; frac ≥ block_frac → BLOCK.
    Unknown footprint or unknown memory → FIT (fail-open: we never had the data to block on, and
    blocking every model when Ollama size info is absent would be worse than the risk). The `reason`
    string records the estimate so the fail-open is visible, not silent.
    """
    if not footprint_bytes or not available_bytes:
        return FitVerdict(
            verdict=FIT,
            footprint_bytes=footprint_bytes,
            available_bytes=available_bytes,
            headroom_frac=None,
            recommendation=None,
            reason="size/memory unknown — fit not evaluated",
        )
    frac = footprint_bytes / available_bytes
    if frac >= block_frac:
        verdict = BLOCK
    elif frac >= warn_frac:
        verdict = WARN
    else:
        verdict = FIT
    return FitVerdict(
        verdict=verdict,
        footprint_bytes=footprint_bytes,
        available_bytes=available_bytes,
        headroom_frac=frac,
        recommendation=recommendation if verdict != FIT else None,
        reason=_reason(verdict, footprint_bytes, available_bytes, recommendation),
    )


def _gb(n: int | float) -> str:
    return f"{n / 1e9:.0f} GB"


def _reason(verdict: str, footprint: int, available: int, rec: str | None) -> str:
    if verdict == BLOCK:
        base = f"needs ~{_gb(footprint)} but only ~{_gb(available)} is free; it will load and then hang"
        return f"{base}; switch to {rec}, which fits" if rec else base
    if verdict == WARN:
        return f"needs ~{_gb(footprint)} against ~{_gb(available)} free — tight; may swap or slow"
    return f"fits (~{_gb(footprint)} of ~{_gb(available)} free)"


def recommend_model(
    models: list[dict[str, Any]],
    *,
    available_bytes: int,
    warn_frac: float,
    block_frac: float,
    footprint_mult: float,
) -> str | None:
    """Largest model that is FIT on this machine — the 'tier that fits'.

    `models` is a list of dicts with `id`, optional `size_bytes`, `param_count`, `available`. Ranks
    available FIT models by footprint and returns the biggest one's id (a user who wanted 27b is best
    served the largest thing that actually runs, not the smallest). None when nothing fits.
    """
    best_id: str | None = None
    best_footprint = -1
    for m in models:
        if m.get("available") is False:
            continue
        fp = estimate_footprint_bytes(
            size_bytes=m.get("size_bytes"), param_count=m.get("param_count"), mult=footprint_mult
        )
        v = fit_verdict(
            footprint_bytes=fp, available_bytes=available_bytes, warn_frac=warn_frac, block_frac=block_frac
        )
        if v.verdict == FIT and fp > best_footprint:
            best_footprint = fp
            best_id = m.get("id")
    return best_id


def evaluate(
    model: dict[str, Any],
    all_models: list[dict[str, Any]],
    *,
    available_bytes: int,
    warn_frac: float,
    block_frac: float,
    footprint_mult: float,
) -> FitVerdict:
    """Convenience: verdict for one model, with the recommendation resolved against the full list.

    This is the single call the API and bench make per model — footprint estimate + band + the
    largest-fitting-model recommendation, in one shot.
    """
    fp = estimate_footprint_bytes(
        size_bytes=model.get("size_bytes"), param_count=model.get("param_count"), mult=footprint_mult
    )
    rec = None
    # Only pay for the recommendation scan when the model isn't obviously fine.
    provisional = fit_verdict(
        footprint_bytes=fp, available_bytes=available_bytes, warn_frac=warn_frac, block_frac=block_frac
    )
    if provisional.verdict != FIT:
        rec = recommend_model(
            all_models,
            available_bytes=available_bytes,
            warn_frac=warn_frac,
            block_frac=block_frac,
            footprint_mult=footprint_mult,
        )
    return fit_verdict(
        footprint_bytes=fp,
        available_bytes=available_bytes,
        warn_frac=warn_frac,
        block_frac=block_frac,
        recommendation=rec,
    )
