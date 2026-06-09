#!/usr/bin/env python3
"""
_scope_common_ops.py — Shared corpus-scope resolver (OPS, library; not a command).

ONE scope concept for download / ingest / entity-import / bench. A *scope* is a
named, yaml-defined subset (or full inventory) of a corpus, living under
data/corpora/<corpus>/. The "worksheet" is just a scope in its in-review state.

Naming (ratified 2026-06-09):
  full inventory : data/corpora/<corpus>/<corpus>_<stem>_full_scope.yaml
  named subset   : data/corpora/<corpus>/scopes/<corpus>_<stem>_scope.yaml
  (a full path or any filename is accepted as an explicit override)

Schema v2.0 (superset; extra fields tolerated):
  schema_version: "2.0"
  kind: scope
  corpus: <corpus>
  entities:
    - label: <human label>
      cik: <…>                 # SEC access key
      ticker: <…>
      lei: <…>                 # seed identity
      expected_xbrl_name: <…>  # 667/CBOE→Larimar ingest guard
      xbrl_name: <…>           # self-reported tag (populated by scan)
      gleif_canonical: <…>     # machine guess (review)
      gleif_lei: <…>           # machine guess (review)
      lei_corrected: <…>       # human-verified (review; authoritative)
      files: [<…>]

Selectors (single-entity): match one row by ANY ONE of
  --label / --tkr / --cik / --xbrl / --gleif / --lei
Resolution is type-separated (N3, 2026-06-09):
  LEI         : lei_corrected → gleif_lei → lei      (human-verified wins; Lesson #180)
  display name: canonical → gleif_canonical → xbrl_name → label

Missing-scope policy (AIStudio_882): an explicitly-named scope that does not exist
is a HARD ERROR (ScopeError) — never a silent fallback to corpus defaults.

Version: 1.0.0
"""

from __future__ import annotations

from pathlib import Path

import yaml

VERSION = "1.0.0"
SCHEMA_VERSION = "2.0"
REPO = Path(__file__).parent.parent
SCOPES_SUBDIR = "scopes"


class ScopeError(Exception):
    """Raised on an unresolvable / malformed scope. Callers convert to an
    `❌ …` line + remediation per STD - AIStudio - CLI Output."""


# ── Path resolution ───────────────────────────────────────────────────────────
def _corpus_dir(corpus: str) -> Path:
    return REPO / "data" / "corpora" / corpus


def scope_path(corpus: str, stem: str, *, full: bool = False) -> Path:
    """Canonical path for a scope stem. full=True → the corpus-root full inventory;
    else the subset under scopes/."""
    if full:
        return _corpus_dir(corpus) / f"{corpus}_{stem}_full_scope.yaml"
    return _corpus_dir(corpus) / SCOPES_SUBDIR / f"{corpus}_{stem}_scope.yaml"


def resolve_scope_file(corpus: str, stem: str | None = None,
                       path: str | None = None, *, full: bool = False) -> Path:
    """Resolve a scope reference to a concrete file.
    - path given        → that exact file (any name/location).
    - stem given        → scope_path(corpus, stem, full).
    - neither           → the corpus full inventory (requires a known full stem; see
                          load_full which discovers it).
    Raises ScopeError if the resolved file does not exist."""
    if path:
        p = Path(path).expanduser()
        if not p.is_absolute():
            p = REPO / p
    elif stem is not None:
        p = scope_path(corpus, stem, full=full)
    else:
        raise ScopeError("resolve_scope_file: provide either a stem or an explicit path.")
    if not p.exists():
        raise ScopeError(
            f"Scope not found: {_rel(p)}.\n"
            f"· List available scopes: ls {_rel(_corpus_dir(corpus) / SCOPES_SUBDIR)}/\n"
            f"· Build one from the corpus, or pass --scope <path-to.yaml> for a custom list."
        )
    return p


