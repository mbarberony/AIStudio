# AIStudio — Benchmark Findings
*Generated: 2026-04-19 17:57*

## Configuration
- **Corpus:** `help`
- **Top K:** 5
- **Temperature:** 0.3
- **Model:** API default
- **API:** http://localhost:8000

## Summary
- **Questions:** 20
- **Passed:** 17/20 (85%)
- **Avg latency:** 4.0s

## Infrastructure
- Vector store: Qdrant 1.17.0 (Apple Silicon, local)
- Embedding model: nomic-embed-text (768 dimensions, cosine similarity)
- Reranker: CrossEncoder ms-marco-MiniLM-L-6-v2
- Corpus: `help` (see corpus stats in UI)

## Results

| # | Description | Latency | Pass | Citations | Notes |
|---|-------------|---------|------|-----------|-------|
| 1 | How is Qdrant installed in AIStudio and why is it not available via Homebrew? | 4.83s | ✅ | CODEBASE_GUIDE.pdf, PRODUCT_ROADMAP.pdf, | QUICKSTART-specific — covers the direct binary install method. Cannot be answered from general knowledge.
 |
| 2 | What command activates the AIStudio Python virtual environment and what prompt change confirms it? | 2.93s | ✅ | QUICKSTART.pdf | QUICKSTART Step 8 — specific to AIStudio's venv path and prompt indicator.
 |
| 3 | What system library does AIStudio require for PDF generation and how is it installed? | 7.39s | ❌ | QUICKSTART.pdf, dependencies.pdf | QUICKSTART-specific — pango is an unusual dependency worth testing.
 |
| 4 | What causes the Qdrant WAL lock error and how do you fix it? | 4.41s | ✅ | QUICKSTART.pdf, CODEBASE_GUIDE.pdf, QA_T | HOWTO troubleshooting section — specific error pattern with specific fix.
 |
| 5 | Why did AIStudio switch from ChromaDB to Qdrant as the vector store? | 3.49s | ✅ | QUICKSTART.pdf, dependencies.pdf | architecture_decisions.md — explicit ADR with stated rationale.
 |
| 6 | What is the CrossEncoder model used for in AIStudio and why was it added? | 3.34s | ✅ | CODEBASE_GUIDE.pdf | architecture_decisions.md — reranking ADR. Specific model name required.
 |
| 7 | Why does AIStudio use a single HTML file for the entire frontend? | 2.74s | ✅ | architecture_decisions.pdf | CODEBASE_GUIDE and architecture_decisions — offline-first design decision.
 |
| 8 | What is the purpose of the corpus metadata YAML file and when is it loaded? | 3.76s | ✅ | CODEBASE_GUIDE.pdf, HOWTO.pdf | CODEBASE_GUIDE — corpus_meta.yaml loaded into system prompt at query time.
 |
| 9 | What four processes does ais_start launch and how do you verify the backend is running? | 2.83s | ✅ | QUICKSTART.pdf | QUICKSTART Step 9 — specific to AIStudio's four-process architecture.
 |
| 10 | What is the full command to ingest the demo corpus from the terminal? | 4.97s | ✅ | QUICKSTART.pdf, HOWTO.pdf, architecture_ | QUICKSTART Step 10 — specific command with environment variables.
 |
| 11 | What are the default parameters when running ais_bench with no arguments? | 4.4s | ✅ | HARNESS.pdf, QUICKSTART.pdf | HOWTO or QUICKSTART benchmark section — specific defaults.
 |
| 12 | What did AIStudio benchmarks reveal about the latency difference between llama3.1:8b and llama3.1:70b on Apple Silicon? | 5.38s | ✅ | README.pdf, QUICKSTART.pdf, HOWTO.pdf | README benchmark finding — statistically indistinguishable warm latency. Strong proof point, specific to AIStudio testing.
 |
| 13 | What happens to a file when it is deleted from a corpus in AIStudio? | 5.73s | ✅ | HOWTO.pdf | HOWTO — file moved to trash/, Qdrant chunks removed surgically.
 |
