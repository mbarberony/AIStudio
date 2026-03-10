# Benchmark Harness

AIStudio ships with a benchmark harness (`run_demo.py`) that lets you run
a structured question set against any corpus and produce a timestamped
markdown report. It is designed for the demo corpus out of the box, but
works with any corpus and any question file you provide.

This document explains how to bring your own corpus and questions, how to
interpret reports, and what's coming next for cross-run comparison.

---

## Quick Start (Demo Corpus)

Make sure the backend is running, then from the repo root:

```bash
source .venv/bin/activate
python run_demo.py
```

This runs all 17 demo questions against the `demo` corpus using the default
model and writes a report to `data/demo/reports/`.

To re-ingest the corpus first:

```bash
python run_demo.py --ingest
```

---

## CLI Reference

```
python run_demo.py [OPTIONS]

Options:
  --config FILE         Path to JSON config file (default: run_demo_config.json)
  --api-base URL        Backend URL (default: http://localhost:8000)
  --corpus NAME         Corpus to query (default: demo)
  --model NAME          Ollama model name (default: llama3.1:70b)
  --temperature FLOAT   Sampling temperature 0.0–1.0 (default: 0.3)
  --k INT               Chunks retrieved per query (default: 5)
  --questions FILE      Path to question file (default: data/demo/demo_questions.json)
  --report-dir DIR      Output directory for reports (default: data/demo/reports)
  --corpus-root DIR     Document root used when --ingest is set
  --ingest              Re-ingest corpus before running queries
  -h, --help            Show this help message
```

All options default to values in `run_demo_config.json`. CLI flags override
the config file for a single run without editing it.

---

## Bringing Your Own Corpus

### 1. Create and ingest your corpus

Create a corpus via the UI or API, ingest your documents:

```bash
PYTHONPATH=src python -m local_llm_bot.app.ingest \
  --corpus my_corpus \
  --root /path/to/my/documents
```

### 2. Write a question file

Create a JSON file following this structure:

```json
[
  {
    "topic": "Topic Name",
    "questions": [
      "First question?",
      "Second question?"
    ]
  },
  {
    "topic": "Another Topic",
    "questions": [
      "Third question?"
    ]
  }
]
```

Topics are used to group results in the report. You can have as many topics
and questions as you like.

### 3. Run against your corpus

```bash
python run_demo.py \
  --corpus my_corpus \
  --questions /path/to/my_questions.json \
  --report-dir /path/to/my/reports
```

Or create your own config file (e.g. `my_config.json`) and point to it:

```bash
python run_demo.py --config my_config.json
```

A config file has this shape (all fields optional — missing fields fall back
to built-in defaults):

```json
{
  "api_base": "http://localhost:8000",
  "corpus": "my_corpus",
  "model": "llama3.1:70b",
  "temperature": 0.3,
  "k": 5,
  "question_file": "data/my_corpus/my_questions.json",
  "report_dir": "data/my_corpus/reports",
  "corpus_root": "data/my_corpus/documents",
  "ingest": false
}
```

---

## Running Benchmarks

The harness is designed for systematic benchmarking — varying model, chunking
strategy, temperature, or retrieval depth across runs.

### Compare models

```bash
python run_demo.py --model llama3.2:3b   --report-dir data/demo/reports
python run_demo.py --model llama3.1:70b  --report-dir data/demo/reports
python run_demo.py --model mistral:7b    --report-dir data/demo/reports
```

Each run produces a separate timestamped report named after the model:
```
reports/report_2026-03-10_14-00_llama3.2-3b.md
reports/report_2026-03-10_14-12_llama3.1-70b.md
reports/report_2026-03-10_14-45_mistral-7b.md
```

### Compare retrieval depth

```bash
python run_demo.py --k 3
python run_demo.py --k 5
python run_demo.py --k 10
```

### Compare temperature

```bash
python run_demo.py --temperature 0.0
python run_demo.py --temperature 0.3
python run_demo.py --temperature 0.7
```

---

## Reading a Report

Each report contains:

**Header** — full config snapshot (model, corpus, temperature, k, timestamp)
so every report is self-describing and reproducible.

**Summary table** — total questions, success/error counts, total runtime,
avg/min/max latency.

**Results by topic** — for each question: the answer, sources with document
names and chunk indices, and latency in seconds.

The first query in a session is typically slow (20–50s) because the LLM
loads into memory. Subsequent queries are faster (5–15s). This is reflected
in the min/max latency in the summary.

---

## What's Coming

Cross-run comparison and programmatic analysis are on the roadmap for v1.0:

- **JSON report output** — machine-readable companion to the markdown report,
  enabling automated comparison across runs
- **Compare script** — `compare_runs.py` to diff two or more reports on
  latency, answer length, source overlap, and topic-level performance
- **Benchmark dashboard** — visual summary across all runs for a given corpus

See `docs/roadmap.md` for the full roadmap.

---

## Notes

- Reports are written to `data/demo/reports/` by default, which is gitignored.
  Commit reports you want to preserve by moving them to `docs/` or similar.
- The harness calls the `/query` endpoint directly. Make sure the backend
  is running before starting a run (`uvicorn` in a separate terminal).
- Timeout per query is 300 seconds. For very large models or long documents
  this may need to be increased in `run_demo.py`.
