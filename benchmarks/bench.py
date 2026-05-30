#!/usr/bin/env python3
# Changelog: 2.0.12 — Remove --difficulty flag (redundant — difficulty is encoded
#              in questions filename; --questions basic implies difficulty:basic).
#              Add --scope flag. Fix stem resolution to try corpus_scope_stem,
#              corpus_stem, stem_questions patterns before falling back to stem.yaml.
# Changelog: 2.0.11 — Fix stem expansion: try {corpus}_{stem}_questions.yaml and
#              {stem}_questions.yaml before {stem}.yaml. Enables --questions basic
#              to resolve esef_banks_basic_questions.yaml. Also adds scope-aware
#              resolution: {corpus}_{scope}_{stem}_questions.yaml when --scope active.
# Changelog: 2.0.10 — AIStudio_840 addendum: entity_count field added to
#              load_questions() (v1.2 schema). Captures number of distinct entities
#              needed to answer — analytical field complementing entity_filter.
# Changelog: 2.0.9 — AIStudio_840: questions schema v1.2 support. load_questions() now reads question_language, answer_location, section_count, data_type, difficulty fields (all optional, backward compatible). filter_questions() gains difficulty= parameter. --difficulty flag added (basic|standard|complex). Per-question verbose output shows difficulty + answer_location.
# Changelog: 2.0.8 — AIStudio_841: implement --verbose (-v) and --super-verbose (-vv).
#             --verbose: chunks_retrieved, entity_filter, first_source per question.
#             --super-verbose: retrieval_query, entity_tokens, keywords, model_used, answer preview.
#             Requires api.py v1.8.8 (chunks_retrieved in AskResponse).
# Changelog: 2.0.7 — AIStudio_841 TODO: --verbose (chunks_retrieved, effective_k, entity_filter,
#             first source per question) and --super-verbose (retrieval_query, entity tokens,
#             keywords, model_used, full answer, all citations). Requires AskResponse to return
#             chunks_retrieved + effective_k. Filed HIGH/WEEK.
# Changelog: 2.0.6 — MD report shows retrieval_query (post-expansion), model_used,
#             entity_filter, keywords per question. Replaces firm/year placebo fields.
# Changelog: 2.0.5 — AIStudio_840: wire keywords from YAML through run_query() to
#             /ask payload. Previously keywords were evaluation-only (used by evaluate()
#             for mechanical scoring) but never sent to the API for BM25 boosting.
#             All 17 previous runs had keywords=None reaching retrieve().
# Changelog: 2.0.4 — fix evaluate() failure return missing citation_count and other keys;
#             bench.py crashed with KeyError when API request failed mid-run.
# Changelog: 2.0.3 — move bold bracketed header to Python per STD §7. Shell wrapper
#             no longer prints version header. bench.py main() prints it as first line.
# Changelog: 2.0.2 — AIStudio_829: benchmark reports bundled as zip (json+md+pdf).
#             Audit trigger: "audit that report" — Claude reads zip, adds qualitative
#             ratings + comments, produces _audited_ zip. Protocol in THINK Master T2.47.
# Changelog: 2.0.1 — AIStudio_828: accent + hyphen normalization in evaluate().
#             flag if < 0.1 on non-trivial questions. Language marker (*) for non-English
#             questions via YAML language field. Remove "all keywords found" from terminal
#             output — keyword pass is the pass condition, not a separate signal.
#             Base Top K label in Configuration section (effective K per AIStudio_825).
# Changelog: 1.9.9 — fix keywords field: read "keywords" first, fall back to "expected_keywords";
#             add Alpha and Min Score to report Configuration markdown section.
# Changelog: 1.9.8 — CRITICAL: entity_filter field was not extracted from YAML
#             questions during load_questions() — q.get("entity_filter") always
#             returned None. Added entity_filter to the question dict.
# Changelog: 1.9.7 — auto-copy .md report to ~/Downloads/ at end of run
#             so urc_deploy --last picks it up immediately.
# Changelog: 1.9.6 — fix evaluate() over-aggressive no_info_signal:
#             only penalize no_info when citation_count == 0. When model has
#             citations it is answering substantively — hedging about missing
#             firms is honest, not a failure.
# Changelog: 1.9.5 — corpus metadata defaults applied for top_k/temperature/alpha/min_score
#             when not explicitly passed via CLI. Uses None sentinel.
# Changelog: 1.9.4 — --questions accepts stem (no path, no .yaml extension);
#             auto-expands to benchmarks/<corpus>/<stem>.yaml.
#             Example: --questions sec_10k_questions_no_filter
# Changelog: 1.9.3 — Fix evaluate() false positives/negatives:
#             (a) 0 citations always fails regardless of keyword pass
#             (b) keyword check restricted to substantive answer only —
#             keywords found in refusal phrases no longer count as keyword pass
#             (c) no_info_signal phrases expanded with observed patterns
# Changelog: 1.8.1 — AIStudio_752: add --alpha flag for hybrid retrieval; pass hybrid_alpha
#            to /ask payload. Removes env var workaround.
"""
AIStudio RAG Benchmark Script
Usage:
    ais_bench                                            # demo corpus, defaults
    ais_bench --corpus sec_10k --top-k 10               # SEC corpus
    ais_bench --corpus demo --model llama3.1:70b        # 70b model

Question subset filtering (sec_10k):
    ais_bench --corpus sec_10k --topics "AI Risk Evolution"
    ais_bench --corpus sec_10k --subset big_banks
    ais_bench --corpus sec_10k --question-ids capital_ratios_trend,latency_test
    ais_bench --corpus sec_10k --topics "Capital & Financial Position" --subset big_banks

Flags:
    --corpus        Corpus name to query (default: demo)
    --top-k         Number of chunks to retrieve (default: 5)
    --temperature   LLM temperature (default: 0.3)
    --model         Model to use (default: from API config)
    --questions     Path to YAML question file (auto-detected from corpus name if omitted)
    --api           API base URL (default: http://localhost:8000)
    --no-markdown   Skip writing .md report
    --full          Include full answers in report (default: first 4 paragraphs)
    --firm          Inject firm filter into all queries (overrides YAML firm fields)
    --subset        Filter questions by firm group: big_banks, bulge_bracket, asset_managers,
                    exchanges, insurance, custody, boutiques. Filters by firm names in question text.
    --topics        Filter questions by topic name (comma-separated, AND with --subset)
    --question-ids  Filter to specific question IDs (comma-separated, AND with other filters)
    --alpha         Hybrid retrieval alpha: 0.0=pure vector, 1.0=pure BM25, None=backend default

Output files (in benchmarks/<corpus>/reports/):
    benchmark_<corpus>_<timestamp>.json
    benchmark_<corpus>_<timestamp>.md
    benchmark_<corpus>_<timestamp>.pdf  (if pandoc + weasyprint installed)

Question file auto-detection (in order):
    benchmarks/<corpus>/<corpus>_questions.yaml
    data/corpora/<corpus>/<corpus>_questions.yaml
    Built-in defaults (SEC 10-K questions — fallback only)
"""

