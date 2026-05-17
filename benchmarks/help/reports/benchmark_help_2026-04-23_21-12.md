# AIStudio — Benchmark Findings
*Generated: 2026-04-23 21:15*

## Configuration
- **Corpus:** `help`
- **Top K:** 5
- **Temperature:** 0.3
- **Model:** API default
- **API:** http://localhost:8000

## Summary
- **Questions:** 21
- **Passed:** 14/21 (67%)
- **Avg latency:** 10.2s

## Infrastructure
- Vector store: Qdrant 1.17.0 (Apple Silicon, local)
- Embedding model: nomic-embed-text (768 dimensions, cosine similarity)
- Reranker: CrossEncoder ms-marco-MiniLM-L-6-v2
- Corpus: `help` (see corpus stats in UI)

## Results

| # | Description | Latency | Pass | Citations | Notes |
|---|-------------|---------|------|-----------|-------|
| 1 | What are the prerequisites for installing AIStudio? | 7.42s | ✅ | dependencies.pdf, QUICKSTART.pdf, PRODUC | Should return QUICKSTART.pdf |
| 2 | How do I install Qdrant on a Mac? | 5.75s | ✅ | QUICKSTART.pdf | Should return QUICKSTART.pdf |
| 3 | How do I get AIStudio running for the first time? | 7.24s | ❌ | — | Should return QUICKSTART.pdf |
| 4 | The backend is not reachable at port 8000 — what do I do? | 10.12s | ❌ | QA_TESTING_LESSONS_LEARNED.pdf, PRODUCT_ | Should return QUICKSTART.pdf or HOWTO.pdf |
| 5 | What is a WAL lock error and how do I fix it? | 10.41s | ✅ | QUICKSTART.pdf | Should return QUICKSTART.pdf |
| 6 | How do I create a new corpus? | 9.38s | ✅ | HOWTO.pdf | Should return HOWTO.pdf |
| 7 | How do I delete a file from a corpus? | 13.77s | ❌ | — | Should return HOWTO.pdf |
| 8 | How do I recover a corpus I accidentally deleted? | 9.12s | ✅ | HOWTO.pdf | Should return HOWTO.pdf |
| 9 | How do I rename a corpus? | 7.11s | ✅ | HOWTO.pdf | Should return HOWTO.pdf |
| 10 | What is search guidance and how does it improve answers? | 13.97s | ✅ | PRODUCT_ROADMAP.pdf, README.pdf | Should return HOWTO.pdf or FILE_GUIDE.pdf |
| 11 | Why does AIStudio use Qdrant instead of ChromaDB? | 7.78s | ✅ | CODEBASE_GUIDE.pdf | Should return architecture_decisions.pdf |
| 12 | How does the citation system work? | 9.86s | ✅ | README.pdf, PRODUCT_ROADMAP.pdf | Should return architecture_decisions.pdf or CODEBASE_GUIDE.pdf |
| 13 | What is the CrossEncoder reranker and what does it do? | 11.45s | ✅ | CODEBASE_GUIDE.pdf, architecture_decisio | Should return architecture_decisions.pdf |
| 14 | How does AIStudio chunk documents for indexing? | 9.19s | ❌ | FILE_GUIDE.pdf, dependencies.pdf, CODEBA | Should return architecture_decisions.pdf or CODEBASE_GUIDE.pdf |
| 15 | How is the AIStudio codebase organized? | 11.97s | ❌ | — | Should return CODEBASE_GUIDE.pdf |
| 16 | How fast is AIStudio at answering queries? | 11.6s | ✅ | QUICKSTART.pdf, README.pdf | Should return README.pdf |
| 17 | Does using a larger model make queries slower? | 10.01s | ✅ | HOWTO.pdf | Should return README.pdf |
| 18 | How do I run a benchmark on my corpus? | 14.88s | ❌ | — | Should return HARNESS.pdf |
| 19 | What commands does AIStudio provide? | 13.57s | ❌ | — | Should return FILE_GUIDE.pdf |
| 20 | What does ais_start do? | 9.35s | ✅ | QUICKSTART.pdf, FILE_GUIDE.pdf | Should return FILE_GUIDE.pdf or HOWTO.pdf |
| 21 | How do I set up the SEC 10-K corpus? | 10.06s | ✅ | HOWTO.pdf | Should return QUICKSTART.pdf or README.pdf |

