# AIStudio — Benchmark Findings
*Generated: 2026-04-19 20:41*

## Configuration
- **Corpus:** `help`
- **Top K:** 5
- **Temperature:** 0.3
- **Model:** API default
- **API:** http://localhost:8000

## Summary
- **Questions:** 18
- **Passed:** 17/18 (94%)
- **Avg latency:** 4.2s

## Infrastructure
- Vector store: Qdrant 1.17.0 (Apple Silicon, local)
- Embedding model: nomic-embed-text (768 dimensions, cosine similarity)
- Reranker: CrossEncoder ms-marco-MiniLM-L-6-v2
- Corpus: `help` (see corpus stats in UI)

## Results

| # | Description | Latency | Pass | Citations | Notes |
|---|-------------|---------|------|-----------|-------|
| 1 | How is the Qdrant binary installed in AIStudio — what curl command is used and where is the binary moved to? | 3.61s | ✅ | README.pdf | QUICKSTART Step 5 — specific curl command downloading aarch64 binary, moved to ~/bin/. Distinctive terms that only appear in the Qdrant install chunk and cannot be answered from general knowledge.
 |
| 2 | What command activates the AIStudio Python virtual environment and what prompt change confirms it? | 3.81s | ✅ | QUICKSTART.pdf | QUICKSTART Step 8 — specific to AIStudio's venv path and prompt indicator.
 |
| 3 | What system library does WeasyPrint require and how is it installed on macOS for AIStudio? | 3.73s | ✅ | dependencies.pdf, QUICKSTART.pdf, CODEBA | QUICKSTART Step 1 — pango is required by WeasyPrint for PDF generation. WeasyPrint keyword forces the right chunk.
 |
| 4 | What causes the Qdrant WAL lock error and how do you fix it? | 5.1s | ✅ | QUICKSTART.pdf, QA_TESTING_LESSONS_LEARN | HOWTO troubleshooting section — specific error pattern with specific fix.
 |
| 5 | Why did AIStudio switch from ChromaDB to Qdrant as the vector store? | 3.85s | ✅ | QUICKSTART.pdf, dependencies.pdf, CODEBA | architecture_decisions.md — explicit ADR with stated rationale.
 |
| 6 | What is the CrossEncoder model used for in AIStudio and why was it added? | 3.83s | ❌ | CODEBASE_GUIDE.pdf | architecture_decisions.md — reranking ADR. Specific model name required.
 |
| 7 | Why does AIStudio use a single HTML file for the entire frontend? | 3.29s | ✅ | CODEBASE_GUIDE.pdf, architecture_decisio | architecture_decisions.pdf — offline-first, no build step, opens directly in browser. Keywords match the ADR rationale text.
 |
| 8 | What is the purpose of the corpus metadata YAML file and when is it loaded? | 4.83s | ✅ | CODEBASE_GUIDE.pdf | CODEBASE_GUIDE — corpus_meta.yaml loaded into system prompt at query time.
 |
| 9 | What services run when AIStudio is started, what ports do they use, and what does each one do? | 8.52s | ✅ | dependencies.pdf, CODEBASE_GUIDE.pdf, QU | FILE_GUIDE.pdf services table — FastAPI:8000, Qdrant:6333, Ollama:11434. Port numbers are distinctive and only appear in the services table.
 |
| 10 | What is the full command to ingest the demo corpus from the terminal? | 4.48s | ✅ | QUICKSTART.pdf | QUICKSTART Step 10 — specific command with environment variables.
 |
| 11 | When running ais_bench with no arguments, what corpus does it target and what are the default top-k and temperature values? | 5.04s | ✅ | HARNESS.pdf | HARNESS.pdf — defaults: corpus=demo, top-k=5, temperature=0.3. Numeric values are distinctive and force the right chunk.
 |
| 12 | What did AIStudio benchmarks reveal about the latency difference between llama3.1:8b and llama3.1:70b on Apple Silicon? | 2.96s | ✅ | README.pdf, QUICKSTART.pdf | README benchmark finding — statistically indistinguishable warm latency. Strong proof point, specific to AIStudio testing.
 |
| 13 | What happens to a file when it is deleted from a corpus in AIStudio? | 4.22s | ✅ | HOWTO.pdf | HOWTO — file moved to trash/, Qdrant chunks removed surgically.
 |
| 14 | How do you create a new corpus in the AIStudio UI? | 3.46s | ✅ | HOWTO.pdf, architecture_decisions.pdf | HOWTO — UI-specific workflow for corpus creation.
 |
