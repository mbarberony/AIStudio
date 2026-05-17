# AIStudio — Benchmark Findings
*Generated: 2026-04-19 18:36*

## Configuration
- **Corpus:** `help`
- **Top K:** 5
- **Temperature:** 0.3
- **Model:** API default
- **API:** http://localhost:8000

## Summary
- **Questions:** 20
- **Passed:** 19/20 (95%)
- **Avg latency:** 4.0s

## Infrastructure
- Vector store: Qdrant 1.17.0 (Apple Silicon, local)
- Embedding model: nomic-embed-text (768 dimensions, cosine similarity)
- Reranker: CrossEncoder ms-marco-MiniLM-L-6-v2
- Corpus: `help` (see corpus stats in UI)

## Results

| # | Description | Latency | Pass | Citations | Notes |
|---|-------------|---------|------|-----------|-------|
| 1 | How is Qdrant installed in AIStudio and why is it not available via Homebrew? | 5.99s | ❌ | CODEBASE_GUIDE.pdf, PRODUCT_ROADMAP.pdf | QUICKSTART-specific — covers the direct binary install method. Cannot be answered from general knowledge.
 |
| 2 | What command activates the AIStudio Python virtual environment and what prompt change confirms it? | 2.82s | ✅ | QUICKSTART.pdf | QUICKSTART Step 8 — specific to AIStudio's venv path and prompt indicator.
 |
| 3 | What system library does WeasyPrint require and how is it installed on macOS for AIStudio? | 2.92s | ✅ | dependencies.pdf, QUICKSTART.pdf | QUICKSTART Step 1 — pango is required by WeasyPrint for PDF generation. WeasyPrint keyword forces the right chunk.
 |
| 4 | What causes the Qdrant WAL lock error and how do you fix it? | 4.1s | ✅ | QUICKSTART.pdf | HOWTO troubleshooting section — specific error pattern with specific fix.
 |
| 5 | Why did AIStudio switch from ChromaDB to Qdrant as the vector store? | 4.42s | ✅ | QUICKSTART.pdf, dependencies.pdf | architecture_decisions.md — explicit ADR with stated rationale.
 |
| 6 | What is the CrossEncoder model used for in AIStudio and why was it added? | 2.82s | ✅ | CODEBASE_GUIDE.pdf | architecture_decisions.md — reranking ADR. Specific model name required.
 |
| 7 | Why does AIStudio use a single HTML file for the entire frontend? | 3.75s | ✅ | CODEBASE_GUIDE.pdf, architecture_decisio | CODEBASE_GUIDE and architecture_decisions — offline-first design decision.
 |
| 8 | What is the purpose of the corpus metadata YAML file and when is it loaded? | 3.79s | ✅ | architecture_decisions.pdf, HOWTO.pdf | CODEBASE_GUIDE — corpus_meta.yaml loaded into system prompt at query time.
 |
| 9 | What four processes does ais_start launch and how do you verify the backend is running? | 4.31s | ✅ | QUICKSTART.pdf | QUICKSTART Step 9 — specific to AIStudio's four-process architecture.
 |
| 10 | What is the full command to ingest the demo corpus from the terminal? | 4.52s | ✅ | HOWTO.pdf | QUICKSTART Step 10 — specific command with environment variables.
 |
| 11 | What are the default parameters when running ais_bench with no arguments? | 5.52s | ✅ | HARNESS.pdf, QUICKSTART.pdf | HOWTO or QUICKSTART benchmark section — specific defaults.
 |
| 12 | What did AIStudio benchmarks reveal about the latency difference between llama3.1:8b and llama3.1:70b on Apple Silicon? | 4.18s | ✅ | README.pdf, QUICKSTART.pdf | README benchmark finding — statistically indistinguishable warm latency. Strong proof point, specific to AIStudio testing.
 |
