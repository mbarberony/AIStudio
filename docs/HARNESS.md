# Benchmark Harness

AIStudio ships with a benchmark harness (`benchmarks/benchmark.py`) that runs a structured question set against any corpus and produces timestamped reports. It is designed for the demo corpus out of the box but works with any corpus and any YAML question file you provide.

Reports are written to `benchmarks/reports/` as paired `.md` and `.json` files, named by corpus and timestamp.

---

## Quick Start (Demo Corpus)

Make sure the backend is running, then from the repo root:

```bash
source .venv/bin/activate
python benchmarks/benchmark.py --corpus demo --top-k 5 --temperature 0.3
```

This runs all 12 demo questions against the `demo` corpus and writes a timestamped report to `benchmarks/reports/`.

---

## CLI Reference

```
python benchmarks/benchmark.py [OPTIONS]

Options:
  --corpus NAME         Corpus to query (default: demo)
  --top-k INT           Chunks retrieved per query (default: 5)
  --temperature FLOAT   LLM sampling temperature 0.0–2.0 (default: 0.3)
  --model NAME          Ollama model name (default: API default)
  --questions FILE      Path to YAML question file (auto-detected from corpus name if omitted)
  --api URL             Backend URL (default: http://localhost:8000)
  --no-markdown         Skip writing .md report
  --full                Include full answers in report (default: first 4 paragraphs)
  -h, --help            Show this help message
```

Question files are auto-detected: for `--corpus demo`, the harness looks for
`benchmarks/demo_questions.yaml` automatically. For custom corpora, pass `--questions`.

---

## Question File Format

Questions are YAML files organized by topic. Each question has an `id`, a `question` string, optional `keywords` for retrieval hints, and optional `notes`:

```yaml
- topic: Architecture Methodology
  questions:
    - id: my_first_question
      question: What is the relationship between business strategy and technology strategy?
      keywords: [business, strategy, technology]
      notes: Core intellectual thread — business strategy drives technology strategy.

    - id: my_second_question
      question: How do you design an IT organization around architectural principles?
      keywords: [organization, architecture, principles]
```

Place question files in `benchmarks/` named `{corpus}_questions.yaml` for auto-detection.

---

## Bringing Your Own Corpus

### 1. Create and ingest your corpus

Create a corpus via the UI, then ingest your documents:

```bash
AISTUDIO_VECTORSTORE=qdrant PYTHONPATH=src python -m local_llm_bot.app.ingest \
  --corpus my_corpus \
  --root data/corpora/my_corpus/uploads
```

### 2. Write a question file

Create `benchmarks/my_corpus_questions.yaml` following the format above.

### 3. Run the benchmark

```bash
python benchmarks/benchmark.py --corpus my_corpus --top-k 5 --temperature 0.3
```

---

## Running Systematic Benchmarks

### Compare models

```bash
python benchmarks/benchmark.py --corpus demo --top-k 5 --temperature 0.3 --model llama3.1:8b
python benchmarks/benchmark.py --corpus demo --top-k 5 --temperature 0.3 --model llama3.1:70b
python benchmarks/benchmark.py --corpus demo --top-k 5 --temperature 0.3 --model mistral:7b
```

### Compare retrieval depth

```bash
python benchmarks/benchmark.py --corpus demo --top-k 3
python benchmarks/benchmark.py --corpus demo --top-k 5
python benchmarks/benchmark.py --corpus demo --top-k 10
```

### Compare temperature

```bash
python benchmarks/benchmark.py --corpus demo --temperature 0.0
python benchmarks/benchmark.py --corpus demo --temperature 0.3
python benchmarks/benchmark.py --corpus demo --temperature 0.7
```

Each run produces a separate timestamped report in `benchmarks/reports/`:
```
benchmarks/reports/benchmark_demo_2026-03-19_23-50.md
benchmarks/reports/benchmark_demo_2026-03-19_23-50.json
```

---

## Reading a Report

Each report contains:

**Configuration** — full snapshot (corpus, model, top-k, temperature, timestamp) so every report is self-describing and reproducible.

**Summary** — total questions, pass rate, average latency.

**Infrastructure** — vector store, embedding model, reranker, corpus stats.

**Results table** — per question: latency, pass/fail, citation sources, notes.

**Detailed results** — full answer text with inline citations, per question.

**Known limitations** — retrieval quality notes, corpus-specific issues.

The first query in a cold session is slow (20–50s) while the LLM loads into memory. Subsequent queries run at ~6–7s warm on Apple Silicon. The benchmark summary reflects warm latency once the first query completes.

---

## SEC 10-K Corpus

To benchmark against the full 143-filing SEC corpus:

```bash
python benchmarks/benchmark.py --corpus sec_10k --top-k 10 --temperature 0.3
```

The SEC corpus must be downloaded and ingested first — see QUICKSTART.md for instructions. Ingest takes ~34 minutes on M4 Max.

---

## What's Coming

- **Cross-run comparison** — diff two reports on latency, answer quality, source overlap
- **Hardware metadata** — machine specs recorded in report header for M4 Air vs M4 Max comparisons
- **Model quality evaluation** — human eval framework for 8b vs 70b answer quality (latency is already characterized)

See `docs/roadmap.md` for the full roadmap.
