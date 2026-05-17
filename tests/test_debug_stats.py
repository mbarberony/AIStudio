from __future__ import annotations

import json
from pathlib import Path

from local_llm_bot.app.debug_stats import compute_jsonl_stats


def test_compute_jsonl_stats(tmp_path: Path) -> None:
    data_dir = tmp_path

    (data_dir / "index.jsonl").write_text(
        json.dumps(
            {
                "chunk_id": "a::chunk-0",
                "doc_id": "a",
                "source_path": "/x/a",
                "text": "Bridgewater Associates",
            }
        )
        + "\n",
        encoding="utf-8",
    )
    (data_dir / "manifest.jsonl").write_text(
        json.dumps({"path": "/x/a", "mtime": 1, "size": 10}) + "\n", encoding="utf-8"
    )
    (data_dir / "ingest_failures.jsonl").write_text("", encoding="utf-8")
    (data_dir / "doc_chunk_map.json").write_text(
        json.dumps({"a": ["a::chunk-0"]}), encoding="utf-8"
    )

    s = compute_jsonl_stats(data_dir=data_dir)

    assert s.chunks_total == 1
    assert s.docs_unique == 1
    assert s.sources_unique == 1
    assert s.docmap_entries == 1