## Detailed Results

****
### 1. install_prerequisites
**Query:** What are the prerequisites for installing AIStudio?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 7.42s | **Pass:** ✅

**Answer:**

> To install AIStudio, you need to meet the following prerequisites:
>
> * Install Homebrew on your macOS system [1]:
> 	+ Check if it's already installed: `brew --version`
> 	+ If not installed, run: `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"` and then run: `echo >> ~/.zprofile`, `echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile`, `eval "$(/opt/homebrew/bin/brew shellenv)"`
> * Install Python 3.13 [1]:
> 	+ Check if you already have Python 3.10 or later: `python3 --version`
> 	+ If not installed, install Python 3.13: (installation command not provided in the source)
> * Note that Intel Macs are not supported in this release [2].
> * Ensure you have an Apple Silicon chip (M1, M2, M3, or M4) [2].
>
> These prerequisites are necessary for installing AIStudio using the One-Click Installer, which is available starting from v2.0 [3].

**Citations:**

- [1] dependencies.pdf p.1
- [2] QUICKSTART.pdf p.7
- [3] PRODUCT_ROADMAP.pdf p.3


****
### 2. install_qdrant
**Query:** How do I install Qdrant on a Mac?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 5.75s | **Pass:** ✅

**Answer:**

> To install Qdrant on a Mac, you need to follow these steps:
>
> First, ensure you have Homebrew installed by running `brew --version` in your terminal ([3]). If it's not installed, run the installation script:
> ```
> /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
> ```
> Then, add Homebrew to your PATH by running these three lines:
> ```
> echo >> ~/.zprofile
> echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
> eval "$(/opt/homebrew/bin/brew shellenv)"
> ```
> Verify that Homebrew is installed correctly by running `brew --version` again.
>
> Next, install the pango system library required for PDF generation:
> ```
> brew install pango
> ```
>
> Then, ensure you have Python 3.13 installed by checking the version with `python3 --version`. If it's not installed or if you're running an older version, follow [3] and install Python 3.13.
>
> *[truncated — use --full for complete answer]*

**Citations:**

- [3] QUICKSTART.pdf p.2


****
### 3. install_fresh
**Query:** How do I get AIStudio running for the first time?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 7.24s | **Pass:** ❌

**Answer:**

> To get AIStudio running for the first time, follow these steps:
>
> 1. Open Terminal first. Press ⌘ Space, type Terminal, press Enter.
> 2. Use python3 — not python — on macOS: `python3`
> 3. Create a folder for your development projects: `mkdir -p ~/Developer`
> 4. Clone the AIStudio repo from GitHub:
>    ```
>    cd ~/Developer
>    git clone git@github.com:mbarberony/AIStudio.git
>    cd AIStudio
>    ```
> 5. Install AIStudio Commands: `./ais_install`
> 6. Run `ais_start` to wait for indexing to complete.
>
> Make sure you have a Mac with Apple Silicon (M1/M2/M3/M4) and that your PATH includes ~/bin (if Qdrant is not found).


****
### 4. troubleshoot_port
**Query:** The backend is not reachable at port 8000 — what do I do?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 10.12s | **Pass:** ❌

**Answer:**

> The sources do not address the specific issue of port 8000 being unreachable due to it already being in use.
>
> However, [1] mentions that the root cause category for this issue is [BUG], and a fix has been documented in the troubleshooting section but not yet applied.
>
> [3] describes AIStudio's core value proposition, which does not address the issue at hand.
>
> The most relevant information comes from [1], which suggests adding a preflight check script to catch such issues automatically.

**Citations:**

- [1] QA_TESTING_LESSONS_LEARNED.pdf p.5
- [3] PRODUCT_ROADMAP.pdf p.1

**⚠ Model said 'no information' — possible retrieval miss**

****
### 5. troubleshoot_wal
**Query:** What is a WAL lock error and how do I fix it?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 10.41s | **Pass:** ✅

**Answer:**

> A WAL lock error is caused by a collection's write-ahead log being left locked from an unclean shutdown [1]. To fix it, you need to:
>
> 1. Stop AIStudio with `ais_stop`
> 2. Delete the affected collection (not the entire qdrant_storage folder) with `rm -rf ~/qdrant_storage/collections/aistudio_help` (replace with the collection named in the error)
> 3. Start AIStudio again with `ais_start`
>
> This will re-ingest the affected corpus via the UI (Add button).

