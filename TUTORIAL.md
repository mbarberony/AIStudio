# AIStudio Tutorial
*Version: 0.1.0-draft*
*Status: DRAFT — not yet published*

Get the most out of AIStudio with three guided modules — from your first query to benchmarking at scale.

> **Prerequisites:** AIStudio must be installed and running. If you haven't done that yet, start with [QUICKSTART.md](QUICKSTART.md).

---

## Module 1 — Quick Tour

*Goal: Run your first query, understand citations, explore the interface. ~15 minutes.*

### 1.1 Your First Query

AIStudio ships with a demo corpus — 9 original documents spanning 2003–2026 covering enterprise architecture, IT strategy, financial services technology, and agentic AI. It's already indexed and ready to query.

Open AIStudio:
```bash
ais_start
```

The **demo** corpus is pre-selected. Try these questions:

- *"What is QFD and how does it apply to technology architecture?"*
- *"How should a CTO prioritize a three-year technology strategy?"*
- *"What are the key principles for modernizing legacy applications?"*

### 1.2 Understanding Citations

Every answer includes citations — numbered references like `[1]`, `[2]` — and a **References** panel below showing exactly which document and page each answer came from.

Click **Open ↗** next to any reference to open the source document at that page.

This is AIStudio's core value proposition: answers grounded in your documents, with a direct path back to the source.

### 1.3 Follow-up Questions

AIStudio maintains conversation context across a session. After your first answer, ask a follow-up:

- *"Can you give me a specific example from the documents?"*
- *"How does this apply to a financial services firm specifically?"*

The model uses the previous exchange as context — no need to repeat yourself.

### 1.4 Tuning Your Query

Try adjusting **Top K** in the settings sidebar:
- Default: 5 chunks retrieved
- Try 10 for complex questions spanning multiple documents
- Try 3 for faster, more focused answers

**Temperature** controls creativity:
- 0.1–0.3: precise, factual, stays close to source documents
- 0.5–0.7: more varied synthesis across sources
- Default 0.3 is right for document Q&A

### 1.5 The Help Corpus — AIStudio Answering About Itself

Switch to the **help** corpus in the dropdown. Now ask:

- *"How do I re-ingest a corpus?"*
- *"What embedding model does AIStudio use?"*
- *"How does the reranker work?"*

AIStudio answers questions about itself using its own documentation as the corpus. This is the same RAG pipeline — just pointed at the AIStudio docs. Try it when you're stuck before reaching for the manual.

---

## Module 2 — At Scale: The SEC 10-K Corpus

*Goal: Build a large corpus from scratch, query it, run the benchmark harness. ~45 minutes total (30 min ingest).*

This module walks you through downloading 143 SEC 10-K annual filings from 25 major financial services firms, ingesting them into AIStudio, and running a pre-built benchmark suite.

It demonstrates AIStudio operating at production scale: 105,964 chunks, 34-minute ingest, sub-7s query latency.

### 2.1 Download the Filings

AIStudio includes a downloader that handles the SEC EDGAR access protocol automatically:

```bash
ais_download_sec_10k
```

This downloads ~2 GB of filings to `~/Downloads/sec_10k/`. Allow 5–10 minutes depending on your connection.

> **What is SEC EDGAR?** The SEC requires all public companies to file annual reports (10-K). EDGAR is the public database where these filings live. AIStudio's downloader handles the access protocol — you get the files, AIStudio handles the plumbing.

> **Firms included:** Goldman Sachs, JPMorgan Chase, Morgan Stanley, BlackRock, BNY Mellon, Citigroup, and 19 others — bulge bracket banks, asset managers, exchanges, and custody banks.

### 2.2 Ingest the Corpus

With AIStudio running (`ais_start`), ingest the downloaded filings:

```bash
ais_ingest_sec_10k
```

Expected: ~30 minutes on an M4 MacBook Pro. The command shows progress and confirms when done.

> Leave this terminal open. Ingestion is CPU and memory intensive — don't run other heavy tasks during this time.

