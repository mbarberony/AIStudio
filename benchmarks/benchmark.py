#!/usr/bin/env python3
"""
AIStudio RAG Benchmark Script
Usage:
    python3 scripts/benchmark.py
    python3 scripts/benchmark.py --corpus sec_10k --top-k 10 --temperature 0.3
    python3 scripts/benchmark.py --questions scripts/benchmark_questions.jsonl --output results/benchmark_out.json

Flags:
    --corpus        Corpus name to query (default: sec_10k)
    --top-k         Number of chunks to retrieve (default: 10)
    --temperature   LLM temperature (default: 0.3)
    --model         Model to use (default: from API config)
    --questions     Path to questions JSONL file (default: scripts/benchmark_questions.jsonl)
    --output        Path to write results JSON (default: scripts/benchmark_results.json)
    --api           API base URL (default: http://localhost:8000)
    --no-markdown   Skip writing .md report
    --full          Include full answers in report (default: first 4 paragraphs)
    --pdf           Generate PDF report (requires pandoc: brew install pandoc)

Output files (in benchmarks/reports/):
    benchmark_<corpus>_<timestamp>.json
    benchmark_<corpus>_<timestamp>.md
    benchmark_<corpus>_<timestamp>.pdf  (with --pdf)
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

# ── CLI ───────────────────────────────────────────────────────────────────────


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
        # Check data/corpora/{corpus}/ first, then data/{corpus}/
        search_roots = [
            script_dir,  # benchmarks/{corpus}_questions.yaml
            repo_root / "data" / "corpora" / corpus,  # data/corpora/{corpus}/
            repo_root / "data" / corpus,  # data/{corpus}/
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
        "- Note: SEC 10-K corpus = 143 filings, 105,964 chunks — ChromaDB crashed at 32,285; Qdrant stable at 105,964",
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

    for r in results:
        q = r["question"]
        ev = r["eval"]
        res = r["result"]
        lines += [
            f"### {q['id']}",
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

    lines += [
        "## Known Limitations",
        "- Cross-corpus semantic pollution: queries without firm filter may return non-target firm chunks",
        "- XBRL/structured data noise in HTML 10-K filings — BeautifulSoup parser needs XBRL stripping",
        "- Relevance threshold not yet implemented — low-scoring chunks included in context",
        "- Northern Trust / Nuveen CIK collision — duplicate filings in corpus",
        "- BNY Mellon CIK incorrect — old filings only",
        "",
        "## Roadmap",
        "- Metadata filtering UI (firm/year dropdown in query area)",
        "- Relevance threshold — discard chunks below similarity cutoff",
        "- XBRL stripping in HTML ingestion",
        "- Reranker pass (CrossEncoder ms-marco-MiniLM)",
        "- Embedding model eval: nomic-embed-text vs bge-large",
        "- PDF viewer with click-to-source citation",
    ]

    with open(md_path, "w") as f:
        f.write("\n".join(lines))
    print(f"  * {md_path.name}")


# ── Main ──────────────────────────────────────────────────────────────────────


def main() -> None:
    args = parse_args()

    # Resolve paths — output to benchmarks/reports/ with corpus+timestamp
    script_dir = Path(__file__).parent
    reports_dir = script_dir / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    base_name = f"benchmark_{args.corpus}_{timestamp}"
    output_path = reports_dir / f"{base_name}.json"
    questions_path = args.questions

    questions = load_questions(questions_path, corpus=args.corpus)

    model_label = args.model if args.model else "API default (llama3.1:8b)"
    questions_label = str(questions_path) if questions_path else "(built-in defaults)"
    print(f"\n{'=' * 50}")
    print("  AIStudio Benchmark")
    print(f"{'=' * 50}")
    print(f"   Corpus      : {args.corpus}")
    print(f"   Top K       : {args.top_k}")
    print(f"   Temperature : {args.temperature}")
    print(f"   Model       : {model_label}")
    print(f"   Questions   : {len(questions)} (loaded from {questions_label})")
    print()

    results = []
    for i, q in enumerate(questions, 1):
        corpus = q.get("corpus") or args.corpus
        print(f"[{i}/{len(questions)}] {q['description']}...")

        result = run_query(
            api=args.api,
            query=q.get("query") or q.get("question", ""),
            corpus=corpus,
            top_k=args.top_k,
            temperature=args.temperature,
            model=args.model,
            firm=q.get("firm"),
            year=q.get("year"),
        )

        ev = evaluate(result, q.get("expected_keywords", []))
        status = "✅" if ev["pass"] else "❌"
        print(
            f"   {status} {result['elapsed_sec']}s | citations: {ev['citation_count']} | {ev.get('missing_keywords') or 'all keywords found'}"
        )

        results.append(
            {
                "question": q,
                "result": result,
                "eval": ev,
            }
        )

    # Summary
    passed = sum(1 for r in results if r["eval"]["pass"])
    total = len(results)
    avg_latency = sum(r["result"]["elapsed_sec"] for r in results if r["result"]["ok"]) / max(
        1, total
    )

    print(f"\n{'=' * 50}")
    print(f"  Results: {passed}/{total} passed | avg latency: {round(avg_latency, 1)}s")
    print(f"{'=' * 50}")

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
    print(f"\n  Folder: {reports_dir}")
    print(f"  * {output_path.name}")

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
        # Step 1: md -> html (pandoc, no LaTeX needed)
        r1 = subprocess.run(
            ["pandoc", str(md_path), "-o", str(html_path), "--standalone"],
            capture_output=True,
            text=True,
        )
        if r1.returncode != 0:
            print(f"  * PDF skipped: pandoc error: {r1.stderr.strip()[:80]}")
        else:
            # Step 2: html -> pdf via weasyprint
            import os
            import sys
            import tempfile

            # Write a temp script to avoid quoting issues in -c argument
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
            if r2.returncode == 0:
                print(f"  * {pdf_path.name}")
            else:
                print("  * PDF skipped — install weasyprint:")
                print("    pip install weasyprint --break-system-packages")
    except FileNotFoundError:
        print("  * PDF skipped — install pandoc: brew install pandoc")
        print("    Install: brew install pandoc")


if __name__ == "__main__":
    main()
