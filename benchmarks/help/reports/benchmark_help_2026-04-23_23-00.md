# AIStudio — Benchmark Findings
*Generated: 2026-04-23 23:02*

## Configuration
- **Corpus:** `help`
- **Top K:** 5
- **Temperature:** 0.3
- **Model:** API default
- **API:** http://localhost:8000

## Summary
- **Questions:** 21
- **Passed:** 16/21 (76%)
- **Avg latency:** 4.8s

## Infrastructure
- Vector store: Qdrant 1.17.0 (Apple Silicon, local)
- Embedding model: nomic-embed-text (768 dimensions, cosine similarity)
- Reranker: CrossEncoder ms-marco-MiniLM-L-6-v2
- Corpus: `help` (see corpus stats in UI)

## Results

| # | Description | Latency | Pass | Citations | Notes |
|---|-------------|---------|------|-----------|-------|
| 1 | What are the prerequisites for installing AIStudio? | 7.16s | ❌ | dependencies.pdf | Should return QUICKSTART.pdf |
| 2 | How do I install Qdrant on a Mac? | 7.02s | ✅ | CODEBASE_GUIDE.pdf, QUICKSTART.pdf | Should return QUICKSTART.pdf |
| 3 | How do I get AIStudio running for the first time? | 4.58s | ✅ | QUICKSTART.pdf | Should return QUICKSTART.pdf |
| 4 | The backend is not reachable at port 8000 — what do I do? | 5.77s | ❌ | — | Should return QUICKSTART.pdf or HOWTO.pdf |
| 5 | What is a WAL lock error and how do I fix it? | 4.95s | ✅ | QUICKSTART.pdf | Should return QUICKSTART.pdf |
| 6 | How do I create a new corpus? | 3.3s | ✅ | HOWTO.pdf | Should return HOWTO.pdf |
| 7 | How do I delete a file from a corpus? | 4.38s | ✅ | HOWTO.pdf | Should return HOWTO.pdf |
| 8 | How do I recover a corpus I accidentally deleted? | 3.83s | ✅ | HOWTO.pdf | Should return HOWTO.pdf |
| 9 | How do I rename a corpus? | 3.03s | ✅ | HOWTO.pdf | Should return HOWTO.pdf |
| 10 | What is search guidance and how does it improve answers? | 3.78s | ❌ | README.pdf | Should return HOWTO.pdf or FILE_GUIDE.pdf |
| 11 | Why does AIStudio use Qdrant instead of ChromaDB? | 3.48s | ❌ | CODEBASE_GUIDE.pdf | Should return architecture_decisions.pdf |
| 12 | How does the citation system work? | 3.91s | ❌ | README.pdf, PRODUCT_ROADMAP.pdf | Should return architecture_decisions.pdf or CODEBASE_GUIDE.pdf |
| 13 | What is the CrossEncoder reranker and what does it do? | 4.18s | ✅ | architecture_decisions.pdf | Should return architecture_decisions.pdf |
| 14 | How does AIStudio chunk documents for indexing? | 3.65s | ✅ | dependencies.pdf | Should return architecture_decisions.pdf or CODEBASE_GUIDE.pdf or FILE_GUIDE.pdf |
| 15 | How is the AIStudio codebase organized? | 6.18s | ✅ | CODEBASE_GUIDE.pdf | Should return CODEBASE_GUIDE.pdf |
| 16 | How fast is AIStudio at answering queries? | 4.51s | ✅ | QUICKSTART.pdf, README.pdf | Should return README.pdf |
| 17 | Does using a larger model make queries slower? | 4.61s | ✅ | HOWTO.pdf, README.pdf | Should return README.pdf |
| 18 | How do I run a benchmark on my corpus? | 6.0s | ✅ | HARNESS.pdf | Should return HARNESS.pdf |
| 19 | What commands does AIStudio provide? | 8.09s | ✅ | FILE_GUIDE.pdf, HOWTO.pdf, QUICKSTART.pd | Should return FILE_GUIDE.pdf |
| 20 | What does ais_start do? | 4.23s | ✅ | QUICKSTART.pdf, FILE_GUIDE.pdf | Should return FILE_GUIDE.pdf or HOWTO.pdf |
| 21 | How do I set up the SEC 10-K corpus? | 3.84s | ✅ | HOWTO.pdf | Should return QUICKSTART.pdf or README.pdf |

## Detailed Results

****
### 1. install_prerequisites
**Query:** What are the prerequisites for installing AIStudio?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 7.16s | **Pass:** ❌

**Answer:**

