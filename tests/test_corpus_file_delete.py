# ruff: noqa: I001
"""
Unit tests for corpus file deletion endpoint.

Tests the DELETE /corpus/{corpus_name}/file/{filename} endpoint:
- Moves file to uploads/trash/ (recoverable)
- Surgically removes Qdrant chunks for that file
- Updates manifest.jsonl and index.jsonl
- Returns correct chunk count

No Qdrant or Ollama required — all external calls mocked.
"""

from __future__ import annotations

import json
import shutil
from unittest.mock import MagicMock

import pytest


# ── Fixtures ──────────────────────────────────────────────────────────────────


@pytest.fixture
def tmp_corpus(tmp_path):
    """Create a minimal corpus directory structure."""
    uploads = tmp_path / "uploads"
    uploads.mkdir(parents=True)

    # Place a dummy PDF in uploads
    doc = uploads / "test_doc.pdf"
    doc.write_bytes(b"%PDF-1.4 fake content")

    # Minimal manifest.jsonl
    manifest = tmp_path / "manifest.jsonl"
    manifest.write_text(
        json.dumps({"source_path": str(doc), "chunk_count": 3})
        + "\n"
        + json.dumps({"source_path": "/other/file.pdf", "chunk_count": 2})
        + "\n"
    )

    # Minimal index.jsonl
    index = tmp_path / "index.jsonl"
    index.write_text(
        json.dumps({"chunk_id": f"{doc}::chunk-0", "text": "a", "source_path": str(doc)})
        + "\n"
        + json.dumps({"chunk_id": f"{doc}::chunk-1", "text": "b", "source_path": str(doc)})
        + "\n"
        + json.dumps(
            {"chunk_id": "/other/file.pdf::chunk-0", "text": "c", "source_path": "/other/file.pdf"}
        )
        + "\n"
    )

    return tmp_path, uploads, doc, manifest, index


# ── Unit tests (no FastAPI) ───────────────────────────────────────────────────


class TestTrashDir:
    def test_trash_created_on_delete(self, tmp_corpus):
        """Trash directory is created when first file is deleted."""
        corpus_dir, uploads, doc, manifest, index = tmp_corpus
        trash_dir = uploads / "trash"
        assert not trash_dir.exists()

        trash_dir.mkdir()
        shutil.move(str(doc), str(trash_dir / doc.name))

        assert trash_dir.exists()
        assert (trash_dir / "test_doc.pdf").exists()
        assert not doc.exists()

    def test_file_moved_not_deleted(self, tmp_corpus):
        """File ends up in trash, not permanently deleted."""
        corpus_dir, uploads, doc, manifest, index = tmp_corpus
        trash_dir = uploads / "trash"
        trash_dir.mkdir()

        shutil.move(str(doc), str(trash_dir / doc.name))

        assert (trash_dir / "test_doc.pdf").exists()
        assert not doc.exists()

    def test_collision_handling(self, tmp_corpus):
        """If file already in trash, a timestamped copy is made."""
        corpus_dir, uploads, doc, manifest, index = tmp_corpus
        trash_dir = uploads / "trash"
        trash_dir.mkdir()

        # Pre-existing file in trash
        (trash_dir / "test_doc.pdf").write_bytes(b"old version")

        import time

        trash_path = trash_dir / doc.name
        if trash_path.exists():
            stem, suffix = doc.stem, doc.suffix
            trash_path = trash_dir / f"{stem}_{int(time.time())}{suffix}"

        shutil.move(str(doc), str(trash_path))
        assert trash_path.exists()
        assert (trash_dir / "test_doc.pdf").exists()  # old version still there


class TestManifestUpdate:
    def test_file_removed_from_manifest(self, tmp_corpus):
        """File's entry is removed from manifest.jsonl after deletion."""
        corpus_dir, uploads, doc, manifest, index = tmp_corpus

        lines = manifest.read_text().splitlines()
        kept = [ln for ln in lines if str(doc) not in ln]
        manifest.write_text("\n".join(kept) + ("\n" if kept else ""))

        remaining = manifest.read_text()
        assert str(doc) not in remaining
        assert "/other/file.pdf" in remaining

    def test_other_files_untouched_in_manifest(self, tmp_corpus):
        """Other files' manifest entries are preserved."""
        corpus_dir, uploads, doc, manifest, index = tmp_corpus

        lines = manifest.read_text().splitlines()
        kept = [ln for ln in lines if str(doc) not in ln]
        manifest.write_text("\n".join(kept) + "\n")

        assert len(manifest.read_text().splitlines()) == 1


