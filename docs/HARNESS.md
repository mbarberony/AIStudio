# Benchmark Harness

AIStudio ships with a benchmark harness (`benchmarks/bench.py`) that runs a structured question set against any corpus and produces timestamped reports. It is designed for the demo corpus out of the box but works with any corpus and any YAML question file you provide.

Reports are written to `benchmarks/<corpus>/reports/` as paired `.md` and `.json` files, named by corpus and timestamp.

---

## Quick Start (Demo Corpus)

Make sure the backend is running (`ais_start`), then:

```bash
ais_bench
```

This runs all 12 demo questions against the `demo` corpus and writes a timestamped report to `benchmarks/demo/reports/`.

---

## CLI Reference

```
ais_bench [OPTIONS]

Options:
  --corpus NAME         Corpus to query (default: demo)
  --top-k INT           Chunks retrieved per query (default: 5)
  --temperature FLOAT   LLM sampling temperature 0.0–2.0 (default: 0.3)
  --model NAME          Ollama model name (default: API default)
  --questions FILE      Path to YAML question file (auto-detected from corpus name if omitted)
  --api URL             Backend URL (default: http://localhost:8000)
  --no-markdown         Skip writing .md report
  --full                Include full answers in report (default: first 4 paragraphs)
  --help                Show this help message
  --version             Show version
```

Question files are auto-detected: for `--corpus demo`, the harness looks for
`benchmarks/demo/demo_questions.yaml` automatically. For any other corpus, place a
`{corpus}_questions.yaml` file in `benchmarks/{corpus}/` and it will be auto-detected.

---

## Question File Format

Questions are YAML files organized by topic. Each question has an `id`, a `question` string, optional `keywords` for pass/fail evaluation, and optional `notes`:

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

Place question files at `benchmarks/{corpus}/{corpus}_questions.yaml` for auto-detection.
See `benchmarks/demo/demo_questions.yaml` for a fully annotated example.

---

## Bringing Your Own Corpus

### 1. Create and ingest your corpus

Create a corpus via the UI, upload your documents, and ingest them.

### 2. Write a question file

Create `benchmarks/{corpus}/{corpus}_questions.yaml` following the format above.

### 3. Run the benchmark

```bash
ais_bench --corpus my_corpus
```

Reports are written to `benchmarks/my_corpus/reports/`.

---

## Running Systematic Benchmarks

### Compare models

```bash
ais_bench --model llama3.1:8b
ais_bench --model llama3.1:70b
```

### Compare retrieval depth

```bash
ais_bench --top-k 3
ais_bench --top-k 5
ais_bench --top-k 10
```

### Compare temperature

```bash
ais_bench --temperature 0.0
ais_bench --temperature 0.3
ais_bench --temperature 0.7
```

Each run produces a separate timestamped report in `benchmarks/demo/reports/`:
```
benchmarks/demo/reports/benchmark_demo_2026-04-15_21-30.md
benchmarks/demo/reports/benchmark_demo_2026-04-15_21-30.json
```

---

## Reading a Report

Each report contains:

**Configuration** — full snapshot (corpus, model, top-k, temperature, timestamp) so every report is self-describing and reproducible.

**Summary** — total questions, pass rate, average latency.

**Infrastructure** — vector store, embedding model, reranker, corpus stats.

**Results table** — per question: latency, pass/fail, citation sources, notes.

**Detailed results** — full answer text with inline citations, per question.

The first query in a cold session is slow (20–50s) while the LLM loads into memory. Subsequent queries run at ~6–7s warm on Apple Silicon. The benchmark summary reflects warm latency once the first query completes.

---

## SEC 10-K Corpus

To benchmark against the full 143-filing SEC corpus:

```bash
# Download and ingest first (one-time, ~35 min total)
ais_download_sec_10k
ais_ingest_sec_10k

# Then benchmark
ais_bench --corpus sec_10k --top-k 10
```

Question file is auto-generated at `benchmarks/sec_10k/sec_10k_questions.yaml` on first `ais_ingest_sec_10k` run.

Reports are written to `benchmarks/sec_10k/reports/`.

---

## Benchmark Data in Demo Corpus (Operator)

Running `ais_bench_ops` (operator command) automatically:
- Runs the benchmark
- Copies the latest PDF report as `AIStudio - Benchmark Data.pdf` to `data/corpora/demo/uploads/`
- Triggers a demo corpus re-ingest

This means users querying the demo corpus can ask questions about benchmark results without any manual steps. Running `ais_bench_ops` is the canonical way to keep benchmark data current.

---

## What's Coming

- **Cross-run comparison** — diff two reports on latency, answer quality, source overlap
- **Hardware metadata** — machine specs recorded in report header for M4 Air vs M4 Max comparisons
- **Model quality evaluation** — human eval framework for 8b vs 70b answer quality

See `docs/PRODUCT_ROADMAP.md` for the full roadmap.
