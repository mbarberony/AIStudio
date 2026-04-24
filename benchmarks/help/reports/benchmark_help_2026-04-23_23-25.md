# AIStudio — Benchmark Findings
*Generated: 2026-04-23 23:26*

## Configuration
- **Corpus:** `help`
- **Top K:** 5
- **Temperature:** 0.3
- **Model:** API default
- **API:** http://localhost:8000

## Summary
- **Questions:** 16
- **Passed:** 15/16 (94%)
- **Avg latency:** 4.5s

## Infrastructure
- Vector store: Qdrant 1.17.0 (Apple Silicon, local)
- Embedding model: nomic-embed-text (768 dimensions, cosine similarity)
- Reranker: CrossEncoder ms-marco-MiniLM-L-6-v2
- Corpus: `help` (see corpus stats in UI)

## Results

| # | Description | Latency | Pass | Citations | Notes |
|---|-------------|---------|------|-----------|-------|
| 1 | How do I install Qdrant on a Mac? | 7.81s | ✅ | QUICKSTART.pdf | Should return QUICKSTART.pdf |
| 2 | How do I get AIStudio running for the first time? | 4.19s | ✅ | QUICKSTART.pdf | Should return QUICKSTART.pdf |
| 3 | What is a WAL lock error and how do I fix it? | 3.95s | ✅ | QUICKSTART.pdf | Should return QUICKSTART.pdf |
| 4 | How do I create a new corpus? | 3.17s | ✅ | HOWTO.pdf | Should return HOWTO.pdf |
| 5 | How do I delete a file from a corpus? | 2.86s | ✅ | HOWTO.pdf | Should return HOWTO.pdf |
| 6 | How do I recover a corpus I accidentally deleted? | 3.48s | ✅ | HOWTO.pdf | Should return HOWTO.pdf |
| 7 | How do I rename a corpus? | 2.57s | ✅ | HOWTO.pdf | Should return HOWTO.pdf |
| 8 | What is the CrossEncoder reranker and what does it do? | 6.65s | ✅ | CODEBASE_GUIDE.pdf, architecture_decisio | Should return architecture_decisions.pdf |
| 9 | How does AIStudio chunk documents for indexing? | 3.11s | ❌ | FILE_GUIDE.pdf | Should return architecture_decisions.pdf or CODEBASE_GUIDE.pdf or FILE_GUIDE.pdf |
| 10 | How is the AIStudio codebase organized? | 5.01s | ✅ | CODEBASE_GUIDE.pdf | Should return CODEBASE_GUIDE.pdf |
| 11 | How fast is AIStudio at answering queries? | 3.95s | ✅ | QUICKSTART.pdf, README.pdf | Should return README.pdf |
| 12 | Does using a larger model make queries slower? | 4.26s | ✅ | QUICKSTART.pdf, HOWTO.pdf | Should return README.pdf |
| 13 | How do I run a benchmark on my corpus? | 6.62s | ✅ | HARNESS.pdf | Should return HARNESS.pdf |
| 14 | What commands does AIStudio provide? | 5.88s | ✅ | FILE_GUIDE.pdf, HOWTO.pdf | Should return FILE_GUIDE.pdf |
| 15 | What does ais_start do? | 4.27s | ✅ | QUICKSTART.pdf, FILE_GUIDE.pdf | Should return FILE_GUIDE.pdf or HOWTO.pdf |
| 16 | How do I set up the SEC 10-K corpus? | 3.63s | ✅ | HOWTO.pdf | Should return QUICKSTART.pdf or README.pdf |

## Detailed Results

****
### 1. install_qdrant
**Query:** How do I install Qdrant on a Mac?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 7.81s | **Pass:** ✅

**Answer:**