def discover_full(corpus: str) -> Path:
    """Find the corpus's single *_full_scope.yaml inventory. ScopeError if 0 or >1."""
    hits = sorted(_corpus_dir(corpus).glob(f"{corpus}_*_full_scope.yaml"))
    if not hits:
        raise ScopeError(
            f"No full-inventory scope for '{corpus}' "
            f"(expected {_rel(_corpus_dir(corpus))}/{corpus}_<stem>_full_scope.yaml).\n"
            f"· Build it from the seed (see the corpus build command)."
        )
    if len(hits) > 1:
        raise ScopeError(
            f"Ambiguous full inventory for '{corpus}' — {len(hits)} match "
            f"{corpus}_*_full_scope.yaml: {', '.join(h.name for h in hits)}."
        )
    return hits[0]


# ── Load ────────────────────────────────────────────────────────────────────
def load_scope(corpus: str, stem: str | None = None, path: str | None = None,
               *, full: bool = False) -> dict:
    """Load a scope file → its parsed dict (with at least `entities`).
    No stem + no path → the corpus full inventory (discover_full)."""
    p = discover_full(corpus) if (stem is None and path is None) else \
        resolve_scope_file(corpus, stem, path, full=full)
    try:
        data = yaml.safe_load(p.read_text()) or {}
    except yaml.YAMLError as e:
        raise ScopeError(f"Malformed scope YAML: {_rel(p)} — {e}") from e
    if "entities" not in data:
        raise ScopeError(f"Scope has no `entities` list: {_rel(p)}.")
    data.setdefault("corpus", corpus)
    data["_path"] = str(p)
    return data


def load_entities(corpus: str, stem: str | None = None, path: str | None = None,
                  *, full: bool = False) -> list[dict]:
    """Convenience: just the entity rows."""
    return load_scope(corpus, stem, path, full=full).get("entities", []) or []


# ── Single-entity selection ───────────────────────────────────────────────────
_SELECTOR_FIELDS = {
    "label": ("label",),
    "ticker": ("ticker",),
    "cik": ("cik",),
    "xbrl": ("xbrl_name",),
    "gleif": ("gleif_lei",),
    "lei": ("lei_corrected", "gleif_lei", "lei"),   # any LEI field may carry it
}


def select_entity(entities: list[dict], *, label: str | None = None,
                  ticker: str | None = None, cik: str | None = None,
                  xbrl: str | None = None, gleif: str | None = None,
                  lei: str | None = None) -> dict:
    """Return the single row matching exactly one provided selector.
    ScopeError on zero matches, multiple selectors, or ambiguous (>1) match."""
    provided = {k: v for k, v in dict(
        label=label, ticker=ticker, cik=cik, xbrl=xbrl, gleif=gleif, lei=lei
    ).items() if v is not None}
    if not provided:
        raise ScopeError("select_entity: give exactly one selector "
                         "(--label/--tkr/--cik/--xbrl/--gleif/--lei).")
    if len(provided) > 1:
        raise ScopeError(f"select_entity: selectors are mutually exclusive — "
                         f"got {', '.join('--' + k for k in provided)}.")
    key, want = next(iter(provided.items()))
    fields = _SELECTOR_FIELDS[key]
    norm = _norm(want)
    hits = [e for e in entities
            if any(_norm(e.get(f)) == norm for f in fields if e.get(f) is not None)]
    if not hits:
        raise ScopeError(f"No entity in scope matches --{key} {want!r}.")
    if len(hits) > 1:
        raise ScopeError(f"--{key} {want!r} is ambiguous — {len(hits)} rows match.")
    return hits[0]


# ── Type-separated identity resolution (N3) ───────────────────────────────────
def entity_lei(row: dict) -> str | None:
    """Authoritative LEI: lei_corrected → gleif_lei → lei (human-verified wins)."""
    for f in ("lei_corrected", "gleif_lei", "lei"):
        v = (row.get(f) or "").strip()
        if v:
            return v
    return None


def entity_name(row: dict) -> str | None:
    """Display/canonical name: canonical → gleif_canonical → xbrl_name → label."""
    for f in ("canonical", "gleif_canonical", "xbrl_name", "label"):
        v = (row.get(f) or "").strip()
        if v:
            return v
    return None


# ── helpers ───────────────────────────────────────────────────────────────────
def _norm(v) -> str:
    return str(v).strip().lower() if v is not None else ""


def _rel(p: Path) -> str:
    try:
        return str(p.relative_to(REPO))
    except ValueError:
        return str(p)