| 13 | What happens to a file when it is deleted from a corpus in AIStudio? | 4.99s | ✅ | HOWTO.pdf | HOWTO — file moved to trash/, Qdrant chunks removed surgically.
 |
| 14 | How do you create a new corpus in the AIStudio UI? | 2.89s | ✅ | HOWTO.pdf | HOWTO — UI-specific workflow for corpus creation.
 |
| 15 | What does the AIStudio demo corpus contain and what time period does it cover? | 3.85s | ✅ | QUICKSTART.pdf, DEMO_CORPUS.pdf | DEMO_CORPUS.md and README — curated 9-document corpus, 2003-2026.
 |
| 16 | What does the QUICKSTART troubleshooting section say to do when you see "Failed to fetch in UI" and the FastAPI backend is down? | 3.51s | ✅ | QUICKSTART.pdf | QUICKSTART page 9 — chunk contains exact phrase "Failed to fetch in UI" followed by kill $(lsof -ti:8000) command. Keywords match the fix commands in that specific chunk.
 |
| 17 | Why does AIStudio require Python 3.10 or later and what fails on 3.9? | 4.29s | ✅ | QUICKSTART.pdf | QUICKSTART prerequisites — float | None syntax incompatibility.
 |
| 18 | What happened when a user copy-pasted the Qdrant install command from the AIStudio PDF during a fresh Mac install, and what was the fix? | 6.05s | ✅ | QA_TESTING_LESSONS_LEARNED.pdf, HOWTO.pd | QA_TESTING_LESSONS_LEARNED.pdf showstopper #2 — PDF line-wrapping broke the Qdrant PATH command across lines, corrupting ~/.zshrc. Fix was single-line &&-chained command. Very specific — cannot come from QUICKSTART.
 |
| 19 | What are the criteria for AIStudio to reach Beta status? | 3.08s | ✅ | PRODUCT_ROADMAP.pdf, CODEBASE_GUIDE.pdf | PRODUCT_ROADMAP.md — specific Beta gate requirements.
 |
| 20 | What is the primary new capability planned for AIStudio v2.0? | 2.68s | ✅ | PRODUCT_ROADMAP.pdf | PRODUCT_ROADMAP.md — v2.0 headline feature. |

## Detailed Results

### qdrant_install_method
**Query:** How is Qdrant installed in AIStudio and why is it not available via Homebrew?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 5.99s | **Pass:** ❌

**Answer:**

> Qdrant is installed in AIStudio through the ingest layer, which loads documents, chunks them, embeds them, and stores them in Qdrant as part of a one-time operation per document [1].
>
> However, Qdrant is not available via Homebrew. The sources do not address how Qdrant is made available for installation.
>
> To start the services that must be running (Qdrant, Ollama, FastAPI backend), run: 
> ais_start
>
> This command starts all three services [1].
>
> *[truncated — use --full for complete answer]*

**Citations:**

- [1] CODEBASE_GUIDE.pdf p.2
- [2] PRODUCT_ROADMAP.pdf p.3

**⚠ Model said 'no information' — possible retrieval miss**

### venv_activation
**Query:** What command activates the AIStudio Python virtual environment and what prompt change confirms it?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 2.82s | **Pass:** ✅

**Answer:**

> To activate the AIStudio Python virtual environment, run:
> source ~/Developer/AIStudio/.venv/bin/activate [1]
> This will change your prompt to show (.venv) when active.
>
> Note that ais_start handles this automatically, but you only need to activate manually if running Python commands directly.

**Citations:**

- [1] QUICKSTART.pdf p.5


### pango_requirement
**Query:** What system library does WeasyPrint require and how is it installed on macOS for AIStudio?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 2.92s | **Pass:** ✅

**Answer:**

> WeasyPrint requires the Cairo library [3]. To install it on macOS for AIStudio, run:
> ais_install
>
> This command installs all dependencies and sets up the environment. The prompt will show (.venv) when the virtual environment is activated. This step creates and populates the Python virtual environment automatically, which includes installing the necessary system libraries such as Cairo [2][3].

