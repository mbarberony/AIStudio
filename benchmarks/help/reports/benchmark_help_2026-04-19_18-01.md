# AIStudio — Benchmark Findings
*Generated: 2026-04-19 18:02*

## Configuration
- **Corpus:** `help`
- **Top K:** 5
- **Temperature:** 0.3
- **Model:** API default
- **API:** http://localhost:8000

## Summary
- **Questions:** 20
- **Passed:** 19/20 (95%)
- **Avg latency:** 3.9s

## Infrastructure
- Vector store: Qdrant 1.17.0 (Apple Silicon, local)
- Embedding model: nomic-embed-text (768 dimensions, cosine similarity)
- Reranker: CrossEncoder ms-marco-MiniLM-L-6-v2
- Corpus: `help` (see corpus stats in UI)

## Results

| # | Description | Latency | Pass | Citations | Notes |
|---|-------------|---------|------|-----------|-------|
| 1 | How is Qdrant installed in AIStudio and why is it not available via Homebrew? | 5.22s | ✅ | CODEBASE_GUIDE.pdf, PRODUCT_ROADMAP.pdf, | QUICKSTART-specific — covers the direct binary install method. Cannot be answered from general knowledge.
 |
| 2 | What command activates the AIStudio Python virtual environment and what prompt change confirms it? | 2.45s | ✅ | QUICKSTART.pdf | QUICKSTART Step 8 — specific to AIStudio's venv path and prompt indicator.
 |
| 3 | What system library does WeasyPrint require and how is it installed on macOS for AIStudio? | 3.95s | ✅ | dependencies.pdf, QUICKSTART.pdf | QUICKSTART Step 1 — pango is required by WeasyPrint for PDF generation. WeasyPrint keyword forces the right chunk.
 |
| 4 | What causes the Qdrant WAL lock error and how do you fix it? | 4.71s | ✅ | QUICKSTART.pdf | HOWTO troubleshooting section — specific error pattern with specific fix.
 |
| 5 | Why did AIStudio switch from ChromaDB to Qdrant as the vector store? | 4.04s | ✅ | dependencies.pdf, CODEBASE_GUIDE.pdf | architecture_decisions.md — explicit ADR with stated rationale.
 |
| 6 | What is the CrossEncoder model used for in AIStudio and why was it added? | 2.9s | ✅ | CODEBASE_GUIDE.pdf | architecture_decisions.md — reranking ADR. Specific model name required.
 |
| 7 | Why does AIStudio use a single HTML file for the entire frontend? | 3.39s | ✅ | CODEBASE_GUIDE.pdf, architecture_decisio | CODEBASE_GUIDE and architecture_decisions — offline-first design decision.
 |
| 8 | What is the purpose of the corpus metadata YAML file and when is it loaded? | 3.85s | ✅ | HOWTO.pdf | CODEBASE_GUIDE — corpus_meta.yaml loaded into system prompt at query time.
 |
| 9 | What four processes does ais_start launch and how do you verify the backend is running? | 3.66s | ✅ | QUICKSTART.pdf | QUICKSTART Step 9 — specific to AIStudio's four-process architecture.
 |
| 10 | What is the full command to ingest the demo corpus from the terminal? | 4.2s | ✅ | HOWTO.pdf | QUICKSTART Step 10 — specific command with environment variables.
 |
| 11 | What are the default parameters when running ais_bench with no arguments? | 5.42s | ✅ | QUICKSTART.pdf | HOWTO or QUICKSTART benchmark section — specific defaults.
 |
| 12 | What did AIStudio benchmarks reveal about the latency difference between llama3.1:8b and llama3.1:70b on Apple Silicon? | 3.84s | ✅ | README.pdf, QUICKSTART.pdf | README benchmark finding — statistically indistinguishable warm latency. Strong proof point, specific to AIStudio testing.
 |
| 13 | What happens to a file when it is deleted from a corpus in AIStudio? | 4.08s | ✅ | HOWTO.pdf | HOWTO — file moved to trash/, Qdrant chunks removed surgically.
 |
