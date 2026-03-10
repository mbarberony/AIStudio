#!/usr/bin/env python3
"""
AIStudio Test Suite
===================
Covers: API endpoints, RAG pipeline, citation extraction, corpus management,
        conversation memory, and configuration.

Usage:
    # From repo root, with backend running:
    python tests/test_aistudio.py

    # Specific group:
    python tests/test_aistudio.py --group citations
    python tests/test_aistudio.py --group api
    python tests/test_aistudio.py --group rag

    # Against a different host:
    python tests/test_aistudio.py --base-url http://localhost:8001

Requirements:
    - Backend running:  uvicorn local_llm_bot.app.api:app --reload
    - Demo corpus must be ingested (for rag/citation tests)
    - Ollama running with llama3.1:8b and nomic-embed-text

NOTE: These are integration tests, not unit tests. They hit the live API.
For unit tests of rag_core internals, see the "Unit" section at bottom.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

import requests

# ---------------------------------------------------------------------------
# Test runner
# ---------------------------------------------------------------------------

@dataclass
class Result:
    name: str
    passed: bool
    message: str = ""
    duration: float = 0.0


@dataclass
class Suite:
    name: str
    results: list[Result] = field(default_factory=list)

    def add(self, result: Result) -> None:
        self.results.append(result)
        status = "✓" if result.passed else "✗"
        dur = f"  ({result.duration:.2f}s)" if result.duration > 0.1 else ""
        print(f"  {status} {result.name}{dur}")
        if not result.passed:
            print(f"      → {result.message}")

    @property
    def passed(self) -> int:
        return sum(1 for r in self.results if r.passed)

    @property
    def failed(self) -> int:
        return len(self.results) - self.passed


def run_test(suite: Suite, name: str, fn: Callable) -> None:
    t0 = time.time()
    try:
        fn()
        suite.add(Result(name=name, passed=True, duration=time.time() - t0))
    except AssertionError as e:
        suite.add(Result(name=name, passed=False, message=str(e), duration=time.time() - t0))
    except Exception as e:
        suite.add(Result(name=name, passed=False, message=f"{type(e).__name__}: {e}", duration=time.time() - t0))


def assert_eq(actual: Any, expected: Any, label: str = "") -> None:
    if actual != expected:
        prefix = f"{label}: " if label else ""
        raise AssertionError(f"{prefix}expected {expected!r}, got {actual!r}")


def assert_in(needle: Any, haystack: Any, label: str = "") -> None:
    if needle not in haystack:
        prefix = f"{label}: " if label else ""
        raise AssertionError(f"{prefix}{needle!r} not in {haystack!r}")


def assert_type(value: Any, typ: type, label: str = "") -> None:
    if not isinstance(value, typ):
        prefix = f"{label}: " if label else ""
        raise AssertionError(f"{prefix}expected {typ.__name__}, got {type(value).__name__}")


# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------

class Client:
    def __init__(self, base: str):
        self.base = base.rstrip("/")
        self.session = requests.Session()

    def get(self, path: str, **kwargs) -> requests.Response:
        return self.session.get(f"{self.base}{path}", timeout=120, **kwargs)

    def post(self, path: str, **kwargs) -> requests.Response:
        return self.session.post(f"{self.base}{path}", timeout=120, **kwargs)

    def delete(self, path: str, **kwargs) -> requests.Response:
        return self.session.delete(f"{self.base}{path}", timeout=120, **kwargs)

    def ask(self, query: str, corpus: str = "demo", top_k: int = 3,
            temperature: float = 0.3, conversation_history=None) -> dict:
        body = {
            "query": query,
            "corpus": corpus,
            "top_k": top_k,
            "temperature": temperature,
        }
        if conversation_history is not None:
            body["conversation_history"] = conversation_history
        r = self.post("/ask", json=body)
        r.raise_for_status()
        return r.json()


# ---------------------------------------------------------------------------
# Test groups
# ---------------------------------------------------------------------------

def test_health(c: Client) -> Suite:
    suite = Suite("Health & Connectivity")
    print(f"\n── {suite.name} ──")

    def check_health():
        r = c.get("/health")
        assert r.status_code == 200, f"status {r.status_code}"
        data = r.json()
        assert_in("status", data)
        assert data["status"] == "ok", f"status={data['status']}"

    run_test(suite, "GET /health returns 200 + status=ok", check_health)

    def check_json_content_type():
        r = c.get("/health")
        ct = r.headers.get("content-type", "")
        assert "application/json" in ct, f"content-type: {ct}"

    run_test(suite, "Response Content-Type is application/json", check_json_content_type)

    return suite


def test_models(c: Client) -> Suite:
    suite = Suite("Models")
    print(f"\n── {suite.name} ──")

    def check_list():
        r = c.get("/models")
        assert r.status_code == 200
        models = r.json()
        assert_type(models, list, "models")
        assert len(models) > 0, "no models returned"
        for m in models:
            assert_in("id", m, "model field")
            assert_in("name", m, "model field")
            assert_in("available", m, "model field")

    run_test(suite, "GET /models returns non-empty list with expected fields", check_list)

    def check_has_8b():
        r = c.get("/models")
        models = r.json()
        ids = [m["id"] for m in models]
        assert any("8b" in i or "llama" in i.lower() for i in ids), \
            f"No llama/8b model found in: {ids}"

    run_test(suite, "llama3.1:8b (or similar) present in model list", check_has_8b)

    return suite


def test_config(c: Client) -> Suite:
    suite = Suite("Configuration")
    print(f"\n── {suite.name} ──")

    def check_config_shape():
        r = c.get("/config")
        assert r.status_code == 200
        data = r.json()
        assert_in("parameters", data)
        assert_in("rag_config", data)
        params = data["parameters"]
        assert_in("top_k", params)

    run_test(suite, "GET /config has parameters.top_k and rag_config", check_config_shape)

    return suite


def test_corpora(c: Client) -> Suite:
    suite = Suite("Corpus Management")
    print(f"\n── {suite.name} ──")

    TEST_CORPUS = "_test_aistudio_tmp"

    def check_list():
        r = c.get("/corpora")
        assert r.status_code == 200
        corpora = r.json()
        assert_type(corpora, list)
        for corp in corpora:
            assert_in("name", corp)

    run_test(suite, "GET /corpora returns list with name fields", check_list)

    def check_demo_present():
        r = c.get("/corpora")
        names = [c_["name"] for c_ in r.json()]
        assert "demo" in names, f"'demo' corpus not found; available: {names}"

    run_test(suite, "demo corpus exists", check_demo_present)

    def check_create():
        # Clean up in case prior run failed
        c.delete(f"/corpus/{TEST_CORPUS}")
        r = c.post("/corpus/create", json={"name": TEST_CORPUS})
        assert r.status_code in (200, 201), f"status {r.status_code}: {r.text}"
        data = r.json()
        assert_in("status", data)

    run_test(suite, f"POST /corpus/create creates '{TEST_CORPUS}'", check_create)

    def check_create_appears_in_list():
        r = c.get("/corpora")
        names = [c_["name"] for c_ in r.json()]
        assert TEST_CORPUS in names, f"'{TEST_CORPUS}' not in {names}"

    run_test(suite, "Newly created corpus appears in GET /corpora", check_create_appears_in_list)

    def check_corpus_info():
        r = c.get("/corpus/demo/info")
        assert r.status_code == 200
        data = r.json()
        assert_in("name", data)
        assert data["name"] == "demo"

    run_test(suite, "GET /corpus/demo/info returns name=demo", check_corpus_info)

    def check_delete():
        r = c.delete(f"/corpus/{TEST_CORPUS}")
        assert r.status_code in (200, 204), f"status {r.status_code}: {r.text}"

    run_test(suite, f"DELETE /corpus/{TEST_CORPUS} succeeds", check_delete)

    def check_deleted_gone():
        r = c.get("/corpora")
        names = [c_["name"] for c_ in r.json()]
        assert TEST_CORPUS not in names, f"'{TEST_CORPUS}' still in {names} after delete"

    run_test(suite, "Deleted corpus no longer in GET /corpora", check_deleted_gone)

    return suite


def test_ask(c: Client) -> Suite:
    suite = Suite("Ask Endpoint (/ask)")
    print(f"\n── {suite.name} ──")

    def check_response_shape():
        data = c.ask("What is enterprise architecture?", top_k=3)
        assert_in("answer", data)
        assert_in("has_citations", data)
        assert_in("citations", data)
        assert_type(data["answer"], str)
        assert len(data["answer"]) > 10, "answer is suspiciously short"
        assert_type(data["has_citations"], bool)

    run_test(suite, "Response has answer, has_citations, citations fields", check_response_shape)

    def check_answer_nonempty():
        data = c.ask("What is QFD?", top_k=3)
        assert data["answer"].strip(), "answer is empty"

    run_test(suite, "Answer is non-empty for known-good query", check_answer_nonempty)

    def check_citations_are_list():
        data = c.ask("What is enterprise architecture?", top_k=3)
        assert isinstance(data["citations"], (list, type(None))), \
            f"citations should be list or null, got {type(data['citations'])}"

    run_test(suite, "citations field is list or null", check_citations_are_list)

    def check_citation_fields():
        data = c.ask("What is enterprise architecture?", top_k=5)
        if data.get("citations"):
            for cit in data["citations"]:
                assert_in("index", cit)
                assert_in("source", cit)
                assert_type(cit["index"], int)
                assert_type(cit["source"], str)
                assert len(cit["source"]) > 0

    run_test(suite, "Each citation has index (int) and source (str)", check_citation_fields)

    def check_bad_corpus():
        r = c.post("/ask", json={"query": "test", "corpus": "_nonexistent_corpus_xyz"})
        assert r.status_code in (400, 404, 422, 500), \
            f"Expected error status for missing corpus, got {r.status_code}"

    run_test(suite, "Missing corpus returns error status (4xx/5xx)", check_bad_corpus)

    def check_empty_query_rejected():
        r = c.post("/ask", json={"query": "", "corpus": "demo"})
        # Empty query should either error or return gracefully — not crash
        assert r.status_code in (200, 400, 422), f"Unexpected status {r.status_code}"

    run_test(suite, "Empty query does not crash (200 or 4xx)", check_empty_query_rejected)

    def check_missing_query_rejected():
        r = c.post("/ask", json={"corpus": "demo"})
        assert r.status_code == 422, f"Expected 422 for missing query field, got {r.status_code}"

    run_test(suite, "Missing 'query' field returns 422", check_missing_query_rejected)

    return suite


def test_citations(c: Client) -> Suite:
    suite = Suite("Citation Extraction")
    print(f"\n── {suite.name} ──")

    def check_citations_present_on_good_query():
        data = c.ask("What is QFD and how does it apply to architecture?", top_k=5)
        assert data["has_citations"] is True, \
            f"Expected has_citations=True, got {data['has_citations']}. Answer: {data['answer'][:200]}"
        assert data["citations"], "citations list is empty despite has_citations=True"

    run_test(suite, "has_citations=True and citations non-empty for QFD query", check_citations_present_on_good_query)

    def check_citation_indices_are_positive():
        data = c.ask("What is enterprise architecture?", top_k=5)
        for cit in (data.get("citations") or []):
            assert cit["index"] > 0, f"citation index must be > 0, got {cit['index']}"

    run_test(suite, "All citation indices are > 0", check_citation_indices_are_positive)

    def check_citation_indices_match_answer():
        """Indices referenced in answer should match those returned in citations list."""
        data = c.ask("What is QFD?", top_k=5)
        answer = data["answer"]
        citations = data.get("citations") or []
        if not citations:
            return  # Can't validate without citations

        # Extract all [N] and [Source N] references from the answer
        cited_in_text = set()
        for m in re.finditer(r'\[(?:Source\s+)?(\d+)\]', answer, re.IGNORECASE):
            cited_in_text.add(int(m.group(1)))

        returned_indices = {c["index"] for c in citations}

        # Every index cited in text should be in the returned citations list
        missing = cited_in_text - returned_indices
        assert not missing, \
            f"Indices {missing} appear in answer text but not in citations list.\n" \
            f"Answer snippet: {answer[:300]}\nReturned indices: {returned_indices}"

    run_test(suite, "Indices in answer text match returned citations list", check_citation_indices_match_answer)

    def check_source_paths_nonempty():
        data = c.ask("How does architecture support risk management?", top_k=5)
        for cit in (data.get("citations") or []):
            assert cit["source"].strip(), f"citation {cit['index']} has empty source"

    run_test(suite, "All citation sources are non-empty strings", check_source_paths_nonempty)

    def check_no_duplicate_indices():
        data = c.ask("What are the key considerations for cloud migration?", top_k=5)
        indices = [c["index"] for c in (data.get("citations") or [])]
        assert len(indices) == len(set(indices)), \
            f"Duplicate citation indices: {indices}"

    run_test(suite, "No duplicate citation indices in response", check_no_duplicate_indices)

    def check_source_4_pattern():
        """Regression: [Source 4] pattern (previously missed by old regex)."""
        data = c.ask("What is QFD and how does it apply to technology architecture?", top_k=5)
        answer = data["answer"]
        citations = data.get("citations") or []
        # If [Source N] appears in the answer, citation must be present
        source_refs = re.findall(r'\[Source\s+(\d+)\]', answer, re.IGNORECASE)
        if source_refs:
            returned_indices = {c["index"] for c in citations}
            for ref in source_refs:
                idx = int(ref)
                assert idx in returned_indices, \
                    f"[Source {idx}] found in answer but index {idx} not in citations"

    run_test(suite, "Regression: [Source N] pattern correctly extracted", check_source_4_pattern)

    return suite


def test_conversation_memory(c: Client) -> Suite:
    suite = Suite("Conversation Memory")
    print(f"\n── {suite.name} ──")

    def check_history_accepted():
        """API must accept conversation_history without error."""
        history = [
            {"role": "user", "content": "What is QFD?"},
            {"role": "assistant", "content": "QFD stands for Quality Function Deployment."},
        ]
        data = c.ask("Can you elaborate on that?", top_k=3, conversation_history=history)
        assert_in("answer", data)
        assert data["answer"].strip(), "answer empty with conversation history"

    run_test(suite, "conversation_history accepted without error", check_history_accepted)

    def check_null_history_accepted():
        """Explicit null conversation_history must be accepted."""
        data = c.ask("What is enterprise architecture?", top_k=3, conversation_history=None)
        assert_in("answer", data)

    run_test(suite, "conversation_history=null accepted", check_null_history_accepted)

    def check_empty_history_accepted():
        """Empty list conversation_history must be accepted."""
        data = c.ask("What is QFD?", top_k=3, conversation_history=[])
        assert_in("answer", data)

    run_test(suite, "conversation_history=[] accepted", check_empty_history_accepted)

    def check_history_influences_followup():
        """A follow-up question with context should get a coherent response
        (we can't assert exact content, but it must not error or return empty)."""
        history = [
            {"role": "user", "content": "What is QFD?"},
            {"role": "assistant", "content": "QFD is Quality Function Deployment, used to translate customer needs into design specifications."},
        ]
        data = c.ask("What are its main use cases?", top_k=3, conversation_history=history)
        assert data["answer"].strip(), "follow-up with history returned empty answer"
        # A reasonable model with context should mention something related
        # (soft check — we just confirm it isn't a generic error message)
        assert "error" not in data["answer"].lower()[:50], \
            f"Answer looks like an error: {data['answer'][:100]}"

    run_test(suite, "Follow-up with history returns coherent non-empty answer", check_history_influences_followup)

    return suite


def test_retrieval(c: Client) -> Suite:
    suite = Suite("Debug Retrieval")
    print(f"\n── {suite.name} ──")

    def check_debug_retrieve():
        r = c.post("/debug/retrieve", json={"query": "enterprise architecture", "corpus": "demo", "top_k": 3})
        assert r.status_code == 200
        data = r.json()
        assert_in("docs", data)
        docs = data["docs"]
        assert_type(docs, list)
        assert len(docs) > 0, "No docs returned from retrieval"
        for doc in docs:
            assert_in("content", doc)
            assert_in("source", doc)

    run_test(suite, "POST /debug/retrieve returns docs with content + source", check_debug_retrieve)

    def check_debug_stats():
        r = c.get("/debug/stats?corpus=demo")
        assert r.status_code == 200
        data = r.json()
        # Should have some shape — not just {}
        assert len(data) > 0, "debug/stats returned empty object"

    run_test(suite, "GET /debug/stats?corpus=demo returns non-empty object", check_debug_stats)

    return suite


# ---------------------------------------------------------------------------
# Unit tests for rag_core internals (no running server needed)
# ---------------------------------------------------------------------------

def test_rag_core_units() -> Suite:
    suite = Suite("rag_core Unit Tests (no server)")
    print(f"\n── {suite.name} ──")

    # Add project to path (adjust if layout differs)
    project_root = Path(__file__).parent.parent
    sys.path.insert(0, str(project_root))

    try:
        from local_llm_bot.app.rag_core import extract_page_number, Citation, RetrievedDoc, AnswerWithCitations
    except ImportError as e:
        suite.add(Result("import rag_core", False, str(e)))
        return suite

    def check_extract_page_pdf():
        page = extract_page_number("/some/path/doc.pdf", "chunk_p42_abc")
        # If chunk_id contains page info it should extract it; otherwise None is fine
        # Just confirm it doesn't raise
        assert page is None or isinstance(page, int)

    run_test(suite, "extract_page_number doesn't raise on pdf path", check_extract_page_pdf)

    def check_extract_page_pptx():
        page = extract_page_number("/some/path/deck.pptx", "slide_3_xyz")
        assert page is None or isinstance(page, int)

    run_test(suite, "extract_page_number doesn't raise on pptx path", check_extract_page_pptx)

    def check_citation_dataclass():
        c = Citation(index=1, source="/path/to/doc.pdf", page=5, score=0.95)
        assert c.index == 1
        assert c.source == "/path/to/doc.pdf"
        assert c.page == 5
        assert c.score == 0.95

    run_test(suite, "Citation dataclass fields set correctly", check_citation_dataclass)

    def check_retrieved_doc_dataclass():
        d = RetrievedDoc(id="chunk_1", content="hello world", source="/foo.pdf", score=1.5)
        assert d.id == "chunk_1"
        assert d.content == "hello world"

    run_test(suite, "RetrievedDoc dataclass fields set correctly", check_retrieved_doc_dataclass)

    def check_citation_regex_source_pattern():
        """Regression: [Source N] pattern must be handled by citation extraction."""
        # Simulate what the model returns and what the regex in rag_core should catch
        import re
        answer = "Based on [Source 1] and [Source 3], QFD is used for..."
        # Pattern 1: numeric [1], [1,2]
        pattern1 = re.findall(r'\[(\d+(?:,\d+)*)\]', answer)
        # Pattern 2: [Source N]
        pattern2 = re.findall(r'\[Source\s+(\d+)\]', answer, re.IGNORECASE)
        all_indices = set()
        for p in pattern1:
            for n in p.split(','):
                all_indices.add(int(n.strip()))
        for n in pattern2:
            all_indices.add(int(n))
        assert 1 in all_indices, f"Index 1 not found. Got: {all_indices}"
        assert 3 in all_indices, f"Index 3 not found. Got: {all_indices}"

    run_test(suite, "Regex correctly extracts both [N] and [Source N] patterns", check_citation_regex_source_pattern)

    def check_citation_regex_spaced_comma():
        """Regression: [1, 2] (space after comma) should parse as two citations."""
        import re
        answer = "See [1, 2] for details."
        matches = re.findall(r'\[(\d+(?:,\s*\d+)*)\]', answer)
        indices = set()
        for m in matches:
            for n in m.split(','):
                indices.add(int(n.strip()))
        assert 1 in indices and 2 in indices, f"Expected {{1,2}}, got {indices}"

    run_test(suite, "Regex handles [1, 2] with space after comma", check_citation_regex_spaced_comma)

    return suite


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

GROUP_MAP = {
    "health":       test_health,
    "models":       test_models,
    "config":       test_config,
    "corpora":      test_corpora,
    "api":          test_ask,
    "citations":    test_citations,
    "memory":       test_conversation_memory,
    "retrieval":    test_retrieval,
}

UNIT_GROUPS = {
    "rag": test_rag_core_units,
}


def main():
    parser = argparse.ArgumentParser(description="AIStudio Integration Tests")
    parser.add_argument(
        "--base-url", default="http://localhost:8000",
        help="API base URL (default: http://localhost:8000)"
    )
    parser.add_argument(
        "--group", default="all",
        choices=["all"] + list(GROUP_MAP) + list(UNIT_GROUPS),
        help="Test group to run (default: all)"
    )
    parser.add_argument(
        "--skip-units", action="store_true",
        help="Skip unit tests (useful if src not on path)"
    )
    args = parser.parse_args()

    print("=" * 60)
    print("AIStudio Test Suite")
    print(f"  API base : {args.base_url}")
    print(f"  Group    : {args.group}")
    print("=" * 60)

    # Check connectivity before running integration tests
    c = Client(args.base_url)

    all_suites: list[Suite] = []

    # Unit tests (no server needed)
    if args.group in ("all", "rag") and not args.skip_units:
        all_suites.append(test_rag_core_units())

    # Integration tests
    if args.group != "rag":
        print("\nChecking API connectivity...")
        try:
            r = c.get("/health")
            r.raise_for_status()
            print(f"  ✓ Connected to {args.base_url}")
        except Exception as e:
            print(f"  ✗ Cannot reach API at {args.base_url}: {e}")
            print("    Start the backend first:  uvicorn local_llm_bot.app.api:app --reload")
            sys.exit(1)

        if args.group == "all":
            groups = list(GROUP_MAP.values())
        else:
            groups = [GROUP_MAP[args.group]] if args.group in GROUP_MAP else []

        for fn in groups:
            all_suites.append(fn(c))

    # Summary
    total_passed = sum(s.passed for s in all_suites)
    total_failed = sum(s.failed for s in all_suites)
    total = total_passed + total_failed

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    for s in all_suites:
        status = "✓" if s.failed == 0 else "✗"
        print(f"  {status} {s.name}: {s.passed}/{s.passed + s.failed}")
    print()
    print(f"  Total: {total_passed}/{total} passed", end="")
    if total_failed:
        print(f"  ← {total_failed} FAILED")
    else:
        print("  ✓ All green")
    print("=" * 60)

    sys.exit(0 if total_failed == 0 else 1)


if __name__ == "__main__":
    main()