| 14 | How do you create a new corpus in the AIStudio UI? | 2.48s | ✅ | HOWTO.pdf | HOWTO — UI-specific workflow for corpus creation.
 |
| 15 | What does the AIStudio demo corpus contain and what time period does it cover? | 3.8s | ✅ | QUICKSTART.pdf, DEMO_CORPUS.pdf | DEMO_CORPUS.md and README — curated 9-document corpus, 2003-2026.
 |
| 16 | How do you fix the Failed to fetch error in the AIStudio UI? | 3.54s | ❌ | HOWTO.pdf | QUICKSTART troubleshooting — backend down, specific restart command.
 |
| 17 | Why does AIStudio require Python 3.10 or later and what fails on 3.9? | 2.99s | ✅ | QA_TESTING_LESSONS_LEARNED.pdf, QUICKSTA | QUICKSTART prerequisites — float | None syntax incompatibility.
 |
| 18 | What was the most significant finding from AIStudio QA testing on a fresh machine? | 4.81s | ❌ | HOWTO.pdf, HARNESS.pdf | QA_TESTING_LESSONS_LEARNED.pdf — specific findings from install testing.
 |
| 19 | What are the criteria for AIStudio to reach Beta status? | 3.71s | ✅ | PRODUCT_ROADMAP.pdf | PRODUCT_ROADMAP.md — specific Beta gate requirements.
 |
| 20 | What is the primary new capability planned for AIStudio v2.0? | 2.84s | ✅ | PRODUCT_ROADMAP.pdf, architecture_decisi | PRODUCT_ROADMAP.md — v2.0 headline feature. |

## Detailed Results

### qdrant_install_method
**Query:** How is Qdrant installed in AIStudio and why is it not available via Homebrew?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 4.83s | **Pass:** ✅

**Answer:**

> Qdrant is installed in AIStudio through the ingestion process, which is triggered via the UI and lives in the `src/local_llm_bot/app/ingest/` directory [1]. This process loads, chunks, embeds, and stores documents in Qdrant.
>
> The installation of Qdrant is not available via Homebrew as it is a part of the AIStudio setup, which involves multiple components, including FastAPI, CrossEncoder, and Ollama [2]. The installation guide for v2.0 mentions that it ships with a `.dmg` installer that handles the full setup, including Python environment, Qdrant, Ollama pull, and alias registration without requiring terminal familiarity.
>
> To manage AIStudio aliases, which may affect Qdrant's availability, run `source ~/.zshrc` in your terminal [3].

**Citations:**

- [1] CODEBASE_GUIDE.pdf p.2
- [2] PRODUCT_ROADMAP.pdf p.3
- [3] HOWTO.pdf p.1


### venv_activation
**Query:** What command activates the AIStudio Python virtual environment and what prompt change confirms it?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 2.93s | **Pass:** ✅

**Answer:**

> To activate the AIStudio Python virtual environment, run:
> source ~/Developer/AIStudio/.venv/bin/activate [1]
>
> This command is mentioned in the section "Activate the Virtual Environment" on page 4 of the QUICKSTART.pdf document.
>
> When the virtual environment is active, your prompt will show (.venv) [1].

**Citations:**

- [1] QUICKSTART.pdf p.5


### pango_requirement
**Query:** What system library does AIStudio require for PDF generation and how is it installed?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 7.39s | **Pass:** ❌

**Answer:**

> To determine which system library is required for PDF generation and how it's installed, we need to look at the source that discusses PDF generation.
>
> The only relevant source here is [2] QUICKSTART.pdf. According to it:
>
> 8. Activate the Virtual Environment
> ./ais_install creates and populates the Python virtual environment automatically. Each time
> you open a new terminal tab, activate it before running any AIStudio commands:
> source ~/Developer/AIStudio/.venv/bin/activate
>
> However, there's no mention of PDF generation in this section.
>
> *[truncated — use --full for complete answer]*

**Citations:**

- [2] QUICKSTART.pdf p.5
- [3] dependencies.pdf p.1