> The prerequisites for installing AIStudio are:
>
> 1. Install Homebrew [1]
>    - Check if it's already installed:
>      brew --version
>    - If not, install it with a one-liner command that downloads and runs an installer script:
>      /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
>    - Run three lines to add Homebrew to your PATH:
>      echo >> ~/.zprofile
>      echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
>      eval "$(/opt/homebrew/bin/brew shellenv)"
>
> 2. Install Python 3.13 [1]
>    - Check if you already have Python 3.10 or later:
>      python3 --version
>    - If not, install it with a command that installs the required version:
>      (no specific command is provided in the sources for installing a specific version of Python)
>
> Note: The sources do not address the installation of dependencies for AIStudio beyond Homebrew and Python.

**Citations:**

- [1] dependencies.pdf p.1

**⚠ Model said 'no information' — possible retrieval miss**

****
### 2. install_qdrant
**Query:** How do I install Qdrant on a Mac?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 7.02s | **Pass:** ✅

**Answer:**

> To install Qdrant on a Mac, you need to follow the steps outlined in [3] QUICKSTART.pdf.
>
> First, ensure that Homebrew is installed by running `brew --version`. If it's already installed, skip to installing Python 3.13. Otherwise, install Homebrew using the provided instructions: 
> /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
> Then, add Homebrew to your PATH:
> echo >> ~/.zprofile
> echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
> eval "$(/opt/homebrew/bin/brew shellenv)"
>
> Next, install the pango system library required for PDF generation: `brew install pango`
>
> After that, check if you already have Python 3.10 or later installed by running `python3 --version`. If it's not installed or is lower than 3.10, install Python 3.13:
>
> *[truncated — use --full for complete answer]*

**Citations:**

- [1] CODEBASE_GUIDE.pdf p.2
- [3] QUICKSTART.pdf p.2


****
### 3. install_fresh
**Query:** How do I get AIStudio running for the first time?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 4.58s | **Pass:** ✅

**Answer:**

> To get AIStudio running for the first time, follow these steps:
>
> 1. Open Terminal first by pressing ⌘ Space, typing "Terminal", and pressing Enter.
> 2. Use python3 instead of python on macOS, as specified in [1].
> 3. Create a folder for your development projects using the command:
> ```bash
> mkdir -p ~/Developer
> ```
> 4. Clone the AIStudio repository from GitHub by running:
> ```bash
> cd ~/Developer
> git clone git@github.com:mbarberony/AIStudio.git
> cd AIStudio
> ```
> 5. Install AIStudio commands by running:
> ```bash
> ./ais_install
> ```
> 6. Verify that Qdrant is installed and functioning correctly, as specified in [1].
> 7. Run `ais_start` to start the services, including Qdrant, Ollama, and the FastAPI backend.
>
> [1] states that you should see all green checkmarks after running `./ais_install`, indicating that the environment has been verified and dependencies have been installed successfully.

**Citations:**

- [1] QUICKSTART.pdf p.1


****
### 4. troubleshoot_port
**Query:** The backend is not reachable at port 8000 — what do I do?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 5.77s | **Pass:** ❌

**Answer:**

> You are experiencing an issue where the backend is not reachable at port 8000.
>
> To resolve this, you can try killing the old process and restarting uvicorn. However, since the current implementation does not have a fix for this issue, it's recommended to add a preflight check script that would catch this error automatically.
>
> Here are some potential steps to troubleshoot and resolve this issue:
>
> 1. Check if port 8000 is occupied by running:
> ```
> lsof -i :8000
> ```
>
> *[truncated — use --full for complete answer]*


****
### 5. troubleshoot_wal
**Query:** What is a WAL lock error and how do I fix it?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 4.95s | **Pass:** ✅

**Answer:**

> A WAL lock error is caused by a collection's write-ahead log being left locked from an unclean shutdown ([1], page 9). To fix it, follow these steps:
>
> 1. Stop Qdrant with `ais_stop`.
> 2. Delete the affected collection using `rm -rf ~/qdrant_storage/collections/aistudio_help # replace with collection named in error`. Note that only the specific collection should be deleted, not the entire `qdrant_storage/` folder.
> 3. Restart Qdrant with `ais_start`.
> 4. Re-ingest the affected corpus via the UI (Add button).
>
> To prevent this issue from occurring in the future, always stop Qdrant cleanly with `ais_stop`, and never force-quit the terminal while running ([1], page 9).

**Citations:**

- [1] QUICKSTART.pdf p.10


****
### 6. create_corpus
**Query:** How do I create a new corpus?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 3.3s | **Pass:** ✅

