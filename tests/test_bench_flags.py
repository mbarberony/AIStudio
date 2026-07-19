# tests/test_bench_flags.py
# AIStudio_1020 / _1012 — behavior test for bench.py's --fit-policy resolution and the --dry-run guard
# (HOWTO_OPS flag protocol Step 11: a behavior test for the new parameters, not just help conformance).
#
# bench.py imports scripts/_scope_common at module load (it self-adds ../scripts to sys.path). Where
# that operator module isn't present (e.g. a meta-only checkout), skip the whole module rather than
# error — on Beast it resolves and these run.
import builtins
import sys
from pathlib import Path

import pytest

_BENCH_DIR = Path(__file__).resolve().parents[1] / "benchmarks"
if str(_BENCH_DIR) not in sys.path:
    sys.path.insert(0, str(_BENCH_DIR))
try:
    import bench  # noqa: E402
except Exception as e:  # pragma: no cover - environment guard
    pytest.skip(f"bench.py not importable here ({e}); runs on Beast", allow_module_level=True)


class _FakeStdin:
    def __init__(self, tty: bool):
        self._tty = tty

    def isatty(self) -> bool:
        return self._tty


def _patch_fit(monkeypatch, verdict, recommendation=None):
    monkeypatch.setattr(
        bench, "_fetch_model_fit",
        lambda api, model: {"verdict": verdict, "recommendation": recommendation, "reason": "test"},
    )


# ── --fit-policy resolution ───────────────────────────────────────────────────────────────────

def test_fit_returns_run_unchanged(monkeypatch):
    _patch_fit(monkeypatch, "FIT")
    assert bench._resolve_fit_policy("http://x", "gemma3:12b", None) == ("run", "gemma3:12b")


def test_warn_runs_unchanged(monkeypatch):
    _patch_fit(monkeypatch, "WARN")
    assert bench._resolve_fit_policy("http://x", "gemma3:12b", None) == ("run", "gemma3:12b")


def test_block_skip(monkeypatch):
    _patch_fit(monkeypatch, "BLOCK", "gemma3:12b")
    assert bench._resolve_fit_policy("http://x", "gemma3:27b", "skip") == ("skip", None)


def test_block_downshift_uses_recommendation(monkeypatch):
    _patch_fit(monkeypatch, "BLOCK", "gemma3:12b")
    assert bench._resolve_fit_policy("http://x", "gemma3:27b", "downshift") == ("run", "gemma3:12b")


def test_block_downshift_no_recommendation_skips(monkeypatch):
    _patch_fit(monkeypatch, "BLOCK", None)
    assert bench._resolve_fit_policy("http://x", "gemma3:27b", "downshift") == ("skip", None)


def test_block_force_runs_original(monkeypatch):
    _patch_fit(monkeypatch, "BLOCK", "gemma3:12b")
    assert bench._resolve_fit_policy("http://x", "gemma3:27b", "force") == ("run", "gemma3:27b")


def test_block_no_policy_noninteractive_fails_closed(monkeypatch):
    # The key anti-silent-failure contract: no --fit-policy + no terminal → exit 1, never a guess.
    _patch_fit(monkeypatch, "BLOCK", "gemma3:12b")
    monkeypatch.setattr(bench.sys, "stdin", _FakeStdin(tty=False))
    with pytest.raises(SystemExit) as ei:
        bench._resolve_fit_policy("http://x", "gemma3:27b", None)
    assert ei.value.code == 1


def test_block_no_policy_interactive_pick_downshifts(monkeypatch):
    # The interactive gate is a NUMBERED picker, not a YES/n prompt: on BLOCK it lists the models
    # that do fit, largest first, and "1" selects the largest. This test previously fed "YES", which
    # the picker treats as invalid input and therefore cancels — it was asserting a contract the
    # command stopped honouring when the picker replaced the yes/no prompt.
    _patch_fit(monkeypatch, "BLOCK", "gemma3:12b")
    monkeypatch.setattr(bench.sys, "stdin", _FakeStdin(tty=True))
    # The interactive gate offers the models that DO fit, which it fetches from the API. Without
    # mocking that fetch the list is empty, the gate has nothing to offer and cancels — which is why
    # this test failed regardless of the input given. With exactly one fitting model the prompt is
    # "(r)un <model>, (f)ree memory & restart, (Enter) cancel", so the affirmative is "r".
    monkeypatch.setattr(bench, "_fetch_fitting_models",
                        lambda api, exclude=None: [{"id": "gemma3:12b", "gb": 10}])
    monkeypatch.setattr(builtins, "input", lambda *_a: "r")
    assert bench._resolve_fit_policy("http://x", "gemma3:27b", None) == ("run", "gemma3:12b")


def test_block_no_policy_interactive_non_yes_aborts(monkeypatch):
    _patch_fit(monkeypatch, "BLOCK", "gemma3:12b")
    monkeypatch.setattr(bench.sys, "stdin", _FakeStdin(tty=True))
    monkeypatch.setattr(builtins, "input", lambda *_a: "n")
    with pytest.raises(SystemExit):
        bench._resolve_fit_policy("http://x", "gemma3:27b", None)


# ── --dry-run guard (single-run path stops instead of silently executing) ──────────────────────

def test_dry_run_without_batch_previews_and_returns(monkeypatch, capsys):
    # --dry-run without --batch now PREVIEWS the single run and returns, rather than printing an
    # advisory and refusing (bench 2.21.0). The assertion is that nothing executes and nothing is
    # written — the previous version of this test asserted the old advisory text, which no longer
    # exists, and so failed for a reason unrelated to the behaviour it was guarding.
    ns = bench.argparse.Namespace(
        canonical=False, canonical_id=None, dry_run=True, corpus="demo", model=None, fit_policy=None,
    )
    monkeypatch.setattr(bench, "parse_args", lambda: ns)
    bench.main()
    out = capsys.readouterr().out
    assert "Would run ONE job" in out
    assert "no report was written" in out
