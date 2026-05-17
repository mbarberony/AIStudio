# AIStudio — Benchmark Findings
*Generated: 2026-04-19 20:08*

## Configuration
- **Corpus:** `help`
- **Top K:** 5
- **Temperature:** 0.3
- **Model:** API default
- **API:** http://localhost:8000

## Summary
- **Questions:** 20
- **Passed:** 16/20 (80%)
- **Avg latency:** 3.8s

## Infrastructure
- Vector store: Qdrant 1.17.0 (Apple Silicon, local)
- Embedding model: nomic-embed-text (768 dimensions, cosine similarity)
- Reranker: CrossEncoder ms-marco-MiniLM-L-6-v2
- Corpus: `help` (see corpus stats in UI)

## Results

| # | Description | Latency | Pass | Citations | Notes |
|---|-------------|---------|------|-----------|-------|
| 1 | How is the Qdrant binary installed in AIStudio — what curl command is used and where is the binary moved to? | 4.53s | ✅ | README.pdf | QUICKSTART Step 5 — specific curl command downloading aarch64 binary, moved to ~/bin/. Distinctive terms that only appear in the Qdrant install chunk and cannot be answered from general knowledge.
 |
| 2 | What command activates the AIStudio Python virtual environment and what prompt change confirms it? | 3.71s | ✅ | QUICKSTART.pdf, HOWTO.pdf | QUICKSTART Step 8 — specific to AIStudio's venv path and prompt indicator.
 |
| 3 | What system library does WeasyPrint require and how is it installed on macOS for AIStudio? | 2.32s | ✅ | PRODUCT_ROADMAP.pdf, QUICKSTART.pdf | QUICKSTART Step 1 — pango is required by WeasyPrint for PDF generation. WeasyPrint keyword forces the right chunk.
 |
| 4 | What causes the Qdrant WAL lock error and how do you fix it? | 5.01s | ✅ | QUICKSTART.pdf | HOWTO troubleshooting section — specific error pattern with specific fix.
 |
| 5 | Why did AIStudio switch from ChromaDB to Qdrant as the vector store? | 3.98s | ✅ | QUICKSTART.pdf, dependencies.pdf, CODEBA | architecture_decisions.md — explicit ADR with stated rationale.
 |
| 6 | What is the CrossEncoder model used for in AIStudio and why was it added? | 3.18s | ✅ | CODEBASE_GUIDE.pdf | architecture_decisions.md — reranking ADR. Specific model name required.
 |
| 7 | Why does AIStudio use a single HTML file for the entire frontend? | 3.11s | ❌ | architecture_decisions.pdf | CODEBASE_GUIDE and architecture_decisions — offline-first design decision.
 |
| 8 | What is the purpose of the corpus metadata YAML file and when is it loaded? | 4.62s | ✅ | CODEBASE_GUIDE.pdf, architecture_decisio | CODEBASE_GUIDE — corpus_meta.yaml loaded into system prompt at query time.
 |
| 9 | What four processes does ais_start launch and how do you verify the backend is running? | 3.04s | ❌ | — | QUICKSTART Step 9 — specific to AIStudio's four-process architecture.
 |
| 10 | What is the full command to ingest the demo corpus from the terminal? | 5.08s | ✅ | QUICKSTART.pdf | QUICKSTART Step 10 — specific command with environment variables.
 |
| 11 | What are the default parameters when running ais_bench with no arguments? | 4.78s | ✅ | HARNESS.pdf, QUICKSTART.pdf, HOWTO.pdf,  | HOWTO or QUICKSTART benchmark section — specific defaults.
 |
| 12 | What did AIStudio benchmarks reveal about the latency difference between llama3.1:8b and llama3.1:70b on Apple Silicon? | 4.98s | ✅ | README.pdf, QUICKSTART.pdf | README benchmark finding — statistically indistinguishable warm latency. Strong proof point, specific to AIStudio testing.
 |
| 13 | What happens to a file when it is deleted from a corpus in AIStudio? | 3.38s | ✅ | HOWTO.pdf | HOWTO — file moved to trash/, Qdrant chunks removed surgically.
 |
| 14 | How do you create a new corpus in the AIStudio UI? | 2.68s | ✅ | HOWTO.pdf | HOWTO — UI-specific workflow for corpus creation.
 |
| 15 | What does the AIStudio demo corpus contain and what time period does it cover? | 4.39s | ✅ | HARNESS.pdf, DEMO_CORPUS.pdf | DEMO_CORPUS.md and README — curated 9-document corpus, 2003-2026.
 |
