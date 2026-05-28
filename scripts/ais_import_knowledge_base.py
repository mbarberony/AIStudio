#!/usr/bin/env python3
"""
ais_import_knowledge_base.py — Import external knowledge source data for a corpus scope
Version: 1.0.1

Reads:
  data/knowledge_sources/<K>/<K>_metadata.yaml       — API config, license, endpoint structure
  benchmarks/<C>/<C>_<S>_scope.yaml                  — flat list of entity/term names to fetch

Writes:
  data/knowledge_sources/<K>/<K>_<C>_<S>_<A>.yaml    — fetched + enriched output
  data/knowledge_sources/catalog.yaml                 — registry of all imported sources

Usage (via wrapper):
  ais_import_knowledge_base --source gleif --corpus sec_10k --scope 25_firms
  ais_import_knowledge_base --source bis_basel --corpus any_corpus --scope full
  ais_import_knowledge_base --list
"""

import argparse
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

VERSION = "1.0.12"
# Changelog:
# 1.0.12 — Propagate xbrl_name from scope entity into GLEIF record. Allows
#           ais_enrich_qdrant to match chunks by exact XBRL EntityRegistrantName.
# 1.0.11 — Add explicit wikidata_label, wikidata_short_name, wikidata_tickers fields.
# 1.0.2 — Fix GLEIF entity matching: prefer US jurisdiction, score by exact/partial
#          name match, fetch 10 results and rank rather than taking first. Fixes
#          wrong entities (Citigroup Congo, Blackrock College, etc.) returned by
#          naive first-match approach.
# 1.0.1 — Fix lint: spurious f-strings, inline if statements.
# 1.0.0 — Initial implementation: gleif source handler, catalog.yaml writer.
SCRIPT_NAME = "ais_import_knowledge_base"

# ── Repo root resolution ──────────────────────────────────────────────────────
REPO = Path(__file__).parent.parent
KNOWLEDGE_SOURCES_DIR = REPO / "data" / "knowledge_sources"
CATALOG_PATH = KNOWLEDGE_SOURCES_DIR / "catalog.yaml"

# ── Supported sources ─────────────────────────────────────────────────────────
SUPPORTED_SOURCES = ["gleif", "sec_edgar", "bis_basel", "nist_ai_rmf", "esrs"]

# ── Output attribute type per source ─────────────────────────────────────────
SOURCE_ATTRIBUTE_TYPE = {
    "gleif":       "entities",
    "sec_edgar":   "companies",
    "bis_basel":   "glossary",
    "nist_ai_rmf": "glossary",
    "esrs":        "glossary",
}

# ── Sources that require a scope (no full download fallback) ──────────────────
SCOPE_REQUIRED = {"gleif", "sec_edgar"}

# ── Sources that use full download (scope is always "full") ───────────────────
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

    return records


def _import_gleif(scope_entities: list[dict], metadata: dict) -> tuple[list[dict], list[str]]:
    """Fetch GLEIF data for each entity in scope. Returns (records, failed_names)."""
    records = []
    failed = []
    total = len(scope_entities)
    width = len(str(total))

    for i, entity in enumerate(scope_entities, 1):
        name = entity["name"]
        hint = entity.get("legal_name_hint")
        lei_override = entity.get("lei_override")
        print(f"  [{i:{width}}/{total}] {name}...", end=" ", flush=True)

        if lei_override:
            result = _fetch_gleif_by_lei(lei_override, metadata)
        else:
            search_name = hint if hint else name
            jurisdiction = entity.get("jurisdiction")
            result = _fetch_gleif_entity(search_name, metadata, common_name=name,
                                         jurisdiction=jurisdiction)
        if result:
            result["scope_name"] = name
            result["aliases"] = []   # populated by _enrich_aliases
            # Propagate xbrl_name from scope if present — exact XBRL EntityRegistrantName
            # string used by ais_enrich_qdrant to match existing Qdrant chunk prefixes
            if entity.get("xbrl_name"):
                result["xbrl_name"] = entity["xbrl_name"]
            records.append(result)
            print(f"✅ {result['lei']} — {result['canonical']}")
        else:
            print("⚠ not found")
            failed.append(name)
        time.sleep(0.3)

    # Enrich aliases — Wikidata batch + mechanical normalization + scope manual aliases
    print("--- Enriching aliases")
    records = _enrich_aliases(records, scope_entities)

    return records, failed


def _load_metadata(source: str) -> dict:
    """Load knowledge source metadata YAML."""
    path = KNOWLEDGE_SOURCES_DIR / source / f"{source}_metadata.yaml"
    if not path.exists():
        raise FileNotFoundError(f"Metadata file not found: {path}")
    with open(path) as f:
        return yaml.safe_load(f)


def _load_scope(corpus: str, scope: str) -> list[str]:
    """Load scope YAML and return list of entity/term names."""
    path = REPO / "benchmarks" / corpus / f"{corpus}_{scope}_scope.yaml"
    if not path.exists():
        raise FileNotFoundError(
            f"Scope file not found: {path}\n"
            f"  Expected: benchmarks/{corpus}/{corpus}_{scope}_scope.yaml"
        )
    with open(path) as f:
        data = yaml.safe_load(f)
    entities = data.get("entities", [])
    if not entities:
        raise ValueError(f"Scope file has no entities: {path}")
    # Normalize: support both plain strings and dicts with name + optional legal_name_hint
    normalized = []
    for e in entities:
        if isinstance(e, str):
            normalized.append({"name": e})
        elif isinstance(e, dict):
            normalized.append(e)
    return normalized


