"""test_scope_resolver.py — unit tests for scripts/_scope_common_ops.py.

Companion to the unified-scope refactor (NOTES - AIStudio - Unified Corpus Scope
Architecture - 2026-06-09). Pure-logic + temp-file tests; no network, runs under
`make test-unit`. Covers: type-separated identity cascades (N3), single-entity
selection + guards, the AIStudio_882 hard-error-on-missing-scope policy, and the
single-full-inventory discovery rule.
"""

import sys
from pathlib import Path

import pytest

# scripts/ is a sibling of tests/ under the repo root.
_REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_REPO / "scripts"))

import _scope_common_ops as sc  # noqa: E402


# ── fixtures ──────────────────────────────────────────────────────────────────
def _write(p: Path, body: str) -> Path:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(body)
    return p


ROWS = [
    {"label": "Bank of New York", "ticker": "BK", "cik": "0001390777",
     "lei": "AAA", "gleif_lei": "BBB",
     "xbrl_name": "THE BANK OF NEW YORK MELLON CORPORATION"},
    {"label": "Goldman Sachs", "ticker": "GS", "cik": "0000886982",
     "canonical": "THE GOLDMAN SACHS GROUP, INC.",
     "gleif_canonical": "GOLDMAN SACHS GROUP INC",
     "gleif_lei": "GGG", "lei_corrected": "784F5XWPLTWKTBV3E584"},
]


# ── identity cascades (N3) ────────────────────────────────────────────────────
def test_entity_lei_prefers_corrected():
    assert sc.entity_lei(ROWS[1]) == "784F5XWPLTWKTBV3E584"   # lei_corrected wins


def test_entity_lei_falls_to_gleif_then_seed():
    assert sc.entity_lei(ROWS[0]) == "BBB"                    # gleif_lei (no corrected)
    assert sc.entity_lei({"lei": "ZZZ"}) == "ZZZ"            # bare seed lei
    assert sc.entity_lei({}) is None


def test_entity_name_prefers_canonical_then_falls_through():
    assert sc.entity_name(ROWS[1]) == "THE GOLDMAN SACHS GROUP, INC."   # canonical
    assert sc.entity_name(ROWS[0]) == "THE BANK OF NEW YORK MELLON CORPORATION"  # → xbrl_name
    assert sc.entity_name({"gleif_canonical": "X"}) == "X"
    assert sc.entity_name({"label": "L"}) == "L"
    assert sc.entity_name({}) is None


# ── selection + guards ────────────────────────────────────────────────────────
@pytest.mark.parametrize("kw,val,expect", [
    ("ticker", "BK", "Bank of New York"),
    ("cik", "0000886982", "Goldman Sachs"),
    ("label", "goldman sachs", "Goldman Sachs"),   # case-insensitive
    ("xbrl", "the goldman sachs group, inc.", "Goldman Sachs"),  # via canonical? no — xbrl matches xbrl_name
])
def test_select_by_each_selector(kw, val, expect):
    if kw == "xbrl":
        # xbrl matches xbrl_name; GS has none, so use BNY's xbrl_name instead
        row = sc.select_entity(ROWS, xbrl="the bank of new york mellon corporation")
        assert row["label"] == "Bank of New York"
        return
    row = sc.select_entity(ROWS, **{kw: val})
    assert row["label"] == expect


def test_select_lei_matches_any_lei_field():
    assert sc.select_entity(ROWS, lei="784F5XWPLTWKTBV3E584")["label"] == "Goldman Sachs"
    assert sc.select_entity(ROWS, lei="BBB")["label"] == "Bank of New York"  # gleif_lei
    assert sc.select_entity(ROWS, gleif="GGG")["label"] == "Goldman Sachs"


def test_select_mutual_exclusion():
    with pytest.raises(sc.ScopeError, match="mutually exclusive"):
        sc.select_entity(ROWS, ticker="GS", cik="x")


def test_select_no_selector():
    with pytest.raises(sc.ScopeError, match="exactly one selector"):
        sc.select_entity(ROWS)


def test_select_no_match():
    with pytest.raises(sc.ScopeError, match="No entity in scope matches"):
        sc.select_entity(ROWS, lei="NOPE")


def test_select_ambiguous():
    dupes = [{"ticker": "X", "label": "a"}, {"ticker": "X", "label": "b"}]
    with pytest.raises(sc.ScopeError, match="ambiguous"):
        sc.select_entity(dupes, ticker="X")


# ── load + path resolution (uses tmp REPO) ────────────────────────────────────
@pytest.fixture
def repo(tmp_path, monkeypatch):
    monkeypatch.setattr(sc, "REPO", tmp_path)
    return tmp_path


def _scope_yaml(entities="- {label: GS, ticker: GS, lei: AAA}") -> str:
    return f'schema_version: "2.0"\nkind: scope\ncorpus: sec_10k\nentities:\n  {entities}\n'


def test_load_scope_by_stem(repo):
    _write(repo / "data/corpora/sec_10k/scopes/sec_10k_big_banks_scope.yaml", _scope_yaml())
    rows = sc.load_entities("sec_10k", stem="big_banks")
    assert rows[0]["ticker"] == "GS"


def test_missing_named_scope_hard_errors(repo):
    # AIStudio_882 — never a silent fallback
    with pytest.raises(sc.ScopeError, match="Scope not found"):
        sc.load_scope("sec_10k", stem="does_not_exist")


def test_load_scope_no_entities_errors(repo):
    _write(repo / "data/corpora/sec_10k/scopes/sec_10k_bad_scope.yaml",
           'schema_version: "2.0"\nkind: scope\n')
    with pytest.raises(sc.ScopeError, match="no `entities`"):
        sc.load_scope("sec_10k", stem="bad")


def test_load_scope_malformed_yaml_errors(repo):
    _write(repo / "data/corpora/sec_10k/scopes/sec_10k_x_scope.yaml", "entities: [a: b: c]")
    with pytest.raises(sc.ScopeError, match="Malformed scope YAML"):
        sc.load_scope("sec_10k", stem="x")


def test_discover_full_single(repo):
    _write(repo / "data/corpora/sec_10k/sec_10k_entity_full_scope.yaml", _scope_yaml())
    assert sc.discover_full("sec_10k").name == "sec_10k_entity_full_scope.yaml"
    # no stem + no path → loads the full inventory
    assert sc.load_entities("sec_10k")[0]["label"] == "GS"


def test_discover_full_none_errors(repo):
    (repo / "data/corpora/sec_10k").mkdir(parents=True)
    with pytest.raises(sc.ScopeError, match="No full-inventory scope"):
        sc.discover_full("sec_10k")


def test_discover_full_ambiguous_errors(repo):
    _write(repo / "data/corpora/sec_10k/sec_10k_a_full_scope.yaml", _scope_yaml())
    _write(repo / "data/corpora/sec_10k/sec_10k_b_full_scope.yaml", _scope_yaml())
    with pytest.raises(sc.ScopeError, match="Ambiguous full inventory"):
        sc.discover_full("sec_10k")


def test_explicit_path_override(repo, tmp_path):
    custom = _write(tmp_path / "my_firms.yaml", _scope_yaml())
    rows = sc.load_entities("sec_10k", path=str(custom))
    assert rows[0]["label"] == "GS"