| 14 | How do you create a new corpus in the AIStudio UI? | 3.59s | ✅ | HOWTO.pdf | HOWTO — UI-specific workflow for corpus creation.
 |
| 15 | What does the AIStudio demo corpus contain and what time period does it cover? | 3.48s | ✅ | QUICKSTART.pdf, DEMO_CORPUS.pdf | DEMO_CORPUS.md and README — curated 9-document corpus, 2003-2026.
 |
| 16 | What command do you run to kill the AIStudio backend process on port 8000 and restart it? | 4.03s | ❌ | — | QUICKSTART troubleshooting — specific lsof/kill command for port 8000. Command-specific keywords force the right troubleshooting chunk.
 |
| 17 | Why does AIStudio require Python 3.10 or later and what fails on 3.9? | 3.19s | ✅ | QA_TESTING_LESSONS_LEARNED.pdf, QUICKSTA | QUICKSTART prerequisites — float | None syntax incompatibility.
 |
| 18 | What happened when a user copy-pasted the Qdrant install command from the AIStudio PDF during a fresh Mac install, and what was the fix? | 6.01s | ✅ | QA_TESTING_LESSONS_LEARNED.pdf, HOWTO.pd | QA_TESTING_LESSONS_LEARNED.pdf showstopper #2 — PDF line-wrapping broke the Qdrant PATH command across lines, corrupting ~/.zshrc. Fix was single-line &&-chained command. Very specific — cannot come from QUICKSTART.
 |
| 19 | What are the criteria for AIStudio to reach Beta status? | 3.3s | ✅ | PRODUCT_ROADMAP.pdf | PRODUCT_ROADMAP.md — specific Beta gate requirements.
 |
| 20 | What is the primary new capability planned for AIStudio v2.0? | 2.97s | ✅ | PRODUCT_ROADMAP.pdf | PRODUCT_ROADMAP.md — v2.0 headline feature. |

## Detailed Results

### qdrant_install_method
**Query:** How is Qdrant installed in AIStudio and why is it not available via Homebrew?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 5.22s | **Pass:** ✅

**Answer:**

> Qdrant is installed in AIStudio as part of the ingest layer, which is triggered via the UI as a one-time operation per document. This process lives in src/local_llm_bot/app/ingest/ ([1]).
>
> The current install requires terminal familiarity, but v2.0 will ship with a .dmg installer that handles the full setup, including Qdrant installation, without requiring a terminal ([2]).
>
> Qdrant is not available via Homebrew because AIStudio ships when it is ready, and there is no version 1.0; instead, it goes directly from Beta to v2.0. This implies that v2.0 includes the necessary dependencies, such as Qdrant ([2]).
>
> To load AIStudio aliases in the terminal, which may resolve issues with 'command not found' errors when trying to run commands, use:
>
> source ~/.zshrc [3]
>
> *[truncated — use --full for complete answer]*

**Citations:**

- [1] CODEBASE_GUIDE.pdf p.2
- [2] PRODUCT_ROADMAP.pdf p.3
- [3] HOWTO.pdf p.1


### venv_activation
**Query:** What command activates the AIStudio Python virtual environment and what prompt change confirms it?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 2.45s | **Pass:** ✅

**Answer:**

> To activate the AIStudio Python virtual environment, run:
> source ~/Developer/AIStudio/.venv/bin/activate [1]
>
> Your prompt will show (.venv) when active.

**Citations:**

- [1] QUICKSTART.pdf p.5


### pango_requirement
**Query:** What system library does WeasyPrint require and how is it installed on macOS for AIStudio?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 3.95s | **Pass:** ✅

**Answer:**

