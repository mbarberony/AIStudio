# AIStudio — Benchmark Findings
*Generated: 2026-04-23 18:19*

## Configuration
- **Corpus:** `help`
- **Top K:** 5
- **Temperature:** 0.3
- **Model:** API default
- **API:** http://localhost:8000

## Summary
- **Questions:** 21
- **Passed:** 18/21 (86%)
- **Avg latency:** 4.8s

## Infrastructure
- Vector store: Qdrant 1.17.0 (Apple Silicon, local)
- Embedding model: nomic-embed-text (768 dimensions, cosine similarity)
- Reranker: CrossEncoder ms-marco-MiniLM-L-6-v2
- Corpus: `help` (see corpus stats in UI)

## Results

| # | Description | Latency | Pass | Citations | Notes |
|---|-------------|---------|------|-----------|-------|
| 1 | What are the prerequisites for installing AIStudio? | 4.32s | ✅ | dependencies.pdf, QUICKSTART.pdf | Should return QUICKSTART.pdf |
| 2 | How do I install Qdrant on a Mac? | 4.09s | ✅ | QUICKSTART.pdf | Should return QUICKSTART.pdf |
| 3 | How do I get AIStudio running for the first time? | 4.44s | ✅ | QUICKSTART.pdf, CODEBASE_GUIDE.pdf | Should return QUICKSTART.pdf |
| 4 | The backend is not reachable at port 8000 — what do I do? | 4.87s | ✅ | QUICKSTART.pdf, QA_TESTING_LESSONS_LEARN | Should return QUICKSTART.pdf or HOWTO.pdf |
| 5 | What is a WAL lock error and how do I fix it? | 5.17s | ✅ | QUICKSTART.pdf | Should return QUICKSTART.pdf |
| 6 | How do I create a new corpus? | 3.99s | ✅ | HOWTO.pdf | Should return HOWTO.pdf |
| 7 | How do I delete a file from a corpus? | 5.02s | ✅ | HOWTO.pdf | Should return HOWTO.pdf |
| 8 | How do I recover a corpus I accidentally deleted? | 5.0s | ✅ | HOWTO.pdf | Should return HOWTO.pdf |
| 9 | How do I rename a corpus? | 2.79s | ✅ | HOWTO.pdf | Should return HOWTO.pdf |
| 10 | What is search guidance and how does it improve answers? | 4.83s | ❌ | PRODUCT_ROADMAP.pdf, README.pdf | Should return HOWTO.pdf or FILE_GUIDE.pdf |
| 11 | Why does AIStudio use Qdrant instead of ChromaDB? | 5.74s | ❌ | CODEBASE_GUIDE.pdf, HOWTO.pdf, FILE_GUID | Should return architecture_decisions.pdf |
| 12 | How does the citation system work? | 4.69s | ✅ | PRODUCT_ROADMAP.pdf | Should return architecture_decisions.pdf or CODEBASE_GUIDE.pdf |
| 13 | What is the CrossEncoder reranker and what does it do? | 4.01s | ✅ | CODEBASE_GUIDE.pdf, architecture_decisio | Should return architecture_decisions.pdf |
| 14 | How does AIStudio chunk documents for indexing? | 6.8s | ✅ | FILE_GUIDE.pdf, README.pdf, QUICKSTART.p | Should return architecture_decisions.pdf or CODEBASE_GUIDE.pdf |
| 15 | How is the AIStudio codebase organized? | 6.22s | ✅ | CODEBASE_GUIDE.pdf | Should return CODEBASE_GUIDE.pdf |
| 16 | How fast is AIStudio at answering queries? | 3.68s | ✅ | README.pdf | Should return README.pdf |
| 17 | Does using a larger model make queries slower? | 3.3s | ✅ | README.pdf | Should return README.pdf |
| 18 | How do I run a benchmark on my corpus? | 7.63s | ✅ | HOWTO.pdf, HARNESS.pdf | Should return HARNESS.pdf |
| 19 | What commands does AIStudio provide? | 5.59s | ✅ | HOWTO.pdf | Should return FILE_GUIDE.pdf |
| 20 | What does ais_start do? | 3.04s | ✅ | QUICKSTART.pdf, FILE_GUIDE.pdf | Should return FILE_GUIDE.pdf or HOWTO.pdf |
| 21 | How do I set up the SEC 10-K corpus? | 5.45s | ❌ | HOWTO.pdf | Should return QUICKSTART.pdf or README.pdf |

## Detailed Results