> To install Qdrant on a Mac, you need to follow these steps:
>
> 1. Install Homebrew (if not already installed) [3]:
>    ```
>    brew --version
>    ```
>    If Homebrew is not installed, install it using the following command:
>    ```
>    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
>    ```
>    Verify that Homebrew was installed successfully:
>    ```
>    brew --version
>    ```
>
> 2. Install Python 3.13 (if not already installed) [3]:
>    Check if you have a version of Python 3.10 or higher installed:
>    ```
>    python3 --version
>    ```
>    If you have a lower version, install Python 3.13 using the following command:
>    ```
>    brew install python
>    ```
>
> 3. Install AIStudio using the `ais_install` command [3]:
>    Navigate to the AIStudio directory and run:
>    ```
>    cd ~/Developer/AIStudio
>    ./ais_install
>    ```
>    This will verify your environment, create a Python environment, install dependencies, and install the `ais_*` commands.
>
> *[truncated — use --full for complete answer]*

**Citations:**

- [3] QUICKSTART.pdf p.2


****
### 2. install_fresh
**Query:** How do I get AIStudio running for the first time?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 4.19s | **Pass:** ✅

**Answer:**

> To get AIStudio running for the first time, follow these steps:
>
> 1. Open Terminal first. Press ⌘ Space, type Terminal, press Enter.
> 2. Use python3 — not python — on macOS. The system python command may point to Python 2 or not exist.
>
> Create a folder for your development projects:
> ```bash
> mkdir -p ~/Developer
> ```
> Clone the repo (this downloads ~115 MB — expect under 30 seconds on a fast connection):
> ```bash
> cd ~/Developer
> git clone git@github.com:mbarberony/AIStudio.git
> cd AIStudio
> ```
> Install AIStudio Commands:
> ```bash
> ./ais_install
> ```
> You should see all green checkmarks. Then:
>
> ```bash
> ais_start
> ```
>
> *[truncated — use --full for complete answer]*

**Citations:**

- [1] QUICKSTART.pdf p.1


****
### 3. troubleshoot_wal
**Query:** What is a WAL lock error and how do I fix it?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 3.95s | **Pass:** ✅

**Answer:**

> A WAL lock error is a Qdrant write-ahead log that was left locked from an unclean shutdown [1]. To fix it, stop AIStudio using `ais_stop`, delete the affected collection in `~/qdrant_storage/collections/aistudio_help` (replace with the actual collection name), and then restart AIStudio with `ais_start`. Finally, re-ingest the affected corpus via the UI by clicking the "Add" button [1].

**Citations:**

- [1] QUICKSTART.pdf p.10


****
### 4. create_corpus
**Query:** How do I create a new corpus?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 3.17s | **Pass:** ✅

**Answer:**

> To create a new corpus in AIStudio, use the UI to:
>
> 1. Open AIStudio.
> 2. Create a new corpus using the "New" button.
> 3. Upload your files using the "Add" button.
>
> AIStudio will handle ingestion automatically and show progress in the chat area. [1]
>
> If you want to ingest a special case corpus like the SEC 10-K corpus, download it first using `ais_download_sec_10k`, then ingest it using the AIStudio UI as described above. [1]

**Citations:**

- [1] HOWTO.pdf p.3


****
### 5. delete_file
**Query:** How do I delete a file from a corpus?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 2.86s | **Pass:** ✅

**Answer:**

> To delete a file from a corpus, move it to the trash:
>
> 1. `ls ~/Developer/AIStudio/data/corpora/<name>/uploads/trash/`
> 2. `mv ~/Developer/AIStudio/data/corpora/<name>/uploads/trash/<filename> \
> ~/Developer/AIStudio/data/corpora/<name>/uploads/`
>
> [1]

**Citations:**

- [1] HOWTO.pdf p.8


****
### 6. recover_corpus
**Query:** How do I recover a corpus I accidentally deleted?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 3.48s | **Pass:** ✅

**Answer:**

> To recover a corpus you accidentally deleted, first find the folder in Trash — it may have a timestamp suffix:
>
> `ls ~/.Trash/ | grep AIStudio_<name>`
>
> Then move it back and re-ingest:
> `mv ~/.Trash/AIStudio_<name> ~/Developer/AIStudio/data/corpora/<name>` 
> or if it has a timestamp suffix: `mv ~/.Trash/AIStudio_<name>_<timestamp> ~/Developer/AIStudio/data/corpora/<name>`
>
> Then re-upload the files via the UI (Add button) to restore the corpus in Qdrant.
>
> *[truncated — use --full for complete answer]*