| 16 | What does the QUICKSTART troubleshooting section say to do when you see "Failed to fetch in UI" and the FastAPI backend is down? | 3.44s | ✅ | QUICKSTART.pdf | QUICKSTART page 9 — chunk contains exact phrase "Failed to fetch in UI" followed by kill $(lsof -ti:8000) command. Keywords match the fix commands in that specific chunk.
 |
| 17 | Why does AIStudio require Python 3.10 or later and what fails on 3.9? | 4.55s | ✅ | QUICKSTART.pdf | QUICKSTART prerequisites — float | None syntax incompatibility.
 |
| 18 | What happened when a user copy-pasted the Qdrant install command from the AIStudio PDF during a fresh Mac install, and what was the fix? | 3.7s | ❌ | — | QA_TESTING_LESSONS_LEARNED.pdf showstopper #2 — PDF line-wrapping broke the Qdrant PATH command across lines, corrupting ~/.zshrc. Fix was single-line &&-chained command. Very specific — cannot come from QUICKSTART.
 |
| 19 | What are the criteria for AIStudio to reach Beta status? | 3.51s | ✅ | PRODUCT_ROADMAP.pdf | PRODUCT_ROADMAP.md — specific Beta gate requirements.
 |
| 20 | What is the primary new capability planned for AIStudio v2.0? | 2.9s | ❌ | PRODUCT_ROADMAP.pdf | PRODUCT_ROADMAP.md — v2.0 headline feature. |

## Detailed Results

### qdrant_install_method
**Query:** How is the Qdrant binary installed in AIStudio — what curl command is used and where is the binary moved to?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 4.53s | **Pass:** ✅

**Answer:**

> To install the Qdrant binary, the following `curl` command is used:
> ```bash
> curl -L https://github.com/qdrant/qdrant/releases/latest/download/qdrant-aarch64-apple-darwin.tar.gz | tar xz
> ```
> The Qdrant binary is then moved to the ~/bin directory with the following commands:
> ```bash
> mkdir -p ~/bin && mv qdrant ~/bin/qdrant && echo 'export PATH="$HOME/bin:$PATH"' >> ~/.zshrc && source ~/.zshrc
> ```
> This information can be found in [1] README.pdf, which describes the installation process for AIStudio.

**Citations:**

- [1] README.pdf p.4


### venv_activation
**Query:** What command activates the AIStudio Python virtual environment and what prompt change confirms it?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 3.71s | **Pass:** ✅

**Answer:**

> To activate the AIStudio Python virtual environment, you need to run:
>
> [source ~/Developer/AIStudio/.venv/bin/activate]
>
> This can be found on page 4 of [1] and is also mentioned in passing in [2].
>
> The prompt will show "(.venv)" when active, which confirms it has been activated. This is stated in [1].

**Citations:**

- [1] QUICKSTART.pdf p.5
- [2] HOWTO.pdf p.3


### pango_requirement
**Query:** What system library does WeasyPrint require and how is it installed on macOS for AIStudio?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 2.32s | **Pass:** ✅

**Answer:**

> WeasyPrint requires the system library pango[1].
>
> To install it on macOS for AIStudio, run:
> ais_install [3]

**Citations:**

- [1] PRODUCT_ROADMAP.pdf p.3
- [3] QUICKSTART.pdf p.5


### qdrant_wal_error
**Query:** What causes the Qdrant WAL lock error and how do you fix it?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 5.01s | **Pass:** ✅

**Answer:**

> The Qdrant WAL lock error is caused by an unclean shutdown, such as a force-quit, power loss, or crash [1]. To fix this issue, you need to stop Qdrant with `ais_stop`, delete the corrupted collection using `rm -rf ~/qdrant_storage/collections/aistudio_help` (replace with the actual collection name), and then restart Qdrant with `ais_start`. After that, re-ingest the affected corpus via the UI [1].
>
> Note: The sources do not explicitly mention how to identify the corrupted collection or which steps to follow in case of a power loss or crash. However, based on the provided information, it appears that stopping and restarting Qdrant, deleting the corrupted collection, and re-ingesting the corpus are necessary steps to resolve the issue [1].

**Citations:**

- [1] QUICKSTART.pdf p.9


### why_qdrant_over_chroma
**Query:** Why did AIStudio switch from ChromaDB to Qdrant as the vector store?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 3.98s | **Pass:** ✅

**Answer:**

> ChromaDB crashed at 32,285 chunks during SEC 10-K corpus ingest [1][2], whereas Qdrant is stable at 105,964 chunks with native metadata filtering and near-zero GC overhead [1][3]. The decision to switch from ChromaDB to Qdrant is discussed in more detail in architecture_decisions.md Decision #2 (see docs/architecture_decisions.md) [3].

