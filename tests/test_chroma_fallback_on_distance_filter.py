from __future__ import annotations

import json
from pathlib import Path

from local_llm_bot.app import rag_core


class _FakeChromaHit:
    def __init__(self, chunk_id: str, text: str, metadata: dict, distance: float) -> None:
        self.chunk_id = chunk_id
        self.text = text
        self.metadata = metadata
        self.distance = distance


def test_fallback_triggers_when_distance_filters_all(monkeypatch, tmp_path: Path) -> None:
    corpus = "unit_test"
    data_dir = tmp_path / corpus
    data_dir.mkdir(parents=True, exist_ok=True)

    # Prepare JSONL corpus (fallback path)
    (data_dir / "index.jsonl").write_text(
        json.dumps(
            {
                "chunk_id": "doc1::chunk-0",
                "doc_id": "doc1",
                "source_path": "/tmp/doc1",
                "text": "NORTHWESTERN MUTUAL appears in this chunk.",
            }
        )
        + "\n",
        encoding="utf-8",
    )
    (data_dir / "manifest.jsonl").write_text("", encoding="utf-8")
    (data_dir / "ingest_failures.jsonl").write_text("", encoding="utf-8")
    (data_dir / "doc_chunk_map.json").write_text(json.dumps({}), encoding="utf-8")

    # Make rag_core resolve paths to our tmp corpus
    def _fake_corpus_paths(_repo_root: Path, corpus_name: str) -> dict[str, Path]:
        assert corpus_name == corpus
        return {
            "base": data_dir,
            "index": data_dir / "index.jsonl",
            "manifest": data_dir / "manifest.jsonl",
            "failures": data_dir / "ingest_failures.jsonl",
            "docmap": data_dir / "doc_chunk_map.json",
            "chroma": data_dir / "chroma",
        }

    monkeypatch.setattr(rag_core, "corpus_paths", _fake_corpus_paths)

    # Force Chroma mode ON and make distance filter strict
    monkeypatch.setattr(rag_core.CONFIG.rag, "use_chroma", True, raising=False)
    monkeypatch.setattr(rag_core.CONFIG.rag, "max_distance", 0.01, raising=False)

    # Mock Chroma returning hits, but all too far away => filtered to zero
    def _fake_query(**kwargs):
        return [
            _FakeChromaHit(
                chunk_id="chroma::1",
                text="Some semantically unrelated chunk",
                metadata={"source_path": "/tmp/chroma"},
                distance=999.0,
            )
        ]

    monkeypatch.setattr(rag_core.chroma_store, "query", _fake_query)

    hits = rag_core.retrieve(query="NORTHWESTERN", top_k=5, corpus=corpus)

    # Must come from JSONL fallback
    assert len(hits) >= 1
    assert any("northwestern" in h.content.lower() for h in hits)
