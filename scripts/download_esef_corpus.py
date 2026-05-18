#!/usr/bin/env python3
"""
download_esef_corpus.py — Download ESEF iXBRL annual reports from filings.xbrl.org
Version: 1.3.0

Queries filings.xbrl.org API using fxo_id LIKE filter (LEI prefix match) —
the only server-side filter that reliably returns filings for a specific entity.
Downloads the primary XHTML report file for the most recent filing per firm.

API pattern confirmed 2026-05-18:
  filter=[{"name":"fxo_id","op":"like","val":"<LEI>%"}]
  → returns all filings for that LEI, sorted by period_end descending

Usage (via wrapper):
  ais_download_esef [--out DIR] [--period-start YYYY] [--period-end YYYY]
"""

import argparse
import json
import ssl
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

import yaml

try:
    import certifi
    _SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    _SSL_CONTEXT = None

VERSION = "1.3.0"
SCRIPT_NAME = "ais_download_esef"
API_BASE = "https://filings.xbrl.org"

# ── Target firms — loaded from operator seed YAML, fallback to hardcoded ─────
# Edit meta/_special_corpus_seed_info/esef_banks/_esef_banks_metadata_seed_ops.yaml
# to add/remove firms or correct LEIs. Script reads that file at runtime.

_SEED_YAML = Path(__file__).parent.parent / "meta/_special_corpus_seed_info/esef_banks/_esef_banks_metadata_seed_ops.yaml"

_FALLBACK_TARGETS = [
    {"lei": "549300NYKK9MWM7GGW15", "short": "ING_Group"},
    {"lei": "R0MUWSFPU8MPRO8K5P83", "short": "BNP_Paribas"},
    {"lei": "7LTWFZYICNSX8D621K86", "short": "Deutsche_Bank"},
    {"lei": "5493006QMFDDMYWIAM13", "short": "Santander"},
    {"lei": "O2RNE8IBXP4R0TD8PU41", "short": "Societe_Generale"},
    {"lei": "549300TRUWO2CD2G5692", "short": "UniCredit"},
    {"lei": "BFXS5XCH7N0Y05NIXW11", "short": "ABN_AMRO"},
    {"lei": "213800X3Q9LSAKRUWY91", "short": "KBC_Group"},
    {"lei": "969500TJ5KRTCJQWXH05", "short": "Credit_Agricole"},
    {"lei": "529900ODI3047E2LIV03", "short": "Nordea"},
]


def _load_targets() -> list[dict]:
    """Load esef_targets from operator seed YAML; fall back to hardcoded list."""
    if _SEED_YAML.exists():
        with open(_SEED_YAML) as f:
            meta = yaml.safe_load(f)
        targets = meta.get("esef_targets", [])
        if targets:
            return [{"lei": t["lei"], "short": t["short"]} for t in targets]
    return _FALLBACK_TARGETS


TARGET_FIRMS = _load_targets()


def _bold(text: str) -> str:
    return f"\033[1m{text}\033[0m"


