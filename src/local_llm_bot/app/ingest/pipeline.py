# Version: 1.2.0
# Changelog: 1.2.0 — Per-file embed+upsert (constant memory, live Qdrant progress); alphabetical file order
#            1.1.0 — MD5 stored in Qdrant payload; skip logic fixed (Qdrant-only); per-file INFO logging
from __future__ import annotations

import contextlib
import hashlib
import json
import os as _os
import sys as _sys
import time
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from local_llm_bot.app.config import CONFIG
from local_llm_bot.app.ingest.chunking import chunk_text
from local_llm_bot.app.ingest.index_jsonl import append_rows
from local_llm_bot.app.ingest.loaders import SUPPORTED_EXTS, load_document
from local_llm_bot.app.ingest.manifest import (
    build_entry,
    write_manifest_entry,
)
from local_llm_bot.app.utils.corpus_paths import corpus_paths
from local_llm_bot.app.utils.repo_root import find_repo_root

# Qdrant is the only supported vectorstore.
# Chroma support has been removed — see chroma eradication ticket.
from local_llm_bot.app.vectorstore import qdrant_store as _store


@dataclass(frozen=True)
class IngestResult:
    corpus: str
    root: str
    chunk_size: int
    overlap: int
    embed_model: str

    files_discovered: int
    files_supported: int
    files_processed: int
    files_skipped_unchanged: int
    files_failed: int

    chunks_written: int

    duration_sec: float
    vectorstore: str = "qdrant"


def _repo_root() -> Path:
    return find_repo_root(Path(__file__))


def _iter_files(root: Path) -> Iterable[Path]:
    """
    Yield all files under root, excluding the trash/ directory.

    trash/ is now a sibling of uploads/ at the corpus level, so this guard
    is belt-and-suspenders — uploads/ should never contain a trash/ subdir.
    Kept explicitly to prevent any legacy or accidental trash/ inside uploads/
    from being ingested.
    """
    for p in root.rglob("*"):
        if p.is_file() and "trash" not in p.parts:
            yield p