from __future__ import annotations

import argparse
import json
import time

try:
    import yaml as _yaml

    _YAML_AVAILABLE = True
except ImportError:
    _YAML_AVAILABLE = False
from datetime import datetime
from pathlib import Path

# Version — single source of truth for urc_deploy and runtime display.
# Must be within first 8KB (extract_version limit). No # Version: comment.
VERSION = "2.0.12"

# ── Firm subset registry ──────────────────────────────────────────────────────
# Hardwired firm groups for --subset filtering. Mirrors the FIRMS list in
# scripts/download_sec_corpus.py. Used to filter questions by firm name match
# in the question text (case-insensitive). Heuristic but works for v2.0+
# questions which name firms explicitly.

FIRM_SUBSETS: dict[str, list[str]] = {
    "big_banks": [
        "JPMorgan",
        "JPMorgan Chase",
        "Bank of America",
        "Wells Fargo",
        "Citigroup",
        "Citi",
    ],
    "bulge_bracket": [
        "Goldman Sachs",
        "Goldman",
        "Morgan Stanley",
        "JPMorgan",
        "JPMorgan Chase",
        "Bank of America",
        "Citigroup",
        "Citi",
    ],
    "asset_managers": [
        "BlackRock",
        "T. Rowe Price",
        "T Rowe Price",
        "Franklin Templeton",
        "Invesco",
        "AllianceBernstein",
    ],
    "exchanges": [
        "CME Group",
        "CME",
        "Intercontinental Exchange",
        "ICE",
        "Nasdaq",
        "CBOE",
        "CBOE Global Markets",
    ],
    "insurance": [
        "AIG",
        "MetLife",
        "Prudential",
        "Prudential Financial",
        "Travelers",
    ],
    "custody": [
        "BNY Mellon",
        "BNY",
        "State Street",
        "Northern Trust",
    ],
    "boutiques": [
        "Jefferies",
        "Raymond James",
        "Stifel",
        "Stifel Financial",
    ],
}

# ── CLI ───────────────────────────────────────────────────────────────────────


def _sep(label: str) -> None:
    """Print a dim italic section separator per STD - AIStudio - CLI Output."""
    print(f"\033[2m\033[3m--- {label}\033[0m")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="AIStudio RAG Benchmark")
    p.add_argument("--corpus", default="demo", help="Corpus name")
    p.add_argument(
        "--scope",
        default=None,
        help=(
            "Scope stem: filters to a language/firm subset defined in "
            "benchmarks/<corpus>/<corpus>_<scope>_scope.yaml. "
            "e.g. --scope lang_en. Used to resolve --questions stem: "
            "--questions basic → <corpus>_<scope>_basic_questions.yaml."
        ),
    )
    p.add_argument("--top-k", type=int, default=None, help="Top K chunks to retrieve (default: corpus metadata or 5)")
    p.add_argument("--temperature", type=float, default=None, help="LLM temperature (default: corpus metadata or 0.3)")
    p.add_argument("--model", default=None, help="Model ID (default: API default)")
    p.add_argument("--questions", default=None,
                    help="Path to questions YAML file, or bare stem (e.g. sec_10k_questions_no_filter). "
                         "Stem auto-expands to benchmarks/<corpus>/<stem>.yaml.")
    p.add_argument("--api", default="http://localhost:8000", help="API base URL")
    p.add_argument("--no-markdown", action="store_true", help="Skip writing .md report")
    p.add_argument("--full", action="store_true", help="Include full answers in report")
    p.add_argument(
        "--firm",
        default=None,
        help=(
            "Firm name to inject into all queries (e.g. 'Wells Fargo'). "
            "Overrides any per-question 'firm' field in the YAML. Caller is "
            "responsible for spelling and firm selection."
        ),
    )
    p.add_argument(
        "--subset",
        default=None,
        choices=list(FIRM_SUBSETS.keys()),
        help=(
            "Filter questions by firm group. Available: "
            + ", ".join(sorted(FIRM_SUBSETS.keys()))
            + ". Heuristic match: question text must mention at least one firm in the group."
        ),
    )
    p.add_argument(
        "--topics",
        default=None,
        help=(
            "Filter questions by topic name (comma-separated). "
            "Example: --topics 'AI Risk Evolution,Capital & Financial Position'"
        ),
    )
    p.add_argument(
        "--question-ids",
        default=None,
        help=(
            "Filter to specific question IDs (comma-separated). "
            "Example: --question-ids capital_ratios_trend,latency_test"
        ),
    )

    p.add_argument(
        "--alpha",
        type=float,
        default=None,
        help="Hybrid retrieval alpha: 0.0=pure vector, 1.0=pure BM25. None=corpus metadata or backend default.",
    )
    p.add_argument(
        "--min-score",
        type=float,
        default=None,
        dest="min_score",
        help="Minimum chunk score threshold. None=corpus metadata or backend default.",
    )
    p.add_argument(
        "--lang",
        nargs="+",
        default=None,
        metavar="LANG",
        help=(
            "Filter questions by language code (space-separated). "
            "Example: --lang en  OR  --lang en fr. "
            "Questions without a language field default to 'en'. "
            "Use to exclude non-English questions from mechanical scoring."
        ),
    )
    p.add_argument(
        "--verbose", "-v",
        action="store_true",
        help=(
            "Per-question: show chunks_retrieved, effective entity_filter, first source. "
            "AIStudio_841."
        ),
    )
    p.add_argument(
        "--super-verbose", "-vv",
        action="store_true",
        dest="super_verbose",
        help=(
            "Per-question: show retrieval_query (post-expansion), entity tokens, "
            "keywords sent, model_used, and full answer text. Implies --verbose. "
            "AIStudio_841."
        ),
    )

    return p.parse_args()