| 15 | What does the AIStudio demo corpus contain and what time period does it cover? | 3.5s | ✅ | DEMO_CORPUS.pdf | DEMO_CORPUS.md and README — curated 9-document corpus, 2003-2026.
 |
| 16 | What does the QUICKSTART troubleshooting section say to do when you see "Failed to fetch in UI" and the FastAPI backend is down? | 3.61s | ✅ | QUICKSTART.pdf | QUICKSTART page 9 — chunk contains exact phrase "Failed to fetch in UI" followed by kill $(lsof -ti:8000) command. Keywords match the fix commands in that specific chunk.
 |
| 17 | Why does AIStudio require Python 3.10 or later and what fails on 3.9? | 3.83s | ✅ | QUICKSTART.pdf | QUICKSTART prerequisites — float | None syntax incompatibility.
 |
| 18 | What is the Source Dive feature planned for AIStudio v2.0 and what will it enable? | 3.71s | ✅ | PRODUCT_ROADMAP.pdf | PRODUCT_ROADMAP.pdf — Source Dive is the headline v2.0 feature: click citation → open PDF at exact page with passage highlighted. Distinctive name that only appears in the roadmap. |

## Detailed Results

---
### 1. qdrant_install_method
**Query:** How is the Qdrant binary installed in AIStudio — what curl command is used and where is the binary moved to?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 3.61s | **Pass:** ✅

**Answer:**

> The Qdrant binary is installed using the following command:
>
> ```
> curl -L https://github.com/qdrant/qdrant/releases/latest/download/qdrant-aarch64-apple-darwin.tar.gz | tar xz
> mkdir -p ~/bin && mv qdrant ~/bin/qdrant && echo 'export PATH="$HOME/bin:$PATH"' >> ~/.zshrc && source ~/.zshrc
> ```
>
> This is stated in [1] README.pdf on page 3 of 7, under the section "Working today" and also partially shown.
>
> The Qdrant binary is moved to `~/bin/qdrant`.

**Citations:**

- [1] README.pdf p.4


---
### 2. venv_activation
**Query:** What command activates the AIStudio Python virtual environment and what prompt change confirms it?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 3.81s | **Pass:** ✅

**Answer:**

> To activate the AIStudio Python virtual environment, you need to run:
> ```
> source ~/Developer/AIStudio/.venv/bin/activate
> ```
> This command is mentioned in [1] QUICKSTART.pdf, page 4 of 10.
>
> Once activated, your prompt will show (.venv) when active. This confirmation is also from [1] QUICKSTART.pdf, page 4 of 10.

**Citations:**

- [1] QUICKSTART.pdf p.5


---
### 3. pango_requirement
**Query:** What system library does WeasyPrint require and how is it installed on macOS for AIStudio?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 3.73s | **Pass:** ✅

**Answer:**

> WeasyPrint requires the system library "cairo" [2]. To install it on macOS for AIStudio, run:
> ```bash
> pip install cairo
> ```
> Note that this command is not explicitly mentioned in any of the provided sources. However, based on [2], which lists Cairo as a dependency, and [3] and [4], which discuss setting up dependencies and virtual environments, it can be inferred that installing Cairo is necessary for WeasyPrint to function.
>
> Alternatively, you can install WeasyPrint using conda by running:
> ```bash
> conda install -c conda-forge weasyprint cairo
> ```
> This command installs both WeasyPrint and Cairo from the Conda Forge repository.

**Citations:**

- [2] dependencies.pdf p.1
- [3] QUICKSTART.pdf p.5
- [4] CODEBASE_GUIDE.pdf p.2


---
### 4. qdrant_wal_error
**Query:** What causes the Qdrant WAL lock error and how do you fix it?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 5.1s | **Pass:** ✅

**Answer:**

> The Qdrant WAL lock error is caused by a crash or unclean shutdown, and it results in the collection being left locked [1].
>
> To fix this issue:
>
> 1. Run `ais_stop` to stop all services.
> 2. Remove the affected collection with `rm -rf ~/qdrant_storage/collections/aistudio_help # replace with collection named in error`.
> 3. Restart the AIStudio services with `ais_start`.
>
> It is essential to note that to prevent this issue, it's crucial to always stop the services with `ais_stop` and not force-quit the terminal while running [1].
>
> *[truncated — use --full for complete answer]*

**Citations:**

- [1] QUICKSTART.pdf p.9
- [3] QA_TESTING_LESSONS_LEARNED.pdf p.5


---
### 5. why_qdrant_over_chroma
**Query:** Why did AIStudio switch from ChromaDB to Qdrant as the vector store?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 3.85s | **Pass:** ✅

**Answer:**

