# tests/test_model_fit.py
# AIStudio_1020 — behavior test for the memory-fit policy (app/model_fit.py). Pure functions, no
# backend deps. Anchors the 24GB-tier intent: 27b BLOCKs, 12b/8b FIT, and the recommender returns
# the largest fitting tier. When the ESEF calibration moves warn_frac/block_frac, update the fracs
# here alongside config — the SHAPE assertions (27b blocks, recommend largest-fit) must hold.
import sys
from pathlib import Path

# The suite runs with PYTHONPATH=src (see the ruff/pytest invocation), so the package import is the
# primary path and matches how api.py imports it. Fallback to a direct path insert for a standalone
# `python tests/test_model_fit.py` run. model_fit is pure functions (dataclasses/typing only) — no
# pydantic/fastapi/ollama pulled in either way, so this test stays dependency-light.
try:
    from local_llm_bot.app import model_fit as mf
except ModuleNotFoundError:
    _APP = Path(__file__).resolve().parents[1] / "src" / "local_llm_bot" / "app"
    if str(_APP) not in sys.path:
        sys.path.insert(0, str(_APP))
    import model_fit as mf  # noqa: E402

GB = 1_000_000_000
# 24GB box: ~15GB available after a ~3GB reserve on a lightly-loaded machine.
AVAIL_24GB = 15 * GB
WARN, BLOCK, MULT = 0.80, 0.92, 1.2

# Approximate Q4 on-disk sizes.
M_8B = {"id": "llama3.1:8b", "size_bytes": 5 * GB, "param_count": 8_000_000_000, "available": True}
M_12B = {"id": "gemma3:12b", "size_bytes": 8 * GB, "param_count": 12_000_000_000, "available": True}
M_27B = {"id": "gemma3:27b", "size_bytes": 16 * GB, "param_count": 27_000_000_000, "available": True}
ALL = [M_8B, M_12B, M_27B]


def _verdict(m, avail=AVAIL_24GB):
    fp = mf.estimate_footprint_bytes(size_bytes=m["size_bytes"], param_count=m["param_count"], mult=MULT)
    return mf.fit_verdict(footprint_bytes=fp, available_bytes=avail, warn_frac=WARN, block_frac=BLOCK).verdict


def test_27b_blocks_on_24gb():
    # 16GB disk × 1.2 = 19.2GB footprint vs 15GB available → frac 1.28 ≥ block_frac → BLOCK (the wedge).
    assert _verdict(M_27B) == mf.BLOCK


def test_8b_fits_on_24gb():
    # 5GB × 1.2 = 6GB vs 15GB → frac 0.4 → FIT.
    assert _verdict(M_8B) == mf.FIT


def test_12b_fits_on_24gb():
    # 8GB × 1.2 = 9.6GB vs 15GB → frac 0.64 → FIT (the safer quantitative tier for 24GB).
    assert _verdict(M_12B) == mf.FIT


def test_recommend_returns_largest_fitting_tier():
    # Both 8b and 12b fit; the recommendation should be the LARGER one (12b), not the smallest.
    rec = mf.recommend_model(ALL, available_bytes=AVAIL_24GB, warn_frac=WARN, block_frac=BLOCK, footprint_mult=MULT)
    assert rec == "gemma3:12b"


def test_evaluate_block_carries_recommendation():
    v = mf.evaluate(M_27B, ALL, available_bytes=AVAIL_24GB, warn_frac=WARN, block_frac=BLOCK, footprint_mult=MULT)
    assert v.verdict == mf.BLOCK
    assert v.recommendation == "gemma3:12b"
    assert "gemma3:12b" in v.reason  # the message names the fitting tier


def test_unknown_size_fails_open_not_closed():
    # No size/params → footprint 0 → FIT (never block on missing data; the reason records it).
    v = mf.fit_verdict(footprint_bytes=0, available_bytes=AVAIL_24GB, warn_frac=WARN, block_frac=BLOCK)
    assert v.verdict == mf.FIT
    assert "unknown" in v.reason


def test_warn_band():
    # Construct a model that lands between warn and block (frac ~0.85): footprint ≈ 12.75GB.
    m = {"id": "mid:20b", "size_bytes": int(10.6 * GB), "param_count": 20_000_000_000, "available": True}
    assert _verdict(m) == mf.WARN


if __name__ == "__main__":
    import traceback

    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    passed = 0
    for fn in fns:
        try:
            fn()
            print(f"PASS {fn.__name__}")
            passed += 1
        except Exception:
            print(f"FAIL {fn.__name__}")
            traceback.print_exc()
    print(f"\n{passed}/{len(fns)} passed")
    sys.exit(0 if passed == len(fns) else 1)