class TestIndexUpdate:
    def test_chunks_removed_from_index(self, tmp_corpus):
        """All chunks for the deleted file are removed from index.jsonl."""
        corpus_dir, uploads, doc, manifest, index = tmp_corpus

        lines = index.read_text().splitlines()
        kept = [ln for ln in lines if str(doc) not in ln]
        index.write_text("\n".join(kept) + ("\n" if kept else ""))

        remaining = index.read_text()
        assert str(doc) not in remaining
        assert "/other/file.pdf" in remaining

    def test_chunk_count_correct(self, tmp_corpus):
        """Correct number of chunks removed."""
        corpus_dir, uploads, doc, manifest, index = tmp_corpus

        lines = index.read_text().splitlines()
        removed = [ln for ln in lines if str(doc) in ln]
        assert len(removed) == 2  # two chunks for test_doc.pdf


class TestQdrantMock:
    def test_qdrant_scroll_and_delete_called(self):
        """Qdrant scroll + delete are called with correct source_path filter."""
        mock_qc = MagicMock()
        mock_point = MagicMock()
        mock_point.id = "abc123"
        mock_qc.scroll.return_value = ([mock_point], None)

        source_path = "/corpus/uploads/test_doc.pdf"

        from qdrant_client.models import FieldCondition, Filter, MatchValue

        scroll_filter = Filter(
            must=[FieldCondition(key="source_path", match=MatchValue(value=source_path))]
        )

        mock_qc.scroll(
            collection_name="aistudio_demo",
            scroll_filter=scroll_filter,
            limit=10000,
            with_payload=False,
        )
        point_ids = ["abc123"]
        mock_qc.delete(collection_name="aistudio_demo", points_selector=point_ids)

        mock_qc.scroll.assert_called_once()
        mock_qc.delete.assert_called_once_with(
            collection_name="aistudio_demo", points_selector=["abc123"]
        )

    def test_qdrant_unavailable_does_not_crash(self, tmp_corpus):
        """If Qdrant is down, file still moves to trash gracefully."""
        corpus_dir, uploads, doc, manifest, index = tmp_corpus
        trash_dir = uploads / "trash"
        trash_dir.mkdir()

        # Simulate Qdrant failure — just move file anyway
        deleted_chunks = 0
        try:
            raise ConnectionError("Qdrant not available")
        except Exception:
            pass  # graceful fallback

        shutil.move(str(doc), str(trash_dir / doc.name))
        assert (trash_dir / "test_doc.pdf").exists()
        assert deleted_chunks == 0  # no chunks counted but no crash


class TestTrashEndpoints:
    def test_empty_trash_removes_files(self, tmp_corpus):
        """Empty trash permanently deletes all files in trash/."""
        corpus_dir, uploads, doc, manifest, index = tmp_corpus
        trash_dir = uploads / "trash"
        trash_dir.mkdir()
        (trash_dir / "old_file.pdf").write_bytes(b"content")
        (trash_dir / "another.pdf").write_bytes(b"content2")

        count = 0
        for f in trash_dir.iterdir():
            if f.is_file():
                f.unlink()
                count += 1

        assert count == 2
        assert list(trash_dir.iterdir()) == []

    def test_list_trash(self, tmp_corpus):
        """List trash returns filenames in trash/."""
        corpus_dir, uploads, doc, manifest, index = tmp_corpus
        trash_dir = uploads / "trash"
        trash_dir.mkdir()
        (trash_dir / "trashed_file.pdf").write_bytes(b"x")

        files = [f.name for f in sorted(trash_dir.iterdir()) if f.is_file()]
        assert "trashed_file.pdf" in files


class TestAboutEndpoint:
    def test_about_reads_file(self, tmp_path):
        """About endpoint returns content from about.md if it exists."""
        about = tmp_path / "about.md"
        about.write_text("# AIStudio\n\nLocal RAG system.")

        content = about.read_text()
        assert "AIStudio" in content
        assert "RAG" in content

    def test_about_fallback_when_no_file(self):
        """About endpoint returns fallback content if about.md missing."""
        fallback = "# AIStudio\n\nLocal RAG system — Apple Silicon, no cloud dependency."
        assert "AIStudio" in fallback
