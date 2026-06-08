#!/usr/bin/env python3
"""
_kb_common_ops.py — Shared helpers for the OPS knowledge-base importers.

Carved verbatim from ais_import_knowledge_base.py v1.1.0 so the entity importer
(ais_import_entity_kb_ops) and the glossary importer (ais_import_glossary_kb_ops)
share one copy of: console/HTTP primitives, GLEIF fetch (by name and by LEI),
alias derivation (mechanical + Wikidata + collision guard), metadata loading,
catalog writing, and catalog listing. Schema/keying/binding-time logic that
DIFFERS between the two commands does NOT live here — it stays in each command.

Lives in scripts/ (parent.parent == repo root). Imported as a sibling:
    import _kb_common_ops as kb       # when run via `python3 scripts/<cmd>.py`

Version: 1.0.0
"""

import json
import re
import ssl
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path

import yaml

try:
    import certifi
    _SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    _SSL_CONTEXT = None

# ── Repo root resolution (this module is scripts/kb_common_ops.py) ────────────
REPO = Path(__file__).parent.parent
KNOWLEDGE_SOURCES_DIR = REPO / "data" / "knowledge_sources"
CATALOG_PATH = KNOWLEDGE_SOURCES_DIR / "catalog.yaml"

# ── Supported sources / output attribute type per source ─────────────────────
SUPPORTED_SOURCES = ["gleif", "sec_edgar", "bis_basel", "nist_ai_rmf", "esrs"]
SOURCE_ATTRIBUTE_TYPE = {
    "gleif":       "entities",
    "sec_edgar":   "companies",
    "bis_basel":   "glossary",
    "nist_ai_rmf": "glossary",
    "esrs":        "glossary",
}
SCOPE_REQUIRED = {"gleif", "sec_edgar"}
FULL_DOWNLOAD_SOURCES = {"bis_basel", "nist_ai_rmf", "esrs"}


def _bold(text: str) -> str:
    return f"\033[1m{text}\033[0m"


def _err(msg: str) -> None:
    print(f"❌ {msg}", file=sys.stderr)