**Citations:**

- [1] HOWTO.pdf p.3


****
### 7. rename_corpus
**Query:** How do I rename a corpus?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 2.57s | **Pass:** ✅

**Answer:**

> To rename a corpus, use the Rename button in the corpus header in the UI. AIStudio renames the directory, cascades the corpus_meta.yaml, and triggers a background re-index automatically [1].
>
> Note that it is not recommended to rename corpus folders manually on disk — use the UI only [1].

**Citations:**

- [1] HOWTO.pdf p.8


****
### 8. crossencoder
**Query:** What is the CrossEncoder reranker and what does it do?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 6.65s | **Pass:** ✅

**Answer:**

> The CrossEncoder reranker is a two-stage retrieval system that uses a CrossEncoder model to reorder the top-K retrieved chunks against the query, improving answer quality significantly with minimal latency overhead [1][2]. This is necessary because embedding-based retrieval can be fast but imprecise, retrieving semantically similar chunks rather than necessarily the most relevant ones [1].
>
> The CrossEncoder reranker reads the query and chunk concatenated as a single input, with full attention across both, scoring relevance directly rather than approximating via cosine distance [2]. This is in contrast to bi-encoder compression, which can lose nuance due to vocabulary mismatch [2].
>
> In more detail, the two-stage architecture consists of Stage 1: Qdrant HNSW vector search (fast and retrieves top-K candidates), followed by Stage 2: CrossEncoder reranker (slower but reorders by true relevance) [2]. The model selection for the CrossEncoder reranker is ms-marco-MiniLM-L-6-v2, a fine-tuned model on MS MARCO with 22M parameters and 90MB size, which loads in less than 1 second on Apple Silicon [2].
>
> There is no explicit mention of what tasks or goals this reranker addresses. However, based on the context that it's used for retrieval quality improvement, it can be inferred that its primary purpose is to enhance the accuracy and relevance of search results.
>
> *[truncated — use --full for complete answer]*

**Citations:**

- [1] CODEBASE_GUIDE.pdf p.6
- [2] architecture_decisions.pdf p.6


****
### 9. chunking
**Query:** How does AIStudio chunk documents for indexing?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 3.11s | **Pass:** ❌

**Answer:**

> [1] does not mention how AIStudio chunks documents for indexing.
>
> The sources do not address how AIStudio chunks documents for indexing.

**Citations:**

- [1] FILE_GUIDE.pdf p.2

**⚠ Model said 'no information' — possible retrieval miss**

****
### 10. codebase_structure
**Query:** How is the AIStudio codebase organized?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 5.01s | **Pass:** ✅

**Answer:**

> The AIStudio codebase is organized as follows:
>
> The general architecture of the codebase has three layers: ingest, query, and UI. The ingest layer lives in `src/local_llm_bot/app/ingest/`, the query pipeline lives in `src/local_llm_bot/app/rag_core.py` and is orchestrated by `api.py`, and the UI layer is a single HTML file that communicates with the FastAPI backend over localhost [1].
>
> The three services that must be running are: Qdrant (vector store), Ollama (LLM host), and the FastAPI backend (uvicorn). ais_start starts all three [1].
>
> The first-level directory structure of AIStudio is:
> ```
> AIStudio/
> ├── src/ Application source code
> ├── tests/ Test suite
> ├── front_end/ Single-file frontend
> └── ...
> ```
>
> *[truncated — use --full for complete answer]*

**Citations:**

- [1] CODEBASE_GUIDE.pdf p.1


****
### 11. latency
**Query:** How fast is AIStudio at answering queries?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 3.95s | **Pass:** ✅

**Answer:**

> According to [1] and [2], AIStudio's query latency is around ~6–7 seconds after the model has been loaded into memory, which is referred to as a "warm" session. This is consistent across both models (llama3.1:70b and llama3.1:8b) on Apple Silicon.

**Citations:**

- [1] QUICKSTART.pdf p.5
- [2] README.pdf p.3


****
### 12. model_size_latency
**Query:** Does using a larger model make queries slower?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 4.26s | **Pass:** ✅

