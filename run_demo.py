#!/usr/bin/env python3
"""
run_demo.py — AIStudio Benchmark Harness

Runs a question file against a live AIStudio backend and produces a
timestamped markdown report with per-question responses, citations,
latency, and summary statistics.

Designed for the AIStudio demo corpus but works with any corpus and
question file. See docs/HARNESS.md for how to bring your own.

Usage
-----
  # Run with all defaults from run_demo_config.json
  python run_demo.py

  # Override model and k for a single run
  python run_demo.py --model llama3.2:3b --k 8

  # Re-ingest corpus before running
  python run_demo.py --ingest

  # Point at a different corpus and question file
  python run_demo.py --corpus my_corpus --questions data/my_questions.json

  # Full help
  python run_demo.py --help
"""

import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

import requests

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

DEFAULT_CONFIG_FILE = "run_demo_config.json"


def load_config(config_file: str) -> dict:
    path = Path(config_file)
    if not path.exists():
        print(f"[warn] Config file '{config_file}' not found — using built-in defaults.")
        return {}
    with open(path) as f:
        return json.load(f)


def build_config(args: argparse.Namespace) -> dict:
    """Merge config file defaults with CLI overrides. CLI always wins."""
    cfg = load_config(args.config)

    # CLI overrides
    overrides = {
        "api_base":     args.api_base,
        "corpus":       args.corpus,
        "model":        args.model,
        "temperature":  args.temperature,
        "k":            args.k,
        "question_file": args.questions,
        "report_dir":   args.report_dir,
        "corpus_root":  args.corpus_root,
        "ingest":       args.ingest,
    }

    for key, val in overrides.items():
        if val is not None:
            cfg[key] = val

    # Final defaults for anything still missing
    defaults = {
        "api_base":     "http://localhost:8000",
        "corpus":       "demo",
        "model":        "llama3.1:70b",
        "temperature":  0.3,
        "k":            5,
        "question_file": "data/demo/demo_questions.json",
        "report_dir":   "data/demo/reports",
        "corpus_root":  "data/demo/demo_data",
        "ingest":       False,
    }
    for key, val in defaults.items():
        cfg.setdefault(key, val)

    return cfg


# ---------------------------------------------------------------------------
# Ingest
# ---------------------------------------------------------------------------

def run_ingest(cfg: dict) -> None:
    print(f"\n[ingest] Ingesting corpus '{cfg['corpus']}' from '{cfg['corpus_root']}' ...")
    cmd = [
        sys.executable, "-m", "local_llm_bot.app.ingest",
        "--corpus", cfg["corpus"],
        "--root",   cfg["corpus_root"],
    ]
    env = {**os.environ, "PYTHONPATH": "src"}
    result = subprocess.run(cmd, env=env, capture_output=False, text=True)
    if result.returncode != 0:
        print("[error] Ingest failed — aborting.")
        sys.exit(1)
    print("[ingest] Done.\n")


# ---------------------------------------------------------------------------
# Query
# ---------------------------------------------------------------------------

def query(api_base: str, corpus: str, question: str, model: str,
          temperature: float, k: int) -> dict:
    """
    POST /ask and return a dict with:
      answer, sources, latency_sec, error (if any)
    """
    url = f"{api_base}/ask"
    payload = {
        "query":       question,
        "corpus":      corpus,
        "temperature": temperature,
        "top_k":       k,
    }

    start = time.time()
    try:
        resp = requests.post(url, json=payload, timeout=300)
        latency = time.time() - start
        resp.raise_for_status()
        data = resp.json()
        return {
            "answer":      data.get("answer", ""),
            "sources":     data.get("citations", []),
            "latency_sec": round(latency, 2),
            "error":       None,
        }
    except requests.exceptions.ConnectionError:
        return {
            "answer":      "",
            "sources":     [],
            "latency_sec": round(time.time() - start, 2),
            "error":       f"Connection refused — is the backend running at {api_base}?",
        }
    except Exception as e:
        return {
            "answer":      "",
            "sources":     [],
            "latency_sec": round(time.time() - start, 2),
            "error":       str(e),
        }


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------

def format_sources(sources: list) -> str:
    if not sources:
        return "_No sources returned._"
    lines = []
    for s in sources:
        idx = s.get("index", "?")
        doc = s.get("source", "unknown")
        page = s.get("page")
        score = s.get("score")
        page_str = f" p.{page}" if page else ""
        score_str = f" (score: {score:.3f})" if score else ""
        lines.append(f"- [{idx}] `{doc}`{page_str}{score_str}")
    return "\n".join(lines)


def build_report(cfg: dict, results: list, total_sec: float) -> str:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")

    latencies = [r["latency_sec"] for r in results if r["error"] is None]
    errors = [r for r in results if r["error"]]

    lines = []

    # Header
    lines += [
        "# AIStudio Benchmark Report",
        "",
        f"**Generated:** {ts}  ",
        f"**Corpus:** `{cfg['corpus']}`  ",
        f"**Model:** `{cfg['model']}`  ",
        f"**Temperature:** {cfg['temperature']}  ",
        f"**k (chunks retrieved):** {cfg['k']}  ",
        f"**Question file:** `{cfg['question_file']}`  ",
        "",
        "---",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "|---|---|",
        f"| Total questions | {len(results)} |",
        f"| Successful | {len(latencies)} |",
        f"| Errors | {len(errors)} |",
        f"| Total runtime | {round(total_sec, 1)}s |",
    ]

    if latencies:
        lines += [
            f"| Avg latency | {round(sum(latencies)/len(latencies), 1)}s |",
            f"| Min latency | {min(latencies)}s |",
            f"| Max latency | {max(latencies)}s |",
        ]

    lines += ["", "---", ""]

    # Results by topic
    current_topic = None
    for r in results:
        if r["topic"] != current_topic:
            current_topic = r["topic"]
            lines += [f"## {current_topic}", ""]

        lines += [
            f"### Q: {r['question']}",
            "",
            f"**Latency:** {r['latency_sec']}s  ",
            "",
        ]

        if r["error"]:
            lines += [f"**Error:** {r['error']}", ""]
        else:
            lines += [
                "**Answer:**",
                "",
                r["answer"].strip(),
                "",
                "**Sources:**",
                "",
                format_sources(r["sources"]),
                "",
            ]

        lines.append("---")
        lines.append("")

    return "\n".join(lines)