def _api_get(url: str) -> dict:
    """GET JSON from URL with retry."""
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={"Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=30, context=_SSL_CONTEXT) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception as e:
            if attempt < 2:
                time.sleep(2 ** attempt)
                continue
            raise RuntimeError(str(e)) from e


# ── Source handlers ───────────────────────────────────────────────────────────

def _fetch_gleif_entity(name: str, metadata: dict, common_name: str | None = None,
                        jurisdiction: str | None = None) -> dict | None:
    """
    Search GLEIF API by legal name. Returns best match or None.
    name: primary search term (legal_name_hint if provided, else common name)
    common_name: the short name from scope file, used for alias building and scoring
    jurisdiction: ISO jurisdiction code hint (e.g. "US", "NL", "FR") — optional
    """
    base_url = metadata["access"]["base_url"]
    score_name = common_name if common_name else name
    jur_filter = jurisdiction if jurisdiction else "US"

    def _score_record(rec: dict, query_name: str) -> tuple[int, int, int]:
        """
        Score a GLEIF record for match quality. Higher = better.
        Returns (primary_score, active_score, entity_type_score) for sorting.
        Primary:   3=US+exact, 2=US+partial, 1=other+exact, 0=other
        Active:    1=ACTIVE, 0=other
        Type:      0=parent/corp, -1=fund/ETF/trust/subsidiary (penalized)
        """
        attrs = rec["attributes"]
        canonical = attrs["entity"]["legalName"]["name"].upper()
        jurisdiction = attrs["entity"].get("jurisdiction", "")
        status = attrs["entity"]["status"]
        query_upper = query_name.upper()

        is_us = jurisdiction.startswith("US")
        is_active = status == "ACTIVE"
        is_exact = canonical == query_upper
        is_partial = query_upper in canonical or canonical in query_upper

        if is_us and is_exact:
            primary = 3
        elif is_us and is_partial:
            primary = 2
        elif is_exact:
            primary = 1
        else:
            primary = 0

        active_score = 1 if is_active else 0

        # Penalize funds, ETFs, trusts, subsidiaries, partnerships unless query implies them
        _SUBSIDIARY_MARKERS = {
            "FUND", "FUNDS", "ETF", "ETFS", "TRUST", "TRUSTS",
            "LLC", "L.L.C", "LP", "L.P", "LTD", "L.T.D",
            "HOLDINGS", "PARTNERS", "PARTNERSHIP",
            "CAPITAL", "SECURITIES", "BANK",
            "VENTURES", "INVESTMENTS", "INVESTMENT",
            "PORTFOLIOS", "PORTFOLIO",
            "ASSOCIATES", "ADVISORY", "ADVISORS",
            "SOLUTIONS", "SERVICES", "MANAGEMENT",
        }
        query_words = set(query_upper.split())
        canonical_words = set(canonical.split())
        penalty_words = _SUBSIDIARY_MARKERS - query_words
        has_penalty = bool(canonical_words & penalty_words)

        # Extra penalty: name contains " - " (fund subfund pattern e.g. "Goldman Sachs Trust - XYZ Fund")
        if " - " in canonical:
            has_penalty = True

        # Extra penalty: name contains "/" (partnership pattern e.g. "AIG/Baker Partnership")
        if "/" in canonical:
            has_penalty = True

        entity_type_score = -1 if has_penalty else 0

        return (primary, active_score, entity_type_score)

    def _fetch_with_filter(url: str) -> list[dict]:
        try:
            data = _api_get(url)
            return data.get("data", [])
        except RuntimeError:
            return []

    def _jur_search(query: str) -> list[dict]:
        enc = urllib.parse.quote(query)
        return _fetch_with_filter(
            f"{base_url}/lei-records?filter[entity.legalName]={enc}"
            f"&filter[entity.jurisdiction]={jur_filter}&page[size]=10"
        )

    # Try multiple name variants to find the parent holding company.
    # Large conglomerates often register as "THE {NAME} GROUP, INC." while
    # subsidiaries/funds register as "{NAME} {Fund/Trust/LLC/etc}".
    # Strategy: collect results from all variants, pool them, score, pick best.
    all_records: list[dict] = []
    variants = [
        name,
        f"THE {name} GROUP",
        f"{name} GROUP",
        f"THE {name}",
    ]
    # Also try common_name variants if different from primary name
    if common_name and common_name.upper() != name.upper():
        variants += [common_name, f"THE {common_name} GROUP", f"{common_name} GROUP"]

    for variant in variants:
        results = _jur_search(variant)
        all_records.extend(results)

    # Deduplicate by LEI
    seen: set[str] = set()
    records = []
    for rec in all_records:
        lei = rec["attributes"]["lei"]
        if lei not in seen:
            seen.add(lei)
            records.append(rec)

    # Fall back to global search if no US results at all
    if not records:
        enc = urllib.parse.quote(name)
        records = _fetch_with_filter(
            f"{base_url}/lei-records?filter[entity.legalName]={enc}&page[size]=25"
        )

    # Last resort — fuzzy name (drop punctuation)
    if not records:
        fuzzy = urllib.parse.quote(name.replace("&", "").replace(",", "").replace(".", ""))
        records = _fetch_with_filter(
            f"{base_url}/lei-records?filter[entity.legalName]={fuzzy}&page[size]=10"
        )

    if not records:
        return None

    # Score and sort — best match first, using common_name for scoring if available
    scored = sorted(records, key=lambda r: _score_record(r, score_name), reverse=True)
    best = scored[0]
    attrs = best["attributes"]
    return {
        "canonical": attrs["entity"]["legalName"]["name"],
        "lei": attrs["lei"],
        "jurisdiction": attrs["entity"].get("jurisdiction", ""),
        "status": attrs["entity"]["status"],
        "gleif_url": f"https://search.gleif.org/#/record/{attrs['lei']}",
    }


def _fetch_gleif_by_lei(lei: str, metadata: dict) -> dict | None:
    """Fetch a single GLEIF record by exact LEI code. Deterministic — no scoring needed."""
    base_url = metadata["access"]["base_url"]
    url = f"{base_url}/lei-records/{lei}"
    try:
        data = _api_get(url)
        attrs = data.get("data", {}).get("attributes", {})
        if not attrs:
            return None
        return {
            "canonical": attrs["entity"]["legalName"]["name"],
            "lei": attrs["lei"],
            "jurisdiction": attrs["entity"].get("jurisdiction", ""),
            "status": attrs["entity"]["status"],
            "gleif_url": f"https://search.gleif.org/#/record/{attrs['lei']}",
        }
    except RuntimeError:
        return None


def _derive_aliases(canonical: str, scope_name: str, hint: str | None = None) -> set[str]:
    """
    Generate mechanical alias variants from a canonical legal name and scope name.
    Covers: case variants, punctuation stripping, legal suffix removal,
    accent normalization, ampersand expansion, THE/La prefix stripping.
    """
    def _normalize_accents(s: str) -> str:
        """Convert accented chars to ASCII equivalents."""
        return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")

    def _strip_legal_suffixes(s: str) -> str:
        """Remove common legal entity suffixes."""
        suffixes = [
            r"\bINC\.?$", r"\bCORP\.?$", r"\bLLC\.?$", r"\bLTD\.?$",
            r"\bPLC\.?$", r"\bN\.V\.?$", r"\bS\.A\.?$", r"\bS\.P\.A\.?$",
            r"\bABP\.?$", r"\bGMBH\.?$", r"\bAG\.?$", r"\bSE\.?$",
            r"\bSOCIETA' PER AZIONI$", r"\bSPERSONEN AZIONI$",
            r"\bCORPORATION$", r"\bCOMPANY$", r"\bGROUP$", r"\bGROEP$",
            r"\bBANK$", r"\bFINANCIAL$", r"\bHOLDINGS?$",
        ]
        result = s.strip()
        for suffix in suffixes:
            result = re.sub(suffix, "", result, flags=re.IGNORECASE).strip().rstrip(",").strip()
        return result.strip()

    def _strip_leading_articles(s: str) -> str:
        """Remove THE, La, Le, L', De, The from start."""
        return re.sub(r"^(THE|LA|LE|L'|DE|DER|DIE|DAS)\s+", "", s, flags=re.IGNORECASE).strip()

    def _expand_ampersand(s: str) -> str:
        return s.replace(" & ", " and ").replace("&", "and")

    def _contract_ampersand(s: str) -> str:
        return re.sub(r"\band\b", "&", s, flags=re.IGNORECASE)

    aliases: set[str] = set()

    # Seed set — canonical, scope_name, hint
    seeds = [canonical, scope_name]
    if hint:
        seeds.append(hint)

    for seed in seeds:
        if not seed:
            continue
        s = seed.strip()
        aliases.add(s)                          # original
        aliases.add(s.upper())                  # UPPER
        aliases.add(s.lower())                  # lower
        aliases.add(s.title())                  # Title Case
        aliases.add(_normalize_accents(s))      # accent stripped
        aliases.add(_normalize_accents(s).title())

        # Ampersand variants
        aliases.add(_expand_ampersand(s))
        aliases.add(_contract_ampersand(s))

        # Strip leading article
        stripped_article = _strip_leading_articles(s)
        if stripped_article != s:
            aliases.add(stripped_article)
            aliases.add(stripped_article.title())
            aliases.add(_normalize_accents(stripped_article))

        # Strip legal suffix
        stripped_suffix = _strip_legal_suffixes(s)
        if stripped_suffix and stripped_suffix != s:
            aliases.add(stripped_suffix)
            aliases.add(stripped_suffix.title())
            aliases.add(_normalize_accents(stripped_suffix))
            aliases.add(_normalize_accents(stripped_suffix).title())
            # Strip article from suffix-stripped too
            stripped_both = _strip_leading_articles(stripped_suffix)
            if stripped_both != stripped_suffix:
                aliases.add(stripped_both)
                aliases.add(stripped_both.title())
                aliases.add(_normalize_accents(stripped_both))

        # Strip punctuation entirely
        no_punct = re.sub(r"[.,'\-]", "", s).strip()
        if no_punct != s:
            aliases.add(no_punct)
            aliases.add(no_punct.title())

    # AIStudio_876 — distinctive single-token candidates so users typing one word
    # ("JPMorgan", "Goldman", "Citigroup") are recognized even though GLEIF stores
    # multi-word forms. A word qualifies only if it's ≥4 chars and not a corporate
    # stopword. Cross-firm collision is filtered later in _enrich_aliases (which has
    # the full roster) — a single word shared by two firms must NOT become an alias.
    _CORP_STOPWORDS = {
        "the", "and", "for", "bank", "banco", "group", "groep", "groupe", "gruppo",
        "holding", "holdings", "corp", "corporation", "inc", "incorporated", "ltd",
        "plc", "company", "financial", "services", "capital", "partners", "trust",
        "fund", "global", "markets", "national", "international", "general",
        "société", "societe", "generale", "générale", "per", "azioni",
    }
    for seed in seeds:
        if not seed:
            continue
        for word in re.split(r"[\s.,·\-/&]+", _normalize_accents(seed)):
            w = re.sub(r"[^A-Za-z0-9]", "", word)
            if len(w) >= 4 and w.lower() not in _CORP_STOPWORDS:
                aliases.add(w)
                aliases.add(w.title())

    # Filter: remove empty strings and single chars
    return {a for a in aliases if a and len(a) > 1}


def _fetch_wikidata_aliases(records: list[dict]) -> dict[str, dict]:
    """
    Batch Wikidata SPARQL lookup by LEI code (P1278).
    Returns dict mapping LEI → {label, short_names, tickers}.
    One round trip for all entities.
    """
    leis = [r["lei"] for r in records if r.get("lei")]
    if not leis:
        return {}

    # Build VALUES block — Wikidata handles up to ~200 values fine
    values = " ".join(f'"{lei}"' for lei in leis)
    sparql = f"""
SELECT ?lei ?itemLabel ?shortName ?ticker WHERE {{
  VALUES ?lei {{ {values} }}
  ?item wdt:P1278 ?lei .
  OPTIONAL {{ ?item wdt:P1813 ?shortName . }}
  OPTIONAL {{ ?item p:P414 ?stmt . ?stmt pq:P249 ?ticker . }}
  SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en" }}
}}
"""
    url = (
        "https://query.wikidata.org/sparql?query="
        + urllib.parse.quote(sparql.strip())
        + "&format=json"
    )
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "AIStudio/1.0 ais_import_knowledge_base"})
        with urllib.request.urlopen(req, timeout=30, context=_SSL_CONTEXT) as r:
            data = json.loads(r.read())
    except Exception as e:
        print(f"  ⚠ Wikidata lookup failed: {e} — skipping enrichment")
        return {}

    result: dict[str, dict] = {}
    for row in data.get("results", {}).get("bindings", []):
        lei = row.get("lei", {}).get("value", "")
        if not lei:
            continue
        if lei not in result:
            result[lei] = {"label": "", "short_names": set(), "tickers": set()}
        label = row.get("itemLabel", {}).get("value", "")
        if label:
            result[lei]["label"] = label
        short = row.get("shortName", {}).get("value", "")
        if short:
            result[lei]["short_names"].add(short)
        ticker = row.get("ticker", {}).get("value", "")
        if ticker:
            result[lei]["tickers"].add(ticker)

    return result