# ── Load questions ────────────────────────────────────────────────────────────

DEFAULT_QUESTIONS = [
    {
        "id": "goldman_ai_risk",
        "description": "Goldman Sachs AI risk — firm filter",
        "query": "What does Goldman Sachs say about the risks of artificial intelligence?",
        "corpus": None,  # uses CLI --corpus
        "firm": "Goldman Sachs",
        "year": None,
        "expected_keywords": ["artificial intelligence", "AI", "risk", "Goldman"],
        "notes": "Should return Goldman-specific AI risk disclosure",
    },
    {
        "id": "jpmorgan_cybersecurity",
        "description": "JPMorgan cybersecurity risk — firm filter",
        "query": "How does JPMorgan Chase describe their cybersecurity risk management?",
        "corpus": None,
        "firm": "JPMorgan Chase",
        "year": None,
        "expected_keywords": ["cybersecurity", "JPMorgan", "risk"],
        "notes": "Should return JPMorgan cybersecurity section",
    },
    {
        "id": "morgan_stanley_model_risk",
        "description": "Morgan Stanley model risk — firm filter",
        "query": "What is Morgan Stanley's approach to model risk?",
        "corpus": None,
        "firm": "Morgan Stanley",
        "year": None,
        "expected_keywords": ["model risk", "Morgan Stanley"],
        "notes": "Should return model risk governance section",
    },
    {
        "id": "goldman_ai_committee",
        "description": "Goldman AI governance committee — firm filter",
        "query": "Does Goldman Sachs have an AI governance committee and what does it do?",
        "corpus": None,
        "firm": "Goldman Sachs",
        "year": None,
        "expected_keywords": ["Artificial Intelligence", "committee", "governance"],
        "notes": "Should mention Firmwide Artificial Intelligence Risk and Controls Committee",
    },
    {
        "id": "cross_corpus_ai_governance",
        "description": "Cross-corpus AI governance — no filter",
        "query": "Which financial firms have dedicated AI governance committees?",
        "corpus": None,
        "firm": None,
        "year": None,
        "expected_keywords": ["AI", "committee", "governance"],
        "notes": "No firm filter — tests cross-corpus retrieval quality",
    },
    {
        "id": "bofa_climate_risk",
        "description": "Bank of America climate risk — firm filter",
        "query": "How does Bank of America describe climate risk in their annual report?",
        "corpus": None,
        "firm": "Bank of America",
        "year": None,
        "expected_keywords": ["climate", "risk", "Bank of America"],
        "notes": "Should return climate risk section",
    },
    {
        "id": "goldman_2026_revenue",
        "description": "Goldman 2025 revenue — firm + year filter",
        "query": "What were Goldman Sachs total revenues in 2025?",
        "corpus": None,
        "firm": "Goldman Sachs",
        "year": "2026",  # filing year
        "expected_keywords": ["revenue", "billion", "2025"],
        "notes": "Tests year filter combined with firm filter",
    },
    {
        "id": "latency_test",
        "description": "Simple factual — latency baseline",
        "query": "What is Goldman Sachs?",
        "corpus": None,
        "firm": "Goldman Sachs",
        "year": None,
        "expected_keywords": ["Goldman Sachs", "bank", "financial"],
        "notes": "Simple query for latency baseline measurement",
    },
]