> AIStudio switched from ChromaDB to Qdrant as the vector store because ChromaDB crashed at 32,285 chunks during SEC 10-K corpus ingest [2][3]. Qdrant, on the other hand, is stable at 105,964 chunks and provides native metadata filtering, near-zero GC overhead, and a production upgrade path [1][2][3].

**Citations:**

- [1] QUICKSTART.pdf p.4
- [2] dependencies.pdf p.3
- [3] CODEBASE_GUIDE.pdf p.2


---
### 6. crossencoder_purpose
**Query:** What is the CrossEncoder model used for in AIStudio and why was it added?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 3.83s | **Pass:** ❌

**Answer:**

> The CrossEncoder model is used for reranking chunks retrieved from Qdrant in the query layer. This is stated on page [1] as part of the architecture overview:
>
> "The query pipeline lives in src/local_llm_bot/app/rag_core.py and is orchestrated by api.py . ... a FastAPI backend receives questions, retrieves relevant chunks from Qdrant, reranks them with a CrossEncoder, assembles a prompt, and sends it to an Ollama-hosted LLM."
>
> The sources do not address why the CrossEncoder model was added.

**Citations:**

- [1] CODEBASE_GUIDE.pdf p.2

**⚠ Model said 'no information' — possible retrieval miss**

---
### 7. single_html_frontend
**Query:** Why does AIStudio use a single HTML file for the entire frontend?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 3.29s | **Pass:** ✅

**Answer:**

> The single HTML file for the entire frontend, `front_end/rag_studio.html`, is used because of its operational simplicity and the ability to "Clone and open. Works immediately." [2] The tradeoff is that a single ~1,900-line file is harder to navigate than a componentized React app. [2]
>
> Additionally, using a single HTML file eliminates the need for a build step, npm, or node_modules, making it easier to run AIStudio on a new machine. [2][1]

**Citations:**

- [1] CODEBASE_GUIDE.pdf p.2
- [2] architecture_decisions.pdf p.5


---
### 8. corpus_metadata_yaml
**Query:** What is the purpose of the corpus metadata YAML file and when is it loaded?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 4.83s | **Pass:** ✅

**Answer:**

> The corpus metadata YAML file is loaded into the system prompt at query time as "{name} Search routing guidance — loaded into system prompt at query" [1].
>
> This suggests that the corpus metadata is used for search routing, but it does not specify when or how the _corpus_meta.yaml file is loaded. However, it is mentioned that this type of file is "Tracked in git: Only data/corpora/demo/ (full uploads tracked — ships with repo) and data/corpora/help/help_corpus_meta.yaml (config only)" [1].
>
> There is no explicit information provided on when the _corpus_meta.yaml file is loaded, but it can be inferred that it is loaded at some point after corpus creation or re-ingestion.

**Citations:**

- [1] CODEBASE_GUIDE.pdf p.4


---
### 9. ais_start_services
**Query:** What services run when AIStudio is started, what ports do they use, and what does each one do?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 8.52s | **Pass:** ✅

**Answer:**

> When AIStudio is started, the following services run:
>
> * Qdrant (vector store) on port 6333 [1]
> * Ollama (LLM host) [2] 
> * The FastAPI backend (uvicorn) on port 8000 [4]
>
> These services are required for AIStudio to function properly and can be started using the `ais_start` command.

**Citations:**

- [1] dependencies.pdf p.2
- [2] CODEBASE_GUIDE.pdf p.2
- [4] QUICKSTART.pdf p.6


---
### 10. corpus_ingest_command
**Query:** What is the full command to ingest the demo corpus from the terminal?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 4.48s | **Pass:** ✅

**Answer:**

> To ingest the demo corpus from the terminal, you need to run the following command:
>
> ```bash
> AISTUDIO_VECTORSTORE=qdrant PYTHONPATH=src python3 -m local_llm_bot.app.ingest \
> --corpus demo --root data/corpora/demo/uploads --force
> ```
>
> [1] This command is found on Page 10 of QUICKSTART.pdf, which provides instructions for ingesting the demo corpus.
>
> Note that this command uses the `--force` flag to wipe and rebuild the corpus cleanly.

**Citations:**

- [1] QUICKSTART.pdf p.10


---
### 11. ais_bench_default
**Query:** When running ais_bench with no arguments, what corpus does it target and what are the default top-k and temperature values?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 5.04s | **Pass:** ✅

**Answer:**

