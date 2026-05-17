from __future__ import annotations

from pathlib import Path

from local_llm_bot.app.utils.corpus_paths import corpus_paths


def test_corpus_paths_creates_structure(tmp_path: Path) -> None:
    # Fake repo root
    repo_root = tmp_path
    (repo_root / "pyproject.toml").write_text("x", encoding="utf-8")

    paths = corpus_paths(repo_root, "unit-test")
    assert paths["base"].exists()
    assert "chroma" not in paths  # chroma folder removed — AIStudio uses Qdrant only
    assert not (paths["base"] / "chroma").exists()  # chroma dir must not be created
    assert str(paths["index"]).endswith("data/corpora/unit-test/index.jsonl")