def write_report(cfg: dict, report_text: str) -> Path:
    report_dir = Path(cfg["report_dir"])
    report_dir.mkdir(parents=True, exist_ok=True)

    ts = datetime.now().strftime("%Y-%m-%d_%H-%M")
    model_slug = cfg["model"].replace(":", "-").replace("/", "-")  # noqa: F841
    filename = f"report_{ts}_{model_slug}.md"
    path = report_dir / filename

    with open(path, "w") as f:
        f.write(report_text)

    return path


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="run_demo.py",
        description=(
            "AIStudio Benchmark Harness — runs a question file against a live "
            "AIStudio backend and produces a timestamped markdown report.\n\n"
            "All options default to values in run_demo_config.json. "
            "CLI flags override the config file for a single run."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python run_demo.py\n"
            "  python run_demo.py --model llama3.2:3b --k 8\n"
            "  python run_demo.py --ingest\n"
            "  python run_demo.py --corpus my_corpus --questions data/my_questions.json\n"
            "  python run_demo.py --model llama3.1:70b --temperature 0.5 --report-dir /tmp/reports\n"
        ),
    )

    parser.add_argument(
        "--config",
        default=DEFAULT_CONFIG_FILE,
        metavar="FILE",
        help=f"Path to JSON config file (default: {DEFAULT_CONFIG_FILE})",
    )
    parser.add_argument(
        "--api-base",
        default=None,
        metavar="URL",
        help="Base URL of the AIStudio backend (default: http://localhost:8000)",
    )
    parser.add_argument(
        "--corpus",
        default=None,
        metavar="NAME",
        help="Corpus name to query (default: demo)",
    )
    parser.add_argument(
        "--model",
        default=None,
        metavar="NAME",
        help="LLM model name as recognised by Ollama (default: llama3.1:70b)",
    )
    parser.add_argument(
        "--temperature",
        default=None,
        type=float,
        metavar="FLOAT",
        help="Sampling temperature 0.0–1.0 (default: 0.3)",
    )
    parser.add_argument(
        "--k",
        default=None,
        type=int,
        metavar="INT",
        help="Number of chunks to retrieve per query (default: 5)",
    )
    parser.add_argument(
        "--questions",
        default=None,
        metavar="FILE",
        help="Path to JSON question file (default: data/demo/demo_questions.json)",
    )
    parser.add_argument(
        "--report-dir",
        default=None,
        metavar="DIR",
        help="Directory for report output (default: data/demo/reports)",
    )
    parser.add_argument(
        "--corpus-root",
        default=None,
        metavar="DIR",
        help="Corpus document root used when --ingest is set (default: data/demo/demo_data)",
    )
    parser.add_argument(
        "--ingest",
        action="store_true",
        default=None,
        help="Re-ingest the corpus before running queries",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()
    cfg = build_config(args)

    print("=" * 60)
    print("AIStudio Benchmark Harness")
    print("=" * 60)
    print(f"  corpus      : {cfg['corpus']}")
    print(f"  model       : {cfg['model']}")
    print(f"  temperature : {cfg['temperature']}")
    print(f"  k           : {cfg['k']}")
    print(f"  questions   : {cfg['question_file']}")
    print(f"  report dir  : {cfg['report_dir']}")
    print(f"  api base    : {cfg['api_base']}")
    print("=" * 60)

    # Optionally re-ingest
    if cfg.get("ingest"):
        run_ingest(cfg)

    # Load questions
    qfile = Path(cfg["question_file"])
    if not qfile.exists():
        print(f"[error] Question file not found: {qfile}")
        sys.exit(1)

    with open(qfile) as f:
        topics = json.load(f)

    total_questions = sum(len(t["questions"]) for t in topics)
    print(f"\nRunning {total_questions} questions across {len(topics)} topics...\n")

    # Run queries
    results = []
    overall_start = time.time()
    q_num = 0

    for topic in topics:
        topic_name = topic["topic"]
        for question in topic["questions"]:
            q_num += 1
            print(f"[{q_num}/{total_questions}] {topic_name}: {question[:70]}...")
            result = query(
                api_base=cfg["api_base"],
                corpus=cfg["corpus"],
                question=question,
                model=cfg["model"],
                temperature=cfg["temperature"],
                k=cfg["k"],
            )
            result["topic"] = topic_name
            result["question"] = question
            results.append(result)

            status = f"✓ {result['latency_sec']}s" if not result["error"] else f"✗ {result['error']}"
            print(f"    {status}")

    total_sec = time.time() - overall_start

    # Build and write report
    print(f"\nAll questions complete. Total time: {round(total_sec, 1)}s")
    report_text = build_report(cfg, results, total_sec)
    report_path = write_report(cfg, report_text)
    print(f"\nReport written to: {report_path}")


if __name__ == "__main__":
    main()
