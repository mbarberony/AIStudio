import json
from collections import Counter
from pathlib import Path

from local_llm_bot.app.ingest.chunking import chunk_text  # whatever you already use
from local_llm_bot.app.ingest.loaders import SUPPORTED_EXTS, extract_text, should_skip_filename
from local_llm_bot.app.ingest.manifest import (
    ManifestEntry,
    append_manifest,
    load_manifest,
    should_skip,
)
from local_llm_bot.app.rag_core import FAILURES_PATH, INDEX_PATH, MANIFEST_PATH

try:
    from tqdm import tqdm  # type: ignore
except Exception:
    tqdm = None  # type: ignore


def ingest(root: Path, chunk_size: int, overlap: int) -> None:
    manifest = load_manifest(MANIFEST_PATH)

    paths: list[Path] = []
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        if should_skip_filename(p.name):
            continue
        if p.suffix.lower() not in SUPPORTED_EXTS:
            continue
        paths.append(p)

    iterator = paths
    if tqdm is not None:
        iterator = tqdm(paths, desc="Ingesting", unit="file")  # type: ignore

    counts = Counter()

    INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    with (
        INDEX_PATH.open("a", encoding="utf-8") as index_f,
        FAILURES_PATH.open("a", encoding="utf-8") as fail_f,
    ):
        for path in iterator:  # type: ignore
            try:
                st = path.stat()
                mtime = float(st.st_mtime)
                size = int(st.st_size)
            except Exception as e:
                counts["stat_error"] += 1
                fail_f.write(
                    json.dumps(
                        {
                            "path": str(path),
                            "ext": path.suffix.lower(),
                            "reason": f"stat_error:{type(e).__name__}",
                        }
                    )
                    + "\n"
                )
                continue

            key = str(path.resolve())
            if should_skip(manifest.get(key), mtime=mtime, size=size):
                counts["skipped_unchanged"] += 1
                continue

            res = extract_text(path)
            if not res.ok or not res.text.strip():
                counts["failed_extract"] += 1
                fail_f.write(
                    json.dumps(
                        {
                            "path": key,
                            "ext": path.suffix.lower(),
                            "reason": res.reason or "extract_failed",
                        }
                    )
                    + "\n"
                )
                continue

            text = res.text
            chunks = chunk_text(text, chunk_size=chunk_size, overlap=overlap)

            # write chunks to index.jsonl
            for i, c in enumerate(chunks):
                row = {
                    "chunk_id": f"{key}::chunk-{i}",
                    "doc_id": key,
                    "source_path": key,
                    "text": c,
                }
                index_f.write(json.dumps(row, ensure_ascii=False) + "\n")

            entry = ManifestEntry(
                path=key,
                mtime=mtime,
                size=size,
                extracted_chars=len(text),
                chunks=len(chunks),
            )
            append_manifest(MANIFEST_PATH, entry)
            manifest[key] = entry  # update in-memory
            counts["ingested"] += 1

    print("\n=== Ingestion summary ===")
    for k, v in counts.most_common():
        print(f"{k:18s} {v:,}")
    print(f"index:     {INDEX_PATH}")
    print(f"manifest:  {MANIFEST_PATH}")
    print(f"failures:  {FAILURES_PATH}")
