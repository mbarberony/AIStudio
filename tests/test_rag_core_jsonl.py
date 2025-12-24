from __future__ import annotations

import importlib
import json
import os
from pathlib import Path

# Force JSONL retrieval no matter what config/env says


def test_retrieve_finds_hits_jsonl(monkeypatch, tmp_path: Path) -> None:
    # Force JSONL retrieval for this test run
    os.environ["AISTUDIO_USE_CHROMA"] = "false"

    # Import after env is set (CONFIG is created at import-time)
    from local_llm_bot.app import rag_core

    monkeypatch.setattr(rag_core.CONFIG.rag, "use_chroma", False, raising=False)

    importlib.reload(rag_core)  # ensure it re-reads CONFIG under the env override

    corpus = "unit_test"
    data_dir = tmp_path / corpus
    data_dir.mkdir(parents=True, exist_ok=True)

    index = data_dir / "index.jsonl"
    index.write_text(
        "\n".join(
            [
                json.dumps(
                    {
                        "chunk_id": "doc1::chunk-0",
                        "doc_id": "doc1",
                        "source_path": "/tmp/doc1",
                        "text": "Manuel Barbero was Head of Architecture at Bridgewater Associates 2012-2017.",
                    }
                ),
                json.dumps(
                    {
                        "chunk_id": "doc2::chunk-0",
                        "doc_id": "doc2",
                        "source_path": "/tmp/doc2",
                        "text": "Unrelated content about gardening.",
                    }
                ),
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    # Provide minimal companion artifacts the code may look for
    (data_dir / "manifest.jsonl").write_text("", encoding="utf-8")
    (data_dir / "ingest_failures.jsonl").write_text("", encoding="utf-8")
    (data_dir / "doc_chunk_map.json").write_text(json.dumps({}), encoding="utf-8")

    # Monkeypatch corpus_paths() so rag_core reads our tmp corpus directory
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

    hits = rag_core.retrieve(query="Bridgewater", top_k=3, corpus=corpus)

    assert len(hits) >= 1
    assert any("bridgewater" in h.content.lower() for h in hits)