**Citations:**

- [2] dependencies.pdf p.1
- [3] QUICKSTART.pdf p.5


### qdrant_wal_error
**Query:** What causes the Qdrant WAL lock error and how do you fix it?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 4.1s | **Pass:** ✅

**Answer:**

> The Qdrant WAL lock error is caused by an unclean shutdown, such as a force-quit or power loss, which leaves the Qdrant collection locked [1]. This can be fixed by stopping AIStudio with `ais_stop`, deleting the affected collection (named in the panic message) from the `qdrant_storage` folder, and then re-ingesting the affected corpus via the UI [1].
>
> Note: The sources do not mention what causes the Qdrant WAL lock error explicitly.

**Citations:**

- [1] QUICKSTART.pdf p.9


### why_qdrant_over_chroma
**Query:** Why did AIStudio switch from ChromaDB to Qdrant as the vector store?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 4.42s | **Pass:** ✅

**Answer:**

> AIStudio switched from ChromaDB to Qdrant as the vector store due to instability at scale. Specifically, ChromaDB crashed at 32,285 chunks during SEC 10-K corpus ingest [2]. In contrast, Qdrant is stable at 105,964 chunks with native metadata filtering, near-zero GC overhead, and a production upgrade path (sharding, replication, quantization) [1].
>
> Note: There is no explicit mention in the provided sources of why Qdrant was chosen over other alternatives. However, it can be inferred that Qdrant's stability and scalability features were the primary reasons for the switch.
>
> Citations:
> [1]
> [2]

**Citations:**

- [1] QUICKSTART.pdf p.4
- [2] dependencies.pdf p.3


### crossencoder_purpose
**Query:** What is the CrossEncoder model used for in AIStudio and why was it added?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 2.82s | **Pass:** ✅

**Answer:**

> The CrossEncoder model is used for reranking chunks retrieved from Qdrant in the query layer of AIStudio [1].
>
> There is no information about why it was added to AIStudio.

**Citations:**

- [1] CODEBASE_GUIDE.pdf p.2


### single_html_frontend
**Query:** Why does AIStudio use a single HTML file for the entire frontend?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 3.75s | **Pass:** ✅

**Answer:**

> According to [2], the entire UI is front_end/rag_studio.html — one file, ~1,900 lines, no build step. The reason for this design choice is that it allows for "Zero build toolchain. Clone and open. Works immediately."
>
> Additionally, [2] mentions that another reason for a single HTML file frontend is to avoid having npm, webpack, or node_modules. This aligns with the goal of being able to "runnable in under 30 minutes" as promised by the QUICKSTART guide.
>
> However, it's worth noting that [1] only briefly mentions the same front_end/rag_studio.html file but does not provide additional context on why a single HTML file is used.

**Citations:**

- [1] CODEBASE_GUIDE.pdf p.2
- [2] architecture_decisions.pdf p.5


### corpus_metadata_yaml
**Query:** What is the purpose of the corpus metadata YAML file and when is it loaded?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 3.79s | **Pass:** ✅

**Answer:**

> The corpus metadata YAML file is referred to as _corpus_meta.yaml [3]. However, there is no explicit information provided in the sources about its purpose or when it is loaded.
>
> It seems that the corpus metadata index is stored in the `index.jsonl` file [2], and the corpus manifest is tracked in the `manifest.jsonl` file.

**Citations:**

- [2] architecture_decisions.pdf p.8
- [3] HOWTO.pdf p.4


### ais_start_services
**Query:** What four processes does ais_start launch and how do you verify the backend is running?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 4.31s | **Pass:** ✅

**Answer:**