**Citations:**

- [1] QUICKSTART.pdf p.10


****
### 6. create_corpus
**Query:** How do I create a new corpus?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 9.38s | **Pass:** ✅

**Answer:**

> To create a new corpus in AIStudio, use the UI. Open AIStudio, create a new corpus using the New button, then upload your files using the Add button [1]. This will automatically ingest the files and show progress in the chat area [1].
>
> If you want to ingest a new corpus from scratch or re-ingest an existing one, delete the corpus using the Delete Corpus button in the UI (type YES to confirm — it moves to Trash, recoverable), then create a new corpus with the same name and re-upload your files via Add [1].

**Citations:**

- [1] HOWTO.pdf p.3


****
### 7. delete_file
**Query:** How do I delete a file from a corpus?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 13.77s | **Pass:** ❌

**Answer:**

> To delete a file from a corpus, you can move it to the trash folder temporarily:
>
> 1. Go to `~/Developer/AIStudio/data/corpora/<name>/uploads/trash/` using your terminal.
> 2. Run the command:
> ```
> mv ~/Developer/AIStudio/data/corpus/<name>/uploads/<filename> \
> ~/Developer/AIStudio/data/corpus/<name>/uploads/trash/
> ```
> This will move the file to the trash folder, where it can be easily recovered if needed.
>
> To recover a deleted file, you can move it back from the trash folder and re-ingest:
>
> 1. Go to `~/Developer/AIStudio/data/corpora/<name>/uploads/` using your terminal.
> 2. Run the command:
> ```
> mv ~/Developer/AIStudio/data/corpus/<name>/uploads/trash/<filename> \
> ~/Developer/AIStudio/data/corpus/<name>/uploads/
> ```
>
> *[truncated — use --full for complete answer]*


****
### 8. recover_corpus
**Query:** How do I recover a corpus I accidentally deleted?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 9.12s | **Pass:** ✅

**Answer:**

> To recover a corpus you accidentally deleted, first find the folder in Trash — it may have a timestamp suffix:
>
> ```bash
> ls ~/.Trash/ | grep AIStudio_<name>
> ```
>
> Then move it back and re-ingest:
>
> ```bash
> mv ~/.Trash/AIStudio_<name> ~/Developer/AIStudio/data/corpora/<name>
> # Or if it has a timestamp suffix:
> mv ~/.Trash/AIStudio_<name>_<timestamp> ~/Developer/AIStudio/data/corpora/<name>
> ```
>
> *[truncated — use --full for complete answer]*

**Citations:**

- [1] HOWTO.pdf p.3


****
### 9. rename_corpus
**Query:** How do I rename a corpus?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 7.11s | **Pass:** ✅

**Answer:**

> To rename a corpus, use the Rename button in the corpus header in the UI. AIStudio will automatically rename the directory, cascade the corpus_meta.yaml, and trigger a background re-index. [1]
>
> Alternatively, you can delete the corpus via the UI, recreate it with the new name, and re-ingest your files using the Add button. This approach is not recommended due to potential issues with citation lookup. [1]

**Citations:**

- [1] HOWTO.pdf p.8


****
### 10. search_guidance
**Query:** What is search guidance and how does it improve answers?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 13.97s | **Pass:** ✅

**Answer:**

> The search guidance is described as "routing guidance (hints about which documents answer which kinds of questions)" in [2]. This metadata is injected into the system prompt at query time to improve retrieval precision.
>
> In [1], it's mentioned that v2.0 adds UI fields to the New Corpus modal for providing this routing guidance, making it easier for users to create corpora with relevant search guidance.
>
> The purpose of search guidance is to improve answers by helping the system understand which documents are most relevant to a particular question. This is achieved by injecting metadata into the system prompt at query time, as mentioned in [2].
>
> According to [1], v2.0 publishes full API documentation (API_DOC.md) with request/response schemas, error codes, and examples, which should help developers understand how search guidance works under the hood.
>
> *[truncated — use --full for complete answer]*

**Citations:**

- [1] PRODUCT_ROADMAP.pdf p.3
- [2] README.pdf p.1


****
### 11. why_qdrant
**Query:** Why does AIStudio use Qdrant instead of ChromaDB?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 7.78s | **Pass:** ✅