### 2.3 Query at Scale

Switch to the **sec_10k** corpus in the AIStudio dropdown. Try:

- *"What does Goldman Sachs say about the risks of artificial intelligence?"*
- *"How does JPMorgan Chase describe their cybersecurity risk management?"*
- *"Which financial firms have dedicated AI governance committees?"*

> **Tip:** Use the **Firm** filter in the sidebar to restrict retrieval to a specific firm. Type `Goldman Sachs` (exact match) to get Goldman-only results. Leave blank for cross-corpus queries.

### 2.4 Run the Benchmark

When you ran `ais_ingest_sec_10k`, it automatically created a benchmark questions file at `benchmarks/sec_10k/sec_10k_questions.yaml`. You can run it now:

```bash
ais_bench --corpus sec_10k --top-k 10
```

This runs 7 pre-built questions, reports pass/fail per question with latency, and writes a timestamped report to `benchmarks/sec_10k/reports/`.

> **What makes a benchmark question "pass"?** The harness checks whether the answer references the expected source document and contains key terms from the `notes` field. It's a quality signal, not a strict pass/fail test.

> **Want to run the demo corpus benchmark too?**
> ```bash
> ais_bench
> ```
> 14 questions, auto-detected from `benchmarks/demo/demo_questions.yaml`.

---

## Module 3 — Bring Your Own Corpus

*Goal: Ingest your own documents and query them. ~15 minutes + ingest time.*

### 3.1 Create a New Corpus

Open AIStudio in your browser. Click **New** in the corpus panel. Enter a name (e.g. `my_docs`). Click **Create**.

### 3.2 Upload Your Documents

With your new corpus selected, click **Add** and select your files. AIStudio supports:

- PDF (`.pdf`) — page-aware chunking with page numbers in citations
- Word documents (`.docx`)
- PowerPoint (`.pptx`)
- Excel (`.xlsx`)
- Markdown (`.md`)
- HTML (`.html`)

AIStudio ingests automatically after upload and shows progress in the chat area.

### 3.3 Query Your Corpus

Select your corpus from the dropdown and start asking questions. Same interface, your content.

### 3.4 Optional — Write Your Own Benchmark Questions

To run `ais_bench` against your corpus, create a questions file at:
```
benchmarks/<your-corpus-name>/<your-corpus-name>_questions.yaml
```

Format (use the SEC or demo files as examples):
```yaml
- topic: Your Topic
  questions:
    - id: your_question_id
      question: What is the main argument of this document?
      keywords: [main, argument, key]
      notes: Should reference the introduction section
```

Then run:
```bash
ais_bench --corpus your-corpus-name
```

### 3.5 Optional — Add Corpus Guidance

Each corpus can carry search guidance — routing hints that tell the model which document to consult for which type of question. This improves retrieval precision significantly.

In this release, guidance is added by manually editing the corpus metadata file:
```
data/corpora/<your-corpus-name>/<your-corpus-name>_corpus_meta.yaml
```

See `data/corpora/demo/demo_corpus_meta.yaml` for a worked example.

> **Coming in next release:** Corpus description, summary, and search guidance will be editable directly in the AIStudio UI at corpus creation time — no manual YAML editing required.

---

## Reference

### All ais_* Commands

| Command | What it does |
|---------|-------------|
| `ais_start` | Start all services and open the UI |
| `ais_stop` | Stop all services |
| `ais_bench` | Run benchmark on demo corpus |
| `ais_bench --corpus <name>` | Run benchmark on a specific corpus |
| `ais_download_sec_10k` | Download SEC 10-K filings (~2 GB) |
| `ais_ingest_sec_10k` | Ingest SEC 10-K corpus (~30 min) |
| `ais_log` | Tail live backend log |
| `ais_install` | Install or update AIStudio commands |
| `ais_help` | Show command reference |

---

For day-to-day usage recipes, see [HOWTO.md](HOWTO.md).
For architecture and technical decisions, see [docs/architecture_decisions.md](docs/architecture_decisions.md).