> When running `ais_bench` with no arguments, it targets the demo corpus and uses default top-k and temperature values.
>
> The sources state that `ais_bench` runs all 12 demo questions against the demo corpus by default (HARNESS.pdf). Additionally, the CLI Reference in HARNESS.pdf lists the default values for the `--top-k` and `--temperature` options as 5 and 0.3, respectively.
>
> Therefore, when running `ais_bench` with no arguments, it targets the demo corpus [1] and uses default top-k and temperature values [1].
>
> Specifically:
>
> *[truncated — use --full for complete answer]*

**Citations:**

- [1] HARNESS.pdf p.1


---
### 12. latency_benchmark_finding
**Query:** What did AIStudio benchmarks reveal about the latency difference between llama3.1:8b and llama3.1:70b on Apple Silicon?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 2.96s | **Pass:** ✅

**Answer:**

> According to [2] and [1], AIStudio benchmarks revealed that warm llama3.1:8b and llama3.1:70b on Apple Silicon have identical query latency (~6–7s).

**Citations:**

- [1] README.pdf p.3
- [2] QUICKSTART.pdf p.4


---
### 13. file_deletion_behavior
**Query:** What happens to a file when it is deleted from a corpus in AIStudio?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 4.22s | **Pass:** ✅

**Answer:**

> When a file is deleted from a corpus in AIStudio, it does not get permanently deleted [1]. Instead, the deleted file moves to data/corpora/<name>/uploads/trash/, where it can be recovered. To recover the deleted file, one needs to move it back from trash using the terminal command `mv ~/Developer/AIStudio/data/corpora/<name>/uploads/trash/<filename> ~/Developer/AIStudio/data/corpora/<name>/uploads/` [1].

**Citations:**

- [1] HOWTO.pdf p.4


---
### 14. corpus_creation_ui
**Query:** How do you create a new corpus in the AIStudio UI?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 3.46s | **Pass:** ✅

**Answer:**

> To create a new corpus in the AIStudio UI:
>
> 1. Open AIStudio.
> 2. Create a new corpus using the New button.
> 3. Upload your files using the Add button.
>
> AIStudio will handle ingestion automatically and show progress in the chat area. [HOWTO][1,2]
>
> Note: The HOWTO document provides a step-by-step guide on how to ingest a new corpus using the UI. The architecture decisions document [2] does not provide information on creating a new corpus in the UI, but rather focuses on the API endpoints related to corpora.

**Citations:**

- [1] HOWTO.pdf p.4
- [2] architecture_decisions.pdf p.8


---
### 15. demo_corpus_description
**Query:** What does the AIStudio demo corpus contain and what time period does it cover?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 3.5s | **Pass:** ✅

**Answer:**

> The demo corpus contains 11 documents spanning a date range of [3] 2003 — 2021. It covers the domain of financial services technology architecture and includes formats such as PDF, PPTX, and PPT.

**Citations:**

- [3] DEMO_CORPUS.pdf p.4


---
### 16. failed_to_fetch_fix
**Query:** What does the QUICKSTART troubleshooting section say to do when you see "Failed to fetch in UI" and the FastAPI backend is down?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 3.61s | **Pass:** ✅

**Answer:**

> [2] When you see "Failed to fetch in UI" and the FastAPI backend is down, run:
>
> ```
> kill $(lsof -ti:8000)
> cd ~/Developer/AIStudio && source .venv/bin/activate
> OLLAMA_KEEP_ALIVE=30m AISTUDIO_VECTORSTORE=qdrant PYTHONPATH=src \
> uvicorn local_llm_bot.app.api:app --reload --port 8000
> ```
>
> This is stated in the QUICKSTART.pdf document, page 8.

**Citations:**

- [2] QUICKSTART.pdf p.9


---
### 17. python_version_requirement
**Query:** Why does AIStudio require Python 3.10 or later and what fails on 3.9?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 3.83s | **Pass:** ✅

**Answer:**

> AIStudio requires Python 3.10 or later because it uses type syntax (float | None) that fails on Python 3.9 [2]. This is explicitly stated in the QUICKSTART document, which advises users to install a newer version of Python if their system Python is 3.9 [2].

**Citations:**

- [2] QUICKSTART.pdf p.1


---
### 18. v2_feature
**Query:** What is the Source Dive feature planned for AIStudio v2.0 and what will it enable?
**Firm filter:** `none` | **Year filter:** `none`
**Latency:** 3.71s | **Pass:** ✅

**Answer:**

> The Source Dive feature, planned for AIStudio v2.0, will enable users to click a citation and have the PDF open at the exact page with the cited passage highlighted [1]. The backend already stores chunk-level page positions in Qdrant, but the remaining work is implementing the frontend PDF viewer using PDF.js [1].

**Citations:**

- [1] PRODUCT_ROADMAP.pdf p.1