**Answer:**

> To create a new corpus, use the UI — open AIStudio, create a new corpus using the New button, then upload your files using the Add button ([1]). AIStudio handles ingestion automatically and shows progress in the chat area.
>
> If you need to ingest the SEC 10-K corpus, follow these steps: download the filings to ~/Downloads/sec_10k/ using `ais_download_sec_10k`, then ingest using the AIStudio UI by uploading the files from ~/Downloads/sec_10k/ using the Upload button ([1]).

**Citations:**

- [1] HOWTO.pdf p.3


****
### 7. delete_file
**Query:** How do I delete a file from a corpus?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 4.38s | **Pass:** ✅

**Answer:**

> To delete a file from a corpus, you cannot directly delete it using the UI or terminal commands. However, you can move it to trash and then re-ingest the corpus to restore the file.
>
> First, see what's in trash:
> ```bash
> ls ~/Developer/AIStudio/data/corpora/<name>/uploads/trash/
> ```
> Then, move the desired file back to its original location:
> ```bash
> mv ~/Developer/AIStudio/data/corpora/<name>/uploads/trash/<filename> \
> ~/Developer/AIStudio/data/corpora/<name>/uploads/
> ```
> Finally, re-ingest the corpus using the --force flag to restore the file:
> ```
> AISTUDIO_VECTORSTORE=qdrant PYTHONPATH=src python3 -m local_llm_bot.app.ingest \
> --corpus <name> --root data/corpora/<name>/uploads --force
> ```
> [1]

**Citations:**

- [1] HOWTO.pdf p.8


****
### 8. recover_corpus
**Query:** How do I recover a corpus I accidentally deleted?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 3.83s | **Pass:** ✅

**Answer:**

> To recover a corpus you accidentally deleted, follow these steps:
>
> 1. Find the folder in Trash — it may have a timestamp suffix:
> ```bash
> ls ~/.Trash/ | grep AIStudio_<name>
> ```
> 2. Move it back and re-ingest:
> ```bash
> mv ~/.Trash/AIStudio_<name> ~/Developer/AIStudio/data/corpora/<name>
> # Or if it has a timestamp suffix:
> mv ~/.Trash/AIStudio_<name>_<timestamp> ~/Developer/AIStudio/data/corpora/<name>
> ```
> 3. Then re-upload the files via the UI (Add button) to restore the corpus in Qdrant.
>
> [1]

**Citations:**

- [1] HOWTO.pdf p.3


****
### 9. rename_corpus
**Query:** How do I rename a corpus?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 3.03s | **Pass:** ✅

**Answer:**

> To rename a corpus in AIStudio, use the Rename button in the corpus header in the UI. AIStudio renames the directory, cascades the corpus_meta.yaml, and triggers a background re-index automatically [1].
>
> If you need to rename files or folders after ingestion, do not manually modify them on disk. Instead, delete the corpus via the UI, recreate it, and re-ingest with the correct filenames [1].

**Citations:**

- [1] HOWTO.pdf p.8


****
### 10. search_guidance
**Query:** What is search guidance and how does it improve answers?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 3.78s | **Pass:** ❌

**Answer:**

> Search guidance is a feature that allows users to provide metadata when creating a corpus, which includes hints about which documents answer which kinds of questions [2]. This metadata is injected into the system prompt at query time to improve retrieval precision [2].
>
> The sources do not address how search guidance improves answers directly.

**Citations:**

- [2] README.pdf p.1

**⚠ Model said 'no information' — possible retrieval miss**

****
### 11. why_qdrant
**Query:** Why does AIStudio use Qdrant instead of ChromaDB?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 3.48s | **Pass:** ❌

**Answer:**

> According to [1] architecture overview, the ingest layer stores documents in Qdrant, a vector store.
>
> The sources do not address why Qdrant is used instead of ChromaDB.

**Citations:**

- [1] CODEBASE_GUIDE.pdf p.2

**⚠ Model said 'no information' — possible retrieval miss**

****
### 12. how_citations
**Query:** How does the citation system work?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 3.91s | **Pass:** ❌

**Answer:**

> The citation system works as follows:
>
> When you click on a citation in the chat interface, the PDF opens at the exact page with the cited passage highlighted. This is currently possible for document name and page number, but Source Dive will allow clicking a citation to open the PDF at the exact page with the cited passage highlighted.
>
> [1]
> The sources do not address how citations are initially generated or linked to specific passages in the PDFs. However, it does mention that "the backend already stores chunk-level page positions in Qdrant" which is related to Source Dive feature.
>
>  The citation system is described as "inline source citations ( [1] , [2] )" and is available for questions asked in plain English through the chat interface.

