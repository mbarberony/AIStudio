from __future__ import annotations

import argparse
import heapq
import json
import time
from collections import Counter, defaultdict
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

from ..config import (
    DEFAULT_CHUNK_SIZE,
    DEFAULT_CORPUS_DIRECTORY,
    DEFAULT_EMBED_CHUNKS_PER_SEC,
    DEFAULT_EMBED_DIM,
    DEFAULT_FLOAT_BYTES,
    DEFAULT_OVERHEAD_HIGH,
    DEFAULT_OVERHEAD_LOW,
    DEFAULT_OVERLAP,
    DEFAULT_PARSE_FILES_PER_SEC,
    default_excludes,
)
from ..ingest.loaders import SUPPORTED_EXTS, extract_text, is_excluded, should_skip_filename

try:
    from tqdm import tqdm  # type: ignore
except Exception:  # pragma: no cover
    tqdm = None  # type: ignore


@dataclass(frozen=True)
class Estimates:
    db_low_bytes: int
    db_high_bytes: int
    extract_low_s: float
    extract_high_s: float
    embed_low_s: float
    embed_high_s: float


def estimate_chunks(n_chars: int, chunk_size: int, overlap: int) -> int:
    if n_chars <= 0:
        return 0
    if n_chars <= chunk_size:
        return 1
    step = max(1, chunk_size - overlap)
    return 1 + max(0, (n_chars - chunk_size + step - 1) // step)


def human_bytes(n: int) -> str:
    units = ["B", "KB", "MB", "GB", "TB"]
    x = float(n)
    for u in units:
        if x < 1024 or u == units[-1]:
            return f"{x:.2f} {u}"
        x /= 1024
    return f"{x:.2f} TB"


def fmt_duration(seconds: float) -> str:
    if seconds < 60:
        return f"{seconds:.1f}s"
    minutes = seconds / 60
    if minutes < 60:
        return f"{minutes:.1f}m"
    hours = minutes / 60
    if hours < 48:
        return f"{hours:.1f}h"
    days = hours / 24
    return f"{days:.1f}d"


def iter_files(root: Path, excludes: list[str]) -> Iterable[Path]:
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        if should_skip_filename(p.name):
            continue
        if is_excluded(p, excludes):
            continue
        yield p


def compute_estimates(
    *,
    files_supported: int,
    chunks: int,
    embed_dim: int,
    float_bytes: int,
    overhead_low: float,
    overhead_high: float,
    parse_files_per_sec: float,
    embed_chunks_per_sec: float,
) -> Estimates:
    raw_vec_bytes = chunks * embed_dim * float_bytes
    db_low = int(raw_vec_bytes * overhead_low)
    db_high = int(raw_vec_bytes * overhead_high)

    # Throughput to time
    extract_s = (files_supported / parse_files_per_sec) if parse_files_per_sec > 0 else 0.0
    embed_s = (chunks / embed_chunks_per_sec) if embed_chunks_per_sec > 0 else 0.0

    # Bands (conservative)
    extract_low, extract_high = extract_s * 0.7, extract_s * 1.5
    embed_low, embed_high = embed_s * 0.7, embed_s * 1.8

    return Estimates(
        db_low_bytes=db_low,
        db_high_bytes=db_high,
        extract_low_s=extract_low,
        extract_high_s=extract_high,
        embed_low_s=embed_low,
        embed_high_s=embed_high,
    )


def main() -> None:
    p = argparse.ArgumentParser(description="Corpus sizing + ingestion/embedding estimates")
    p.add_argument("--root", default=DEFAULT_CORPUS_DIRECTORY, help="Directory to scan")

    p.add_argument("--chunk-size", type=int, default=DEFAULT_CHUNK_SIZE)
    p.add_argument("--overlap", type=int, default=DEFAULT_OVERLAP)

    p.add_argument("--embed-dim", type=int, default=DEFAULT_EMBED_DIM)
    p.add_argument("--float-bytes", type=int, default=DEFAULT_FLOAT_BYTES)
    p.add_argument("--overhead-low", type=float, default=DEFAULT_OVERHEAD_LOW)
    p.add_argument("--overhead-high", type=float, default=DEFAULT_OVERHEAD_HIGH)

    p.add_argument("--parse-files-per-sec", type=float, default=DEFAULT_PARSE_FILES_PER_SEC)
    p.add_argument("--embed-chunks-per-sec", type=float, default=DEFAULT_EMBED_CHUNKS_PER_SEC)

    p.add_argument(
        "--exclude", action="append", default=[], help="Glob pattern to exclude (repeatable)"
    )
    p.add_argument("--no-default-excludes", action="store_true")

    p.add_argument("--top", type=int, default=20, help="Top N to print for extensions & failures")
    p.add_argument("--report-json", default="", help="Write JSON report to this path")

    args = p.parse_args()

    root = Path(args.root).expanduser()
    if not root.exists():
        raise SystemExit(f"Path not found: {root}")

    excludes = [] if args.no_default_excludes else default_excludes()
    excludes.extend(args.exclude)

    ext_counts_all = Counter()
    ext_counts_supported = Counter()

    bytes_total = 0
    files_total = 0
    files_supported = 0

    extracted_chars_total = 0
    estimated_chunks_total = 0

    failure_counts: dict[str, Counter] = defaultdict(Counter)
    failure_samples: dict[tuple[str, str], list[str]] = defaultdict(list)

    largest: list[tuple[int, Path]] = []  # min-heap (size, path)

    t0 = time.time()

    paths = list(iter_files(root, excludes))
    iterator = paths
    if tqdm is not None:
        iterator = tqdm(paths, desc="Scanning files", unit="file")  # type: ignore

    for path in iterator:  # type: ignore
        files_total += 1
        try:
            size = path.stat().st_size
        except Exception:
            ext = path.suffix.lower()
            ext_counts_all[ext] += 1
            failure_counts[ext]["stat_error"] += 1
            key = (ext, "stat_error")
            if len(failure_samples[key]) < 10:
                failure_samples[key].append(str(path))
            continue

        bytes_total += size

        # top-N largest tracking
        if len(largest) < args.top:
            heapq.heappush(largest, (size, path))
        else:
            heapq.heappushpop(largest, (size, path))

        ext = path.suffix.lower()
        ext_counts_all[ext] += 1

        if ext in SUPPORTED_EXTS:
            files_supported += 1
            ext_counts_supported[ext] += 1

            res = extract_text(path)
            if not res.ok:
                reason = res.reason or "unknown"
                failure_counts[ext][reason] += 1
                key = (ext, reason)
                if len(failure_samples[key]) < 10:
                    failure_samples[key].append(str(path))
                continue

            extracted_chars_total += len(res.text)
            estimated_chunks_total += estimate_chunks(len(res.text), args.chunk_size, args.overlap)

    t1 = time.time()
    scan_seconds = t1 - t0

    largest_sorted = sorted(largest, reverse=True, key=lambda x: x[0])

    est = compute_estimates(
        files_supported=files_supported,
        chunks=estimated_chunks_total,
        embed_dim=args.embed_dim,
        float_bytes=args.float_bytes,
        overhead_low=args.overhead_low,
        overhead_high=args.overhead_high,
        parse_files_per_sec=args.parse_files_per_sec,
        embed_chunks_per_sec=args.embed_chunks_per_sec,
    )

    print("\n=== Corpus stats ===")
    print(f"Root:                  {root}")
    print(f"Excluded patterns:      {len(excludes)}")
    print(f"Total files scanned:    {files_total:,}")
    print(f"Total size:             {human_bytes(bytes_total)}")
    print(f"Supported files seen:   {files_supported:,}  ({', '.join(sorted(SUPPORTED_EXTS))})")
    print(f"Extracted text chars:   {extracted_chars_total:,}")
    print(
        f"Estimated chunks:       {estimated_chunks_total:,}  (chunk={args.chunk_size}, overlap={args.overlap})"
    )
    print(f"Scan wall time:         {fmt_duration(scan_seconds)}")

    print("\n=== Extensions (top) ===")
    for ext, n in ext_counts_all.most_common(args.top):
        label = ext if ext else "[no_ext]"
        print(f"{label:10s} {n:,}")

    print("\n=== Supported extensions (counts) ===")
    for ext in sorted(SUPPORTED_EXTS):
        print(f"{ext:10s} {ext_counts_supported.get(ext, 0):,}")

    total_failures = sum(sum(c.values()) for c in failure_counts.values())
    print("\n=== Parse/extraction failures ===")
    print(f"Total failures:         {total_failures:,}")
    if total_failures:
        flat: list[tuple[int, str, str]] = []
        for ext, c in failure_counts.items():
            for reason, n in c.items():
                flat.append((n, ext, reason))
        flat.sort(reverse=True)

        for n, ext, reason in flat[: args.top]:
            print(f"{n:8d}  {ext:6s}  {reason}")

        print("\n--- Sample failing paths (top categories) ---")
        for _n, ext, reason in flat[: min(5, len(flat))]:
            key = (ext, reason)
            samples = failure_samples.get(key, [])
            if samples:
                print(f"\n[{ext} | {reason}] showing up to {len(samples)} samples:")
                for s in samples:
                    print(f"  - {s}")

    print("\n=== Largest files (top) ===")
    for size, path in largest_sorted:
        print(f"{size / 1024 / 1024:9.2f} MB  {path}")

    print("\n=== Embedding DB size estimate (Chroma) ===")
    print(f"Embedding dim:          {args.embed_dim}")
    print(
        f"Vector raw bytes/chunk: {args.embed_dim * args.float_bytes} bytes (float{args.float_bytes * 8})"
    )
    print(
        f"Estimated DB size:      {human_bytes(est.db_low_bytes)}  to  {human_bytes(est.db_high_bytes)} "
        f"(overhead {args.overhead_low}x–{args.overhead_high}x)"
    )

    print("\n=== Rough time bands (high-level) ===")
    print("These are back-of-the-envelope estimates based on the throughput knobs.")
    print(f"  parse-files-per-sec:  {args.parse_files_per_sec}")
    print(f"  embed-chunks-per-sec: {args.embed_chunks_per_sec}")
    print()
    print(
        f"Extraction / I-O time:  {fmt_duration(est.extract_low_s)}  to  {fmt_duration(est.extract_high_s)}"
    )
    print(
        f"Embedding time:         {fmt_duration(est.embed_low_s)}  to  {fmt_duration(est.embed_high_s)}"
    )
    print(
        f"Total (rough):          {fmt_duration(est.extract_low_s + est.embed_low_s)}  to  {fmt_duration(est.extract_high_s + est.embed_high_s)}"
    )

    print("\n=== Practical exclusions guidance ===")
    print("Defaults already exclude macOS/system/media/caches. Consider adding excludes for:")
    print("  - large archives/backups (.zip, .tar, .dmg)")
    print("  - cloud sync caches (Dropbox/.dropbox.cache, OneDrive caches)")
    print("  - build artifacts (dist/, build/, target/)")
    print("  - VM images")

    if args.report_json:
        report = {
            "root": str(root),
            "excludes": excludes,
            "files_total": files_total,
            "bytes_total": bytes_total,
            "files_supported": files_supported,
            "ext_counts_all": dict(ext_counts_all),
            "ext_counts_supported": dict(ext_counts_supported),
            "extracted_chars_total": extracted_chars_total,
            "estimated_chunks_total": estimated_chunks_total,
            "failures": {ext: dict(cnt) for ext, cnt in failure_counts.items()},
            "embedding_estimate": {
                "embed_dim": args.embed_dim,
                "float_bytes": args.float_bytes,
                "overhead_low": args.overhead_low,
                "overhead_high": args.overhead_high,
                "db_size_bytes_low": est.db_low_bytes,
                "db_size_bytes_high": est.db_high_bytes,
            },
            "time_estimate": {
                "parse_files_per_sec": args.parse_files_per_sec,
                "embed_chunks_per_sec": args.embed_chunks_per_sec,
                "extract_low_s": est.extract_low_s,
                "extract_high_s": est.extract_high_s,
                "embed_low_s": est.embed_low_s,
                "embed_high_s": est.embed_high_s,
                "scan_wall_seconds": scan_seconds,
            },
        }
        out = Path(args.report_json).expanduser()
        out.write_text(json.dumps(report, indent=2), encoding="utf-8")
        print(f"\nWrote JSON report: {out}")


if __name__ == "__main__":
    main()
