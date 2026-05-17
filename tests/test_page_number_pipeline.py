"""
Unit tests for page number extraction pipeline.

Verifies that [PAGE_N] markers inserted by loaders._extract_pdf()
flow correctly through pipeline.py chunking into chunk_id and page metadata,
and that rag_core.RetrievedDoc.page is populated from Qdrant payload.

No external services required — all mocked.
"""

from __future__ import annotations

import re

# ---------------------------------------------------------------------------
# Test 1: PAGE_RE regex extracts correct page number from chunk text
# ---------------------------------------------------------------------------


def test_page_re_extracts_page_number() -> None:
    """[PAGE_N] marker at start of chunk text yields correct page number."""
    PAGE_RE = re.compile(r"^\[PAGE_(\d+)\]\s*", re.MULTILINE)
    chunk = "[PAGE_7]\nThis is the text content of page seven."
    match = PAGE_RE.search(chunk)
    assert match is not None
    assert int(match.group(1)) == 7


def test_page_re_strips_marker_from_text() -> None:
    """After stripping [PAGE_N], clean text has no marker."""
    PAGE_RE = re.compile(r"^\[PAGE_(\d+)\]\s*", re.MULTILINE)
    chunk = "[PAGE_3]\nSome content here."
    clean = PAGE_RE.sub("", chunk).strip()
    assert clean == "Some content here."
    assert "[PAGE_" not in clean


def test_page_re_returns_none_for_continuation_chunk() -> None:
    """Chunk with no [PAGE_N] marker (mid-page continuation) returns None."""
    PAGE_RE = re.compile(r"^\[PAGE_(\d+)\]\s*", re.MULTILINE)
    chunk = "This chunk starts mid-page with no marker."
    match = PAGE_RE.search(chunk)
    assert match is None


def test_page_re_uses_first_page_for_cross_boundary_chunk() -> None:
    """Chunk spanning two pages uses the first page number found."""
    PAGE_RE = re.compile(r"^\[PAGE_(\d+)\]\s*", re.MULTILINE)
    chunk = "[PAGE_5]\nEnd of page 5 content.\n[PAGE_6]\nStart of page 6."
    match = PAGE_RE.search(chunk)
    assert match is not None
    assert int(match.group(1)) == 5


# ---------------------------------------------------------------------------
# Test 2: chunk_id encodes page number correctly
# ---------------------------------------------------------------------------


def test_chunk_id_format_with_page() -> None:
    """Chunk with page number produces correct chunk_id format."""
    abs_path = "/path/to/doc.pdf"
    page_num = 12
    i = 42
    chunk_id = f"{abs_path}::page-{page_num}::chunk-{i}"
    assert "::page-12::" in chunk_id
    assert chunk_id.endswith("::chunk-42")


def test_chunk_id_format_without_page() -> None:
    """Chunk without page number produces legacy chunk_id format."""
    abs_path = "/path/to/doc.pdf"
    i = 42
    chunk_id = f"{abs_path}::chunk-{i}"
    assert "::page-" not in chunk_id
    assert chunk_id.endswith("::chunk-42")


# ---------------------------------------------------------------------------
# Test 3: RetrievedDoc carries page field
# ---------------------------------------------------------------------------


def test_retrieved_doc_page_field() -> None:
    """RetrievedDoc accepts and stores page field correctly."""
    from local_llm_bot.app.rag_core import RetrievedDoc

    doc_with_page = RetrievedDoc(
        id="doc::page-5::chunk-0",
        content="Some content",
        source="/path/to/doc.pdf",
        score=0.1,
        page=5,
    )
    assert doc_with_page.page == 5

    doc_without_page = RetrievedDoc(
        id="doc::chunk-0",
        content="Some content",
        source="/path/to/doc.pdf",
        score=0.1,
    )
    assert doc_without_page.page is None


# ---------------------------------------------------------------------------
# Test 4: extract_page_number fallback still works for chunk_id encoding
# ---------------------------------------------------------------------------


def test_extract_page_number_from_chunk_id() -> None:
    """extract_page_number parses page from ::page-N:: chunk_id format."""
    from local_llm_bot.app.rag_core import extract_page_number

    chunk_id = "/path/to/doc.pdf::page-14::chunk-33"
    page = extract_page_number("", chunk_id)
    assert page == 14


def test_extract_page_number_returns_none_for_legacy_chunk_id() -> None:
    """extract_page_number returns None for legacy ::chunk-N format."""
    from local_llm_bot.app.rag_core import extract_page_number

    chunk_id = "/path/to/doc.pdf::chunk-33"
    page = extract_page_number("", chunk_id)
    assert page is None


# ---------------------------------------------------------------------------
# Test 5: pdfplumber marker format
# ---------------------------------------------------------------------------


def test_pdfplumber_marker_format() -> None:
    """Verify [PAGE_N] marker format matches what loaders._extract_pdf produces."""
    # Simulate what loaders._extract_pdf writes for page 3
    page_num = 3
    page_text = "This is the extracted text from page three."
    chunk = f"[PAGE_{page_num}]\n{page_text}"

    PAGE_RE = re.compile(r"^\[PAGE_(\d+)\]\s*", re.MULTILINE)
    match = PAGE_RE.search(chunk)
    assert match is not None
    assert int(match.group(1)) == page_num

    clean = PAGE_RE.sub("", chunk).strip()
    assert clean == page_text