**Citations:**

- [1] README.pdf p.2
- [2] PRODUCT_ROADMAP.pdf p.2

**⚠ Model said 'no information' — possible retrieval miss**

****
### 13. crossencoder
**Query:** What is the CrossEncoder reranker and what does it do?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 4.18s | **Pass:** ✅

**Answer:**

> The CrossEncoder reranker is a two-stage retrieval architecture that improves answer quality with minimal latency overhead [2]. It consists of two stages:
>
> 1. Stage 1: Qdrant HNSW vector search, which retrieves top-K candidates quickly [2].
> 2. Stage 2: CrossEncoder reranking, which reorders the retrieved chunks by true relevance [2].
>
> The CrossEncoder reads query + chunk concatenated as a single input with full attention across both, scoring relevance directly rather than approximating via cosine distance [2]. It is fine-tuned on MS MARCO (500K passage relevance pairs) and has 22M parameters, loads in <1s on Apple Silicon [2].
>
> The use of the CrossEncoder reranker addresses vocabulary mismatch that occurs when using bi-encoder compression, where semantically equivalent chunks are vector-distant [2].

**Citations:**

- [2] architecture_decisions.pdf p.6


****
### 14. chunking
**Query:** How does AIStudio chunk documents for indexing?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 3.65s | **Pass:** ✅

**Answer:**

> AIStudio chunks documents for indexing using pdfplumber to extract page numbers and markers at each page boundary during extraction [3]. The extracted data flows through the chunking pipeline into Qdrant payload (page field) and chunk_id format (filename::page-N::chunk-M), enabling page numbers in citations and the PDF viewer Open ↗ feature.

**Citations:**

- [3] dependencies.pdf p.4


****
### 15. codebase_structure
**Query:** How is the AIStudio codebase organized?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 6.18s | **Pass:** ✅

**Answer:**

> The AIStudio codebase is organized as follows:
>
> * The first-level directory structure is: AIStudio/
> 	+ src/ Application source code
> 	+ tests/ Test suite
> 	+ front_end/ Single-file frontend (see [1])
> * The architecture has three layers:
> 	+ Ingest layer — documents are loaded, chunked, embedded, and stored in Qdrant. This is a one-time operation per document, triggered via the UI. The ingest pipeline lives in src/local_llm_bot/app/ingest/. ([1])
> 	+ Query layer — a FastAPI backend receives questions, retrieves relevant chunks from Qdrant, reranks them with a CrossEncoder, assembles a prompt, and sends it to an Ollama-hosted LLM. Citations are extracted from the response and returned to the frontend. The query pipeline lives in src/local_llm_bot/app/rag_core.py and is orchestrated by api.py . ([1])
> 	+ UI layer — a single HTML file provides the complete user interface: corpus management, file upload, chat, settings, and citations rendering. It communicates with the FastAPI backend over localhost. ([1])
> * The three services that must be running are: Qdrant (vector store), Ollama (LLM host), and the FastAPI backend (uvicorn). ais_start starts all three. ([1])
>
> Note: The sources provided do not address the question of how the codebase is organized in detail, but rather provide a high-level overview of the architecture and directory structure.

**Citations:**

- [1] CODEBASE_GUIDE.pdf p.1


****
### 16. latency
**Query:** How fast is AIStudio at answering queries?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 4.51s | **Pass:** ✅

**Answer:**

> The latency of AIStudio's queries is around ~6–7 seconds once the model is loaded into memory, also known as a "warm" session [1]. This is consistent with the benchmark results in README.pdf, which states that warm llama3.1:70b and llama3.1:8b models have identical query latency on Apple Silicon (~6–7s average) [2]. The first query after startup can take longer, typically around 10–15 seconds to load the model into memory (the "cold start") [1].

**Citations:**

- [1] QUICKSTART.pdf p.5
- [2] README.pdf p.3


****
### 17. model_size_latency
**Query:** Does using a larger model make queries slower?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 4.61s | **Pass:** ✅

**Answer:**

> According to [3], using a larger model does not necessarily make queries slower. In fact, the authors mention that "model size stops being a latency variable" once the model is loaded into unified memory, as seen in models like llama3.1:70b and llama3.1:8b on Apple Silicon, which have identical query latency (~6–7s) [4].
>
> However, it's worth noting that having more context can increase latency slightly, but only by a small margin. The recommended setting for Top K is 5, which gives good results for most queries, and adjusting this value can impact latency [3].

**Citations:**