****
### 1. install_prerequisites
**Query:** What are the prerequisites for installing AIStudio?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 4.32s | **Pass:** ✅

**Answer:**

> The sources do not explicitly list the prerequisites for installing AIStudio. However, [3] QUICKSTART.pdf describes a guided installation process using the One-Click Installer in v2.0, which suggests that familiarity with terminal commands is required.
>
> A more detailed description of the setup process can be found in [1] dependencies.pdf and [3] QUICKSTART.pdf. According to [3], the `ais_install` command creates and populates the Python virtual environment automatically, but the user needs to have terminal familiarity for this step.
>
> To clarify, we need a source that explicitly lists the prerequisites for installing AIStudio.

**Citations:**

- [1] dependencies.pdf p.1
- [3] QUICKSTART.pdf p.5


****
### 2. install_qdrant
**Query:** How do I install Qdrant on a Mac?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 4.09s | **Pass:** ✅

**Answer:**

> To install Qdrant on a Mac, follow the instructions in [1] QUICKSTART.pdf:
>
> 1. Activate the Virtual Environment:
> ```bash
> source ~/Developer/AIStudio/.venv/bin/activate
> ```
> 2. Start All Services:
> ```bash
> ais_start
> ```
> Alternatively, you can start the services manually:
> ```bash
> # Terminal 1 — Qdrant
> cd ~/qdrant_storage && 
> QDRANT__STORAGE__STORAGE_PATH=~/qdrant_storage qdrant &
>
> # Terminal 2 — Backend
> cd ~/Developer/AIStudio && 
> source .venv/bin/activate
> OLLAMA_KEEP_ALIVE=30m AISTUDIO_STORAGE_PATH=~/Developer/AIStudio/.ais_data ais_start
> ```

**Citations:**

- [1] QUICKSTART.pdf p.5


****
### 3. install_fresh
**Query:** How do I get AIStudio running for the first time?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 4.44s | **Pass:** ✅

**Answer:**

> To get AIStudio running for the first time, follow these steps:
>
> 1. Run `ais_install` to install dependencies and add aliases to your `.zshrc` file.
> 2. Activate the Virtual Environment by running `source ~/Developer/AIStudio/.venv/bin/activate`.
> 3. Start all services by running `ais_start`. This will check whether each service is already running before starting it.
>
> Alternatively, you can start the services manually:
> - Terminal 1: Run `cd ~/qdrant_storage && QDRANT__STORAGE__STORAGE_PATH=~/qdrant_storage qdrant &`
> - Terminal 2: Activate the Virtual Environment by running `source ~/Developer/AIStudio/.venv/bin/activate` and then run `OLLAMA_KEEP_ALIVE=30m AISTUDIO_HOST=localhost ais_start`
>
> These steps are outlined in [1] and verified by [3].

**Citations:**

- [1] QUICKSTART.pdf p.5
- [3] CODEBASE_GUIDE.pdf p.2


****
### 4. troubleshoot_port
**Query:** The backend is not reachable at port 8000 — what do I do?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 4.87s | **Pass:** ✅

**Answer:**

> The problem is described in [1] and [2]. According to [2], the root cause category is [BUG] and the error message is [Errno 48] address already in use.
>
> To resolve this issue, refer to [1]: Verify that the backend is up by running the command `curl http://localhost:8000/health`. If it's not working, try restarting the uvicorn server with a different port or checking if another process is occupying port 8000.
>
> If you want to automate this, as mentioned in [2], an improvement will be made in start.sh (v2.0) by adding a --quiet flag to prevent running Qdrant and ingest in parallel, which causes the logs to mix.
>
> In the meantime, you can manually check if another process is occupying port 8000 by checking your system's process list or by using a tool like lsof.

**Citations:**

- [1] QUICKSTART.pdf p.6
- [2] QA_TESTING_LESSONS_LEARNED.pdf p.5


****
### 5. troubleshoot_wal
**Query:** What is a WAL lock error and how do I fix it?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 5.17s | **Pass:** ✅

**Answer:**

> A WAL lock error is caused by an unclean shutdown, which can occur due to a force-quit, power loss, or crash [1]. The collection name affected by the error will be mentioned in the panic message. To fix this issue:
>
> 1. Run `ais_stop`
> 2. Delete the corrupted collection: `rm -rf ~/qdrant_storage/collections/aistudio_help` (replace with the collection named in the error)
> 3. Run `ais_start`
> 4. Re-ingest the affected corpus via the UI (Add button) [1].
>
> Note that this issue can be prevented by always stopping AIStudio with `ais_stop`, rather than force-quitting the terminal while it is running [1].

