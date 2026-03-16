# Testing

AIStudio has two test layers: **unit tests** (no server required) and **integration tests** (live API). Both live in `tests/`.

---

## Files

| File | Type | What it tests |
|---|---|---|
| `test_aistudio.py` | Integration + Unit | API endpoints, RAG pipeline, citations, conversation memory, corpus management |
| `test_embeddings.py` | Integration | Embedding model quality (King − Man + Woman = Queen, etc.) |
| `test_page_number_pipeline.py` | Unit | Page number extraction pipeline — [PAGE_N] markers → chunk_id → RetrievedDoc.page |
| `test_rag_core_jsonl.py` | Unit | JSONL retrieval path, deterministic results without Qdrant |
| `test_corpus_paths.py` | Unit | Corpus path structure and directory creation |
| `test_health.py` | Unit | /health endpoint via FastAPI TestClient |
| `embedding_arithmetic.py` | Interactive tool | Explore embedding arithmetic interactively or as a test suite |

---

## Prerequisites

Backend must be running for integration tests:

```bash
# Terminal 1 — start Ollama
ollama serve

# Terminal 2 — start the backend
source .venv/bin/activate
AISTUDIO_VECTORSTORE=qdrant PYTHONPATH=src uvicorn local_llm_bot.app.api:app --reload --port 8000
```

The **demo corpus must be ingested** for citation and retrieval tests to pass.
On first run, `scripts/start.sh` handles this automatically. To ingest manually:

```bash
AISTUDIO_VECTORSTORE=qdrant PYTHONPATH=src python3 -m local_llm_bot.app.ingest \
  --corpus demo --root data/demo/demo_data
```

Use `--force` to wipe and rebuild cleanly if chunk format has changed:

```bash
AISTUDIO_VECTORSTORE=qdrant PYTHONPATH=src python3 -m local_llm_bot.app.ingest \
  --corpus demo --root data/demo/demo_data --force
```

The `rag` group (unit tests) has no server dependency and can run any time.

---

## Running Tests

```bash
cd /path/to/AIStudio
source .venv/bin/activate
```

**Run everything:**
```bash
python tests/test_aistudio.py
```

**Run a specific group:**
```bash
python tests/test_aistudio.py --group citations
python tests/test_aistudio.py --group memory
python tests/test_aistudio.py --group rag        # unit tests only — no server needed
```

**Against a non-default port:**
```bash
python tests/test_aistudio.py --base-url http://localhost:8001
```

**Skip unit tests (if src not on path):**
```bash
python tests/test_aistudio.py --skip-units
```

---

## Test Groups

| Group flag | Tests | Server needed |
|---|---|---|
| `health` | `/health` endpoint, content-type | Yes |
| `models` | `/models` shape, llama3.1:8b present | Yes |
| `config` | `/config` has required fields | Yes |
| `corpora` | List, create, info, delete, demo exists | Yes |
| `api` | `/ask` shape, empty/missing query, bad corpus | Yes |
| `citations` | `has_citations`, index integrity, no duplicates | Yes |
| `memory` | `conversation_history` field, follow-up coherence | Yes |
| `retrieval` | `/debug/retrieve`, `/debug/stats` | Yes |
| `rag` | Dataclasses, citation regex patterns (unit tests) | **No** |

---

## What the Citation Tests Cover

The citation group specifically validates the extraction logic that maps model output to source metadata:

- `has_citations=True` and citations list non-empty for known-good queries
- All citation indices are positive integers
- Indices referenced in answer text (`[1]`, `[Source 3]`) match the returned citations list
- No duplicate indices in a single response
- **Regression: `[Source N]` pattern** — was missed by the old single-pass regex; now caught by the two-pass extractor in `rag_core.py`
- **Regression: `[1, 2]` with space after comma** — now handled correctly

---

## Embedding Quality Tests

These test the semantic quality of `nomic-embed-text` (or whichever embedding model is configured). They do not test the RAG pipeline.

```bash
python tests/test_embeddings.py
```

Three tests run: King/Queen/Man/Woman, Paris/France/Italy/Rome, Python/Django/JavaScript. All should pass with similarity score > 0.75. If they fail, re-pull the embedding model:

```bash
ollama pull nomic-embed-text
```

For interactive exploration of embedding arithmetic:

```bash
python tests/embedding_arithmetic.py --interactive
python tests/embedding_arithmetic.py --category tech
python tests/embedding_arithmetic.py --custom king queen man "woman,girl,lady,princess"
```

---

## Interpreting Output

```
── Citations ──
  ✓ has_citations=True and citations non-empty for QFD query  (4.21s)
  ✓ All citation indices are > 0
  ✓ Indices in answer text match returned citations list  (3.87s)
  ✗ No duplicate citation indices in response
      → Duplicate citation indices: [1, 2, 1]
```

A `✗` line shows the assertion message directly. Latency is printed only when > 0.1s.

Exit code is `0` if all tests pass, `1` if any fail — suitable for CI.

---

## Adding Tests

All test groups follow the same pattern:

```python
def test_my_feature(c: Client) -> Suite:
    suite = Suite("My Feature")
    print(f"\n── {suite.name} ──")

    def check_something():
        data = c.ask("some query", top_k=3)
        assert data["answer"].strip(), "answer was empty"

    run_test(suite, "Description of what is being checked", check_something)
    return suite
```

Register it in `GROUP_MAP` at the bottom of the file and it becomes available as `--group my_feature`.

---

## Page Number Pipeline Tests

`test_page_number_pipeline.py` validates the full page number chain without
requiring any external services:

```bash
pytest tests/test_page_number_pipeline.py -v
```

10 tests covering:
- `[PAGE_N]` marker regex extraction
- Marker stripping from chunk text
- Continuation chunk handling (null page expected)
- Cross-page boundary chunks (uses first page)
- `chunk_id` encoding format
- `RetrievedDoc.page` field
- `extract_page_number()` fallback parsing

All 10 pass without Ollama or Qdrant running.

---

## Known Limitations

- Tests are **integration tests hitting a live local API** — they are not hermetic. Flaky results can indicate Ollama being slow or the model not yet loaded into memory (first query latency is 20–50s).
- Citation content tests are soft: we verify structure and index integrity, not the semantic correctness of answers.
- No coverage yet for `/corpus/{name}/upload` (requires multipart file upload fixtures) or ingest pipeline directly.