> The four processes that ais_start launches are:
>
> 1. Ollama [2]
> 2. Qdrant [2]
> 3. FastAPI backend (uvicorn) [2]
> 4. Frontend [2]
>
> To verify the backend is running, you can check if the /health endpoint is responding:
> ais_start checks whether each service is already running before starting it — safe to run multiple times.
>
> You can also manually start the backend and frontend processes in separate terminals using the following commands:
>
> *[truncated — use --full for complete answer]*

**Citations:**

- [2] QUICKSTART.pdf p.5


### corpus_ingest_command
**Query:** What is the full command to ingest the demo corpus from the terminal?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 4.52s | **Pass:** ✅

**Answer:**

> To ingest the demo corpus from the terminal, run:
>
> ais_ingest_sec_10k
>
> However, this is a specific ingest command for the SEC 10-K corpus, not the demo corpus. To ingest the demo corpus specifically, the correct answer is not provided in the given sources.
>
> The closest relevant information is found in [2], which mentions how to re-ingest a corpus from scratch using the --force flag with the following command:
>
> *[truncated — use --full for complete answer]*

**Citations:**

- [2] HOWTO.pdf p.4


### ais_bench_default
**Query:** What are the default parameters when running ais_bench with no arguments?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 5.52s | **Pass:** ✅

**Answer:**

> There are no sources that provide the default parameters when running `ais_bench` with no arguments.
>
> However, we can look at how `ais_bench` is used in [1] HARNESS.pdf:
>
> # Then benchmark
> ais_bench --corpus sec_10k --top-k 10
>
> This suggests that running `ais_bench` with no arguments would result in an error, as the command requires the `--corpus` and `--top-k` flags to be specified.
>
> *[truncated — use --full for complete answer]*

**Citations:**

- [1] HARNESS.pdf p.4
- [2] QUICKSTART.pdf p.10


### latency_benchmark_finding
**Query:** What did AIStudio benchmarks reveal about the latency difference between llama3.1:8b and llama3.1:70b on Apple Silicon?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 4.18s | **Pass:** ✅

**Answer:**

> According to [2], on Apple Silicon, warm llama3.1:70b and llama3.1:8b have identical query latency (~6–7s).
>
> This is also supported by [1] which states that "warm llama3.1:70b and warm llama3.1:8b are statistically identical in query latency on Apple Silicon (~6–7s average)".

**Citations:**

- [1] README.pdf p.3
- [2] QUICKSTART.pdf p.4


### file_deletion_behavior
**Query:** What happens to a file when it is deleted from a corpus in AIStudio?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 4.99s | **Pass:** ✅

**Answer:**

> When a file is deleted from a corpus in AIStudio, it does not get permanently deleted [1]. Instead, the deleted files move to data/corpora/<name>/uploads/trash/ [1]. This allows for file recovery if needed. To recover a deleted file, one can use the terminal commands provided: `ls` to see what's in trash and `mv` to move it back to its original location, followed by re-ingesting the corpus using the `--force` flag [1].
>
> Note that deleting an entire corpus moves the folder to ~/.Trash/ and renames it to avoid conflicts with previous deletions. To recover a deleted corpus, one can find the folder in Trash (which may have a timestamp suffix), move it back to its original location, and then re-ingest the corpus using the UI [1].

**Citations:**

- [1] HOWTO.pdf p.4


### corpus_creation_ui
**Query:** How do you create a new corpus in the AIStudio UI?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 2.89s | **Pass:** ✅

**Answer:**

> To create a new corpus in the AIStudio UI, follow these steps:
>
> 1. Open AIStudio and create a new corpus using the "New" button.
> 2. Then upload your files using the Add button.
>
> The HOWTO.pdf document [1] states that AIStudio handles ingestion automatically and shows progress in the chat area.

**Citations:**

- [1] HOWTO.pdf p.4


### demo_corpus_description
**Query:** What does the AIStudio demo corpus contain and what time period does it cover?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 3.85s | **Pass:** ✅

**Answer:**

