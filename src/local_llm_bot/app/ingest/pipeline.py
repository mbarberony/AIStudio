from __future__ import annotations

import json
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
    load_manifest_map,
    should_skip,
    write_manifest_entry,
)
from local_llm_bot.app.utils.corpus_paths import corpus_paths
from local_llm_bot.app.utils.repo_root import find_repo_root
from local_llm_bot.app.vectorstore import chroma_store


@dataclass(frozen=True)
class IngestResult:
    corpus: str
    root: str
    use_chroma: bool
    chunk_size: int
    overlap: int
    embed_model: str

    files_discovered: int
    files_supported: int
    files_processed: int
    files_skipped_unchanged: int
    files_failed: int

    chunks_written: int
    chroma_upserts: int
    chroma_deletes: int

    duration_sec: float


def _repo_root() -> Path:
    return find_repo_root(Path(__file__))


def _iter_files(root: Path) -> Iterable[Path]:
    # Fast recursive iteration
    for p in root.rglob("*"):
        if p.is_file():
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


def ingest_corpus(
    *,
    root: Path,
    corpus: str,
    reset_index: bool = False,
    reset_chroma: bool = False,
    force: bool = False,
    # CLI overrides (None => use CONFIG defaults)
    use_chroma: bool | None = None,
    chunk_size: int | None = None,
    overlap: int | None = None,
    embed_model: str | None = None,
    max_files: int | None = None,
    # progress bar class (tqdm) passed from __main__
    tqdm_cls: Any | None = None,
) -> IngestResult:
    """
    Ingest a directory into JSONL artifacts and optionally Chroma.

    Progress bars (if tqdm_cls is available):
      1) Discover files
      2) Process supported files (parse + chunk + manifest + JSONL rows)
      3) Embed/upsert chunks (Chroma) in batches
    """
    t0 = time.time()

    repo = _repo_root()
    paths = corpus_paths(repo, corpus)
    paths["base"].mkdir(parents=True, exist_ok=True)

    # Resolve effective settings
    use_chroma_eff = CONFIG.rag.use_chroma if use_chroma is None else bool(use_chroma)
    chunk_size_eff = CONFIG.ingest.chunk_size if chunk_size is None else int(chunk_size)
    overlap_eff = CONFIG.ingest.overlap if overlap is None else int(overlap)
    embed_model_eff = CONFIG.rag.default_embed_model if embed_model is None else str(embed_model)

    # Reset handling
    if reset_index:
        for k in ("index", "manifest", "failures", "docmap"):
            if paths[k].exists():
                paths[k].unlink()

    if reset_chroma:
        chroma_dir = paths["chroma"]
        if chroma_dir.exists():
            import shutil

            shutil.rmtree(chroma_dir, ignore_errors=True)

    manifest_map = load_manifest_map(paths["manifest"])
    prior_docmap = _load_doc_chunk_map(paths["docmap"])

    files_discovered = 0
    files_supported = 0
    files_processed = 0
    files_skipped_unchanged = 0
    files_failed = 0

    chunks_written = 0
    chroma_upserts = 0
    chroma_deletes = 0

    jsonl_rows: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []
    new_docmap: dict[str, list[str]] = {}

    # -----------------------
    # Phase 1: Discover
    # -----------------------

    discovered: list[Path] = []
    p_discover = tqdm_cls(desc="Discover", unit="file") if tqdm_cls is not None else None

    try:
        for p in _iter_files(root):
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
    # Phase 2: Process
    # -----------------------
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
                if should_skip(source_path=file_path, manifest_map=manifest_map, force=force):
                    files_skipped_unchanged += 1
                    if p_process is not None:
                        p_process.set_postfix(
                            processed=files_processed,
                            skipped=files_skipped_unchanged,
                            failed=files_failed,
                            chunks=chunks_written,
                        )
                        p_process.update(1)
                    continue

                abs_path = str(file_path.resolve())

                # Delete stale chunks in Chroma if file changed
                old_chunk_ids = prior_docmap.get(abs_path, [])
                if use_chroma_eff and old_chunk_ids:
                    chroma_store.delete_chunks(
                        persist_dir=paths["chroma"],
                        collection_name=f"aistudio_{corpus}",
                        ids=old_chunk_ids,
                    )
                    chroma_deletes += len(old_chunk_ids)

                doc = load_document(file_path)
                if not doc or not doc.text.strip():
                    write_manifest_entry(paths["manifest"], build_entry(file_path))
                    files_processed += 1
                    new_docmap[abs_path] = []
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
                chunk_ids: list[str] = []

                for i, c in enumerate(chunks):
                    chunk_id = f"{abs_path}::chunk-{i}"
                    chunk_ids.append(chunk_id)
                    jsonl_rows.append(
                        {
                            "chunk_id": chunk_id,
                            "doc_id": abs_path,
                            "source_path": abs_path,
                            "text": c,
                        }
                    )

                new_docmap[abs_path] = chunk_ids
                chunks_written += len(chunk_ids)

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

    # Persist JSONL artifacts
    if jsonl_rows:
        append_rows(paths["index"], jsonl_rows)

    if failures:
        paths["failures"].parent.mkdir(parents=True, exist_ok=True)
        with paths["failures"].open("a", encoding="utf-8") as f:
            for r in failures:
                f.write(json.dumps(r) + "\n")

    merged_docmap = dict(prior_docmap)
    merged_docmap.update(new_docmap)
    _save_doc_chunk_map(paths["docmap"], merged_docmap)

    # -----------------------
    # Phase 3: Embed / Upsert (Approach B)
    # -----------------------
    if use_chroma_eff and jsonl_rows:
        ids = [str(r.get("chunk_id", "")) for r in jsonl_rows]
        documents = [str(r.get("text", "")) for r in jsonl_rows]
        metadatas = [
            {"source_path": str(r.get("source_path", "")), "doc_id": str(r.get("doc_id", ""))}
            for r in jsonl_rows
        ]

        packed = [(i, d, m) for i, d, m in zip(ids, documents, metadatas, strict=False) if i and d]
        if packed:
            ids2, docs2, metas2 = zip(*packed, strict=False)

            # chunk-level embed progress uses batch callbacks
            embed_pbar = None
            if tqdm_cls is not None:
                embed_pbar = tqdm_cls(total=len(ids2), desc="Embed", unit="chunk")

            def on_batch_done(n: int) -> None:
                if embed_pbar is not None:
                    embed_pbar.update(n)

            try:
                chroma_store.upsert_chunks(
                    persist_dir=paths["chroma"],
                    collection_name=f"aistudio_{corpus}",
                    embed_model=embed_model_eff,
                    ids=list(ids2),
                    documents=list(docs2),
                    metadatas=list(metas2),
                    on_batch_done=on_batch_done,
                )
            finally:
                if embed_pbar is not None:
                    embed_pbar.close()

            chroma_upserts = len(ids2)

    dur = time.time() - t0
    return IngestResult(
        corpus=corpus,
        root=str(root),
        use_chroma=use_chroma_eff,
        chunk_size=chunk_size_eff,
        overlap=overlap_eff,
        embed_model=embed_model_eff,
        files_discovered=files_discovered,
        files_supported=files_supported,
        files_processed=files_processed,
        files_skipped_unchanged=files_skipped_unchanged,
        files_failed=files_failed,
        chunks_written=chunks_written,
        chroma_upserts=chroma_upserts,
        chroma_deletes=chroma_deletes,
        duration_sec=round(dur, 3),
    )
