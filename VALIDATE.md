# Validation

`validate.sh` is the single command to verify that AIStudio is working correctly — from a fresh clone, after code changes, or before sharing the repo.

---

## Usage

```bash
./validate.sh              # full validation
./validate.sh --unit-only  # unit tests only, no live services needed
```

---

## What It Runs

The script runs three phases in sequence. Each phase is announced clearly in the output so you know exactly where you are.

### Phase 1 — Unit tests
**Requires:** Nothing. Runs anywhere, any time.

Runs the pytest suite covering RAG core internals, corpus path resolution, Chroma query contracts, embedding quality, and API health. These tests use no live services and complete in under 2 seconds.

```
PYTHONPATH=src pytest -v -m "not integration"
```

### Phase 2 — Integration tests
**Requires:** Ollama running (`brew services start ollama`). Skips gracefully if Ollama is not available.

Runs pytest integration tests that exercise the API layer against a live Ollama instance. The `test_ask_integration` test skips automatically if the required model isn't pulled — no manual intervention needed.

```
PYTHONPATH=src pytest -v -m "integration"
```

### Phase 3 — Live API tests
**Requires:** Backend running + Ollama running + demo corpus ingested. Skips gracefully if the backend is not reachable.

Runs `tests/test_aistudio.py` — a standalone test harness that fires real queries against the live API and validates answers, citations, corpus management, and conversation memory. This is the most comprehensive test of the full stack.

```
PYTHONPATH=src python tests/test_aistudio.py
```

To start the backend before running this phase:
```bash
PYTHONPATH=src uvicorn local_llm_bot.app.api:app --port 8000
```

---

## Exit Codes

| Code | Meaning |
|---|---|
| `0` | All phases passed (or skipped gracefully) |
| `1` | One or more phases failed |

This makes `validate.sh` safe to use in CI pipelines — a non-zero exit stops the pipeline.

---

## Typical Outputs

**Quick sanity check (no services needed):**
```bash
./validate.sh --unit-only
```
```
Phase 1 — Unit tests
  ✓ Unit tests passed

Phase 2 — Integration tests
  ⚠ Skipped (--unit-only)

Phase 3 — Live API tests
  ⚠ Skipped (--unit-only)

  ALL CLEAR — 1 passed, 2 skipped, 0 failed
```

**Full validation (all services running):**
```bash
./validate.sh
```
```
Phase 1 — Unit tests
  ✓ Unit tests passed

Phase 2 — Integration tests
  ✓ Integration tests passed (or skipped gracefully)

Phase 3 — Live API tests
  Backend reachable at localhost:8000 ✓
  ✓ Live API tests passed

  ALL CLEAR — 3 passed, 0 skipped, 0 failed
```

---

## When to Run

| Situation | Command |
|---|---|
| After cloning on a new machine | `./validate.sh` |
| After any code change | `./validate.sh --unit-only` |
| Before pushing to GitHub | `./validate.sh` |
| MacBook Air / lower-spec hardware test | `./validate.sh` |
| CI pipeline | `./validate.sh --unit-only` |