**⚠ Model said 'no information' — possible retrieval miss**

### qdrant_wal_error
**Query:** What causes the Qdrant WAL lock error and how do you fix it?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 4.41s | **Pass:** ✅

**Answer:**

> The Qdrant WAL lock error is caused by a write-ahead log (WAL) lock being left locked from an unclean shutdown ([1]). This can happen due to an unexpected termination, such as a force-quit or power loss. To fix it, you need to:
>
> ais_stop
> rm -rf ~/qdrant_storage/collections/aistudio_help # replace with collection named in error
>
> Then re-ingest the affected corpus via the UI (Add button) ([1]).
>
> Note: This issue is not addressed in [2] or [3], which focus on architecture and testing lessons learned, respectively.

**Citations:**

- [1] QUICKSTART.pdf p.9
- [2] CODEBASE_GUIDE.pdf p.2
- [3] QA_TESTING_LESSONS_LEARNED.pdf p.5


### why_qdrant_over_chroma
**Query:** Why did AIStudio switch from ChromaDB to Qdrant as the vector store?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 3.49s | **Pass:** ✅

**Answer:**

> AIStudio switched from ChromaDB to Qdrant as the vector store because [1] ChromaDB crashed at 32,285 chunks during SEC 10-K corpus ingest, and [2] Qdrant is stable at 105,964 chunks with native metadata filtering, near-zero GC overhead, and a production upgrade path.

**Citations:**

- [1] QUICKSTART.pdf p.4
- [2] dependencies.pdf p.3


### crossencoder_purpose
**Query:** What is the CrossEncoder model used for in AIStudio and why was it added?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 3.34s | **Pass:** ✅

**Answer:**

> The CrossEncoder model is used for reranking relevant chunks from Qdrant in the query layer of AIStudio [1]. It was added to improve the ranking of retrieved chunks before they are assembled into a prompt and sent to an LLM [1].
>
> Note that there is no information provided about why the CrossEncoder model was specifically chosen, what other models were considered, or what benefits it provides over previous implementations.

**Citations:**

- [1] CODEBASE_GUIDE.pdf p.2


### single_html_frontend
**Query:** Why does AIStudio use a single HTML file for the entire frontend?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 2.74s | **Pass:** ✅

**Answer:**

> The sources do not explicitly address why AIStudio uses a single HTML file for the entire frontend.
>
> However, [2] mentions that using a single ~1,900-line file is harder to navigate than a componentized React app, but this tradeoff is deliberate – operational simplicity over developer ergonomics at this scale.

**Citations:**

- [2] architecture_decisions.pdf p.5


### corpus_metadata_yaml
**Query:** What is the purpose of the corpus metadata YAML file and when is it loaded?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 3.76s | **Pass:** ✅

**Answer:**

> The corpus metadata YAML file is loaded into the system prompt at query time, and its name is specified by replacing `{name}` in `_corpus_meta.yaml` with the actual corpus name ([3]).
>
> Note that the exact purpose of this file is not explicitly stated in any provided sources.
>
> It is mentioned in [1] that `_corpus_meta.yaml` is loaded into the system prompt at query time.

**Citations:**

- [1] CODEBASE_GUIDE.pdf p.4
- [3] HOWTO.pdf p.4


### ais_start_services
**Query:** What four processes does ais_start launch and how do you verify the backend is running?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 2.83s | **Pass:** ✅

**Answer:**

> According to [2], ais_start launches four processes:
>
> 1. Ollama,
> 2. Qdrant, 
> 3. FastAPI backend (uvicorn), and 
> 4. the frontend.
>
> To verify the backend is running, check if uvicorn is active in the terminal.

**Citations:**

- [2] QUICKSTART.pdf p.5


### corpus_ingest_command
**Query:** What is the full command to ingest the demo corpus from the terminal?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 4.97s | **Pass:** ✅

**Answer:**

