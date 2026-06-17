#!/usr/bin/env python3
"""
ais_import_glossary_kb_ops.py — Build term→expansion glossary knowledge sources.

OPS command. Splits the glossary half out of the legacy ais_import_knowledge_base
importer (now deprecated). Produces a corpus-wide glossary YAML that rag_core
binds at QUERY time (acronym → BM25 expansion string), distinct from the entity
KB (ais_import_entity_kb_ops), which binds GLEIF identity at INGEST time.

Glossary sources are static, curated seeds (deterministic) — there is nothing to
resolve against an external API, so this command has NO review gate: it imports and
writes in one pass. Output schema is held identical to the legacy importer because
rag_core._apply_glossary_sources reads it.

Usage:
    ais_import_glossary_kb_ops --source bis_basel
    ais_import_glossary_kb_ops --source bis_basel --corpus sec_10k
    ais_import_glossary_kb_ops --list
    ais_import_glossary_kb_ops --version

Shared helpers (_bold, _err, _update_catalog, cmd_list, constants) live in the
sibling library scripts/_kb_common_ops.py (underscore = not a command; no alias,
install:none — exempt from help-conformance by construction).

Changelog
  1.0.0 — Initial split from ais_import_knowledge_base_ops.py v1.1.0. Lifts
          _import_bis_basel (52-term Basel III/IV static seed) verbatim. Glossary
          write schema (schema_version 1.1, attr key "glossary") preserved exactly
          for rag_core compatibility. SOURCE_HANDLERS map; nist_ai_rmf / esrs
          declared PLANNED (no handler yet). No review gate (static deterministic
          data). SCRIPT_NAME = alias per HOWTO_OPS Step 6.
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path

import _kb_common_ops as kb  # shared library (underscore = not a command; no alias, install:none)
import yaml

SCRIPT_NAME = "ais_import_glossary_kb"  # F-024: use civilian name (not _ops) in user-visible output
VERSION = "1.0.1"

# Glossary sources this command knows how to build. bis_basel is live; the other
# two are registered in the shared SOURCE_ATTRIBUTE_TYPE map but have no handler yet.
PLANNED_SOURCES = {"nist_ai_rmf", "esrs"}


def _import_bis_basel() -> tuple[list[dict], list[str]]:
    """
    Build BIS Basel regulatory glossary from static seed data.

    BIS SCO95 glossary uses JavaScript rendering — not scrapeable via urllib.
    Static seed is the correct v1 approach: curated terms with full forms and
    BM25 expansion strings. ~52 terms covering Basel III/IV capital, liquidity,
    leverage, stress testing, and market risk frameworks.

    Returns (records, failed) — failed is always [] for static data.
    Each record: {term, full_form, expansion, scope_type}
    """
    # Static seed: (acronym, full_form, expansion_string)
    # expansion_string = terms to inject into BM25 query when acronym is detected.
    # Designed to bridge the vocabulary gap between user queries (acronyms) and
    # document text (full regulatory language).
    _SEED: list[tuple[str, str, str]] = [
        # Capital — Tier 1 / Tier 2
        ("AT1",    "Additional Tier 1",
         "AT1 Additional Tier 1 capital contingent convertible CoCo"),
        ("CET1",   "Common Equity Tier 1",
         "CET1 Common Equity Tier 1 capital ratio regulatory capital"),
        ("T1",     "Tier 1 Capital",
         "Tier 1 capital ratio core capital going-concern"),
        ("T2",     "Tier 2 Capital",
         "Tier 2 capital gone-concern supplementary capital"),
        ("RWA",    "Risk-Weighted Assets",
         "RWA risk-weighted assets capital requirements standardized approach"),
        ("SCB",    "Stress Capital Buffer",
         "SCB stress capital buffer DFAST Federal Reserve capital requirement"),
        ("CCyB",   "Countercyclical Capital Buffer",
         "CCyB countercyclical capital buffer macroprudential Basel III"),
        ("CCB",    "Capital Conservation Buffer",
         "CCB capital conservation buffer 2.5% CET1 Basel III"),
        ("TLAC",   "Total Loss-Absorbing Capacity",
         "TLAC total loss-absorbing capacity resolution G-SIB bail-in"),
        ("MREL",   "Minimum Requirement for Own Funds and Eligible Liabilities",
         "MREL minimum requirement own funds eligible liabilities resolution EU"),
        # Leverage
        ("SLR",    "Supplementary Leverage Ratio",
         "SLR supplementary leverage ratio 3% Tier 1 capital exposure"),
        ("eSLR",   "Enhanced Supplementary Leverage Ratio",
         "eSLR enhanced supplementary leverage ratio G-SIB 5% 6%"),
        ("LR",     "Leverage Ratio",
         "leverage ratio Tier 1 total exposure Basel III"),
        # Liquidity
        ("LCR",    "Liquidity Coverage Ratio",
         "LCR liquidity coverage ratio HQLA high-quality liquid assets 30-day"),
        ("NSFR",   "Net Stable Funding Ratio",
         "NSFR net stable funding ratio available required stable funding"),
        ("HQLA",   "High-Quality Liquid Assets",
         "HQLA high-quality liquid assets Level 1 Level 2 LCR liquidity"),
        # Market Risk
        ("FRTB",   "Fundamental Review of the Trading Book",
         "FRTB Fundamental Review Trading Book market risk capital IMA SA"),
        ("IMA",    "Internal Models Approach",
         "IMA internal models approach FRTB market risk VaR ES"),
        ("SA",     "Standardized Approach",
         "SA standardized approach capital market risk credit risk Basel"),
        ("VaR",    "Value at Risk",
         "VaR value at risk market risk trading book 99th percentile"),
        ("ES",     "Expected Shortfall",
         "ES expected shortfall CVaR conditional value at risk FRTB"),
        ("CVA",    "Credit Valuation Adjustment",
         "CVA credit valuation adjustment counterparty credit risk OTC derivatives"),
        ("DVA",    "Debit Valuation Adjustment",
         "DVA debit valuation adjustment own credit risk fair value"),
        ("XVA",    "Valuation Adjustments",
         "XVA valuation adjustments CVA DVA FVA MVA KVA"),
        # Credit Risk
        ("ECL",    "Expected Credit Loss",
         "ECL expected credit loss IFRS 9 CECL provision allowance"),
        ("PD",     "Probability of Default",
         "PD probability of default credit risk IRB internal ratings"),
        ("LGD",    "Loss Given Default",
         "LGD loss given default recovery rate credit risk IRB"),
        ("EAD",    "Exposure at Default",
         "EAD exposure at default credit risk loan equivalent"),
        ("IRB",    "Internal Ratings-Based Approach",
         "IRB internal ratings-based approach advanced foundation credit risk"),
        ("NPL",    "Non-Performing Loan",
         "NPL non-performing loan credit quality Stage 3 impaired"),
        ("NIM",    "Net Interest Margin",
         "NIM net interest margin net interest income rate sensitivity"),
        ("NII",    "Net Interest Income",
         "NII net interest income interest rate risk banking book IRRBB"),
        ("IRRBB",  "Interest Rate Risk in the Banking Book",
         "IRRBB interest rate risk banking book NII EVE sensitivity"),
        ("EVE",    "Economic Value of Equity",
         "EVE economic value equity interest rate risk IRRBB"),
        # Stress Testing
        ("DFAST",  "Dodd-Frank Act Stress Test",
         "DFAST Dodd-Frank stress test Federal Reserve annual supervisory"),
        ("CCAR",   "Comprehensive Capital Analysis and Review",
         "CCAR comprehensive capital analysis review Federal Reserve stress test"),
        ("SREP",   "Supervisory Review and Evaluation Process",
         "SREP supervisory review evaluation process ECB Pillar 2"),
        # Regulatory Bodies & Frameworks
        ("BCBS",   "Basel Committee on Banking Supervision",
         "BCBS Basel Committee Banking Supervision Basel III Basel IV BIS"),
        ("FSB",    "Financial Stability Board",
         "FSB Financial Stability Board G-SIB macroprudential systemic risk"),
        ("EBA",    "European Banking Authority",
         "EBA European Banking Authority CRR CRD stress test EU banking"),
        ("ECB",    "European Central Bank",
         "ECB European Central Bank SSM monetary policy EU banks"),
        ("CRR",    "Capital Requirements Regulation",
         "CRR Capital Requirements Regulation EU Basel III Pillar 1"),
        ("CRD",    "Capital Requirements Directive",
         "CRD Capital Requirements Directive EU Basel III supervisory"),
        # G-SIB / D-SIB
        ("G-SIB",  "Global Systemically Important Bank",
         "G-SIB global systemically important bank GSIB surcharge capital buffer"),
        ("GSIB",   "Global Systemically Important Bank",
         "GSIB G-SIB global systemically important bank surcharge FSB"),
        ("D-SIB",  "Domestic Systemically Important Bank",
         "D-SIB domestic systemically important bank national buffer"),
        # Resolution
        ("BRRD",   "Bank Recovery and Resolution Directive",
         "BRRD Bank Recovery Resolution Directive EU bail-in MREL resolution"),
        ("SPOE",   "Single Point of Entry",
         "SPOE single point of entry resolution strategy holding company"),
        # Accounting / Reporting
        ("IFRS9",  "IFRS 9 Financial Instruments",
         "IFRS 9 IFRS9 expected credit loss ECL provision staging"),
        ("CECL",   "Current Expected Credit Loss",
         "CECL current expected credit loss US GAAP ASC 326 allowance"),
        ("ICAAP",  "Internal Capital Adequacy Assessment Process",
         "ICAAP internal capital adequacy assessment process Pillar 2"),
        ("ILAAP",  "Internal Liquidity Adequacy Assessment Process",
         "ILAAP internal liquidity adequacy assessment process Pillar 2"),
    ]

    records = []
    for term, full_form, expansion in _SEED:
        records.append({
            "term": term,
            "full_form": full_form,
            "expansion": expansion,
            "scope_type": "corpus_wide",
        })

    print(f"  ✅ {len(records)} terms loaded from static seed")
    return records, []



# Registered after _import_bis_basel is defined (above).
SOURCE_HANDLERS = {
    "bis_basel": _import_bis_basel,
}


def _output_path(source: str, corpus: str, scope: str) -> Path:
    """Mirror the legacy importer path: <source>/<source>_<corpus>_<scope>_<attr>.yaml."""
    attr_type = kb.SOURCE_ATTRIBUTE_TYPE[source]
    return kb.KNOWLEDGE_SOURCES_DIR / source / f"{source}_{corpus}_{scope}_{attr_type}.yaml"


def _write_output(path: Path, source: str, corpus: str, scope: str,
                  records: list[dict], failed: list[str]) -> None:
    """Write the glossary YAML. Schema held identical to the legacy importer
    (rag_core._apply_glossary_sources depends on the key layout)."""
    attr_type = kb.SOURCE_ATTRIBUTE_TYPE[source]
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


def _cmd_import(source: str, corpus: str, scope: str) -> int:
    print(kb._bold(f"\n  {SCRIPT_NAME} — glossary import"))
    print(f"  · Source  : {source}")
    print(f"  · Corpus  : {corpus}")
    print(f"  · Scope   : {scope}\n")

    if source in PLANNED_SOURCES:
        kb._err(f"Source '{source}' is registered but not yet implemented (no handler).")
        return 1
    if source not in SOURCE_HANDLERS:
        supported = ", ".join(sorted(SOURCE_HANDLERS))
        kb._err(f"Unknown glossary source '{source}'. Available: {supported}")
        return 1

    records, failed = SOURCE_HANDLERS[source]()
    if not records:
        kb._err("No records produced — nothing written.")
        return 1

    out = _output_path(source, corpus, scope)
    _write_output(out, source, corpus, scope, records, failed)
    kb._update_catalog(source, corpus, scope, len(records), out)

    rel = out.relative_to(kb.REPO)
    print(f"\n  ✅ Wrote {len(records)} terms → {rel}")
    print(f"  ✅ Catalog updated → {kb.CATALOG_PATH.relative_to(kb.REPO)}\n")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        prog=SCRIPT_NAME,
        description="Build a term→expansion glossary knowledge source (query-time binding).",
        add_help=True,
    )
    parser.add_argument("--source", help="Glossary source to import (e.g. bis_basel)")
    parser.add_argument("--corpus", default="any_corpus",
                        help="Corpus scope label (default: any_corpus — corpus-wide)")
    parser.add_argument("--scope", default="full",
                        help="Scope id (default: full)")
    parser.add_argument("--list", action="store_true",
                        help="List importable knowledge sources and exit")
    parser.add_argument("--version", action="store_true",
                        help="Print version and exit")
    args = parser.parse_args()

    if args.version:
        print(f"{SCRIPT_NAME} v{VERSION}")
        return 0
    if args.list:
        return kb.cmd_list(SCRIPT_NAME, VERSION)
    if not args.source:
        kb._err("--source is required (or use --list / --version).")
        return 1

    return _cmd_import(args.source, args.corpus, args.scope)


if __name__ == "__main__":
    sys.exit(main())