**Citations:**

- [1] QUICKSTART.pdf p.9


****
### 6. create_corpus
**Query:** How do I create a new corpus?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 3.99s | **Pass:** ✅

**Answer:**

> To create a new corpus, use the UI in AIStudio:
>
> 1. Open AIStudio, create a new corpus using the "New" button.
> 2. Upload your files using the "Add" button.
>
> If you want to ingest a new corpus from the command line, run:
> ingest --corpus <name> --root data/corpora/<name>/uploads --force
>
> [1]

**Citations:**

- [1] HOWTO.pdf p.4


****
### 7. delete_file
**Query:** How do I delete a file from a corpus?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 5.02s | **Pass:** ✅

**Answer:**

> To delete a file from a corpus, you can move it to the trash folder using:
>
> ```bash
> mv ~/Developer/AIStudio/data/corpora/<name>/uploads/<filename> \
> ~/Developer/AIStudio/data/corpora/<name>/uploads/trash/
> ```
>
> According to [1], deleted files are not permanently deleted and instead move to the trash folder.
>
> If you want to recover a file that has been accidentally deleted from a corpus, follow these steps:
>
> *[truncated — use --full for complete answer]*

**Citations:**

- [1] HOWTO.pdf p.8


****
### 8. recover_corpus
**Query:** How do I recover a corpus I accidentally deleted?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 5.0s | **Pass:** ✅

**Answer:**

> To recover a corpus you accidentally deleted, follow these steps:
>
> 1. First, find the folder in Trash — it may have a timestamp suffix:
> ```
> ls ~/.Trash/ | grep AIStudio_<name>
> ```
> 2. Move it back to its original location and re-ingest:
> ```
> mv ~/.Trash/AIStudio_<name> ~/Developer/AIStudio/data/corpora/<name>
> # Or if it has a timestamp suffix:
> mv ~/.Trash/AIStudio_<name>_<timestamp> ~/Developer/AIStudio/data/corpora/<name>
> ```
> 3. Then re-ingest the corpus using the `--force` flag:
> ```
> AISTUDIO_VECTORSTORE=qdrant PYTHONPATH=src python3 -m local_llm_bot.app.ingest \
> --corpus <name> --root data/corpora/<name>/uploads --force
> ```
> Alternatively, you can also re-upload the files via the UI (Add button) to restore the corpus in Qdrant.
>
> [1]

**Citations:**

- [1] HOWTO.pdf p.4


****
### 9. rename_corpus
**Query:** How do I rename a corpus?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 2.79s | **Pass:** ✅

**Answer:**

> To rename a corpus, use the Rename button in the corpus header in the UI [1]. AIStudio will then automatically rename the directory, cascade the corpus_meta.yaml, and trigger a background re-index. Do not rename corpus folders manually on disk — use the UI only.

**Citations:**

- [1] HOWTO.pdf p.8


****
### 10. search_guidance
**Query:** What is search guidance and how does it improve answers?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 4.83s | **Pass:** ❌

**Answer:**

> Search guidance is a feature in AIStudio that improves retrieval precision by allowing users to provide routing guidance, or hints about which documents answer which kinds of questions [2]. This metadata is injected into the system prompt at query time.
>
> The sources do not address what specific improvements search guidance brings to answers. However, they mention that it improves retrieval precision [2].
>
> In version v2.0, corpus metadata creation will be made easier with UI fields in the New Corpus modal, which supports search guidance [1].
>
> A one-click installer is also being developed for AIStudio's setup process, making installation faster and easier without requiring terminal familiarity [1].

**Citations:**

- [1] PRODUCT_ROADMAP.pdf p.3
- [2] README.pdf p.1

**⚠ Model said 'no information' — possible retrieval miss**

****
### 11. why_qdrant
**Query:** Why does AIStudio use Qdrant instead of ChromaDB?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 5.74s | **Pass:** ❌

**Answer:**

> [2] does not address why AIStudio uses Qdrant instead of ChromaDB.
>
> The sources do not address this question directly, but we can look at [1]. According to [1], the ingest layer uses Qdrant for storing documents. It mentions that "the ingest pipeline lives in src/local_llm_bot/app/ingest/", suggesting that there might be more information about why Qdrant is used instead of ChromaDB in the architecture decisions.
>
> [3] provides a version history but does not address this question.
>
> [4] discusses lessons learned from testing, including an issue with multi-line commands in PDFs, but it does not provide any information on why AIStudio uses Qdrant instead of ChromaDB.
>
> *[truncated — use --full for complete answer]*