**Answer:**

> AIStudio uses Qdrant instead of ChromaDB because the architecture has three layers, and the ingest layer stores documents in Qdrant [1].
>
> For context on architecture decisions, refer to docs/architecture_decisions.pdf as mentioned in HOWTO.pdf.

**Citations:**

- [1] CODEBASE_GUIDE.pdf p.2


****
### 12. how_citations
**Query:** How does the citation system work?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 9.86s | **Pass:** ✅

**Answer:**

> According to [1], the citation system in AIStudio works as follows:
>
> * Inline source citations ([1], [2]) are displayed in the chat interface.
> * The References section shows exactly which document and passage each answer came from.
> * Clicking on a citation opens the PDF viewer, but currently only shows the document name and page number with a link that opens the PDF.
>
> However, according to [2], the feature called "Source Dive" will be implemented in v2.0, which will allow users to click a citation and the PDF will open at the exact page, with the cited passage highlighted. The backend already stores chunk-level page positions in Qdrant, but the remaining work is on the frontend PDF viewer (PDF.js).

**Citations:**

- [1] README.pdf p.2
- [2] PRODUCT_ROADMAP.pdf p.2


****
### 13. crossencoder
**Query:** What is the CrossEncoder reranker and what does it do?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 11.45s | **Pass:** ✅

**Answer:**

> The CrossEncoder reranker is a two-stage retrieval architecture used in AIStudio [1,2]. In the first stage, Qdrant HNSW vector search retrieves top-K candidates, and then the CrossEncoder reranker scores relevance directly by reading query + chunk concatenated as a single input with full attention across both [2].
>
> The CrossEncoder model is ms-marco-MiniLM-L-6-v2, which has 22M parameters and loads in <1s on Apple Silicon. It was fine-tuned on MS MARCO (500K passage relevance pairs) and is directly applicable to "rank these passages for this query" [2]. The tradeoff of using the CrossEncoder reranker is ~1-2s additional latency per query, but it improves answer quality significantly with minimal latency overhead [1].
>
> The purpose of the CrossEncoder reranker is to address vocabulary mismatch in embedding-based retrieval by scoring relevance directly rather than approximating via cosine distance [2].

**Citations:**

- [1] CODEBASE_GUIDE.pdf p.6
- [2] architecture_decisions.pdf p.6


****
### 14. chunking
**Query:** How does AIStudio chunk documents for indexing?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 9.19s | **Pass:** ❌

**Answer:**

> AIStudio uses pdfplumber to chunk documents for indexing [1]. According to the CODEBASE_GUIDE.pdf [4], page numbers in citations are made possible by markers placed at each page boundary during extraction, which flow through the chunking pipeline into Qdrant payload.
>
> The exact format of these chunks is `filename::page-N::chunk-M` [3].
>
> The sources do not address how AIStudio determines the relevant chunks to index from the extracted text.

**Citations:**

- [1] FILE_GUIDE.pdf p.2
- [3] dependencies.pdf p.4
- [4] CODEBASE_GUIDE.pdf p.6

**⚠ Model said 'no information' — possible retrieval miss**

****
### 15. codebase_structure
**Query:** How is the AIStudio codebase organized?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 11.97s | **Pass:** ❌

**Answer:**

> The AIStudio codebase is organized with three layers: Ingest, Query, and UI. The Ingest layer lives in `src/local_llm_bot/app/ingest/`, the Query layer lives in `src/local_llm_bot/app/rag_core.py` and is orchestrated by `api.py`, and the UI layer is a single HTML file that communicates with the FastAPI backend over localhost.
>
> The three services that must be running are: Qdrant (vector store), Ollama (LLM host), and the FastAPI backend (uvicorn). The first-level directory structure of AIStudio is:
>
> AIStudio/
> ├── src/ Application source code
> ├── tests/ Test suite
> ├── front_end/ Single-file frontend
>
> [CITE 1]
>
> *[truncated — use --full for complete answer]*


****
### 16. latency
**Query:** How fast is AIStudio at answering queries?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 11.6s | **Pass:** ✅

**Answer:**

> According to [1], the first query after startup takes around 10–15 seconds to load the model into memory, which is known as the "cold start". After that, queries run in ~6–7 seconds.
>
> Also, according to [2], once loaded into unified memory, model size stops being a latency variable and AIStudio can operate at statistically identical query latency on Apple Silicon (~6–7s average) for both llama3.1:70b and warm llama3.1:8b.
>
> Therefore, the answer is that AIStudio answers queries in ~6–7 seconds after the initial "cold start" period of 10–15 seconds.