> There is no specific command to ingest the demo corpus from the terminal in the provided sources [1] through [3]. The HOWTO.pdf [2] mentions ingesting a new corpus using the UI, and the QUICKSTART.pdf [1] provides general instructions for ingesting any corpus. However, it does not specify how to ingest the demo corpus specifically.
>
> The QUICKSTART.pdf mentions running `ais_bench --corpus demo` for benchmarks on the demo corpus but this is not related to ingestion. The only relevant command provided in the sources that might be used for ingestion is `ingest --corpus <name> --root data/corpora/<name>/uploads --force` from HOWTO.pdf, which mentions re-ingesting a corpus from scratch using the `--force` flag.
>
> However, there is no information on how to ingest the demo corpus specifically.

**Citations:**

- [1] QUICKSTART.pdf p.10
- [2] HOWTO.pdf p.4
- [3] architecture_decisions.pdf p.8


### ais_bench_default
**Query:** What are the default parameters when running ais_bench with no arguments?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 4.4s | **Pass:** ✅

**Answer:**

> [2][1] When running `ais_bench` with no arguments, the default parameters are not explicitly stated in either source. However, [2] provides examples of running `ais_bench` with specific options, and [1] shows an example of running `ais_bench_ops`, which is a special case for the demo corpus.
>
> To determine the default parameters, we would need to look at the code or configuration files used by AIStudio. However, based on the provided documentation, it appears that AIStudio expects users to specify the corpus and other options when running `ais_bench`.

**Citations:**

- [1] HARNESS.pdf p.4
- [2] QUICKSTART.pdf p.10


### latency_benchmark_finding
**Query:** What did AIStudio benchmarks reveal about the latency difference between llama3.1:8b and llama3.1:70b on Apple Silicon?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 5.38s | **Pass:** ✅

**Answer:**

> According to [1], warm llama3.1:8b and warm llama3.1:70b are statistically identical in query latency on Apple Silicon (~6–7s average). Additionally, [2] states that once loaded into unified memory, model size stops being a latency variable. Both sources reference the benchmarks/ directory for further analysis.
>
> Furthermore, [3] provides more specific information about model installation and management, stating that "On Apple Silicon, llama3.1:70b and llama3.1:8b have identical query latency (~6–7s) once warm." The source also recommends choosing between these two models based on available RAM, with llama3.1:8b requiring 8GB of RAM as a minimum.
>
> In summary, all three sources confirm that the latency difference between llama3.1:8b and llama3.1:70b is negligible (~6–7s) when warm on Apple Silicon.

**Citations:**

- [1] README.pdf p.3
- [2] QUICKSTART.pdf p.4
- [3] HOWTO.pdf p.5


### file_deletion_behavior
**Query:** What happens to a file when it is deleted from a corpus in AIStudio?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 5.73s | **Pass:** ✅

**Answer:**

> When a file is deleted from a corpus in AIStudio, it does not move to the trash immediately, but rather stays in its original location in the uploads directory ([1]). It is only after deletion that the file moves to the trash location, specifically `data/corpora/<name>/uploads/trash/` ([1]).
>
> If you want to recover a deleted file, you can list the contents of the trash using `ls ~/Developer/AIStudio/data/corpora/<name>/uploads/trash/`, and then move it back to its original location using `mv ~/Developer/AIStudio/data/corpora/<name>/uploads/trash/<filename> ~/Developer/AIStudio/data/corpora/<name>/uploads/`. If the file has a timestamp suffix, you'll need to specify that when moving it back ([1]).
>
> As for what happens when an entire corpus is deleted, it moves to `~/.Trash/` and is renamed to avoid conflicts with previous deletions. You can recover a deleted corpus by finding its folder in Trash using `ls ~/.Trash/ | grep AIStudio_<name>`, then moving it back and re-ingesting ([1]).

**Citations:**

- [1] HOWTO.pdf p.4


### corpus_creation_ui
**Query:** How do you create a new corpus in the AIStudio UI?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 2.48s | **Pass:** ✅

**Answer:**

> To create a new corpus in the AIStudio UI, use the "New" button to open the corpus management interface, then upload your files using the "Add" button.
>
> HOWTO.pdf | [1]