> WeasyPrint requires the Cairo library, which is a system library. According to [2], WeasyPrint's dependencies are listed in requirements.txt and documented in this dependency guide, but no specific information about Cairo or its installation for AIStudio is provided.
>
> However, since we're looking for how it is installed on macOS for AIStudio, let's check if the QUICKSTART.pdf guides us through the process.
>
> Indeed, [3] explains how to install dependencies and set up the environment, including activating the virtual environment with `source ~/Developer/AIStudio/.venv/bin/activate`. This command is relevant but does not mention installing Cairo or any system libraries.
>
> Unfortunately, there's no specific guidance on how to install WeasyPrint's required Cairo library on macOS for AIStudio in the provided sources.

**Citations:**

- [2] dependencies.pdf p.1
- [3] QUICKSTART.pdf p.5


### qdrant_wal_error
**Query:** What causes the Qdrant WAL lock error and how do you fix it?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 4.71s | **Pass:** ✅

**Answer:**

> Unfortunately, none of the provided sources address the Qdrant WAL lock error.
>
> However, based on [1] QUICKSTART.pdf, it appears that the Qdrant WAL lock error can occur due to an unclean shutdown (force-quit, power loss, or crash) as the collection name is in the panic message.
>
> To fix this issue, according to [1], you need to stop AIStudio using `ais_stop`, delete only the affected collection (not the entire qdrant_storage/ folder), and then re-ingest the affected corpus via the UI.
>
> As for what causes the Qdrant WAL lock error, [1] does not explicitly state this. However, it mentions that an unclean shutdown can cause issues with AIStudio's operations.

**Citations:**

- [1] QUICKSTART.pdf p.9


### why_qdrant_over_chroma
**Query:** Why did AIStudio switch from ChromaDB to Qdrant as the vector store?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 4.04s | **Pass:** ✅

**Answer:**

> AIStudio switched from ChromaDB to Qdrant as the vector store because [2] ChromaDB crashed at 32,285 chunks during SEC 10-K corpus ingest. In contrast, [3] Qdrant is stable at 105,964 chunks with native metadata filtering and near-zero GC overhead.
>
> Additionally, the architecture decisions in [3] mention that Qdrant was chosen for its production upgrade path (sharding, replication, quantization, gRPC), which further supports the decision to replace ChromaDB.

**Citations:**

- [2] dependencies.pdf p.3
- [3] CODEBASE_GUIDE.pdf p.2


### crossencoder_purpose
**Query:** What is the CrossEncoder model used for in AIStudio and why was it added?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 2.9s | **Pass:** ✅

**Answer:**

> The CrossEncoder model is used for reranking chunks retrieved from Qdrant in the query layer of AIStudio. [1]
>
> There is no explicit mention of why the CrossEncoder was added to AIStudio in any of the provided sources.

**Citations:**

- [1] CODEBASE_GUIDE.pdf p.2


### single_html_frontend
**Query:** Why does AIStudio use a single HTML file for the entire frontend?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 3.39s | **Pass:** ✅

**Answer:**

> The entire frontend is implemented in a single HTML file, front_end/rag_studio.html, with no build step or separate node_modules [2]. This design choice is intended to provide operational simplicity over developer ergonomics at this scale, and it aligns with the QUICKSTART promise of working immediately after cloning and opening the project [1][2].
>
> The use of a single HTML file allows for zero build toolchain, eliminating the need for npm, webpack, or node_modules. This design is deliberate and reflects the tradeoff between operational simplicity and developer ergonomics [2].

**Citations:**

- [1] CODEBASE_GUIDE.pdf p.2
- [2] architecture_decisions.pdf p.5


### corpus_metadata_yaml
**Query:** What is the purpose of the corpus metadata YAML file and when is it loaded?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 3.85s | **Pass:** ✅

**Answer:**

> The purpose of the corpus metadata YAML file is not explicitly stated in any of the provided sources.
>
> However, [3] mentions that "Corpus Management" is handled automatically by AIStudio when creating a new corpus or re-ingesting an existing one. This suggests that some form of corpus metadata management exists, but its specifics are not detailed.
>
> The timing of loading the corpus metadata YAML file is also unclear from the provided sources.

**Citations:**

- [3] HOWTO.pdf p.4