**Citations:**

- [1] QUICKSTART.pdf p.5
- [2] README.pdf p.3


****
### 17. model_size_latency
**Query:** Does using a larger model make queries slower?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 10.01s | **Pass:** ✅

**Answer:**

> Using a larger model does not make queries slower. According to [3], once loaded into unified memory, model size stops being a latency variable.
>
> However, it's worth noting that the number of passages retrieved (Top K) can increase latency slightly, but this is not directly related to the model size or complexity. The recommended approach in this case is to adjust the Top K value using the input field in the sidebar, as described in [3].

**Citations:**

- [3] HOWTO.pdf p.6


****
### 18. run_benchmark
**Query:** How do I run a benchmark on my corpus?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 14.88s | **Pass:** ❌

**Answer:**

> To run a benchmark on your corpus, you need to use the `ais_bench` command. The steps are as follows:
>
> 1. First, make sure the backend is running by executing:
> ```
> ais_start
> ```
> 2. Then, run the following command to benchmark against the demo corpus:
> ```
> ais_bench
> ```
> This will run all 12 demo questions against the demo corpus and write a timestamped report to `benchmarks/demo/reports/` [HARNESS].
>
> If you want to benchmark a different corpus, you can use the `--corpus` option followed by the name of your corpus. For example:
> ```
> ais_bench --corpus sec_10k --top-k 10
> ```
> This will run the benchmark against the SEC 10-K corpus [HARNESS]. The question file is auto-generated at `benchmarks/sec_10k/sec_10k_questions.yaml` on first `ais_ingest_sec_10k` run.
>
> Note that the report will be written to `benchmarks/<corpus>/reports/`, where `<corpus>` is the name of your corpus [HARNESS].


****
### 19. all_commands
**Query:** What commands does AIStudio provide?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 13.57s | **Pass:** ❌

**Answer:**

> The commands available after running `./ais_install` are:
>
> * `ais_start`: Starts all AIStudio services and opens the UI.
> * `ais_stop`: Stops all AIStudio services cleanly.
> * `ais_log`: Shows the live backend log in real time.
> * `ais_bench`: Runs a benchmark on the demo corpus.
> * `ais_download_sec_10k`: Downloads SEC 10-K filings from EDGAR to ~/Downloads/sec_10k/ (~2 GB).
> * `ais_ingest_sec_10k`: Ingests SEC 10-K corpus into AIStudio (~30 min, backend must be running).
> * `ais_help`: Shows the command reference.
>
> Additionally, every command supports `--help`, for example:
>
> * `ais_start --help`
> * `ais_bench --help`
>
> *[truncated — use --full for complete answer]*


****
### 20. ais_start
**Query:** What does ais_start do?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 9.35s | **Pass:** ✅

**Answer:**

> ais_start starts all AIStudio services and opens the UI in your browser [1] or [3]. It automatically handles activating the virtual environment [1]. The demo corpus is indexed on first run, taking approximately 45 seconds [1]. After running ais_start, you can verify the backend is up by running curl http://localhost:8000/health, which should return {"status": "ok"} [1].

**Citations:**

- [1] QUICKSTART.pdf p.7
- [3] FILE_GUIDE.pdf p.1


****
### 21. sec_10k
**Query:** How do I set up the SEC 10-K corpus?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 10.06s | **Pass:** ✅

**Answer:**

> To set up the SEC 10-K corpus, follow these steps:
>
> Step 1 — Download the filings to ~/Downloads/sec_10k/ (~5 min, ~2 GB):
> ```bash
> ais_download_sec_10k
> ```
> Step 2 — Ingest using the AIStudio UI:
> Open AIStudio, create a new corpus named sec_10k , then upload the files from ~/Downloads/
> sec_10k/ using the Upload button. This is the same process as ingesting any corpus you build yourself — the download step is what's special.
> Allow ~34 minutes for ingestion to complete.
>
> [1]
>
> Note: The process of re-ingesting a corpus is not specific to the SEC 10-K corpus, but rather a general procedure outlined in [1].

**Citations:**

- [1] HOWTO.pdf p.5

