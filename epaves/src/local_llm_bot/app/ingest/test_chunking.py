from local_llm_bot.app.ingest.chunking import chunk_text


def test_chunk_text_splits_and_overlaps() -> None:
    text = "a" * 3000
    chunks = chunk_text(text, chunk_size=1000, overlap=100)
    assert len(chunks) >= 3
    assert all(len(c) <= 1000 for c in chunks)