### ais_start_services
**Query:** What four processes does ais_start launch and how do you verify the backend is running?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 3.66s | **Pass:** ✅

**Answer:**

> According to [2], the four processes that ais_start launches are:
>
> 1. Ollama
> 2. Qdrant
> 3. FastAPI backend
> 4. Frontend
>
> To verify that the backend is running, you can check if the /health endpoint is responding by accessing `http://localhost:8000/health` in your web browser.
>
> Alternatively, you can use the command `curl http://localhost:8000/health` to verify the health of the backend.
>
> *[truncated — use --full for complete answer]*

**Citations:**

- [2] QUICKSTART.pdf p.5


### corpus_ingest_command
**Query:** What is the full command to ingest the demo corpus from the terminal?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 4.2s | **Pass:** ✅

**Answer:**

> To ingest the demo corpus from the terminal, you can use the following command:
> ais_ingest --corpus demo --root data/corpora/demo/uploads --force
>
> This is mentioned in [2] HOWTO.pdf as part of re-ingesting a corpus from scratch. The --force flag wipes and rebuilds the corpus cleanly.
>
> Note: This assumes that the demo corpus has been downloaded or uploaded to the specified location. If not, you may need to download it first using the provided instructions in the same document.

**Citations:**

- [2] HOWTO.pdf p.4


### ais_bench_default
**Query:** What are the default parameters when running ais_bench with no arguments?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 5.42s | **Pass:** ✅

**Answer:**

> Running `ais_bench` with no arguments is not mentioned in the provided sources as a valid use case. However, [2] shows examples of running `ais_bench` with various options, but not without any arguments.
>
> The command to run benchmark on the demo corpus is shown as `ais_bench --corpus demo --top-k 10`, which implies that at least one argument (`--corpus`) is required. Therefore, it can be inferred that running `ais_bench` with no arguments will result in an error or unexpected behavior.
>
> If we follow the usual pattern of command invocation, as shown in [2], where each example command has its own line, we might expect a usage message to be printed when running `ais_bench` without any arguments. However, this is not explicitly stated in the provided sources.
>
> In the absence of explicit information on default parameters or usage messages for `ais_bench`, it's challenging to provide a definitive answer.

**Citations:**

- [2] QUICKSTART.pdf p.10


### latency_benchmark_finding
**Query:** What did AIStudio benchmarks reveal about the latency difference between llama3.1:8b and llama3.1:70b on Apple Silicon?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 3.84s | **Pass:** ✅

**Answer:**

> According to [2], on Apple Silicon, warm llama3.1:70b and warm llama3.1:8b have identical query latency (~6–7s).
>
> Additionally, according to [1], once loaded into unified memory, model size stops being a latency variable.

**Citations:**

- [1] README.pdf p.3
- [2] QUICKSTART.pdf p.4


### file_deletion_behavior
**Query:** What happens to a file when it is deleted from a corpus in AIStudio?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 4.08s | **Pass:** ✅

**Answer:**

> When a file is deleted from a corpus in AIStudio, it does not get permanently deleted. Instead, it moves to the "trash" folder located at `data/corpora/<name>/uploads/trash/`. [1]
>
> To recover a deleted file, you can move it back from the trash using the following command: `mv ~/Developer/AIStudio/data/corpora/<name>/uploads/trash/<filename> ~/Developer/AIStudio/data/corpora/<name>/uploads/` [1]

**Citations:**

- [1] HOWTO.pdf p.4


### corpus_creation_ui
**Query:** How do you create a new corpus in the AIStudio UI?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 3.59s | **Pass:** ✅

**Answer:**

> To create a new corpus in the AIStudio UI, follow these steps:
>
> Open AIStudio, create a new corpus using the New button, then upload your files using the Add button.
> AIStudio handles ingestion automatically and shows progress in the chat area. [1]
>
> Note that the source does not explicitly state how to create a new corpus in detail, but it mentions creating a new corpus using the New button and uploading files using the Add button.
>
> Also, for more specific information on how to ingest a new corpus, see Step 2 of the section "How do I ingest the SEC 10-K corpus?" in [1].

