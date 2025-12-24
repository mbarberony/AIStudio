from __future__ import annotations

import pytest

from local_llm_bot.app.config import CONFIG

pytestmark = pytest.mark.unit


def test_chroma_include_does_not_request_ids() -> None:
    assert "ids" not in CONFIG.chroma.query_include


# def test_chroma_query_include_does_not_request_ids() -> None:
#     # If someone accidentally adds "ids" to include, newer Chroma raises ValueError.
#     # This is a lightweight "contract" test: we just assert our code doesn't contain it.
#     from local_llm_bot.app.vectorstore import chroma_store
#
#     src = chroma_store.query.__code__.co_consts
#     joined = " ".join([c for c in src if isinstance(c, str)])
#     assert "ids" not in joined


def test_chroma_query_include_does_not_request_ids() -> None:
    assert "ids" not in CONFIG.chroma.query_include