> The demo corpus contains a curated set of 11 original documents [3] spanning approximately ~530 pages across formats PDF, PPTX, and PPT, with a date range from 2003 to 2021. The documents cover IT strategy frameworks, enterprise architecture methodology, financial services technology journals, cloud migration analysis, and AI reference architecture produced by senior technology roles at major financial institutions [1].

**Citations:**

- [1] QUICKSTART.pdf p.7
- [3] DEMO_CORPUS.pdf p.4


### failed_to_fetch_fix
**Query:** What does the QUICKSTART troubleshooting section say to do when you see "Failed to fetch in UI" and the FastAPI backend is down?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 3.51s | **Pass:** ✅

**Answer:**

> When you see "Failed to fetch in UI" and the FastAPI backend is down, according to QUICKSTART.pdf [2], you should run:
>
> kill $(lsof -ti:8000)
> cd ~/Developer/AIStudio && source .venv/bin/activate
> OLLAMA_KEEP_ALIVE=30m AISTUDIO_VECTORSTORE=qdrant PYTHONPATH=src \
> uvicorn local_llm_bot.app.api:app --reload --port 8000

**Citations:**

- [2] QUICKSTART.pdf p.9


### python_version_requirement
**Query:** Why does AIStudio require Python 3.10 or later and what fails on 3.9?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 4.29s | **Pass:** ✅

**Answer:**

> AIStudio requires Python 3.10 or later because it uses type syntax (e.g., `float | None`) that fails on Python 3.9 [2]. The system Python on macOS is often 3.9, and users should install a newer version if needed to use AIStudio [2].
>
> Note: There is no specific information in the provided sources about what exactly fails on Python 3.9, but it is mentioned that type syntax used by AIStudio is incompatible with Python 3.9.

**Citations:**

- [2] QUICKSTART.pdf p.1


### qa_testing_lesson
**Query:** What happened when a user copy-pasted the Qdrant install command from the AIStudio PDF during a fresh Mac install, and what was the fix?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 6.05s | **Pass:** ✅

**Answer:**

> According to [1], when a user copy-pasted the Qdrant install command from the AIStudio PDF during a fresh Mac install, it wrote a broken line to ~/.zshrc, corrupting PATH for every subsequent Terminal session. This caused basic commands (mkdir, ollama, echo) to stop working.
>
> The root cause category is [PDF] + [DOC], as multi-line commands are inherently fragile in PDF format and no warning was given. The fix applied was Step 5 now uses a single &&-chained command that PDF cannot break. A warning was added at the top of QUICKSTART directing users to GitHub for copy-paste.
>
> Additionally, according to [2], if your terminal says "command not found" when you paste commands, two common causes are:
>
> * You pasted a # comment line — zsh tries to execute it.
> * Your AIStudio aliases aren't loaded yet. To fix the second cause, run: 
> source ~/.zshrc
> Then try the command again on its own line.
>
> *[truncated — use --full for complete answer]*

**Citations:**

- [1] QA_TESTING_LESSONS_LEARNED.pdf p.1
- [2] HOWTO.pdf p.1


### beta_gate_criteria
**Query:** What are the criteria for AIStudio to reach Beta status?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 3.08s | **Pass:** ✅

**Answer:**

> To reach Beta status, AIStudio must meet two criteria:
>
> retrieval quality [2], 
> full documentation [1][2].

**Citations:**

- [1] PRODUCT_ROADMAP.pdf p.1
- [2] CODEBASE_GUIDE.pdf p.2


### v2_feature
**Query:** What is the primary new capability planned for AIStudio v2.0?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 2.68s | **Pass:** ✅

**Answer:**

> The primary new capability planned for AIStudio v2.0 is the publication of full API documentation (API_DOC.md) with request/response schemas, error codes, and examples [1].
>
> This will be accompanied by FastAPI's built-in Swagger UI (/docs) being enabled, making the API self-documenting for developers integrating AIStudio into their own workflows [1].

**Citations:**

- [1] PRODUCT_ROADMAP.pdf p.3

