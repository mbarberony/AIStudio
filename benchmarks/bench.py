#!/usr/bin/env python3
# Version: 1.8.1
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
    p.add_argument("--top-k", type=int, default=5, help="Top K chunks to retrieve")
    p.add_argument("--temperature", type=float, default=0.3, help="LLM temperature")
    p.add_argument("--model", default=None, help="Model ID (default: API default)")
    p.add_argument("--questions", default=None, help="Path to questions YAML/JSONL file")
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
        help="Hybrid retrieval alpha: 0.0=pure vector, 1.0=pure BM25. None=backend default.",
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


def load_questions(path: str | None, corpus: str = "sec_10k") -> list[dict]:
    """
    Load benchmark questions from a file or auto-detect based on corpus name.

    Priority:
    1. Explicit --questions path (JSONL or JSON)
    2. Auto-detect: data/demo/demo_questions.json for demo corpus
    3. Fallback: DEFAULT_QUESTIONS (sec_10k hardcoded set)
    """
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
                        "notes": q.get("notes", topic),
                        "topic": topic,
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
    if hybrid_alpha is not None:
        payload["hybrid_alpha"] = hybrid_alpha

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


def evaluate(result: dict, expected_keywords: list[str]) -> dict:
    if not result["ok"]:
        return {"pass": False, "reason": f"Request failed: {result['error']}"}

    data = result["data"]
    answer = (data.get("answer") or "").lower()
    citations = data.get("citations") or []
    has_citations = data.get("has_citations", False)

    # Check expected keywords
    missing = [kw for kw in expected_keywords if kw.lower() not in answer]
    keyword_pass = len(missing) == 0

    # Check citation quality
    citation_pass = has_citations and len(citations) > 0

    # Check for hallucination signal — model saying "no information" despite having sources
    no_info_signal = any(
        phrase in answer.lower()
        for phrase in [
            "no information available",
            "no relevant information",
            "sources do not contain",
            "sources do not address",
            "cannot find any information",
            "not found in the provided",
            "no data available",
            # Additional patterns observed in cross-firm bench runs:
            "unfortunately, there is no",
            "no direct mention of",
            "the documents primarily discuss",
            "i cannot find specific information",
            "based on general knowledge",  # model falling back to training data
            "based on my general knowledge",
            "is not mentioned in",
            "i do not see any information about",
            "there is no mention of",
            "purely speculative and not based on actual data",
        ]
    )

    return {
        "pass": keyword_pass and citation_pass and not no_info_signal,
        "keyword_pass": keyword_pass,
        "citation_pass": citation_pass,
        "no_info_signal": no_info_signal,
        "missing_keywords": missing,
        "citation_count": len(citations),
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
        f"- **Top K:** {args.top_k}",
        f"- **Temperature:** {args.temperature}",
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
        lines.append(
            f"| {i} | {q['description']} | {latency} | {status} | {cites} | {q.get('notes', '')} |"
        )

    lines += ["", "## Detailed Results", ""]

    for question_num, r in enumerate(results, 1):
        q = r["question"]
        ev = r["eval"]
        res = r["result"]
        lines += [
            "****",
            f"### {question_num}. {q['id']}",
            f"**Query:** {q['query']}",
            f"**Firm filter:** `{q.get('firm') or 'none'}` | **Year filter:** `{q.get('year') or 'none'}`",
            f"**Latency:** {res['elapsed_sec']}s | **Pass:** {'✅' if ev['pass'] else '❌'}",
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
) -> tuple[list[dict], list[str]]:
    """Filter questions by subset, topics, and/or question IDs.

    All filters compose with AND. Returns (filtered_questions, applied_filter_descriptions).
    """
    applied: list[str] = []
    filtered = list(questions)

    # Filter by question IDs (most specific — apply first)
    if question_ids:
        wanted_ids = {qid.strip() for qid in question_ids.split(",") if qid.strip()}
        filtered = [q for q in filtered if q.get("id") in wanted_ids]
        applied.append(f"--question-ids ({len(wanted_ids)} IDs)")

    # Filter by topics — note: load_questions stores topic in the 'notes' field as fallback
    # Topics tracked separately by re-parsing if YAML structure available
    if topics:
        wanted_topics = {t.strip().lower() for t in topics.split(",") if t.strip()}
        # The notes field holds topic when no per-question notes is provided.
        # When per-question notes are provided, this filter is best-effort.
        # We match against any of: notes (which often = topic), or a stored 'topic' field.
        filtered = [
            q for q in filtered
            if (q.get("topic", "") or q.get("notes", "")).lower() in wanted_topics
            or any(t in (q.get("topic", "") or q.get("notes", "")).lower() for t in wanted_topics)
        ]
        applied.append(f"--topics ({len(wanted_topics)} topics)")

    # Filter by firm subset — match against firm names in question text
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

    # Resolve paths — output to benchmarks/{corpus}/reports/ with timestamp
    script_dir = Path(__file__).parent
    reports_dir = script_dir / args.corpus / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")

    # Build filter suffix for filename so subset runs are distinguishable
    filter_parts = []
    if args.subset:
        filter_parts.append(args.subset)
    if args.topics:
        # Slugify first topic word for filename
        first_topic = args.topics.split(",")[0].strip().lower().replace(" ", "_").replace("&", "and")[:20]
        filter_parts.append(f"topics_{first_topic}")
    if args.question_ids:
        filter_parts.append("subset")
    filter_suffix = ("_" + "_".join(filter_parts)) if filter_parts else ""

    base_name = f"benchmark_{args.corpus}_{timestamp}{filter_suffix}"
    output_path = reports_dir / f"{base_name}.json"
    questions_path = args.questions

    # Preflight header printed by ais_bench.sh shell wrapper

    questions = load_questions(questions_path, corpus=args.corpus)
    questions_label = (
        str(questions_path)
        if questions_path
        else f"benchmarks/{args.corpus}/{args.corpus}_questions.yaml"
    )
    total_loaded = len(questions)

    # Apply filters
    if args.subset or args.topics or args.question_ids:
        questions, applied_filters = filter_questions(
            questions,
            subset=args.subset,
            topics=args.topics,
            question_ids=args.question_ids,
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
    print(
        f"· Corpus: {args.corpus}  |  Top K: {args.top_k}  |  Temperature: {args.temperature}  |  Model: {model_label}"
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
        )

        ev = evaluate(result, q.get("expected_keywords", []))
        status = "✅" if ev["pass"] else "❌"
        missing = (
            f"missing: {', '.join(ev['missing_keywords'])}"
            if ev.get("missing_keywords")
            else "all keywords found"
        )
        print(
            f"  {status} {result['elapsed_sec']}s | {ev['citation_count']} citation(s) | {missing}."
        )

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
        print(f"  {status} {r['question']['id']}")
        if r["eval"].get("no_info_signal"):
            print(
                f"  ⚠ {r['question']['id']}: model said 'no information' — possible retrieval miss."
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

    print(f"\n· Reports written to {reports_dir}/")
    print(f"  · {output_path.name}")
    if not args.no_markdown:
        print(f"  · {md_path.name}")
    if pdf_path.exists():
        print(f"  · {pdf_path.name}")


if __name__ == "__main__":
    main()