- [3] HOWTO.pdf p.6
- [4] README.pdf p.3


****
### 18. run_benchmark
**Query:** How do I run a benchmark on my corpus?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 6.0s | **Pass:** ✅

**Answer:**

> To run a benchmark on your corpus, you need to use the `ais_bench` command. To do this, follow these steps:
>
> 1. First, make sure the backend is running by using the `ais_start` command.
> 2. Then, run the following command:
> ```
> ais_bench
> ```
> This will run all 12 demo questions against the demo corpus and write a timestamped report to `benchmarks/demo/reports/`.
>
> If you want to benchmark a different corpus, you can specify it using the `--corpus` option:
> ```
> ais_bench --corpus <corpus_name>
> ```
> Replace `<corpus_name>` with the name of your corpus.
>
> You can also customize the benchmark settings by adding options such as `--top-k`, `--temperature`, and `--model`. For example:
> ```
> ais_bench --corpus sec_10k --top-k 10 --temperature 0.1
> ```
> This will run a benchmark on the SEC 10-K corpus with a top-k value of 10 and a temperature of 0.1.
>
> *[truncated — use --full for complete answer]*

**Citations:**

- [2] HARNESS.pdf p.1


****
### 19. all_commands
**Query:** What commands does AIStudio provide?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 8.09s | **Pass:** ✅

**Answer:**

> The available commands in AIStudio are:
>
> [1]
> Command What it does When to use it
> Starts all AIStudio services and opens the UI ais_start Beginning of every session
> Stops all AIStudio services ais_stop End of every session cleanly
> Debugging; watching queries in real time ais_log Shows the live backend log
> Runs the benchmark suite against a corpus ais_bench Validating retrieval quality
> Downloads SEC 10-K filings from EDGAR (optional) ais_download_sec_10k Setting up the SEC corpus
> Ingests SEC 10-K filings into AIStudio ais_ingest_sec_10k After downloading SEC filings
>
> [1] also lists additional commands:
> Command What it does When to use it
> Shows the command reference ais_help When you forget a command
> Installs or updates AIStudio ais_install Fresh install; adding a new com
>
> [2]
> Command What it does When to use it
> Install AIStudio user commands — ais_install [cmd] adds a single command, ais_install --verify checks all aliases
> Starts all services and opens the UI in your browser ais_start 
> Stops all services ais_stop 
> Run a benchmark on the demo corpus ais_bench 
> Tail live AIStudio backend log — run in a separate tab after ais_start ais_log 
> Download SEC 10-K filings from EDGAR to ~/Downloads/sec_10k/ (~2 GB) ais_download_sec_10k 
> Ingest SEC 10-K corpus into AIStudio (~30 min, backend must be running) ais_ingest_sec_10k 
> Print this command reference ais_help 
> Every command supports --help : ais_start --help ais_bench --help
>
> *[truncated — use --full for complete answer]*

**Citations:**

- [1] FILE_GUIDE.pdf p.1
- [2] HOWTO.pdf p.1
- [3] QUICKSTART.pdf p.2
- [4] QA_TESTING_LESSONS_LEARNED.pdf p.2


****
### 20. ais_start
**Query:** What does ais_start do?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 4.23s | **Pass:** ✅

**Answer:**

> According to [1], ais_start handles activating the virtual environment automatically, but if running Python commands directly, you need to activate manually. It also starts all services — Qdrant, Ollama, the FastAPI backend, and the frontend — and opens the UI in your browser automatically.
>
> Additionally, according to [3], ais_start is a command that "Starts all AIStudio services and opens the UI" when used at the beginning of every session.

**Citations:**

- [1] QUICKSTART.pdf p.7
- [3] FILE_GUIDE.pdf p.1


****
### 21. sec_10k
**Query:** How do I set up the SEC 10-K corpus?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 3.84s | **Pass:** ✅

**Answer:**

> To set up the SEC 10-K corpus, follow these steps:
>
> Step 1 — Download the filings to `~/Downloads/sec_10k/` (~5 min, ~2 GB):
> ```bash
> ais_download_sec_10k
> ```
> This command automates what would be a complex multi-step download.
>
> Step 2 — Ingest using the AIStudio UI:
> Open AIStudio, create a new corpus named `sec_10k`, then upload the files from `~/Downloads/sec_10k/` using the Upload button. This is the same process as ingesting any corpus you build yourself — the download step is what's special.
>
> Allow ~34 minutes for ingestion to complete.
>
> *[truncated — use --full for complete answer]*

**Citations:**

- [1] HOWTO.pdf p.5