def _output_path(source: str, corpus: str, scope: str) -> Path:
    attr_type = SOURCE_ATTRIBUTE_TYPE[source]
    return KNOWLEDGE_SOURCES_DIR / source / f"{source}_{corpus}_{scope}_{attr_type}.yaml"


def _write_output(path: Path, source: str, corpus: str, scope: str,
                  records: list[dict], failed: list[str]) -> None:
    """Write output YAML file."""
    attr_type = SOURCE_ATTRIBUTE_TYPE[source]
    content = {
        "schema_version": "1.1",
        "source_id": source,
        "corpus": corpus,
        "scope_id": scope,
        "generated": datetime.now().strftime("%Y-%m-%d"),
        "entity_count": len(records),
        "failed_count": len(failed),
        "failed": failed if failed else [],
        attr_type: records,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        yaml.dump(content, f, allow_unicode=True, sort_keys=False, default_flow_style=False)


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


def _cmd_list() -> int:
    """Show catalog of imported knowledge sources."""
    print(_bold(f"[{SCRIPT_NAME} v{VERSION} — Imported knowledge sources]"))
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
            print(f"  ✅ {source} | corpus: {entry['corpus']} | scope: {entry['scope']} "
                  f"| {entry['count']} records | {entry['date']}")
    return 0


def _cmd_import(source: str, corpus: str, scope: str, force: bool) -> int:
    """Main import flow."""
    print(_bold(f"[{SCRIPT_NAME} v{VERSION} — Import knowledge source]"))
    print("--- Config")
    print(f"  · Source  : {source}")
    print(f"  · Corpus  : {corpus}")
    print(f"  · Scope   : {scope}")

    # ── Preflight ─────────────────────────────────────────────────────────────
    print("--- Preflight")

    if source not in SUPPORTED_SOURCES:
        _err(f"Unknown source '{source}'. Supported: {', '.join(SUPPORTED_SOURCES)}")
        return 1

    if source in SCOPE_REQUIRED and not corpus:
        _err(f"--corpus is required for source '{source}'")
        return 1

    try:
        metadata = _load_metadata(source)
        print(f"  ✅ Metadata loaded: data/knowledge_sources/{source}/{source}_metadata.yaml")
    except FileNotFoundError as e:
        _err(str(e))
        return 1

    try:
        scope_entities = _load_scope(corpus, scope)
        print(f"  ✅ Scope loaded: {len(scope_entities)} entities from benchmarks/{corpus}/{corpus}_{scope}_scope.yaml")
    except (FileNotFoundError, ValueError) as e:
        _err(str(e))
        return 1

    output_path = _output_path(source, corpus, scope)
    if output_path.exists() and not force:
        _err(f"Output file already exists: {output_path.relative_to(REPO)}")
        print("  · Use --force to overwrite.")
        return 1

    if _SSL_CONTEXT is None:
        print("  ⚠ certifi not installed — SSL verification disabled")
        print("  · Fix: pip3 install certifi --break-system-packages")

    # ── Fetch ─────────────────────────────────────────────────────────────────
    print(f"--- Fetching from {metadata['access']['base_url']}")

    if source == "gleif":
        records, failed = _import_gleif(scope_entities, metadata)
    else:
        _err(f"Source '{source}' fetch not yet implemented.")
        print("  · Supported for fetch: gleif")
        print("  · Planned: sec_edgar, bis_basel, nist_ai_rmf, esrs")
        return 1

    # ── Write output ──────────────────────────────────────────────────────────
    print("--- Writing output")
    _write_output(output_path, source, corpus, scope, records, failed)
    print(f"  ✅ {output_path.relative_to(REPO)}")
    print(f"  · {len(records)} records written | {len(failed)} failed")
    if failed:
        print(f"  · Failed: {', '.join(failed)}")

    # ── Update catalog ────────────────────────────────────────────────────────
    _update_catalog(source, corpus, scope, len(records), output_path)
    print("  ✅ catalog.yaml updated")

    # ── Summary ───────────────────────────────────────────────────────────────
    print("--- Summary")
    status = "✅" if not failed else "⚠"
    print(f"{status} {source} import complete: {len(records)}/{len(scope_entities)} entities fetched")
    if not failed:
        print(f"· Next: wire {output_path.name} into rag_core._apply_knowledge_sources()")
    return 0 if not failed else 1


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog=SCRIPT_NAME, add_help=False)
    p.add_argument("--source", default=None)
    p.add_argument("--corpus", default=None)
    p.add_argument("--scope",  default=None)
    p.add_argument("--force",  action="store_true")
    p.add_argument("--list",   action="store_true")
    p.add_argument("--version", action="store_true")
    p.add_argument("--help",   action="store_true")
    args = p.parse_args(argv)

    if args.version:
        print(f"{SCRIPT_NAME} v{VERSION}")
        return 0

    if args.help:
        p.print_help()
        return 0

    if args.list:
        return _cmd_list()

    # ── Validate required args ────────────────────────────────────────────────
    missing = []
    if not args.source:
        missing.append("--source")
    if not args.corpus:
        missing.append("--corpus")
    if not args.scope:
        missing.append("--scope")
    if missing:
        _err(f"Missing required arguments: {', '.join(missing)}")
        print(f"  · Usage: {SCRIPT_NAME} --source <K> --corpus <C> --scope <S>")
        print(f"  · Run '{SCRIPT_NAME} --help' for full usage.")
        return 1

    return _cmd_import(args.source, args.corpus, args.scope, args.force)


if __name__ == "__main__":
    raise SystemExit(main())