**Citations:**

- [1] CODEBASE_GUIDE.pdf p.2
- [2] HOWTO.pdf p.1
- [3] FILE_GUIDE.pdf p.4
- [4] QA_TESTING_LESSONS_LEARNED.pdf p.2

**⚠ Model said 'no information' — possible retrieval miss**

****
### 12. how_citations
**Query:** How does the citation system work?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 4.69s | **Pass:** ✅

**Answer:**

> The citation system works as follows:
>
> When a user clicks on a citation, the PDF opens at the exact page with the cited passage highlighted [2]. This is currently a known limitation in the Beta release, but it will be fixed in v2.0 through the Source Dive feature, which will allow users to click on a citation and open the PDF directly at that page [2].
>
> To enable this feature, the backend already stores chunk-level page positions in Qdrant [2]. However, the remaining work is to implement the frontend PDF viewer (PDF.js) [2].

**Citations:**

- [2] PRODUCT_ROADMAP.pdf p.2


****
### 13. crossencoder
**Query:** What is the CrossEncoder reranker and what does it do?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 4.01s | **Pass:** ✅

**Answer:**

> The CrossEncoder reranker is a two-stage retrieval architecture that uses the ms-marco-MiniLM-L-6-v2 model as a reranking pass after vector search, before prompt assembly [2]. This model reads query + chunk concatenated as a single input, with full attention across both, and scores relevance directly rather than approximating via cosine distance [2].
>
> The CrossEncoder reranker is used to improve answer quality significantly with minimal latency overhead by reordering the top-K retrieved chunks against the query [1]. It addresses vocabulary mismatch issues that can arise from bi-encoder compression, where semantically equivalent queries or chunks may have different vector representations due to differences in vocabulary [2].

**Citations:**

- [1] CODEBASE_GUIDE.pdf p.6
- [2] architecture_decisions.pdf p.6


****
### 14. chunking
**Query:** How does AIStudio chunk documents for indexing?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 6.8s | **Pass:** ✅

**Answer:**

> [1] states that "Documents live in data/corpora/<corpus-name>/uploads/ . When you delete a file from the UI, it moves to data/corpora/<corpus-name>/trash/ — it's never permanently destroyed." This implies that documents are stored on disk before being indexed.
>
> [2] mentions that "Filtering happens at the system (vector) layer — not post-hoc on results." However, this is related to filtering rather than chunking for indexing.
>
> The crucial source is [3], which does not directly address chunking. Moving to [4]:
>
> [4] mentions that AIStudio uses markers at each page boundary during extraction, and these markers flow through the chunking pipeline into Qdrant payload (page field) and chunk_id format (filename::page-N::chunk-M). However, this is related to citation and PDF viewer functionality rather than document chunking for indexing.
>
> *[truncated — use --full for complete answer]*

**Citations:**

- [1] FILE_GUIDE.pdf p.2
- [2] README.pdf p.2
- [3] QUICKSTART.pdf p.7
- [4] dependencies.pdf p.4


****
### 15. codebase_structure
**Query:** How is the AIStudio codebase organized?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 6.22s | **Pass:** ✅

**Answer:**

> The AIStudio codebase is organized in the following structure:
>
> * `src/` directory contains all application code.
> * `tests/` directory contains the test suite at the repo root.
> * `front_end/` directory contains a single HTML file (`rag_studio.html`) that serves as the entire frontend. [1]
> * The three-layer architecture consists of:
> 	+ Ingest layer: handles document loading, chunking, embedding, and storage in Qdrant (located in `src/local_llm_bot/app/ingest/`). [1]
> 	+ Query layer: a FastAPI backend receives questions, retrieves chunks from Qdrant, reranks them with CrossEncoder, assembles prompts, and sends them to the Ollama-hosted LLM. The query pipeline lives in `src/local_llm_bot/app/rag_core.py` and is orchestrated by `api.py`. [1]
> 	+ UI layer: a single HTML file provides the user interface for corpus management, file upload, chat, settings, and citations rendering. It communicates with the FastAPI backend over localhost. [1]
> * The three services that must be running are Qdrant (vector store), Ollama (LLM host), and the FastAPI backend (uvicorn). The `ais_start` command starts all three. [1]

**Citations:**

- [1] CODEBASE_GUIDE.pdf p.1