def load_questions(path: str | None, corpus: str = "sec_10k", scope: str | None = None) -> list[dict]:
    """
    Load benchmark questions from a file or auto-detect based on corpus name.

    Priority:
    1. Explicit --questions path (JSONL or JSON)
    2. Auto-detect: data/demo/demo_questions.json for demo corpus
    3. Fallback: DEFAULT_QUESTIONS (sec_10k hardcoded set)
    """
    # AIStudio_618b (v2.0.11): stem expansion — try multiple filename patterns.
    # Allows short stems: --questions basic → esef_banks_lang_en_basic_questions.yaml
    # Resolution order (first match wins):
    #   1. {corpus}_{scope}_{stem}_questions.yaml  — scoped shorthand (future --scope support)
    #   2. {corpus}_{stem}_questions.yaml          — corpus-prefixed shorthand
    #   3. {stem}_questions.yaml                   — bare stem with _questions suffix
    #   4. {stem}.yaml                             — literal (legacy, full filename stem)
    if path is not None and "/" not in path and "\\" not in path and "." not in path:
        script_dir_stem = Path(__file__).parent
        _scope = scope
        candidates = []
        if _scope:
            candidates.append(script_dir_stem / corpus / f"{corpus}_{_scope}_{path}_questions.yaml")
        candidates += [
            script_dir_stem / corpus / f"{corpus}_{path}_questions.yaml",
            script_dir_stem / corpus / f"{path}_questions.yaml",
            script_dir_stem / corpus / f"{path}.yaml",
        ]
        matched = next((c for c in candidates if c.exists()), None)
        if matched:
            path = str(matched)
        else:
            tried = ", ".join(c.name for c in candidates)
            print(f"  ⚠ Questions stem '{path}' not found. Tried: {tried}")
            print("  · Using defaults")

    # Auto-detect corpus question file if no explicit path given
    # Priority: {corpus}_questions.yaml > {corpus}_questions.json > DEFAULT_QUESTIONS
    if path is None:
        script_dir = Path(__file__).parent
        repo_root = script_dir.parent
        # Search order: benchmarks/{corpus}/ first, then data/corpora/{corpus}/
        search_roots = [
            script_dir / corpus,  # benchmarks/{corpus}/
            repo_root / "data" / "corpora" / corpus,  # data/corpora/{corpus}/
        ]
        found = None
        for search_root in search_roots:
            for ext in (".yaml", ".yml", ".json"):
                candidate = search_root / f"{corpus}_questions{ext}"
                if candidate.exists():
                    found = candidate
                    break
            if found:
                break
        if found:
            path = str(found)
            pass  # path shown in header
        else:
            print(f"   No questions file found for corpus '{corpus}' — using defaults")
            return DEFAULT_QUESTIONS

    if path is None:
        return DEFAULT_QUESTIONS

    p = Path(path)
    if not p.exists():
        print(f"Questions file not found: {path} — using defaults")
        return DEFAULT_QUESTIONS

    questions = []
    with p.open() as f:
        content_str = f.read().strip()

    # Support YAML, JSON array, and JSONL formats
    if p.suffix.lower() in (".yaml", ".yml"):
        # YAML format: list of topic blocks with questions
        if not _YAML_AVAILABLE:
            print("   pyyaml not installed — pip install pyyaml")
            return DEFAULT_QUESTIONS
        raw = _yaml.safe_load(content_str)
        for topic_block in raw:
            topic = topic_block.get("topic", "General")
            for q in topic_block.get("questions", []):
                qid = q.get("id", q.get("question", "")[:40].lower().replace(" ", "_"))
                questions.append(
                    {
                        "id": qid,
                        "description": q.get("question", ""),
                        "query": q.get("question", ""),
                        "corpus": q.get("corpus", None),
                        "firm": q.get("firm", None),
                        "year": q.get("year", None),
                        "keywords": q.get("keywords", []),
                        "entity_filter": q.get("entity_filter", None),
                        "notes": q.get("notes", topic),
                        "topic": topic,
                        "language": q.get("language", "en"),
                        # v1.2 fields (optional, backward compatible)
                        "question_language": q.get("question_language", "en"),
                        "answer_location": q.get("answer_location", None),
                        "section_count": q.get("section_count", None),
                        "data_type": q.get("data_type", None),
                        "difficulty": q.get("difficulty", None),
                        "entity_count": q.get("entity_count", None),
                    }
                )
    elif content_str.startswith("["):
        # JSON array format: [{topic, questions: [...]}, ...]
        raw = json.loads(content_str)
        for topic_block in raw:
            topic = topic_block.get("topic", "General")
            for q in topic_block.get("questions", []):
                questions.append(
                    {
                        "id": q.lower().replace(" ", "_")[:40],
                        "description": q,
                        "query": q,
                        "corpus": None,
                        "firm": None,
                        "year": None,
                        "keywords": [],
                        "notes": topic,
                    }
                )
    else:
        # JSONL format: one question object per line
        for line in content_str.splitlines():
            line = line.strip()
            if line:
                questions.append(json.loads(line))

    pass  # count shown in header
    return questions


# ── Run single benchmark query ────────────────────────────────────────────────