**Answer:**

> According to [3], "Higher values give the model more context but increase latency slightly." This suggests that using a larger model, which would require more resources and potentially more complex processing, may indeed make queries slower due to increased latency. However, it's also mentioned in [1] that once the model is loaded into unified memory, model size stops being a latency variable. The exact relationship between model size and query speed depends on various factors, including system resources and specific use cases.

**Citations:**

- [1] QUICKSTART.pdf p.5
- [3] HOWTO.pdf p.6


****
### 13. run_benchmark
**Query:** How do I run a benchmark on my corpus?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 6.62s | **Pass:** ✅

**Answer:**

> To run a benchmark on your corpus, follow these steps:
>
> 1. Make sure the backend is running with `ais_start`.
> 2. If you want to run a benchmark on the demo corpus, simply type:
> ```
> ais_bench
> ```
> This will run all 12 demo questions against the demo corpus and write a timestamped report to `benchmarks/demo/reports/`.
>
> If you want to benchmark a different corpus, use the following command:
> ```bash
> ais_bench --corpus <corpus_name> 
> ```
> Replace `<corpus_name>` with the name of your corpus.
>
> To test with a specific model or settings, use the following command:
> ```bash
> ais_bench --corpus demo --model llama3.1:70b --top-k 10 --temperature 0.1
> ```
> Reports are written to `benchmarks/<corpus>/reports/` as paired `.md` and `.json` files, named by corpus and timestamp.
>
> *[truncated — use --full for complete answer]*

**Citations:**

- [2] HARNESS.pdf p.1


****
### 14. all_commands
**Query:** What commands does AIStudio provide?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 5.88s | **Pass:** ✅

**Answer:**

> According to FILE_GUIDE.pdf [1], the available commands after running `./ais_install` are:
>
> * `ais_start`: Starts all AIStudio services and opens the UI.
> * `ais_stop`: Stops all AIStudio services cleanly.
> * `ais_log`: Shows the live backend log in real time.
> * `ais_bench`: Runs a benchmark on the demo corpus.
> * `ais_download_sec_10k`: Downloads SEC 10-K filings from EDGAR to `~/Downloads/sec_10k/`.
> * `ais_ingest_sec_10k`: Ingests SEC 10-K filings into AIStudio (~30 min, backend must be running).
> * `ais_help`: Shows the command reference.
> * `ais_install`: Installs or updates AIStudio (Fresh install; adding a new com).
>
> According to HOWTO.pdf [2], additional commands are available after running `./ais_install`, including:
>
> * `ais_start --help`
> * `ais_bench --help`
>
> *[truncated — use --full for complete answer]*

**Citations:**

- [1] FILE_GUIDE.pdf p.1
- [2] HOWTO.pdf p.1


****
### 15. ais_start
**Query:** What does ais_start do?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 4.27s | **Pass:** ✅

**Answer:**

> According to [1] (QUICKSTART.pdf), page 7 of 11:
>
> "ais_start handles this automatically — you only need to activate manually if running Python commands directly."
>
> However, according to [3] (FILE_GUIDE.pdf), the command reference for ais_start is more specific:
>
> "Starts all AIStudio services and opens the UI"
>
> *[truncated — use --full for complete answer]*

**Citations:**

- [1] QUICKSTART.pdf p.7
- [3] FILE_GUIDE.pdf p.1


****
### 16. sec_10k
**Query:** How do I set up the SEC 10-K corpus?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 3.63s | **Pass:** ✅

**Answer:**

> To set up the SEC 10-K corpus, follow these steps:
>
> 1. Download the filings to `~/Downloads/sec_10k/` (~5 min, ~2 GB) using the command:
> ```
> ais_download_sec_10k
> ```
> [1]
>
> 2. Ingest using the AIStudio UI:
> Open AIStudio, create a new corpus named `sec_10k`, then upload the files from `~/Downloads/sec_10k/` using the Upload button.
> Allow ~34 minutes for ingestion to complete.
> [1]
>
> Note: The download step is what's special about the SEC 10-K corpus. [1]

**Citations:**

- [1] HOWTO.pdf p.5