def _api_get(url: str) -> dict:
    """GET JSON from API with retry."""
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={"Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=30, context=_SSL_CONTEXT) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception as e:
            if attempt < 2:
                time.sleep(2 ** attempt)
                continue
            raise RuntimeError(str(e)) from e


def _find_best_filing(lei: str, period_start: int, period_end: int) -> dict | None:
    """
    Query filings using fxo_id LIKE filter (LEI prefix match).
    Returns most recent filing with report_url within period range.
    Confirmed working 2026-05-18: filter=[{"name":"fxo_id","op":"like","val":"<LEI>%"}]
    """
    filt = json.dumps([{"name": "fxo_id", "op": "like", "val": f"{lei}%"}])
    params = urllib.parse.urlencode({
        "filter": filt,
        "include": "entity",
        "sort": "-period_end",
        "page[size]": "10",
    })
    url = f"{API_BASE}/api/filings?{params}"
    data = _api_get(url)

    # Build LEI → name map
    lei_to_name: dict[str, str] = {}
    for inc in data.get("included", []):
        if inc.get("type") == "entity":
            lei_to_name[inc["attributes"].get("identifier", "")] = inc["attributes"].get("name", "")

    for filing in data.get("data", []):
        period = filing["attributes"].get("period_end", "")
        year = int(period[:4]) if period else 0
        if period_start <= year <= period_end and filing["attributes"].get("report_url"):
            entity_lei = filing["relationships"]["entity"]["links"]["related"].split("/")[-1]
            return {
                "name": lei_to_name.get(entity_lei, entity_lei),
                "period_end": period,
                "report_url": filing["attributes"]["report_url"],
            }
    return None


def _download_xhtml(report_url: str, dest: Path) -> int:
    """Download XHTML file with progress dots, return size in bytes."""
    req = urllib.request.Request(
        f"{API_BASE}{report_url}", headers={"Accept": "*/*"}
    )
    with urllib.request.urlopen(req, timeout=120, context=_SSL_CONTEXT) as resp:
        content_length = int(resp.headers.get("Content-Length", 0))
        chunks = []
        downloaded = 0
        chunk_size = 65536
        while True:
            chunk = resp.read(chunk_size)
            if not chunk:
                break
            chunks.append(chunk)
            downloaded += len(chunk)
            if content_length:
                pct = downloaded / content_length * 100
                print(f"  ↓ {downloaded / (1024*1024):.1f} / {content_length / (1024*1024):.1f} MB ({pct:.0f}%)", end="\r", flush=True)
            else:
                print(f"  ↓ {downloaded / (1024*1024):.1f} MB", end="\r", flush=True)
        print(" " * 60, end="\r")  # clear progress line
    data = b"".join(chunks)
    dest.write_bytes(data)
    return len(data)


def main(argv=None) -> int:
    print(_bold(f"[{SCRIPT_NAME} v{VERSION} — Download ESEF annual reports from filings.xbrl.org]"))

    p = argparse.ArgumentParser(prog=SCRIPT_NAME, add_help=False)
    p.add_argument("--out", default=None)
    p.add_argument("--period-start", default="2022")
    p.add_argument("--period-end", default="2025")
    p.add_argument("--version", action="store_true")
    args = p.parse_args(argv)

    if args.version:
        print(f"{SCRIPT_NAME} v{VERSION}")
        return 0

    out_dir = Path(args.out).expanduser() if args.out else Path.cwd()
    out_dir.mkdir(parents=True, exist_ok=True)

    print("--- Preflight")
    if _SSL_CONTEXT is None:
        print("  ⚠ certifi not installed — SSL verification disabled")
        print("  · Fix: pip install certifi")
    src = "seed YAML" if _SEED_YAML.exists() else "fallback hardcoded list"
    print(f"✅ Output directory ready: {out_dir}")
    print(f"· Period range : {args.period_start} → {args.period_end}")
    print(f"· Target firms : {len(TARGET_FIRMS)} (from {src})")
    print(f"· Source       : {API_BASE}")
    print("--- Downloading")

    period_start = int(args.period_start[:4])
    period_end = int(args.period_end[:4])
    downloaded = 0
    failed = 0
    skipped = 0
    total = len(TARGET_FIRMS)
    width = len(str(total))

    for i, firm in enumerate(TARGET_FIRMS, 1):
        lei = firm["lei"]
        short = firm["short"]
        print(f"[searching] {i:{width}} of {total} · {short}")

        try:
            filing = _find_best_filing(lei, period_start, period_end)
        except Exception as e:
            print(f"  ❌ API error: {e}")
            failed += 1
            continue

        if not filing:
            print(f"  ⚠ No filing found for {short} in {period_start}–{period_end}")
            skipped += 1
            continue

        year = filing["period_end"][:4]
        fname = f"{short}_ESEF_{year}.xhtml"
        dest = out_dir / fname

        if dest.exists():
            print(f"  ℹ Already exists: {fname} — skipping")
            skipped += 1
            continue

        # HEAD request to get file size before downloading
        try:
            head_req = urllib.request.Request(
                f"{API_BASE}{filing['report_url']}", method="HEAD"
            )
            with urllib.request.urlopen(head_req, timeout=10, context=_SSL_CONTEXT) as h:
                file_size = int(h.headers.get("Content-Length", 0))
            size_hint = f" (~{file_size / (1024*1024):.0f} MB)" if file_size else ""
        except Exception:
            size_hint = ""

        print(f"  ▶ {filing['name']} FY{year} → {fname}{size_hint}")
        try:
            size = _download_xhtml(filing["report_url"], dest)
            print(f"  ✅ {fname} ({size / (1024 * 1024):.1f} MB)")
            downloaded += 1
        except Exception as e:
            print(f"  ❌ Download failed: {e}")
            if dest.exists():
                dest.unlink()
            failed += 1

        time.sleep(0.5)

    print("--- Summary")
    status = "✅" if failed == 0 else ("⚠" if downloaded > 0 else "❌")
    print(f"{status} {downloaded} filings downloaded · {skipped} skipped · {failed} failed")
    print(f"· {len(list(out_dir.glob('*.xhtml')))} total .xhtml files in {out_dir}")
    if downloaded > 0:
        print("· Next step: create corpus \'esef_banks\' in AIStudio UI, then ingest via Upload")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