****
### 16. latency
**Query:** How fast is AIStudio at answering queries?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 3.68s | **Pass:** ✅

**Answer:**

> AIStudio's query latency is approximately 6-7 seconds on average, after the model has loaded into memory.
>
> [2]
> ama3.1:70b and warm llama3.1:8b are statistically identical in 
> query latency on Apple Silicon (~6–7s average).
>
> Note that there may be a slower first query in a cold session (20-50 seconds) due to LLM loading into memory, but subsequent queries run at the 6-7 second rate.
>
> [2]

**Citations:**

- [2] README.pdf p.3


****
### 17. model_size_latency
**Query:** Does using a larger model make queries slower?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 3.3s | **Pass:** ✅

**Answer:**

> Using a larger model may not necessarily make queries slower. [3] states that warm llama3.1:70b and warm llama3.1:8b have identical query latency (~6–7s) on Apple Silicon, suggesting that the size of the model is not a significant factor in determining latency once it is loaded into unified memory.

**Citations:**

- [3] README.pdf p.3


****
### 18. run_benchmark
**Query:** How do I run a benchmark on my corpus?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 7.63s | **Pass:** ✅

**Answer:**

> To run a benchmark on your corpus, you can use the `ais_bench` command.
>
> According to [2], "The benchmark harness serves two purposes: - Performance — measures query latency per question - Veracity — validates answer quality against a questions file"
>
> You can run all 12 demo questions against the demo corpus and write a timestamped report to benchmarks/demo/reports/ by running:
> ```
> ais_bench
> ```
> According to [2], "This runs all 12 demo questions against the demo corpus and writes a timestamped report to benchmarks/demo/reports/."
>
> If you want to benchmark a different corpus, you can use the `--corpus` option followed by the name of your corpus. For example:
> ```
> ais_bench --corpus <your_corpus_name>
> ```
> According to [2], "Reports are written to benchmarks/<corpus>/reports/ as paired .md and .json files, named by corpus and timestamp."
>
> *[truncated — use --full for complete answer]*

**Citations:**

- [1] HOWTO.pdf p.6
- [2] HARNESS.pdf p.1


****
### 19. all_commands
**Query:** What commands does AIStudio provide?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 5.59s | **Pass:** ✅

**Answer:**

> According to [2], after running `./ais_install` from the repository root, these commands are available from any terminal:
>
> * `ais_start`: Start all AIStudio services and opens the UI in your browser.
> * `ais_stop`: Stop all AIStudio services cleanly.
> * `ais_restart`: Stop then restart all AIStudio services.
> * `ais_bench`: Run a benchmark on the demo corpus.
> * `ais_log`: Tail live AIStudio backend log — run in a separate tab after `ais_start`.
> * `ais_download_sec_10k`: Download SEC 10-K filings from EDGAR to `~/Downloads/sec_10k/` (~2 GB).
> * `ais_ingest_sec_10k`: Ingest SEC 10-K corpus into AIStudio (~30 min, backend must be running).
>
> Additionally, every command supports the `--help` flag, which can be used to print a help message. For example:
>
> ```
> ais_start --help
> ```
>
> *[truncated — use --full for complete answer]*

**Citations:**

- [2] HOWTO.pdf p.1


****
### 20. ais_start
**Query:** What does ais_start do?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 3.04s | **Pass:** ✅

**Answer:**

> [1] ais_start starts all AIStudio services and opens the UI in your browser.
>
> Alternatively, [3] also states that ais_start "Starts all AIStudio services and ... opens the UI" (emphasis mine).

**Citations:**

- [1] QUICKSTART.pdf p.5
- [3] FILE_GUIDE.pdf p.1


****
### 21. sec_10k
**Query:** How do I set up the SEC 10-K corpus?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 5.45s | **Pass:** ❌

**Answer:**

> To set up the SEC 10-K corpus, follow these steps:
>
> Step 1 — Download the filings to ~/Downloads/sec_10k/ (~5 min, ~2 GB):
> ais_download_sec_10k [1]
>
> Step 2 — Ingest using the AIStudio UI:
> Open AIStudio, create a new corpus named sec_10k, then upload the files from ~/Downloads/sec_10k/ using the Upload button. This is the same process as ingesting any corpus you build yourself — the download step is what's special [1].
>
> Allow ~34 minutes for ingestion to complete.
>
> *[truncated — use --full for complete answer]*

**Citations:**

- [1] HOWTO.pdf p.4

**⚠ Model said 'no information' — possible retrieval miss**