**Citations:**

- [1] HOWTO.pdf p.4


### demo_corpus_description
**Query:** What does the AIStudio demo corpus contain and what time period does it cover?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 3.8s | **Pass:** ✅

**Answer:**

> The demo corpus contains 11 documents and spans a date range from 2003 to 2021 [3]. The topics covered in the demo corpus include IT strategy frameworks, enterprise architecture methodology, financial services technology journals, cloud migration analysis, and AI reference architecture [1].
>
> Note: This answer only addresses the question of what the demo corpus contains and its time period. For further information on ingesting or managing the demo corpus, please refer to other sources.

**Citations:**

- [1] QUICKSTART.pdf p.7
- [3] DEMO_CORPUS.pdf p.4


### failed_to_fetch_fix
**Query:** How do you fix the Failed to fetch error in the AIStudio UI?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 3.54s | **Pass:** ❌

**Answer:**

> The sources do not address the specific error "Failed to fetch" in the AIStudio UI.
>
> However, according to [1], if your AIStudio aliases aren't loaded yet, you can run `source ~/.zshrc` to load them. Then try the command again on its own line.

**Citations:**

- [1] HOWTO.pdf p.2

**⚠ Model said 'no information' — possible retrieval miss**

### python_version_requirement
**Query:** Why does AIStudio require Python 3.10 or later and what fails on 3.9?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 2.99s | **Pass:** ✅

**Answer:**

> AIStudio requires Python 3.10 or later because it uses type syntax that fails on Python 3.9 [2]. The system Python on macOS is often 3.9, and if a newer version is not installed, AIStudio will fail with a TypeError: Unable to evaluate type annotation 'float | None' [1].

**Citations:**

- [1] QA_TESTING_LESSONS_LEARNED.pdf p.2
- [2] QUICKSTART.pdf p.1


### qa_testing_lesson
**Query:** What was the most significant finding from AIStudio QA testing on a fresh machine?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 4.81s | **Pass:** ❌

**Answer:**

> The most significant finding from AIStudio QA testing on a fresh machine cannot be determined with the provided information. The sources do not address this topic directly.
>
> However, [4] discusses benchmark reports and mentions that the first query in a cold session is slow (20–50s) while the LLM loads into memory, but this information does not pertain to QA testing on a fresh machine.
>
> [3] provides general guidance on benchmarking AIStudio, including how to run benchmarks using the `ais_bench` command. However, there is no explicit mention of significant findings from QA testing.
>
> The only relevant source that might be related to QA testing is [4], but it does not provide specific information about the most significant finding.
>
> *[truncated — use --full for complete answer]*

**Citations:**

- [3] HOWTO.pdf p.6
- [4] HARNESS.pdf p.4

**⚠ Model said 'no information' — possible retrieval miss**

### beta_gate_criteria
**Query:** What are the criteria for AIStudio to reach Beta status?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 3.71s | **Pass:** ✅

**Answer:**

> The criteria for AIStudio to reach Beta status is retrieval quality, full documentation, one-click installer, and API [1].
>
> In order to run the demo corpus as a benchmark and validate the complete machine-readable question set, you can execute `ais_bench` with the following command:
> PYTHONPATH=src python -m local_llm_bot.app.ingest --corpus demo --root data/corpora/demo/uploads

**Citations:**

- [1] PRODUCT_ROADMAP.pdf p.1


### v2_feature
**Query:** What is the primary new capability planned for AIStudio v2.0?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 2.84s | **Pass:** ✅

**Answer:**

> The primary new capability planned for AIStudio v2.0 is the addition of UI fields to the New Corpus modal when creating a corpus, allowing users to provide a short description, summary, and routing guidance through user-friendly interfaces [1]. Additionally, v2.0 will publish full API documentation (API_DOC.md) with request/response schemas, error codes, and examples, making the API self-documenting for developers integrating AIStudio into their workflows [1][2].

**Citations:**

- [1] PRODUCT_ROADMAP.pdf p.3
- [2] architecture_decisions.pdf p.8