def _load_doc_chunk_map(path: Path) -> dict[str, list[str]]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _save_doc_chunk_map(path: Path, m: dict[str, list[str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(m, indent=2), encoding="utf-8")


def _parse_firm_year(file_path: str) -> dict:
    """Parse firm name and year from 10K filename e.g. Goldman_Sachs_10K_2026-02-25.htm"""
    import re as _re
    from pathlib import Path as _Path

    name = _Path(file_path).stem
    m = _re.search(r"_10[Kk]_(\d{4})", name)
    year = m.group(1) if m else "unknown"
    m2 = _re.search(r"^(.+?)_10[Kk]_", name)
    firm = m2.group(1).replace("_", " ").strip() if m2 else "unknown"
    return {"firm": firm, "year": year}


def _load_qdrant_source_paths(collection_name: str) -> set[str]:
    """
    Fetch all source_path values currently indexed in Qdrant for a collection.
    Returns a set of absolute path strings.

    Used at the start of each ingest run to determine which files are already
    indexed — replacing the manifest-based skip check with Qdrant as the
    single source of truth.

    Uses scroll pagination to handle large collections (e.g. 105K chunks).
    Each page fetches up to 1000 points. Payload fetch is limited to
    source_path only to minimise data transfer.
    """
    from qdrant_client import QdrantClient
    from qdrant_client.models import PayloadSelectorInclude

    source_paths: set[str] = set()
    try:
        client = QdrantClient(
            host=_os.getenv("QDRANT_HOST", "localhost"),
            port=int(_os.getenv("QDRANT_PORT", "6333")),
        )
        existing = [c.name for c in client.get_collections().collections]
        if collection_name not in existing:
            return source_paths

        offset = None
        while True:
            result, next_offset = client.scroll(
                collection_name=collection_name,
                limit=1000,
                offset=offset,
                with_payload=PayloadSelectorInclude(include=["source_path"]),
                with_vectors=False,
            )
            for point in result:
                sp = (point.payload or {}).get("source_path")
                if sp:
                    source_paths.add(str(sp))
            if next_offset is None:
                break
            offset = next_offset
    except Exception:
        # If Qdrant is unreachable, return empty set — all files will be processed.
        # This is the safe fallback: re-ingest is idempotent via upsert.
        pass
    return source_paths


def _file_unchanged(source_path: Path, manifest_map: dict) -> bool:
    """
    NOTE: intentionally NOT used in skip decision — kept for reference only.
    Qdrant is the single source of truth for skip logic (AIStudio_186).
    manifest.jsonl is stale after corpus recreation and cannot be relied upon.
    """
    from local_llm_bot.app.ingest.manifest import ManifestEntry

    abs_path = str(source_path.resolve())
    prev: ManifestEntry | None = manifest_map.get(abs_path)
    if prev is None:
        return False
    try:
        st = source_path.stat()
        return (prev.mtime == int(st.st_mtime)) and (prev.size == int(st.st_size))
    except FileNotFoundError:
        return False


def _md5_of_file(path: Path) -> str:
    """Compute MD5 hex digest of a file. Stored in Qdrant payload for duplicate detection."""
    h = hashlib.md5()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(65536), b""):
            h.update(block)
    return h.hexdigest()


def ingest_corpus(
    *,
    root: Path,
    corpus: str,
    reset_index: bool = False,
    force: bool = False,
    # CLI overrides (None => use CONFIG defaults)
    vectorstore: str | None = None,
    chunk_size: int | None = None,
    overlap: int | None = None,
    embed_model: str | None = None,
    max_files: int | None = None,
    # progress bar class (tqdm) passed from __main__
    tqdm_cls: Any | None = None,
) -> IngestResult:
    """
    Ingest a directory into Qdrant.

    Skip logic (Qdrant is the single source of truth):
      - Pre-load all source_path values currently in Qdrant for this corpus.
      - Skip a file if: (a) its abs_path is in the Qdrant source set AND
        (b) its mtime+size match the manifest (i.e. file is unchanged on disk).
      - force=True bypasses both checks.

    Progress bars (if tqdm_cls is available):
      1) Discover files
      2) Process supported files (parse + chunk + manifest + JSONL rows)
      3) Embed/upsert chunks into Qdrant in batches
    """
    t0 = time.time()

    repo = _repo_root()
    paths = corpus_paths(repo, corpus)
    paths["base"].mkdir(parents=True, exist_ok=True)

    # Resolve effective settings
    _vs = (vectorstore or CONFIG.rag.vectorstore or "qdrant").lower()
    chunk_size_eff = CONFIG.ingest.chunk_size if chunk_size is None else int(chunk_size)
    overlap_eff = CONFIG.ingest.overlap if overlap is None else int(overlap)
    embed_model_eff = CONFIG.rag.default_embed_model if embed_model is None else str(embed_model)

    collection_name = f"aistudio_{corpus}"

    # Reset handling
    if reset_index:
        for k in ("index", "manifest", "failures", "docmap"):
            if paths[k].exists():
                paths[k].unlink()

    # --force: atomic wipe of Qdrant collection + manifest + index
    if force:
        for k in ("index", "manifest", "failures", "docmap"):
            if paths[k].exists():
                paths[k].write_text("", encoding="utf-8")  # truncate, don't delete
        with contextlib.suppress(Exception):
            _store.delete_collection(collection_name=collection_name)

    # Pre-load Qdrant source paths — single scroll, O(n chunks), done once per run.
    # This is the skip-decision source of truth. Empty on first ingest or after --force.
    qdrant_source_paths = _load_qdrant_source_paths(collection_name) if not force else set()

    files_discovered = 0
    files_supported = 0
    files_processed = 0
    files_skipped_unchanged = 0
    files_failed = 0

    chunks_written = 0
    failures: list[dict[str, Any]] = []

    import re as _re

    _PAGE_RE = _re.compile(r"^\[PAGE_(\d+)\]\s*", _re.MULTILINE)

    # -----------------------
    # Phase 1: Discover
    # -----------------------
    # Files are sorted alphabetically — consistent order matches the pre-scan
    # in api.py trigger_ingest, which also sorts alphabetically. This ensures
    # bytes_processed accumulates in the correct order for the progress bar.

    discovered: list[Path] = []
    p_discover = tqdm_cls(desc="Discover", unit="file") if tqdm_cls is not None else None

    try:
        for p in sorted(_iter_files(root), key=lambda x: x.name):
            discovered.append(p)
            files_discovered += 1
            if max_files is not None and files_discovered >= int(max_files):
                break
            if p_discover is not None:
                p_discover.update(1)
    finally:
        if p_discover is not None:
            p_discover.close()

    # -----------------------
    # Phase 2: Process + Embed + Upsert (per file)
    # -----------------------
    # Each file is fully processed — chunked, embedded, upserted to Qdrant —
    # before moving to the next. Memory footprint is constant regardless of
    # corpus size. Qdrant gets live chunk counts as each file completes,
    # enabling accurate progress reporting.

    if tqdm_cls is not None:
        p_process = tqdm_cls(total=len(discovered), desc="Process", unit="file")
    else:
        p_process = None

    try:
        for file_path in discovered:
            if p_process is not None:
                p_process.set_postfix_str(file_path.name[:60])

            ext = file_path.suffix.lower()
            if ext not in SUPPORTED_EXTS or file_path.name.startswith("~$"):
                if p_process is not None:
                    p_process.update(1)
                continue

            files_supported += 1

            try:
                abs_path = str(file_path.resolve())

                # Skip decision: Qdrant already has this file — no re-ingest needed.
                # _file_unchanged() removed: manifest.jsonl stale after corpus recreation. (AIStudio_186)
                if not force and abs_path in qdrant_source_paths:
                    files_skipped_unchanged += 1
                    print(
                        f"[ingest] {corpus}: skipped {file_path.name} — already indexed",
                        file=_sys.stderr,
                    )
                    if p_process is not None:
                        p_process.set_postfix(
                            processed=files_processed,
                            skipped=files_skipped_unchanged,
                            failed=files_failed,
                            chunks=chunks_written,
                        )
                        p_process.update(1)
                    continue

                print(
                    f"[ingest] {corpus}: processing {file_path.name} ({files_processed + files_skipped_unchanged + 1}/{len(discovered)})",
                    file=_sys.stderr,
                )
                doc = load_document(file_path)
                if not doc or not doc.text.strip():
                    write_manifest_entry(paths["manifest"], build_entry(file_path))
                    files_processed += 1
                    if p_process is not None:
                        p_process.set_postfix(
                            processed=files_processed,
                            skipped=files_skipped_unchanged,
                            failed=files_failed,
                            chunks=chunks_written,
                        )
                        p_process.update(1)
                    continue

                chunks = chunk_text(doc.text, chunk_size=chunk_size_eff, overlap=overlap_eff)

                # Compute MD5 once per file — stored in every chunk payload
                file_md5 = _md5_of_file(file_path)

                # Build rows for this file only
                file_rows: list[dict[str, Any]] = []
                last_page: int | None = None
                for i, c in enumerate(chunks):
                    page_match = _PAGE_RE.search(c)
                    if page_match:
                        last_page = int(page_match.group(1))
                    page_num = last_page
                    clean_text = _PAGE_RE.sub("", c).strip()
                    chunk_id = (
                        f"{abs_path}::page-{page_num}::chunk-{i}"
                        if page_num is not None
                        else f"{abs_path}::chunk-{i}"
                    )
                    file_rows.append(
                        {
                            "chunk_id": chunk_id,
                            "doc_id": abs_path,
                            "source_path": abs_path,
                            "text": clean_text,
                            "page": page_num,
                            "md5": file_md5,
                        }
                    )

                # Embed + upsert this file's chunks immediately — no accumulation
                if file_rows:
                    ids = [str(r["chunk_id"]) for r in file_rows]
                    documents = [str(r["text"]) for r in file_rows]
                    metadatas = [
                        {
                            "source_path": str(r["source_path"]),
                            "doc_id": str(r["doc_id"]),
                            "page": r["page"],
                            "md5": str(r["md5"]),
                            **_parse_firm_year(str(r["source_path"])),
                        }
                        for r in file_rows
                    ]
                    _store.upsert_chunks(
                        persist_dir=Path("."),
                        collection_name=collection_name,
                        embed_model=embed_model_eff,
                        ids=ids,
                        documents=documents,
                        metadatas=metadatas,
                    )
                    # Persist JSONL audit log per file
                    append_rows(paths["index"], file_rows)

                chunks_written += len(chunks)
                print(
                    f"[ingest] {corpus}: ✓ {file_path.name} — {len(chunks):,} chunks",
                    file=_sys.stderr,
                )

                write_manifest_entry(paths["manifest"], build_entry(file_path))
                files_processed += 1

                if p_process is not None:
                    p_process.set_postfix(
                        processed=files_processed,
                        skipped=files_skipped_unchanged,
                        failed=files_failed,
                        chunks=chunks_written,
                    )
                    p_process.update(1)

            except Exception as e:
                files_failed += 1
                failures.append(
                    {"source_path": str(file_path), "reason": type(e).__name__, "detail": str(e)}
                )
                if p_process is not None:
                    p_process.set_postfix(
                        processed=files_processed,
                        skipped=files_skipped_unchanged,
                        failed=files_failed,
                        chunks=chunks_written,
                    )
                    p_process.update(1)

    finally:
        if p_process is not None:
            p_process.close()

    if failures:
        paths["failures"].parent.mkdir(parents=True, exist_ok=True)
        with paths["failures"].open("a", encoding="utf-8") as f:
            for r in failures:
                f.write(json.dumps(r) + "\n")

    dur = time.time() - t0
    return IngestResult(
        corpus=corpus,
        root=str(root),
        vectorstore=_vs,
        chunk_size=chunk_size_eff,
        overlap=overlap_eff,
        embed_model=embed_model_eff,
        files_discovered=files_discovered,
        files_supported=files_supported,
        files_processed=files_processed,
        files_skipped_unchanged=files_skipped_unchanged,
        files_failed=files_failed,
        chunks_written=chunks_written,
        duration_sec=round(dur, 3),
    )