def _enrich_aliases(records: list[dict], scope_entities: list[dict]) -> list[dict]:
    """
    Enrich each record's aliases using:
    1. Wikidata batch lookup (label, short names, tickers)
    2. Mechanical normalization (_derive_aliases)
    3. Manual aliases from scope file
    Returns records with enriched aliases field.
    """
    # Build scope lookup: scope_name → scope entity dict
    scope_map = {e["name"]: e for e in scope_entities}

    print("  ▶ Fetching Wikidata aliases...", flush=True)
    wikidata = _fetch_wikidata_aliases(records)
    if wikidata:
        print(f"  ✅ Wikidata: {len(wikidata)} entities enriched")
    else:
        print("  ⚠ Wikidata: no data returned")

    for rec in records:
        lei = rec.get("lei", "")
        canonical = rec.get("canonical", "")
        scope_name = rec.get("scope_name", "")
        scope_entity = scope_map.get(scope_name, {})
        hint = scope_entity.get("legal_name_hint")
        manual_aliases = scope_entity.get("aliases", [])

        # Start with mechanical derivation
        alias_set = _derive_aliases(canonical, scope_name, hint)

        # Add Wikidata enrichment — store fields explicitly AND fold into aliases
        wd = wikidata.get(lei, {})
        wd_label = wd.get("label", "")
        wd_short_names = sorted(wd.get("short_names", set()))
        wd_tickers = sorted(wd.get("tickers", set()))

        if wd_label:
            alias_set.add(wd_label)
            alias_set.update(_derive_aliases(wd_label, scope_name))
        for short in wd_short_names:
            alias_set.add(short)
        for ticker in wd_tickers:
            alias_set.add(ticker)

        # Add manual aliases from scope file
        alias_set.update(manual_aliases)

        # Remove canonical itself and very short tokens
        alias_set.discard(canonical)
        alias_set = {a for a in alias_set if len(a) > 1}

        # Store Wikidata fields explicitly — used at ingest time for
        # [Document:] prefix injection (natural query forms only).
        # Full alias set used at query time for BM25 expansion.
        rec["wikidata_label"] = wd_label or ""
        rec["wikidata_short_name"] = wd_short_names[0] if wd_short_names else ""
        rec["wikidata_tickers"] = wd_tickers
        rec["aliases"] = sorted(alias_set)

    # AIStudio_876 — cross-firm collision removal (the distinctiveness guard).
    # A single-token or any alias shared by two or more firms in this scope is
    # ambiguous and must not drive recognition/filtering for either. Count each
    # alias (case-insensitive) across all records; drop any that appear for >1 firm.
    _alias_owners: dict[str, set[str]] = {}
    for rec in records:
        for a in rec["aliases"]:
            _alias_owners.setdefault(a.lower(), set()).add(rec.get("scope_name", "") or rec.get("canonical", ""))
    _ambiguous = {a for a, owners in _alias_owners.items() if len(owners) > 1}
    if _ambiguous:
        dropped_total = 0
        for rec in records:
            kept = [a for a in rec["aliases"] if a.lower() not in _ambiguous]
            dropped_total += len(rec["aliases"]) - len(kept)
            rec["aliases"] = kept
        print(f"  ▶ Collision guard: dropped {dropped_total} ambiguous alias(es) "
              f"shared across firms ({len(_ambiguous)} distinct token(s))")

    return records




