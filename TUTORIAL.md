# AIStudio Tutorial
*Version: 1.3.0 | Updated: 2026-05-26*

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
- **Use 10 for the demo corpus** — the demo includes small documents (the QFD paper has only 34 chunks; the Agentic AI paper has 20). At K=5, these small documents get outcompeted by larger ones in the retrieval pool and never surface. At K=10 they appear reliably. This is why AIStudio sets demo's default to K=10.
- **Use 10 for the SEC 10-K corpus** — necessary for multi-firm queries where you need chunks from several different filings to appear in the same answer.
- Try 3 for faster, more focused answers on single-document queries

**Temperature** controls creativity:
- 0.1–0.3: precise, factual, stays close to source documents
- 0.5–0.7: more varied synthesis across sources
- Default 0.3 is right for document Q&A

**Retrieval Mix (α)** controls how the system finds relevant passages. The value runs 0 to 1:
- **0 = pure keyword matching (Literal/BM25)** — prioritizes exact word matching. Best when you know the specific term, entity name, or ticker that appears verbatim in your documents.
- **1 = pure semantic search (Conceptual/vector)** — prioritizes meaning over exact words. Best for thematic questions where the document may use different phrasing than your query.
- **0.5 (default) blends both.** For the SEC 10-K corpus, try 0.5–0.6 for multi-firm queries; try 0.8–1.0 for single-firm trend questions where thematic understanding matters more than exact term matching.

**Score Threshold** is a quality floor — chunks that scored below it are dropped before reaching the model. This prevents low-confidence results from producing hedged non-answers like *"I don't have information about this topic."*

- The threshold applies after the Retrieval Mix scoring — it's the final gate before the model sees any content.
- **Why it matters:** a corpus like the demo has documents as small as 20 chunks. In a pool where larger documents (200+ chunks) dominate, the small documents score lower by comparison even when highly relevant. Setting the threshold at 0.3 (instead of the default 0.5) ensures these small documents aren't filtered out.
- **Corpus-level setting:** AIStudio stores the right threshold per corpus in its metadata. The demo is set to 0.3; the SEC 10-K corpus uses 0.5 (larger, more uniform documents benefit from tighter filtering). You can override it per-query from the left panel, or update it in the Edit Corpus modal.
- This concept is well-established in the RAG literature as a *similarity cutoff* or *relevance threshold* — the principle being that passing low-confidence chunks to the model reliably degrades answer quality regardless of model size.

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

Reports are written in three formats: `.md` (readable, with answers), `.json` (machine-readable), and `.pdf`. PDF generation requires `weasyprint`:
```bash
pip3 install weasyprint --break-system-packages
```
If weasyprint isn't installed, the run still completes and writes `.md` and `.json` — you'll see `⚠ PDF skipped` at the end.

> **What makes a benchmark question "pass"?** Three checks: (1) all `keywords` in the question appear in the answer, (2) the answer includes at least one citation, (3) the model doesn't hedge with "no information available." A question can pass all three but still cite the wrong source — the keyword check is a signal, not a guarantee of source correctness.

> **Want to run the demo corpus benchmark too?**
> ```bash
> ais_bench
> ```
> 14 questions, auto-detected from `benchmarks/demo/demo_questions.yaml`. AIStudio automatically uses the right parameters for each corpus — Top K, Temperature, Retrieval Mix, and Score Threshold are all read from corpus metadata, so you don't need to pass flags manually.

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

Full format:
```yaml
- topic: Topic Name          # groups questions in the report
  questions:
    - id: unique_id          # snake_case, appears in summary output
      question: The exact question sent to AIStudio.
      keywords: [term1, term2, term3]   # all must appear in the answer to pass
      notes: What a correct answer looks like — which document, what content.
      # Optional: restrict retrieval to a specific firm or year
      # firm: "Goldman Sachs"
      # year: "2026"
```

**What makes a question pass?** Three checks — all must pass:
1. All `keywords` appear in the answer (case-insensitive)
2. The answer includes at least one citation
3. The model doesn't say "no information available" or similar hedging phrases

**Tips for good keywords:** use 2–5 distinctive terms that prove the model retrieved the right content — firm names, regulatory terms, specific concepts. Avoid generic words that would appear in any answer.

Then run:
```bash
ais_bench --corpus your-corpus-name
```

For the full questions file format and how questions are managed for each corpus type (demo, sec_10k, esef_banks, user), see `HOWTO_OPS.md §Benchmark` and `FILE_GUIDE_OPS.md §2a`.

### 3.5 Optional — Add Corpus Guidance

Each corpus can carry search guidance — routing hints that tell the model which document to consult for which type of question. This improves retrieval precision significantly.

In this release, guidance is added by manually editing the corpus metadata file:
```
data/corpora/<your-corpus-name>/<your-corpus-name>_corpus_metadata.yaml
```

See `data/corpora/demo/demo_corpus_meta.yaml` for a worked example.

> **Tip:** Corpus description, summary, and search guidance can be edited directly in the AIStudio UI — use the **Edit** button in the corpus header to update these fields without editing YAML manually.

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
