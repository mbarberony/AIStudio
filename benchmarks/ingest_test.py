#!/usr/bin/env python3
# Version: 1.2.6
"""
AIStudio Ingest Test Harness
Operator-only — run via ais_ingest_test_ops alias (installed by ais_install_ops).

Tests the ingest pipeline end-to-end across four test modes:

  --test 1 (default)  Fresh ingest → MD5 validation → Skip regression → Thematic query
  --test 2            Ingest 6 → MD5 → Upload 6+4 (skip existing 6, ingest 4 new)
  --test 3            Ingest 6 → MD5 → Upload 6+4 (reingest all 10)
  --test 4            Ingest 6 → MD5 → Mixed: skip 1, reingest 2, ingest 3 (new),
                                        skip 4, reingest 5, skip 6 (hardcoded pattern)

Each test ends with Phase 4 (Thematic query) and Phase 5 (Cleanup).

Usage:
    ais_ingest_test_ops                          # test 1, default
    ais_ingest_test_ops --test 2                 # mixed batch test
    ais_ingest_test_ops --test 4 --no-cleanup    # leave corpus after test
    ais_ingest_test_ops --model llama3.1:70b     # override query model
    ais_ingest_test_ops --question "..."         # override Phase 4 query
    ais_ingest_test_ops --seed                   # seed fixtures
    ais_ingest_test_ops --list-sets              # list available test sets

Reports:
    benchmarks/reports/ingest_test_t<N>_<timestamp>.{json,md}
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

try:
    import psutil as _psutil

    _PSUTIL_AVAILABLE = True
except ImportError:
    _PSUTIL_AVAILABLE = False

try:
    import yaml as _yaml

    _YAML_AVAILABLE = True
except ImportError:
    _YAML_AVAILABLE = False

API_BASE = "http://localhost:8000"
POLL_INTERVAL_SEC = 2
MAX_POLLS = 300
DEFAULT_QUERY = "What were the key business risks and headwinds described in these annual reports?"

# Test 4 decision pattern for base files (index 0-5)
# "skip" = already indexed, skip it
# "reingest" = already indexed, delete chunks and re-embed
# "new" = not yet indexed (use extra_files[0] here)
TEST4_PATTERN = ["skip", "reingest", "new", "skip", "reingest", "skip"]


# ── CLI ────────────────────────────────────────────────────────────────────────


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="AIStudio Ingest Test Harness")
    mode = p.add_mutually_exclusive_group()
    mode.add_argument(
        "--test", type=int, choices=[1, 2, 3, 4], default=1, help="Test mode 1-4 (default: 1)"
    )
    mode.add_argument("--set", default=None, help="Legacy: test set ID. Use --test instead.")
    p.add_argument("--corpus", default="ingest_test")
    p.add_argument("--api", default=API_BASE)
    p.add_argument("--model", default=None, help="Model for Phase 4 query")
    p.add_argument("--question", default=None, help="Override Phase 4 query text")
    p.add_argument("--seed", action="store_true")
    p.add_argument("--list-sets", action="store_true")
    p.add_argument("--skip-query", action="store_true")
    p.add_argument("--no-cleanup", action="store_true")
    p.add_argument("--no-markdown", action="store_true")
    return p.parse_args()


# ── Machine info ───────────────────────────────────────────────────────────────


def get_machine_info() -> dict:
    info: dict = {}
    try:
        r = subprocess.run(
            ["sysctl", "-n", "machdep.cpu.brand_string"], capture_output=True, text=True, timeout=5
        )
        info["cpu_model"] = r.stdout.strip() or "unknown"
    except Exception:
        info["cpu_model"] = "unknown"
    try:
        r = subprocess.run(
            ["sysctl", "-n", "hw.logicalcpu"], capture_output=True, text=True, timeout=5
        )
        info["cpu_cores"] = int(r.stdout.strip())
    except Exception:
        info["cpu_cores"] = None
    try:
        if _PSUTIL_AVAILABLE:
            info["ram_gb"] = round(_psutil.virtual_memory().total / (1024**3), 1)
        else:
            r = subprocess.run(
                ["sysctl", "-n", "hw.memsize"], capture_output=True, text=True, timeout=5
            )
            info["ram_gb"] = round(int(r.stdout.strip()) / (1024**3), 1)
    except Exception:
        info["ram_gb"] = None
    try:
        r = subprocess.run(
            ["system_profiler", "SPHardwareDataType"], capture_output=True, text=True, timeout=10
        )
        for line in r.stdout.splitlines():
            if "Chip" in line or "Processor" in line:
                info["gpu_chip"] = line.split(":")[-1].strip()
                break
        else:
            info["gpu_chip"] = "unknown"
    except Exception:
        info["gpu_chip"] = "unknown"
    return info


# ── Fixture management ─────────────────────────────────────────────────────────


def seed_fixtures(fixture_dir: Path) -> None:
    src = Path.home() / "Downloads" / "sec_10k_corpus"
    if not src.exists():
        print(f"ERROR: Source not found: {src}")
        sys.exit(1)
    fixture_dir.mkdir(parents=True, exist_ok=True)
    files = list(src.glob("*.htm"))
    print(f"  Seeding {len(files)} files from {src}")
    for f in files:
        shutil.copy2(f, fixture_dir / f.name)
        print(f"  + {f.name}")
    print(f"\n  Done — {len(files)} files seeded to {fixture_dir}")


def load_test_sets(sets_path: Path) -> dict:
    if not _YAML_AVAILABLE:
        print("ERROR: pyyaml not installed — pip install pyyaml")
        sys.exit(1)
    if not sets_path.exists():
        print(f"ERROR: Test sets file not found: {sets_path}")
        sys.exit(1)
    with open(sets_path) as f:
        return _yaml.safe_load(f)


# ── API helpers ────────────────────────────────────────────────────────────────


def api_get(api: str, path: str) -> dict:
    import urllib.request

    req = urllib.request.urlopen(f"{api}{path}", timeout=30)
    return json.loads(req.read())


def api_post(api: str, path: str, data: dict | None = None) -> dict:
    import urllib.request

    body = json.dumps(data or {}).encode()
    req = urllib.request.Request(
        f"{api}{path}", data=body, headers={"Content-Type": "application/json"}, method="POST"
    )
    return json.loads(urllib.request.urlopen(req, timeout=120).read())


def api_delete(api: str, path: str) -> dict:
    import urllib.request

    req = urllib.request.Request(f"{api}{path}", method="DELETE")
    return json.loads(urllib.request.urlopen(req, timeout=30).read())


def upload_file(api: str, corpus: str, filepath: Path) -> bool:
    import urllib.request
    import uuid

    boundary = uuid.uuid4().hex
    with open(filepath, "rb") as f:
        file_data = f.read()
    body = (
        (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="file"; filename="{filepath.name}"\r\n'
            f"Content-Type: text/html\r\n\r\n"
        ).encode()
        + file_data
        + f"\r\n--{boundary}--\r\n".encode()
    )
    req = urllib.request.Request(
        f"{api}/corpus/{corpus}/upload",
        data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="POST",
    )
    try:
        return urllib.request.urlopen(req, timeout=60).status == 200
    except Exception:
        return False


def delete_file_chunks(api: str, corpus: str, filename: str) -> bool:
    """Delete Qdrant chunks for one file — called before reingest."""
    try:
        api_delete(api, f"/corpus/{corpus}/file/{filename}/chunks")
        return True
    except Exception:
        return False


def check_health(api: str) -> bool:
    try:
        return api_get(api, "/health").get("status") == "ok"
    except Exception:
        return False


def get_md5(api: str, corpus: str, filename: str) -> str | None:
    try:
        return api_get(api, f"/corpus/{corpus}/file/{filename}/md5").get("md5")
    except Exception:
        return None


def poll_ingest(api: str, corpus: str, expected_files: int = 0) -> dict:
    polls = 0
    last_chunks = 0
    start_time = time.time()
    spinner = ["|", "/", "-", "\\"]
    time.sleep(POLL_INTERVAL_SEC)
    while polls < MAX_POLLS:
        time.sleep(POLL_INTERVAL_SEC)
        polls += 1
        try:
            status = api_get(api, f"/corpus/{corpus}/ingest-status")
            state = status.get("status", "unknown")
            chunks = status.get("chunks_written", 0)
            fp = status.get("files_processed", 0)
            ft = status.get("files_total", 0) or expected_files
            bytes_proc = status.get("bytes_processed", 0)
            total_bytes = status.get("total_bytes", 0)
            if chunks > last_chunks:
                last_chunks = chunks
            # File counter: currently active file = completed + 1
            active = min(fp + 1, ft) if state == "running" else ft
            # Progress percentage from bytes if available, else chunks
            if total_bytes > 0:
                pct = min(99, round(bytes_proc / total_bytes * 100))
                mb_total = total_bytes / (1024 * 1024)
            else:
                pct = 0
                mb_total = 0.0
            # Use server-computed pct_complete (D(k) based) if available
            server_pct = min(99, status.get("pct_complete", pct))
            bar_fill = min(20, int(server_pct / 100 * 20))
            bar = ("▓" * bar_fill).ljust(20, "░")
            elapsed = int(time.time() - start_time)
            mins, secs = divmod(elapsed, 60)
            time_str = f"{mins}:{secs:02d}"
            if state in ("done", "error", "cancelled"):
                # Final display: all done
                if total_bytes > 0:
                    label = f"File {ft} of {ft} indexed · {mb_total:.1f}MB · {last_chunks:,} chunks"
                else:
                    label = f"File {ft} of {ft} indexed · {last_chunks:,} chunks"
                print(f"\r  {spinner[polls % 4]} [{bar}] {label}")
                return status
            else:
                # Running: show current file size and D(k) % completion
                # current file size = file_sizes[fp] if available
                file_sizes_list = status.get("file_sizes", [])
                cur_file_mb = (
                    (file_sizes_list[fp] / (1024 * 1024)) if fp < len(file_sizes_list) else 0.0
                )
                if total_bytes > 0 and cur_file_mb > 0:
                    label = (
                        f"File {active} of {ft} being indexed · "
                        f"{cur_file_mb:.1f}MB out of {mb_total:.1f}MB Total · "
                        f"{last_chunks:,} chunks · ~ {server_pct}% completed · "
                        f"{time_str} elapsed"
                    )
                elif total_bytes > 0:
                    label = (
                        f"File {active} of {ft} being indexed · "
                        f"{mb_total:.1f}MB Total · "
                        f"{last_chunks:,} chunks · ~ {server_pct}% completed · "
                        f"{time_str} elapsed"
                    )
                else:
                    label = f"File {active} of {ft} being indexed · {last_chunks:,} chunks · {time_str} elapsed"
                print(f"\r  {spinner[polls % 4]} [{bar}] {label}", end="", flush=True)
        except Exception:
            pass
    print()
    return {"status": "timeout", "chunks_written": last_chunks}


def parse_summary(summary: str) -> tuple[int, int]:
    import re

    new_count, skipped_count = -1, -1
    if summary:
        m = re.search(r"(\d+)\s+new", summary)
        if m:
            new_count = int(m.group(1))
        m = re.search(r"(\d+)\s+skipped", summary)
        if m:
            skipped_count = int(m.group(1))
    return new_count, skipped_count


def compute_metrics(elapsed_sec: float, chunks: int, total_bytes: int, file_count: int) -> dict:
    m: dict = {}
    if elapsed_sec > 0 and chunks > 0:
        m["chunks_per_sec"] = round(chunks / elapsed_sec, 1)
    if elapsed_sec > 0 and total_bytes > 0:
        total_mb = total_bytes / (1024 * 1024)
        m["mb_per_sec"] = round(total_mb / elapsed_sec, 2)
    if elapsed_sec > 0 and file_count > 0:
        m["sec_per_avg_file"] = round(elapsed_sec / file_count, 1)
        m["avg_file_mb"] = round((total_bytes / file_count) / (1024 * 1024), 2)
    return m


def fmt_metrics(m: dict) -> str:
    parts = []
    if m.get("chunks_per_sec"):
        parts.append(f"{m['chunks_per_sec']} chunks/s")
    if m.get("mb_per_sec"):
        parts.append(f"{m['mb_per_sec']} MB/s")
    if m.get("sec_per_avg_file") and m.get("avg_file_mb"):
        parts.append(f"{m['sec_per_avg_file']}s/file (avg {m['avg_file_mb']}MB)")
    return " · ".join(parts)


# ── Test phases ────────────────────────────────────────────────────────────────


def phase_fresh_ingest(api: str, corpus: str, files: list[Path]) -> dict:
    label = f"Phase 1 — Fresh ingest ({len(files)} files)"
    print(f"\n[{label}]")
    total_bytes = sum(f.stat().st_size for f in files)
    for i, f in enumerate(files, 1):
        ok = upload_file(api, corpus, f)
        print(f"  {'OK' if ok else 'FAIL'} [{i}/{len(files)}] {f.name}")
    print("  Triggering ingest...")
    try:
        api_post(api, f"/corpus/{corpus}/ingest")
    except Exception as e:
        return {"pass": False, "error": str(e), "chunks": 0, "elapsed_sec": 0, "label": label}
    t0 = time.time()
    final = poll_ingest(api, corpus, expected_files=len(files))
    elapsed = round(time.time() - t0, 1)
    chunks = final.get("chunks_written", 0)
    summary = final.get("summary", final.get("message", ""))
    passed = final.get("status") == "done" and chunks > 0
    result_str = summary or f"{chunks:,} chunks"
    print(f"  {'PASS' if passed else 'FAIL'} {result_str} · {elapsed}s")
    metrics = compute_metrics(elapsed, chunks, total_bytes, len(files))
    if metrics:
        print(f"  {fmt_metrics(metrics)}")
    return {
        "pass": passed,
        "chunks": chunks,
        "elapsed_sec": elapsed,
        "summary": summary,
        "state": final.get("status"),
        "total_bytes": total_bytes,
        "metrics": metrics,
        "label": label,
    }


def phase_md5_validation(api: str, corpus: str, files: list[Path]) -> dict:
    label = f"Phase 2 — MD5 validation ({len(files)} files)"
    print(f"\n[{label}]")
    results = []
    for f in files:
        md5 = get_md5(api, corpus, f.name)
        ok = md5 is not None and len(md5) == 32
        results.append({"file": f.name, "md5": md5, "pass": ok})
        print(f"  {'OK' if ok else 'FAIL'} {f.name} -> {md5 or 'NOT FOUND'}")
    passed_count = sum(1 for r in results if r["pass"])
    passed = passed_count == len(files)
    print(f"  {'PASS' if passed else 'FAIL'} {passed_count}/{len(files)} files have MD5 in Qdrant")
    return {
        "pass": passed,
        "passed_count": passed_count,
        "total": len(files),
        "results": results,
        "label": label,
    }


def phase_skip_regression(api: str, corpus: str, files: list[Path]) -> dict:
    label = f"Phase 3 — Skip regression (re-upload {len(files)} files)"
    print(f"\n[{label}]")
    for i, f in enumerate(files, 1):
        ok = upload_file(api, corpus, f)
        print(f"  {'OK' if ok else 'FAIL'} [{i}/{len(files)}] {f.name}")
    print("  Triggering ingest...")
    try:
        api_post(api, f"/corpus/{corpus}/ingest")
    except Exception as e:
        return {"pass": False, "error": str(e), "label": label}
    t0 = time.time()
    final = poll_ingest(api, corpus, expected_files=len(files))
    elapsed = round(time.time() - t0, 1)
    summary = final.get("summary", final.get("message", ""))
    new_count, skipped_count = parse_summary(summary)
    passed = final.get("status") == "done" and new_count == 0 and skipped_count == len(files)
    if passed:
        print(f"  PASS {summary} · {elapsed}s")
    else:
        print(f"  FAIL expected 0 new / {len(files)} skipped, got: {summary} · {elapsed}s")
    return {
        "pass": passed,
        "new": new_count,
        "skipped": skipped_count,
        "expected_skipped": len(files),
        "elapsed_sec": elapsed,
        "summary": summary,
        "label": label,
    }


def phase_mixed_batch(
    api: str, corpus: str, base_files: list[Path], extra_files: list[Path], mode: str
) -> dict:
    """
    Phase 3 for tests 2, 3, 4.

    mode='skip_existing'  skip all base files, ingest extra as new
    mode='reingest_all'   delete chunks + reingest all base + ingest extra
    mode='mixed'          TEST4_PATTERN per base file; extra files always ingested as new
    """
    n_base = len(base_files)
    n_extra = len(extra_files)
    all_files = base_files + extra_files
    label = f"Phase 3 — Mixed batch ({n_base} base + {n_extra} new, mode={mode})"
    print(f"\n[{label}]")

    total_bytes = sum(f.stat().st_size for f in all_files)
    reingested: list[str] = []
    pre_skipped: list[str] = []
    new_files: list[str] = []

    for i, f in enumerate(base_files):
        if mode == "skip_existing":
            action = "skip"
        elif mode == "reingest_all":
            action = "reingest"
        else:
            action = TEST4_PATTERN[i] if i < len(TEST4_PATTERN) else "skip"

        if action == "reingest":
            delete_file_chunks(api, corpus, f.name)
            reingested.append(f.name)
            tag = "reingest"
        elif action == "new":
            # In test 4, "new" means use an extra file in this slot
            if extra_files:
                ef = extra_files.pop(0)
                ok = upload_file(api, corpus, ef)
                print(
                    f"  {'OK' if ok else 'FAIL'} [{i + 1}/{len(base_files) + n_extra}] {ef.name} [new]"
                )
                new_files.append(ef.name)
                continue
            else:
                action = "skip"
                tag = "skip(no extra)"
        else:
            pre_skipped.append(f.name)
            tag = "skip"

        ok = upload_file(api, corpus, f)
        print(f"  {'OK' if ok else 'FAIL'} [{i + 1}/{n_base + n_extra}] {f.name} [{tag}]")

    for j, ef in enumerate(extra_files):
        ok = upload_file(api, corpus, ef)
        print(f"  {'OK' if ok else 'FAIL'} [{n_base + j + 1}/{n_base + n_extra}] {ef.name} [new]")
        new_files.append(ef.name)

    print("  Triggering ingest...")
    try:
        api_post(api, f"/corpus/{corpus}/ingest")
    except Exception as e:
        return {"pass": False, "error": str(e), "label": label}

    t0 = time.time()
    final = poll_ingest(api, corpus, expected_files=n_base + n_extra)
    elapsed = round(time.time() - t0, 1)
    chunks = final.get("chunks_written", 0)
    summary = final.get("summary", final.get("message", ""))
    new_count, skipped_count = parse_summary(summary)
    passed = final.get("status") == "done" and chunks > 0

    print(f"  {'PASS' if passed else 'FAIL'} {summary} · {elapsed}s")
    metrics = compute_metrics(elapsed, chunks, total_bytes, n_base + n_extra)
    if metrics:
        print(f"  {fmt_metrics(metrics)}")

    return {
        "pass": passed,
        "new": new_count,
        "skipped": skipped_count,
        "reingested": reingested,
        "pre_skipped": pre_skipped,
        "new_files": new_files,
        "chunks": chunks,
        "elapsed_sec": elapsed,
        "summary": summary,
        "total_bytes": total_bytes,
        "metrics": metrics,
        "label": label,
    }


def phase_thematic_query(
    api: str, corpus: str, question: str | None = None, model: str | None = None
) -> dict:
    label = "Phase 4 — Thematic query"
    print(f"\n[{label}]")
    query = question or DEFAULT_QUERY
    print(f'  Query: "{query}"')
    t0 = time.time()
    payload: dict = {"query": query, "corpus": corpus, "top_k": 10, "temperature": 0.3}
    if model:
        payload["model"] = model
    try:
        result = api_post(api, "/ask", payload)
        elapsed = round(time.time() - t0, 1)
    except Exception as e:
        return {"pass": False, "error": str(e), "elapsed_sec": 0, "label": label}
    citations = result.get("citations") or []
    sources = {c.get("source", "").split("/")[-1] for c in citations if c.get("source")}
    answer = result.get("answer", "")
    passed = len(sources) >= 2 and len(answer) > 100
    print(
        f"  {'PASS' if passed else 'FAIL'} {elapsed}s · citations: {len(citations)} · distinct sources: {len(sources)}"
    )
    for s in sorted(sources)[:5]:
        print(f"    - {s}")
    # Answer NOT printed to terminal — only in .md report
    return {
        "pass": passed,
        "elapsed_sec": elapsed,
        "citation_count": len(citations),
        "distinct_sources": len(sources),
        "sources": sorted(sources),
        "answer": answer,
        "query": query,
        "label": label,
    }


def phase_cleanup(api: str, corpus: str) -> dict:
    label = "Phase 5 — Cleanup"
    print(f"\n[{label}]")
    try:
        api_delete(api, f"/corpus/{corpus}?confirm=yes")
        print(f"  ✓ Corpus '{corpus}' deleted")
        return {"pass": True, "label": label}
    except Exception as e:
        print(f"  FAIL {e}")
        return {"pass": False, "error": str(e), "label": label}


# ── Markdown report ────────────────────────────────────────────────────────────


def write_markdown(
    results: dict, test_mode: int, corpus: str, output_path: Path, machine: dict
) -> None:
    md_path = output_path.with_suffix(".md")
    ts = datetime.fromisoformat(results["run_at"]).strftime("%Y-%m-%d %H:%M")
    phases = results["phases"]
    passed = results["summary"]["phases_passed"]
    total = results["summary"]["phases_total"]
    overall = "PASSED" if results["summary"]["all_passed"] else f"FAILED ({passed}/{total} phases)"

    p1 = phases.get("fresh_ingest", {})
    p2 = phases.get("md5_validation", {})
    p3 = phases.get("skip_regression") or phases.get("mixed_batch", {})
    p4 = phases.get("thematic_query", {})
    p5 = phases.get("cleanup", {})

    report_name = output_path.stem
    lines = [
        "# AIStudio Ingest Test Report",
        "",
        f"**Report:** `{report_name}`",
        f"**Test mode:** `{test_mode}` ({['', 'Fresh ingest → MD5 → Skip → Query', 'Ingest 6+4 skip existing', 'Ingest 6+4 reingest all', 'Ingest 6+4 mixed'][test_mode] if test_mode <= 4 else ''})",
        f"**Corpus:** `{corpus}` | **Run at:** {ts}",
        f"**Result: {overall}**",
        "",
        "## Machine",
        "",
        f"- **Chip:** {machine.get('gpu_chip', 'unknown')}",
        f"- **CPU:** {machine.get('cpu_model', 'unknown')} ({machine.get('cpu_cores', '?')} cores)",
        f"- **RAM:** {machine.get('ram_gb', '?')} GB",
        "",
        "## Summary",
        "",
        "| Phase | Result | Detail |",
        "|---|---|---|",
    ]

    lines.append(
        f"| {p1.get('label', 'Phase 1')} | {'PASS' if p1.get('pass') else 'FAIL'} | "
        f"{p1.get('chunks', 0):,} chunks · {p1.get('elapsed_sec', 0)}s |"
    )
    lines.append(
        f"| {p2.get('label', 'Phase 2')} | {'PASS' if p2.get('pass') else 'FAIL'} | "
        f"{p2.get('passed_count', 0)}/{p2.get('total', 0)} files |"
    )
    lines.append(
        f"| {p3.get('label', 'Phase 3')} | {'PASS' if p3.get('pass') else 'FAIL'} | "
        f"{p3.get('new', '?')} new · {p3.get('skipped', '?')} skipped · {p3.get('elapsed_sec', 0)}s |"
    )
    if p4:
        lines.append(
            f"| {p4.get('label', 'Phase 4')} | {'PASS' if p4.get('pass') else 'FAIL'} | "
            f"{p4.get('distinct_sources', 0)} sources · {p4.get('elapsed_sec', 0)}s |"
        )
    if p5:
        lines.append(
            f"| {p5.get('label', 'Phase 5')} | {'PASS' if p5.get('pass') else 'FAIL'} | "
            f"Corpus deleted |"
        )

    # Performance metrics
    for ph_key in ("fresh_ingest", "skip_regression", "mixed_batch"):
        ph = phases.get(ph_key, {})
        m = ph.get("metrics", {})
        if not m:
            continue
        lines += ["", f"## Performance — {ph.get('label', ph_key)}", ""]
        if m.get("chunks_per_sec"):
            lines.append(f"- **Throughput:** {m['chunks_per_sec']} chunks/sec")
        if m.get("mb_per_sec"):
            lines.append(f"- **Throughput:** {m['mb_per_sec']} MB/s")
        if m.get("sec_per_avg_file") and m.get("avg_file_mb"):
            lines.append(
                f"- **Latency/file:** {m['sec_per_avg_file']}s per avg file "
                f"({m['avg_file_mb']} MB avg)"
            )

    # Files tested
    lines += ["", "## Files Tested", ""]
    for f in results.get("files", []):
        lines.append(f"- `{f}`")

    # Phase 4 model answer — report only
    if p4 and p4.get("answer"):
        lines += [
            "",
            "## Phase 4 — Model Answer",
            f'*Query: "{p4.get("query", DEFAULT_QUERY)}"*',
            "",
            p4["answer"],
            "",
        ]
        if p4.get("sources"):
            lines += ["**Sources cited:**", ""]
            for s in p4["sources"]:
                lines.append(f"- {s}")

    lines.append("")  # trailing blank line

    with open(md_path, "w") as f:
        f.write("\n".join(lines))
    print(f"  * {md_path.name}")


# ── Main ───────────────────────────────────────────────────────────────────────


def main() -> None:
    args = parse_args()
    script_dir = Path(__file__).parent
    fixture_dir = script_dir / "fixtures"
    sets_path = script_dir / "ingest_test_sets.yaml"
    reports_dir = script_dir / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    if args.seed:
        seed_fixtures(fixture_dir)
        return

    sets_data = load_test_sets(sets_path)
    all_sets = {s["id"]: s for s in sets_data.get("sets", [])}

    if args.list_sets:
        print("\nAvailable test sets:")
        for sid, s in all_sets.items():
            print(f"  {sid:20s} {s['description']} ({len(s['files'])} files)")
        return

    base_set_id = args.set or "set_6"
    if base_set_id not in all_sets:
        print(f"ERROR: Test set '{base_set_id}' not found. Use --list-sets.")
        sys.exit(1)

    base_filenames: list[str] = all_sets[base_set_id]["files"]
    base_files = [fixture_dir / f for f in base_filenames]

    # Extra files for tests 2/3/4
    extra_filenames: list[str] = []
    extra_files: list[Path] = []
    test_mode = args.test
    if test_mode in (2, 3, 4):
        if "set_10" in all_sets:
            all10 = all_sets["set_10"]["files"]
            extra_filenames = [f for f in all10 if f not in base_filenames]
        else:
            extra_filenames = [
                "AllianceBernstein_10K_2017-02-14.htm",
                "AllianceBernstein_10K_2018-02-13.htm",
                "AllianceBernstein_10K_2019-02-13.htm",
                "AllianceBernstein_10K_2020-02-12.htm",
            ]
        extra_files = [fixture_dir / f for f in extra_filenames]

    missing = [f for f in base_files + extra_files if not f.exists()]
    if missing:
        print(f"ERROR: Missing {len(missing)} fixtures — run: ais_ingest_test_ops --seed")
        for m in missing[:5]:
            print(f"   {m.name}")
        sys.exit(1)

    machine = get_machine_info()
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    report_stem = f"REP - AIStudio - TEST - Ingestion - Type {test_mode} - {timestamp}"
    output_path = reports_dir / f"{report_stem}.json"

    print(f"\n{'=' * 55}")
    print("  AIStudio Ingest Test")
    print(f"{'=' * 55}")
    test_mode_labels = {
        1: "Fresh ingest → MD5 validation → Skip regression → Query",
        2: "Ingest 6 → MD5 → Upload 6+4 new, skip existing",
        3: "Ingest 6 → MD5 → Upload 6+4 new, reingest all",
        4: "Ingest 6 → MD5 → Mixed: skip/reingest/new per file",
    }
    mode_desc = test_mode_labels.get(test_mode, "")
    print(f"  Test mode   : {test_mode} ({mode_desc})")
    print(f"  Base files  : {len(base_files)}")
    if extra_files:
        print(f"  Extra files : {len(extra_files)}")
    print(f"  Corpus      : {args.corpus}")
    if args.model:
        print(f"  Model       : {args.model}")
    print(f"  Machine     : {machine.get('gpu_chip', '?')} · {machine.get('ram_gb', '?')}GB RAM")
    print()

    if not check_health(args.api):
        print(f"ERROR: Backend not reachable at {args.api} — run: ais_start")
        sys.exit(1)
    print(f"  Backend healthy at {args.api}")

    try:
        api_delete(args.api, f"/corpus/{args.corpus}?confirm=yes")
        print(f"  Deleted existing corpus '{args.corpus}'")
        time.sleep(1)
    except Exception:
        pass
    try:
        api_post(args.api, "/corpus/create", {"name": args.corpus})
        print(f"  Created corpus '{args.corpus}'")
    except Exception as e:
        print(f"ERROR: Could not create corpus: {e}")
        sys.exit(1)

    phases: dict = {}

    # Phase 1 — fresh ingest of base files
    phases["fresh_ingest"] = phase_fresh_ingest(args.api, args.corpus, base_files)

    # Phase 2 — MD5 validation (always before phase 3)
    phases["md5_validation"] = phase_md5_validation(args.api, args.corpus, base_files)

    # Brief pause — ensures _ingest_status is cleared before next ingest
    time.sleep(3)

    # Phase 3 — depends on test mode
    if test_mode == 1:
        phases["skip_regression"] = phase_skip_regression(args.api, args.corpus, base_files)
    elif test_mode == 2:
        phases["mixed_batch"] = phase_mixed_batch(
            args.api, args.corpus, list(base_files), list(extra_files), "skip_existing"
        )
    elif test_mode == 3:
        phases["mixed_batch"] = phase_mixed_batch(
            args.api, args.corpus, list(base_files), list(extra_files), "reingest_all"
        )
    elif test_mode == 4:
        phases["mixed_batch"] = phase_mixed_batch(
            args.api, args.corpus, list(base_files), list(extra_files), "mixed"
        )

    # Phase 4 — thematic query
    if not args.skip_query:
        phases["thematic_query"] = phase_thematic_query(
            args.api, args.corpus, question=args.question, model=args.model
        )

    # Phase 5 — cleanup (before results summary)
    if not args.no_cleanup:
        phases["cleanup"] = phase_cleanup(args.api, args.corpus)
    else:
        print(f"\n  Corpus '{args.corpus}' kept (--no-cleanup)")

    # Count after cleanup so Phase 5 is included in totals
    passed = sum(1 for p in phases.values() if p.get("pass"))
    total = len(phases)
    all_passed = passed == total

    print(f"\n{'=' * 55}")
    print(
        f"  Results: {passed}/{total} phases passed  {'ALL PASSED' if all_passed else 'SOME FAILED'}"
    )
    print(f"{'=' * 55}")

    all_filenames = base_filenames + extra_filenames
    results = {
        "run_at": datetime.now().isoformat(),
        "test_mode": test_mode,
        "machine": machine,
        "config": {
            "corpus": args.corpus,
            "api": args.api,
            "model": args.model,
            "question": args.question,
        },
        "files": all_filenames,
        "summary": {"phases_passed": passed, "phases_total": total, "all_passed": all_passed},
        "phases": phases,
    }
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\n  Folder: {reports_dir}")
    print(f"  * {output_path.name}")
    if not args.no_markdown:
        write_markdown(results, test_mode, args.corpus, output_path, machine)
    print()


if __name__ == "__main__":
    main()