**Citations:**

- [1] HOWTO.pdf p.4


### demo_corpus_description
**Query:** What does the AIStudio demo corpus contain and what time period does it cover?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 3.48s | **Pass:** ✅

**Answer:**

> The AIStudio demo corpus contains 15 original documents spanning 2003–2021 [3]. The documents are IT strategy frameworks, enterprise architecture methodology, financial services technology journals, cloud migration analysis, and AI reference architecture produced across senior technology roles at major financial institutions [1].

**Citations:**

- [1] QUICKSTART.pdf p.7
- [3] DEMO_CORPUS.pdf p.4


### failed_to_fetch_fix
**Query:** What command do you run to kill the AIStudio backend process on port 8000 and restart it?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 4.03s | **Pass:** ❌

**Answer:**

> To kill the AIStudio backend process on port 8000 and restart it, run:
>
> kill $(lsof -ti:8000)
> cd ~/Developer/AIStudio && source .venv/bin/activate
> OLLAMA_KEEP_ALIVE=30m AISTUDIO_VECTORSTORE=qdrant PYTHONPATH=src \
> uvicorn local_llm_bot.app.api:app --reload --port 8000


### python_version_requirement
**Query:** Why does AIStudio require Python 3.10 or later and what fails on 3.9?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 3.19s | **Pass:** ✅

**Answer:**

> AIStudio requires Python 3.10 or later because it uses type syntax that fails on Python 3.9 [2]. The system Python on macOS is often 3.9, so users need to install a newer version if needed [2].
>
> The specific issue with Python 3.9 is a TypeError: Unable to evaluate type annotation 'float | None' [1].

**Citations:**

- [1] QA_TESTING_LESSONS_LEARNED.pdf p.2
- [2] QUICKSTART.pdf p.1


### qa_testing_lesson
**Query:** What happened when a user copy-pasted the Qdrant install command from the AIStudio PDF during a fresh Mac install, and what was the fix?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 6.01s | **Pass:** ✅

**Answer:**

> According to [1], when a user copy-pasted the Qdrant install command from the AIStudio PDF during a fresh Mac install, they wrote a broken line to ~/.zshrc, corrupting PATH for every subsequent Terminal session. This caused basic commands (mkdir, ollama, echo) to stop working.
>
> The root cause was identified as [PDF] + [DOC], with multi-line commands being inherently fragile in PDF format. No warning was given. The fix applied was to change Step 5 to use a single &&-chained command that PDF cannot break, and a warning was added at the top of QUICKSTART directing users to GitHub for copy-paste.
>
> Additionally, according to [2], if your terminal says "command not found" when pasting commands, two common causes are:
>
> * You pasted a # comment line — zsh tries to execute it. Paste only the commands, not the comment lines.
> * Your AIStudio aliases aren't loaded yet. Run: 
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
**Latency:** 3.3s | **Pass:** ✅

**Answer:**

> According to [1], to reach Beta status, AIStudio must meet the following criteria:
>
> * Retrieval quality
> * Full documentation
>
> These criteria are mentioned in the "Milestone Definition" section on page 2 of the PRODUCT_ROADMAP.pdf document.

**Citations:**

- [1] PRODUCT_ROADMAP.pdf p.1


### v2_feature
**Query:** What is the primary new capability planned for AIStudio v2.0?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 2.97s | **Pass:** ✅

**Answer:**

> The primary new capability planned for AIStudio v2.0 is the addition of UI fields to the New Corpus modal for injecting corpus metadata at creation time [1]. This allows users to provide a short description, a summary of what's in it, and routing guidance (hints about which documents answer which kinds of questions) without manual YAML editing.
>
> Additionally, AIStudio v2.0 publishes full API documentation with request/response schemas, error codes, and examples as part of the FastAPI Swagger UI [1].

**Citations:**

- [1] PRODUCT_ROADMAP.pdf p.3