def run_query(
    *,
    api: str,
    query: str,
    corpus: str,
    top_k: int,
    temperature: float,
    model: str | None,
    firm: str | None,
    year: str | None,
    hybrid_alpha: float | None = None,
    min_score: float | None = None,
    entity_filter: list[str] | None = None,
    keywords: list[str] | None = None,
) -> dict:
    import urllib.request

    payload: dict = {
        "query": query,
        "corpus": corpus,
        "top_k": top_k,
        "temperature": temperature,
    }
    if model:
        payload["model"] = model
    if firm:
        payload["firm"] = firm
    if year:
        payload["year"] = year
    if min_score is not None:
        payload["min_score"] = min_score
    if entity_filter:
        payload["entity_filter"] = entity_filter
    if hybrid_alpha is not None:
        payload["hybrid_alpha"] = hybrid_alpha
    if keywords:
        payload["keywords"] = keywords

    body = json.dumps(payload).encode()
    req = urllib.request.Request(
        f"{api}/ask",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    t0 = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            elapsed = time.perf_counter() - t0
            data = json.loads(resp.read())
            return {"ok": True, "elapsed_sec": round(elapsed, 2), "data": data}
    except Exception as e:
        elapsed = time.perf_counter() - t0
        return {"ok": False, "elapsed_sec": round(elapsed, 2), "error": str(e)}


# ── Evaluate result ───────────────────────────────────────────────────────────


# Refusal phrases — keywords found inside these do not count as substantive keyword hits.
# Expanded from observed benchmark failures where model says "no information about X"
# and X happens to be a required keyword — mechanically passing but substantively failing.
_REFUSAL_PHRASES = [
    "no information available",
    "no relevant information",
    "sources do not contain",
    "sources do not address",
    "cannot find any information",
    "not found in the provided",
    "no data available",
    "unfortunately, there is no",
    "no direct mention of",
    "the documents primarily discuss",
    "i cannot find specific information",
    "based on general knowledge",
    "based on my general knowledge",
    "is not mentioned in",
    "i do not see any information about",
    "there is no mention of",
    "purely speculative and not based on actual data",
    "the available sources do not",
    "absent from the available sources",
    "does not contain information about",
    "no sources provided",
    "not explicitly stated",
    "not explicitly mentioned",
    "the provided sources do not",
    "the sources do not provide",
    "based on the provided",
]


def _strip_refusal_context(answer: str) -> str:
    """
    Remove sentences containing refusal phrases from the answer before keyword
    checking. This prevents keywords that appear in 'no information about X'
    phrases from counting as substantive keyword hits.
    """
    sentences = answer.split(".")
    clean = []
    for sentence in sentences:
        if not any(phrase in sentence.lower() for phrase in _REFUSAL_PHRASES):
            clean.append(sentence)
    return ".".join(clean)


def _normalize_text(s: str) -> str:
    """
    Normalize text for keyword matching:
    - Strip accents (Société → Societe, Crédit → Credit)
    - Normalize hyphens (non-performing → non performing)
    - Lowercase
    Applied to both answer text and keywords before comparison.
    Prevents false negatives from accent/hyphen variants (AIStudio_828).
    """
    import unicodedata
    # Strip accents
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
    # Normalize hyphens to spaces
    s = s.replace("-", " ")
    return s.lower()


def evaluate(result: dict, expected_keywords: list[str],
             entity_filter: list[str] | None = None) -> dict:
    if not result["ok"]:
        return {
            "pass": False,
            "reason": f"Request failed: {result['error']}",
            "citation_count": 0,
            "citation_pass": False,
            "citation_density": 0.0,
            "low_citation_density": False,
            "no_info_signal": False,
            "missing_keywords": [],
            "cited_sources": [],
        }

    data = result["data"]
    answer = (data.get("answer") or "").lower()
    answer_normalized = _normalize_text(data.get("answer") or "")
    citations = data.get("citations") or []
    has_citations = data.get("has_citations", False)

    # AIStudio_796 fix (a): 0 citations always fails — no citation means either
    # hallucination or refusal. Never pass a 0-citation answer regardless of keywords.
    citation_pass = has_citations and len(citations) > 0

    # Check for no-information signal
    no_info_signal = any(phrase in answer_normalized for phrase in _REFUSAL_PHRASES)

    # AIStudio_796 fix (b): keyword check on substantive content only.
    # Strip sentences containing refusal phrases before checking keywords —
    # prevents "no information about JPMorgan" from counting as a JPMorgan keyword hit.
    # AIStudio_828: normalize accents + hyphens before comparison.
    substantive_normalized = _normalize_text(_strip_refusal_context(data.get("answer") or ""))
    missing = [kw for kw in expected_keywords if _normalize_text(kw) not in substantive_normalized]
    keyword_pass = len(missing) == 0

    # AIStudio_813: citation density = citations / answer sentences.
    answer_sentences = max(1, len([s for s in answer.split(".") if s.strip()]))
    citation_density = round(len(citations) / answer_sentences, 3)
    low_density = citation_density < 0.1 and answer_sentences > 3

    # AIStudio_813: entity coverage = fraction of entity_filter tokens that appear
    # in at least one cited source filename. Catches "passes on keyword but wrong firm cited".
    # entity_filter tokens are source_path substrings (e.g. "JPMorgan", "Citigroup").
    # cited_sources are bare filenames. Match: any token in any filename (case-insensitive).
    if entity_filter and citations:
        cited_fnames = " ".join(c.get("source", "").split("/")[-1] for c in citations).lower()
        covered = sum(1 for token in entity_filter if token.lower() in cited_fnames)
        entity_coverage = round(covered / len(entity_filter), 2)
        entities_missing = [t for t in entity_filter if t.lower() not in cited_fnames]
    else:
        entity_coverage = None
        entities_missing = []

    # AIStudio_796 fix (a): explicit 0-citation guard — belt and suspenders.
    if not citation_pass:
        return {
            "pass": False,
            "keyword_pass": keyword_pass,
            "citation_pass": False,
            "no_info_signal": no_info_signal,
            "missing_keywords": missing,
            "citation_count": 0,
            "citation_density": 0.0,
            "low_citation_density": False,
            "entity_coverage": entity_coverage,
            "entities_missing": entities_missing,
            "cited_sources": [],
        }

    # AIStudio_796 fix (c): no_info_signal only penalizes when citations are absent.
    # When the model has citations it found substantive content — hedging about
    # missing firms ("sources do not address Wells Fargo") is honest partial coverage,
    # not a failure. Only fire no_info_signal as a hard fail when citation_count == 0.
    effective_no_info = no_info_signal and not citation_pass

    return {
        "pass": keyword_pass and citation_pass and not effective_no_info,
        "keyword_pass": keyword_pass,
        "citation_pass": citation_pass,
        "no_info_signal": effective_no_info,
        "missing_keywords": missing,
        "citation_count": len(citations),
        "citation_density": citation_density,
        "low_citation_density": low_density,
        "entity_coverage": entity_coverage,
        "entities_missing": entities_missing,
        "cited_sources": [c.get("source", "").split("/")[-1] for c in citations],
    }


# ── Write BENCHMARK_FINDINGS.md ───────────────────────────────────────────────


def write_markdown(results: list[dict], args: argparse.Namespace, output_path: Path) -> None:
    md_path = output_path.with_suffix(".md")
    passed = sum(1 for r in results if r["eval"]["pass"])
    total = len(results)
    avg_latency = sum(r["result"]["elapsed_sec"] for r in results if r["result"]["ok"]) / max(
        1, total
    )

    lines = [
        "# AIStudio — Benchmark Findings",
        f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*",
        "",
        "## Configuration",
        f"- **Corpus:** `{args.corpus}`",
        f"- **Base Top K:** {args.top_k} (effective K may be higher for multi-entity queries)",
        f"- **Temperature:** {args.temperature}",
        *([ f"- **Alpha:** {args.alpha}" ] if args.alpha is not None else []),
        *([ f"- **Min Score:** {args.min_score}" ] if args.min_score is not None else []),
        f"- **Model:** {args.model or 'API default'}",
        f"- **API:** {args.api}",
        "",
        "## Summary",
        f"- **Questions:** {total}",
        f"- **Passed:** {passed}/{total} ({round(100 * passed / total)}%)",
        f"- **Avg latency:** {round(avg_latency, 1)}s",
        "",
        "## Infrastructure",
        "- Vector store: Qdrant 1.17.0 (Apple Silicon, local)",
        "- Embedding model: nomic-embed-text (768 dimensions, cosine similarity)",
        "- Reranker: CrossEncoder ms-marco-MiniLM-L-6-v2",
        f"- Corpus: `{args.corpus}` (see corpus stats in UI)",
        "",
        "## Results",
        "",
        "| # | Description | Latency | Pass | Citations | Notes |",
        "|---|-------------|---------|------|-----------|-------|",
    ]

    for i, r in enumerate(results, 1):
        q = r["question"]
        ev = r["eval"]
        res = r["result"]
        status = "✅" if ev["pass"] else "❌"
        latency = f"{res['elapsed_sec']}s"
        cites = ", ".join(ev.get("cited_sources", []))[:40] or "—"
        _lang = q.get("language", "en")
        _lang_marker = " (*)" if _lang and _lang != "en" else ""
        _density_flag = " ⚠low-density" if ev.get("low_citation_density") else ""
        desc = q["description"] + _lang_marker
        lines.append(
            f"| {i} | {desc} | {latency} | {status} | {cites}{_density_flag} | {q.get('notes', '')} |"
        )

    lines += ["", "## Detailed Results", ""]

    for question_num, r in enumerate(results, 1):
        q = r["question"]
        ev = r["eval"]
        res = r["result"]
        _lang = q.get("language", "en")
        _lang_marker = " (*)" if _lang and _lang != "en" else ""
        lines += [
            "****",
            f"### {question_num}. {q['id']}{_lang_marker}",
            f"**Query:** {q['query']}",
            f"**Entity filter:** `{q.get('entity_filter') or 'none'}` | **Keywords sent:** `{q.get('keywords') or 'none'}`",
            f"**Retrieval query:** {res['data'].get('retrieval_query', q['query']) if res['ok'] else q['query']}",
            f"**Model:** `{res['data'].get('model_used', 'unknown') if res['ok'] else 'unknown'}` | **Latency:** {res['elapsed_sec']}s | **Pass:** {'✅' if ev['pass'] else '❌'} | **Citation density:** {ev.get('citation_density', '—')}{'  ⚠ low' if ev.get('low_citation_density') else ''}",
            "",
        ]
        if res["ok"]:
            answer = res["data"].get("answer", "")
            if args.full:
                display_answer = answer
            else:
                paragraphs = [p.strip() for p in answer.split("\n\n") if p.strip()]
                display_answer = "\n\n".join(paragraphs[:4])
                if len(paragraphs) > 4:
                    display_answer += "\n\n*[truncated — use --full for complete answer]*"
            lines += ["**Answer:**", ""]
            for line in display_answer.split("\n"):
                lines.append(f"> {line}" if line.strip() else ">")
            lines.append("")
        if res["ok"] and res["data"].get("citations"):
            lines += ["**Citations:**", ""]
            for c in res["data"].get("citations") or []:
                src = c.get("source", "").split("/")[-1]
                page = f" p.{c['page']}" if c.get("page") else ""
                lines.append(f"- [{c.get('index', '?')}] {src}{page}")
            lines.append("")
        if ev.get("missing_keywords"):
            lines.append(f"**Missing keywords:** {ev['missing_keywords']}")
        if ev.get("no_info_signal"):
            lines.append("**⚠ Model said 'no information' — possible retrieval miss**")
        if ev.get("low_citation_density"):
            lines.append(f"**⚠ Low citation density:** {ev['citation_density']} (correct answer, sparse attribution)")
        if ev.get("entity_coverage") is not None and ev["entity_coverage"] < 1.0:
            lines.append(f"**⚠ Entity coverage:** {ev['entity_coverage']} — uncited firms: {', '.join(ev.get('entities_missing', []))}")
        lines.append("")

    with open(md_path, "w") as f:
        f.write("\n".join(lines))
    print(f"  · {md_path.name}")


# ── Question filtering ────────────────────────────────────────────────────────


def filter_questions(
    questions: list[dict],
    *,
    subset: str | None,
    topics: str | None,
    question_ids: str | None,
    lang: list[str] | None,
) -> tuple[list[dict], list[str]]:
    """Filter questions by subset, topics, question IDs, and/or language codes.

    All filters compose with AND. Returns (filtered_questions, applied_filter_descriptions).
    """
    applied: list[str] = []
    filtered = list(questions)

    # Filter by question IDs (most specific — apply first)
    if question_ids:
        wanted_ids = {qid.strip() for qid in question_ids.split(",") if qid.strip()}
        filtered = [q for q in filtered if q.get("id") in wanted_ids]
        applied.append(f"--question-ids ({len(wanted_ids)} IDs)")

    # Filter by language codes — questions without language field default to 'en'
    if lang:
        wanted_langs = {lc.strip().lower() for lc in lang if lc.strip()}
        filtered = [
            q for q in filtered
            if (q.get("language") or "en").lower() in wanted_langs
        ]
        applied.append(f"--lang {' '.join(sorted(wanted_langs))}")

    # Filter by topics
    if topics:
        wanted_topics = {t.strip().lower() for t in topics.split(",") if t.strip()}
        filtered = [
            q for q in filtered
            if (q.get("topic", "") or q.get("notes", "")).lower() in wanted_topics
            or any(t in (q.get("topic", "") or q.get("notes", "")).lower() for t in wanted_topics)
        ]
        applied.append(f"--topics ({len(wanted_topics)} topics)")

    # Filter by firm subset
    if subset:
        firms_in_subset = FIRM_SUBSETS.get(subset, [])
        firms_lower = [f.lower() for f in firms_in_subset]
        filtered = [
            q for q in filtered
            if any(firm in (q.get("query") or q.get("question") or "").lower() for firm in firms_lower)
        ]
        applied.append(f"--subset {subset} ({len(firms_in_subset)} firm patterns)")

    return filtered, applied


# ── Main ──────────────────────────────────────────────────────────────────────





def main() -> None:
    args = parse_args()
    print(f"\033[1m[ais_bench v{VERSION} — AIStudio RAG Benchmark]\033[0m")

    # ── Fetch corpus metadata defaults ───────────────────────────────────────
    # Apply corpus metadata defaults for params not explicitly set via CLI.
    # CLI flag → corpus metadata default → hardcoded fallback.
    try:
        import urllib.request
        info_url = f"{args.api}/corpus/{args.corpus}/info"
        with urllib.request.urlopen(info_url, timeout=5) as resp:
            _info = __import__("json").loads(resp.read())
        _corpus_top_k = _info.get("default_top_k")
        _corpus_temp  = _info.get("default_temperature")
        _corpus_alpha = _info.get("default_hybrid_alpha")
        _corpus_min   = _info.get("default_min_score")
    except Exception:
        _corpus_top_k = _corpus_temp = _corpus_alpha = _corpus_min = None

    if args.top_k is None:
        args.top_k = _corpus_top_k if _corpus_top_k is not None else 5
    if args.temperature is None:
        args.temperature = _corpus_temp if _corpus_temp is not None else 0.3
    if args.alpha is None and _corpus_alpha is not None:
        args.alpha = _corpus_alpha
    if args.min_score is None and _corpus_min is not None:
        args.min_score = _corpus_min

    # Resolve paths — output to benchmarks/{corpus}/reports/ with timestamp
    script_dir = Path(__file__).parent
    reports_dir = script_dir / args.corpus / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    # STD - General - Naming Conventions: time component is HHMM (no hyphen)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")

    # Model slug for filename — shorten to filesystem-safe form
    # e.g. "gemma3:27b" → "gemma3-27b", "llama3.1:8b" → "llama3.1-8b", None → "default"
    _model_raw = args.model or "default"
    _model_slug = _model_raw.replace(":", "-").replace("/", "-")[:20]

    # Build filter suffix for filename so subset/lang runs are distinguishable
    filter_parts = []
    if args.subset:
        filter_parts.append(args.subset)
    if args.topics:
        first_topic = args.topics.split(",")[0].strip().lower().replace(" ", "_").replace("&", "and")[:20]
        filter_parts.append(f"topics_{first_topic}")
    if args.question_ids:
        filter_parts.append("subset")
    if args.scope:
        filter_parts.append(args.scope)
    if args.lang:
        filter_parts.append("lang_" + "_".join(sorted(args.lang)))
    filter_suffix = ("_" + "_".join(filter_parts)) if filter_parts else ""

    base_name = f"benchmark_{args.corpus}_{_model_slug}_{timestamp}{filter_suffix}"
    output_path = reports_dir / f"{base_name}.json"
    questions_path = args.questions

    # Preflight header printed by ais_bench.sh shell wrapper

    questions = load_questions(questions_path, corpus=args.corpus, scope=args.scope)
    questions_label = (
        str(questions_path)
        if questions_path
        else f"benchmarks/{args.corpus}/{args.corpus}_questions.yaml"
    )
    total_loaded = len(questions)

    # Apply filters
    if args.subset or args.topics or args.question_ids or args.lang:
        questions, applied_filters = filter_questions(
            questions,
            subset=args.subset,
            topics=args.topics,
            question_ids=args.question_ids,
            lang=args.lang,
        )
        if not questions:
            print(f"❌ No questions matched filters: {', '.join(applied_filters)}")
            print(f"   Loaded {total_loaded} from {questions_label}, filtered to 0.")
            return
        print(
            f"✅ Questions loaded: {len(questions)}/{total_loaded} after filters "
            f"({', '.join(applied_filters)}) from {questions_label}"
        )
    else:
        print(f"✅ Questions loaded: {len(questions)} ({questions_label})")

    model_label = args.model if args.model else "API default (llama3.1:8b)"
    _alpha_label = f"  |  Alpha: {args.alpha}" if args.alpha is not None else ""
    _min_label   = f"  |  Min Score: {args.min_score}" if args.min_score is not None else ""
    print(
        f"· Corpus: {args.corpus}  |  Top K: {args.top_k}  |  Temperature: {args.temperature}"
        f"{_alpha_label}{_min_label}  |  Model: {model_label}"
    )

    # --- Firm override message
    if args.firm:
        print(f"· --firm '{args.firm}' active — applied to all queries (overriding YAML firm fields)")

    # --- Running
    _sep("Running")

    results = []
    for i, q in enumerate(questions, 1):
        corpus = q.get("corpus") or args.corpus
        # CLI --firm overrides per-question firm field; otherwise use YAML's firm
        effective_firm = args.firm if args.firm else q.get("firm")
        print(f"▶ [{i}/{len(questions)}] {q['description']}...")

        result = run_query(
            api=args.api,
            query=q.get("query") or q.get("question", ""),
            corpus=corpus,
            top_k=args.top_k,
            temperature=args.temperature,
            model=args.model,
            firm=effective_firm,
            year=q.get("year"),
            hybrid_alpha=args.alpha,
            min_score=args.min_score,
            entity_filter=q.get("entity_filter") or None,
            keywords=q.get("keywords") or None,
        )

        ev = evaluate(result, q.get("expected_keywords", []) or q.get("keywords", []),
                      entity_filter=q.get("entity_filter") or None)
        status = "✅" if ev["pass"] else "❌"
        _lang = q.get("language", "en")
        _lang_marker = " (*)" if _lang and _lang != "en" else ""
        _missing_str = f" | missing: {', '.join(ev['missing_keywords'])}" if ev.get("missing_keywords") else ""
        _density_str = f" | density: {ev['citation_density']}⚠" if ev.get("low_citation_density") else ""
        print(
            f"  {status} {result['elapsed_sec']}s | {ev['citation_count']} citation(s){_missing_str}{_density_str}{_lang_marker}"
        )

        # AIStudio_841: --verbose and --super-verbose output
        _verbose = getattr(args, 'verbose', False) or getattr(args, 'super_verbose', False)
        _super = getattr(args, 'super_verbose', False)
        if _verbose and result["ok"]:
            _data = result["data"]
            _ef = q.get("entity_filter") or []
            _chunks = _data.get("chunks_retrieved", "?")
            _first_src = ""
            if (_data.get("citations") or []):
                _first_src = (_data["citations"][0].get("source") or "").split("/")[-1]
            _diff = q.get("difficulty") or ""
            _aloc = q.get("answer_location") or ""
            _meta = f" | difficulty: {_diff}" if _diff else ""
            _meta += f" | answer_loc: {_aloc}" if _aloc else ""
            print(f"    · chunks_retrieved: {_chunks} | entity_filter: {_ef or 'none'} | first_source: {_first_src or 'none'}{_meta}")
        if _super and result["ok"]:
            _data = result["data"]
            _rq = _data.get("retrieval_query") or q.get("query", "")
            _model = _data.get("model_used", "?")
            _kw = q.get("keywords") or []
            _ef = q.get("entity_filter") or []
            print(f"    · original_query:   {q.get('query', '')[:100]}")
            print(f"    · retrieval_query:  {_rq[:100]}")
            print(f"    · entity_tokens:    {_ef}")
            print(f"    · keywords_sent:    {_kw}")
            print(f"    · model_used:       {_model}")
            _ans = (_data.get("answer") or "").strip()
            print(f"    · answer:           {_ans[:200]}{'...' if len(_ans) > 200 else ''}")

        results.append({"question": q, "result": result, "eval": ev})

    # Summary
    passed = sum(1 for r in results if r["eval"]["pass"])
    total = len(results)
    avg_latency = sum(r["result"]["elapsed_sec"] for r in results if r["result"]["ok"]) / max(
        1, total
    )

    _sep("Summary")
    print(f"· {passed}/{total} passed | avg latency: {round(avg_latency, 1)}s")
    for r in results:
        status = "✅" if r["eval"]["pass"] else "❌"
        _lang = r["question"].get("language", "en")
        _lang_marker = " (*)" if _lang and _lang != "en" else ""
        print(f"  {status} {r['question']['id']}{_lang_marker}")
        if r["eval"].get("no_info_signal"):
            print(
                f"  ⚠ {r['question']['id']}: model said 'no information' — possible retrieval miss."
            )
        if r["eval"].get("low_citation_density"):
            print(
                f"  ⚠ {r['question']['id']}: low citation density ({r['eval']['citation_density']}) — correct answer, sparse attribution."
            )
        if r["eval"].get("entity_coverage") is not None and r["eval"]["entity_coverage"] < 1.0:
            missing_e = r["eval"].get("entities_missing", [])
            print(
                f"  ⚠ {r['question']['id']}: entity coverage {r['eval']['entity_coverage']} — uncited: {', '.join(missing_e)}"
            )

    # Write JSON results
    with open(output_path, "w") as f:
        json.dump(
            {
                "run_at": datetime.now().isoformat(),
                "config": {
                    "corpus": args.corpus,
                    "top_k": args.top_k,
                    "temperature": args.temperature,
                    "model": args.model,
                    "api": args.api,
                },
                "summary": {
                    "total": total,
                    "passed": passed,
                    "avg_latency_sec": round(avg_latency, 2),
                },
                "results": results,
            },
            f,
            indent=2,
        )

    # Write markdown
    if not args.no_markdown:
        write_markdown(results, args, output_path)

    # Write PDF via pandoc (always attempted)
    if args.no_markdown:
        write_markdown(results, args, output_path)
    md_path = output_path.with_suffix(".md")
    pdf_path = output_path.with_suffix(".pdf")
    html_path = output_path.with_suffix(".html")
    import subprocess

    try:
        r1 = subprocess.run(
            ["pandoc", str(md_path), "-o", str(html_path), "--standalone"],
            capture_output=True,
            text=True,
        )
        if r1.returncode != 0:
            print(f"  ⚠ PDF skipped: pandoc error: {r1.stderr.strip()[:80]}")
        else:
            import os
            import sys
            import tempfile

            script = f"""
from weasyprint import HTML
HTML(filename={str(html_path)!r}).write_pdf({str(pdf_path)!r})
"""
            with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as tmp:
                tmp.write(script)
                tmp_name = tmp.name
            r2 = subprocess.run([sys.executable, tmp_name], capture_output=True, text=True)
            os.unlink(tmp_name)
            if html_path.exists():
                html_path.unlink()
            if r2.returncode != 0:
                print(
                    "  ⚠ PDF skipped — install weasyprint: pip3 install weasyprint --break-system-packages"
                )
    except FileNotFoundError:
        print("  ⚠ PDF skipped — install pandoc: brew install pandoc")

    # Bundle reports as zip for upload + audit workflow (AIStudio_829)
    # zip contains: json + md + pdf (if exists). Copied to ~/Downloads/.
    import zipfile as _zipfile

    downloads = Path.home() / "Downloads"
    downloads.mkdir(exist_ok=True)
    zip_name = f"{base_name}.zip"
    zip_dest = downloads / zip_name

    _files_to_zip = [f for f in [output_path, md_path, pdf_path] if f.exists()]
    with _zipfile.ZipFile(zip_dest, "w", _zipfile.ZIP_DEFLATED) as zf:
        for fpath in _files_to_zip:
            zf.write(fpath, fpath.name)

    print(f"\n· Reports written to {reports_dir}/")
    print(f"  · {output_path.name}")
    if md_path.exists():
        print(f"  · {md_path.name}")
    if pdf_path.exists():
        print(f"  · {pdf_path.name}")
    print(f"  · Bundled: ~/Downloads/{zip_name} ({len(_files_to_zip)} files)")
    print("  · Upload zip and say 'audit that report' for qualitative review")


if __name__ == "__main__":
    main()