**Citations:**

- [1] QUICKSTART.pdf p.4
- [2] dependencies.pdf p.3
- [3] CODEBASE_GUIDE.pdf p.2


### crossencoder_purpose
**Query:** What is the CrossEncoder model used for in AIStudio and why was it added?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 3.18s | **Pass:** ✅

**Answer:**

> The CrossEncoder model is used in the query layer of AIStudio for reranking chunks retrieved from Qdrant [1]. It assembles a prompt and sends it to an Ollama-hosted LLM. The reason for its addition is not explicitly stated in any of the provided sources.

**Citations:**

- [1] CODEBASE_GUIDE.pdf p.2


### single_html_frontend
**Query:** Why does AIStudio use a single HTML file for the entire frontend?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 3.11s | **Pass:** ❌

**Answer:**

> The single HTML file for the entire frontend, front_end/rag_studio.html, is used because [2] states "Zero build toolchain. Clone and open. Works immediately." Additionally, [2] mentions that there is a tradeoff in using a single ~1,900-line file: operational simplicity over developer ergonomics at this scale.
>
> The sources do not address why the frontend cannot be componentized or built with tools like React or Webpack.

**Citations:**

- [2] architecture_decisions.pdf p.5

**⚠ Model said 'no information' — possible retrieval miss**

### corpus_metadata_yaml
**Query:** What is the purpose of the corpus metadata YAML file and when is it loaded?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 4.62s | **Pass:** ✅

**Answer:**

> The purpose of the corpus metadata YAML file is not explicitly stated in any of the provided sources [1] through [4]. However, it can be inferred that the corpus metadata YAML file is used to track information about the corpus, such as search routing guidance.
>
> [1] mentions that `_corpus_meta.yaml` is loaded into the system prompt at query.
>
> The system prompt, in turn, is discussed in [2][3], and how the model is instructed is mentioned in [FILE_GUIDE.pdf].
>
> Since there is no explicit information about when it is loaded, we can only say that the corpus metadata YAML file's purpose is to track information about the corpus.

**Citations:**

- [1] CODEBASE_GUIDE.pdf p.4
- [2] architecture_decisions.pdf p.8
- [3] HOWTO.pdf p.4
- [4] QUICKSTART.pdf p.7


### ais_start_services
**Query:** What four processes does ais_start launch and how do you verify the backend is running?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 3.04s | **Pass:** ❌

**Answer:**

> The four processes that `ais_start` launches are:
>
> * Ollama (OLLAMA_KEEP_ALIVE=30m)
> * Qdrant
> * FastAPI backend (uvicorn)
> * Frontend
>
> To verify the backend is running, you can check the live backend log in real-time using `ais_log`.


### corpus_ingest_command
**Query:** What is the full command to ingest the demo corpus from the terminal?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 5.08s | **Pass:** ✅

**Answer:**

> The full command to ingest the demo corpus from the terminal is:
>
> ```bash
> ais_ingest_sec_10k
> ```
>
> However, this only works for the SEC 10-K corpus. For ingesting any other corpus, including the demo corpus, you would use the following command:
>
> ```bash
> AISTUDIO_VECTORSTORE=qdrant PYTHONPATH=src python3 -m local_llm_bot.app.ingest --corpus demo --root data/corpora/demo/uploads --force
> ```
>
> *[truncated — use --full for complete answer]*

**Citations:**

- [1] QUICKSTART.pdf p.10


### ais_bench_default
**Query:** What are the default parameters when running ais_bench with no arguments?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 4.78s | **Pass:** ✅

**Answer:**

> The default parameters when running `ais_bench` with no arguments are not specified in any of the provided sources.
>
> However, we can infer from [3] HOWTO.pdf that the available commands and their descriptions can be accessed by running `ais_help`.
>
> But for the specific question about the default parameters when running `ais_bench` with no arguments, it's actually mentioned in [4] architecture_decisions.pdf that every command supports --help. Hence,
>
> [1][2][3][4][5]
>
> *[truncated — use --full for complete answer]*

**Citations:**

- [1] HARNESS.pdf p.4
- [2] QUICKSTART.pdf p.10
- [3] HOWTO.pdf p.2
- [4] architecture_decisions.pdf p.6
- [5] FILE_GUIDE.pdf p.1


### latency_benchmark_finding
**Query:** What did AIStudio benchmarks reveal about the latency difference between llama3.1:8b and llama3.1:70b on Apple Silicon?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 4.98s | **Pass:** ✅

**Answer:**

