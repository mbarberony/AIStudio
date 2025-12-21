from __future__ import annotations

import argparse
import json
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

from local_llm_bot.app.ingest.index_jsonl import (
    load_doc_chunk_map,
    rewrite_excluding_doc,
    save_doc_chunk_map,
)
from local_llm_bot.app.ingest.loaders import SUPPORTED_EXTS, extract_text, should_skip_filename
from local_llm_bot.app.ingest.manifest import (
    ManifestEntry,
    append_manifest,
    load_manifest,
    unchanged,
)
from local_llm_bot.app.utils.paths import find_repo_root

try:
    from tqdm import tqdm  # type: ignore
except Exception:  # pragma: no cover
    tqdm = None  # type: ignore


def chunk_text(text: str, *, chunk_size: int, overlap: int) -> list[str]:
    """
    Character-based chunking with overlap.
    Good enough as a debug artifact; later we can do token-aware chunking.
    """
    t = text.strip()
    if not t:
        return []
    if len(t) <= chunk_size:
        return [t]

    step = max(1, chunk_size - overlap)
    out: list[str] = []
    i = 0
    while i < len(t):
        out.append(t[i : i + chunk_size])
        i += step
    return out


def iter_supported_files(root: Path) -> list[Path]:
    paths: list[Path] = []
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        if should_skip_filename(p.name):
            continue
        if p.suffix.lower() not in SUPPORTED_EXTS:
            continue
        paths.append(p)
    return paths


@dataclass(frozen=True)
class OutputPaths:
    data_dir: Path
    index: Path
    manifest: Path
    failures: Path
    docmap: Path
    tmp_index: Path


def output_paths() -> OutputPaths:
    repo_root = find_repo_root(Path(__file__))
    data_dir = repo_root / "data"
    return OutputPaths(
        data_dir=data_dir,
        index=data_dir / "index.jsonl",
        manifest=data_dir / "manifest.jsonl",
        failures=data_dir / "ingest_failures.jsonl",
        docmap=data_dir / "doc_chunk_map.json",
        tmp_index=data_dir / "index.tmp.jsonl",
    )


def reset_outputs(paths: OutputPaths) -> None:
    for p in [paths.index, paths.manifest, paths.failures, paths.docmap, paths.tmp_index]:
        if p.exists():
            p.unlink()


def main() -> None:
    p = argparse.ArgumentParser(
        description="Incremental ingestion into data/index.jsonl (debug artifact; resumable)."
    )
    p.add_argument("--root", required=True, help="Directory to ingest")
    p.add_argument("--chunk-size", type=int, default=1200)
    p.add_argument("--overlap", type=int, default=200)
    p.add_argument(
        "--reset-index", action="store_true", help="Delete index/manifest/failures and start fresh"
    )
    args = p.parse_args()

    root = Path(args.root).expanduser()
    if not root.exists():
        raise SystemExit(f"Path not found: {root}")

    paths = output_paths()
    paths.data_dir.mkdir(parents=True, exist_ok=True)

    if args.reset_index:
        reset_outputs(paths)

    manifest = load_manifest(paths.manifest)
    docmap = load_doc_chunk_map(paths.docmap)

    files = iter_supported_files(root)
    iterator = files
    if tqdm is not None:
        iterator = tqdm(files, desc="Ingesting", unit="file")  # type: ignore

    counts = Counter()

    with (
        paths.index.open("a", encoding="utf-8") as index_f,
        paths.failures.open("a", encoding="utf-8") as fail_f,
    ):
        for path in iterator:  # type: ignore
            # stat
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
                        },
                        ensure_ascii=False,
                    )
                    + "\n"
                )
                continue

            key = str(path.resolve())

            # skip unchanged
            if unchanged(manifest.get(key), mtime=mtime, size=size):
                counts["skipped_unchanged"] += 1
                continue

            # extract
            res = extract_text(path)
            if not res.ok or not res.text.strip():
                counts["failed_extract"] += 1
                fail_f.write(
                    json.dumps(
                        {
                            "path": key,
                            "ext": path.suffix.lower(),
                            "reason": res.reason or "extract_failed",
                        },
                        ensure_ascii=False,
                    )
                    + "\n"
                )
                continue

            # if doc existed before, remove its old chunks from index.jsonl (avoid duplicates)
            if key in docmap:
                rewrite_excluding_doc(paths.index, paths.tmp_index, key)
                counts["rewrote_index_for_changed_doc"] += 1

            # chunk
            chunks = chunk_text(res.text, chunk_size=args.chunk_size, overlap=args.overlap)
            if not chunks:
                counts["empty_after_chunking"] += 1
                continue

            # write new chunks
            new_chunk_ids: list[str] = []
            for i, c in enumerate(chunks):
                chunk_id = f"{key}::chunk-{i}"
                new_chunk_ids.append(chunk_id)
                row = {
                    "chunk_id": chunk_id,
                    "doc_id": key,
                    "source_path": key,
                    "text": c,
                }
                index_f.write(json.dumps(row, ensure_ascii=False) + "\n")

            # update doc map
            docmap[key] = new_chunk_ids
            save_doc_chunk_map(paths.docmap, docmap)

            # update manifest
            entry = ManifestEntry(
                path=key,
                mtime=mtime,
                size=size,
                extracted_chars=len(res.text),
                chunks=len(chunks),
            )
            append_manifest(paths.manifest, entry)
            manifest[key] = entry

            counts["ingested"] += 1

    print("\n=== Ingestion summary ===")
    for k, v in counts.most_common():
        print(f"{k:28s} {v:,}")
    print(f"index:     {paths.index}")
    print(f"manifest:  {paths.manifest}")
    print(f"failures:  {paths.failures}")
    print(f"docmap:    {paths.docmap}")


if __name__ == "__main__":
    main()