def _load_metadata(source: str) -> dict:
    """Load knowledge source metadata YAML."""
    path = KNOWLEDGE_SOURCES_DIR / source / f"{source}_metadata.yaml"
    if not path.exists():
        raise FileNotFoundError(f"Metadata file not found: {path}")
    with open(path) as f:
        return yaml.safe_load(f)


def _update_catalog(source: str, corpus: str, scope: str,
                    count: int, output_path: Path) -> None:
    """Update catalog.yaml with this import record."""
    if CATALOG_PATH.exists():
        with open(CATALOG_PATH) as f:
            catalog = yaml.safe_load(f) or {}
    else:
        catalog = {"schema_version": "1.0", "sources": {}}

    if source not in catalog.get("sources", {}):
        catalog.setdefault("sources", {})[source] = {"imported": []}

    # Remove existing entry for same corpus+scope if present
    existing = catalog["sources"][source].get("imported", [])
    existing = [e for e in existing if not (e["corpus"] == corpus and e["scope"] == scope)]

    existing.append({
        "corpus": corpus,
        "scope": scope,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "count": count,
        "file": str(output_path.relative_to(REPO)),
    })
    catalog["sources"][source]["imported"] = existing

    CATALOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CATALOG_PATH, "w") as f:
        yaml.dump(catalog, f, allow_unicode=True, sort_keys=False, default_flow_style=False)


def cmd_list(script_name: str, version: str) -> int:
    """Show catalog of imported knowledge sources. Parametrized (no module SCRIPT_NAME)."""
    print(_bold(f"[{script_name} v{version} — Imported knowledge sources]"))
    if not CATALOG_PATH.exists():
        print("  ℹ No imports yet — catalog is empty.")
        return 0
    with open(CATALOG_PATH) as f:
        catalog = yaml.safe_load(f) or {}
    sources = catalog.get("sources", {})
    if not sources:
        print("  ℹ No imports yet — catalog is empty.")
        return 0
    for source, data in sources.items():
        imports = data.get("imported", [])
        if not imports:
            print(f"  · {source}: no imports")
            continue
        for entry in imports:
            print(f"  ✅ {source} | corpus: {entry['corpus']} | scope: {entry.get('scope', '-')} "
                  f"| {entry['count']} records | {entry['date']}")
    return 0
