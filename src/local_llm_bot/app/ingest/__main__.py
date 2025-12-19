import argparse
from pathlib import Path

from local_llm_bot.app.ingest.pipeline import ingest_directory

DEFAULT_CORPUS_DIRECTORY = "/Users/mbarbero2018/Documents"


def main() -> None:
    p = argparse.ArgumentParser()
    # p.add_argument("--root", required=True, help="Directory to ingest")
    p.add_argument("--root", default=DEFAULT_CORPUS_DIRECTORY, help="Directory to ingest")
    p.add_argument("--out", default="data/index.jsonl", help="Output JSONL index path")
    p.add_argument("--chunk-size", type=int, default=1200)
    p.add_argument("--overlap", type=int, default=200)
    args = p.parse_args()

    n = ingest_directory(
        root=Path(args.root),
        out_index=Path(args.out),
        chunk_size=args.chunk_size,
        overlap=args.overlap,
    )
    print(f"Ingested {n} chunks into {args.out}")


if __name__ == "__main__":
    main()