> According to [2], on Apple Silicon, warm llama3.1:70b and warm llama3.1:8b have identical query latency (~6–7s). Once loaded into unified memory, model size stops being a latency variable.
>
> However, [1] also states that "ama3.1:70b and warm llama3.1:8b are statistically identical in query latency on Apple Silicon (~6–7s average)". This supports the claim made in [2].
>
> There is no further information about the specifics of the benchmarking process or whether there are any differences between the two models, so it's only possible to state that they have identical latency.

**Citations:**

- [1] README.pdf p.3
- [2] QUICKSTART.pdf p.4


### file_deletion_behavior
**Query:** What happens to a file when it is deleted from a corpus in AIStudio?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 3.38s | **Pass:** ✅

**Answer:**

> When you delete a file from a corpus in AIStudio, it moves to data/corpora/<name>/uploads/trash/ — not permanently deleted [1].

**Citations:**

- [1] HOWTO.pdf p.4


### corpus_creation_ui
**Query:** How do you create a new corpus in the AIStudio UI?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 2.68s | **Pass:** ✅

**Answer:**

> To create a new corpus in the AIStudio UI:
>
> 1. Open AIStudio.
> 2. Create a new corpus using the New button.
> 3. Upload your files using the Add button.
>
> AIStudio will handle ingestion automatically and show progress in the chat area. [1]

**Citations:**

- [1] HOWTO.pdf p.4


### demo_corpus_description
**Query:** What does the AIStudio demo corpus contain and what time period does it cover?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 4.39s | **Pass:** ✅

**Answer:**

> The demo corpus contains a curated set of 11 original documents [3] spanning from 2003 to 2021 [2], with a total of ~530 pages (~11 documents x 47.18 pages/document) [3]. The domain is financial services technology architecture [3].
>
> You can ingest the demo corpus by running `PYTHONPATH=src python -m local_llm_bot.app.ingest --corpus demo --root data/corpora/demo/uploads` [3]. This command indexes all documents in `data/demo/` into a corpus named `demo`.

**Citations:**

- [2] HARNESS.pdf p.1
- [3] DEMO_CORPUS.pdf p.4


### failed_to_fetch_fix
**Query:** What does the QUICKSTART troubleshooting section say to do when you see "Failed to fetch in UI" and the FastAPI backend is down?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 3.44s | **Pass:** ✅

**Answer:**

> When you see "Failed to fetch in UI" and the FastAPI backend is down, according to [2], you should run:
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
**Latency:** 4.55s | **Pass:** ✅

**Answer:**

> AIStudio requires Python 3.10 or later because it uses type syntax that fails on Python 3.9 [2]. Specifically, AIStudio uses type annotations like 'float | None' which is not supported in Python 3.9 [2]. If you use the system Python on macOS (which is often version 3.9), you will need to install a newer version of Python [2].
>
> Note: The sources do not explicitly state why Python 3.10 or later is chosen, but it seems that type syntax and other new features are the reasons for this requirement.

**Citations:**

- [2] QUICKSTART.pdf p.1


### qa_testing_lesson
**Query:** What happened when a user copy-pasted the Qdrant install command from the AIStudio PDF during a fresh Mac install, and what was the fix?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 3.7s | **Pass:** ❌

**Answer:**

> When a user copy-pasted the Qdrant install command from the AIStudio PDF during a fresh Mac install, they encountered an issue due to [PDF] + [DOC] Multi-line commands being inherently fragile in PDF format. The root cause category is documented as [PDF] and [DOC].


### beta_gate_criteria
**Query:** What are the criteria for AIStudio to reach Beta status?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 3.51s | **Pass:** ✅

**Answer:**

> According to [1], Beta is the last milestone before the codebase is opened for external use. To reach Beta status, AIStudio must meet the following criteria:
>
> * Retrieval quality
> * Full documentation
> * Source Dive (click citation → open to exact page)
> * One-click installer
> * API
>
> These criteria are explicitly stated in the Milestone Definition section of [1].

**Citations:**

- [1] PRODUCT_ROADMAP.pdf p.1


### v2_feature
**Query:** What is the primary new capability planned for AIStudio v2.0?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 2.9s | **Pass:** ❌

**Answer:**

> The primary new capability planned for AIStudio v2.0 is [1] the addition of UI fields to the New Corpus modal for providing corpus metadata at creation time.
>
> Additionally, [1] publishes full API documentation (API_DOC.md) with request/response schemas, error codes, and examples, making the API self-documenting for developers integrating AIStudio into their workflows.
>
> The sources do not address what is the primary new capability planned for AIStudio v2.0 beyond these two points.

**Citations:**

- [1] PRODUCT_ROADMAP.pdf p.3

**⚠ Model said 'no information' — possible retrieval miss**
