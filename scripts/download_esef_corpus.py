#!/usr/bin/env python3
"""
download_esef_corpus.py — Download ESEF iXBRL annual reports from filings.xbrl.org
Version: 1.5.2

Membership is no longer a bespoke loader: the firm set comes from the corpus scope via
the shared _scope_common_ops resolver (the SAME resolver the SEC downloader, ingest, and
bench use), or a single firm via --lei. ESEF has no CIK/ticker crosswalk — the identity
key is the LEI (the filings.xbrl.org fxo_id filter IS a LEI-prefix match) — so the
download ledger (the *_full_scope inventory) is keyed on LEI, not CIK.

This downloader keeps the ESEF-native I/O that is genuinely better than the SEC path
(streaming chunked download with a live MB/percent bar, a HEAD size pre-check, API
retry/backoff, stdlib urllib + certifi — no requests dep) and adopts the SEC downloader's
architecture layer (scope resolver, *_full_scope write-back, the _cli_output_ops 4-glyph
vocabulary, hard ScopeError on a bad named scope, the --latest/--years year surface).

API pattern (confirmed 2026-05-18):
  filter=[{"name":"fxo_id","op":"like","val":"<LEI>%"}]
  → all filings for that LEI, sorted by period_end descending.

Usage (via wrapper):
  ais_download_esef                                  # full inventory, latest 1
  ais_download_esef --latest 3                       # 3 most-recent per firm
  ais_download_esef --years 2024                     # fiscal year 2024 only
  ais_download_esef --years 2023 2024                # FY2023 and FY2024
  ais_download_esef --lei 549300NYKK9MWM7GGW15       # single firm by LEI
  ais_download_esef --scope lang_en                  # a named subset (scopes/…)
  ais_download_esef --scope scopes/my_banks_scope.yaml   # bring your own list

Changelog:
- 1.5.1 — Batch-mode hygiene: removed the internal bold banner print from main() (and the
          now-unused _bold helper). The wrapper (ais_download_esef.sh) owns the human-facing
          banner; the .py stays silent when called directly in batch, so it composes in
          pipelines without a stray banner line. Per STD CLI Output (.sh owns banner, .py owns
          version). No logic change. --version still prints the version string.
- 1.5.0 — Architecture-layer port to match download_sec_corpus.py 1.7.0, keeping ESEF's
          superior download I/O + UX:
          (1) Membership via _scope_common_ops — no --scope → discover_full("esef_banks");
              a bare --scope stem → scopes/esef_banks_<stem>_scope.yaml; a value with / or .
              is a literal path. A missing named scope is a HARD ScopeError (AIStudio_882),
              never a silent fallback to a seed list. Retires _load_scope_targets and the
              _FALLBACK_TARGETS hardcode.
          (2) Inventory write-back keyed on LEI (entity_lei cascade): after a run every firm
              with >=1 file on disk is upserted into the *_full_scope inventory, preserving
              hand-corrected fields (lei_corrected / gleif_* / aliases) and stamping
              last_updated. Subset scopes are READ-ONLY. --no-inventory suppresses (test harness).
          (3) Year surface: --latest [N] (most-recent N by period_end; bare = 1; default 1)
              and --years YYYY [YYYY…] (explicit fiscal years by period_end), mutually
              exclusive — building toward multi-year European portfolios (corpus independence).
          (4) Output via _cli_output_ops (the STD 4-glyph vocabulary): a skip is white-✓-on-
              yellow (succeeded, no new fetch), a fresh download ✅, an API/download error
              white-✗-on-red, a no-filing-in-range firm the yellow-✗ recoverable case.
          (5) Atomic publish: each file streams to a .part temp, then Path.replace()s into
              place — an interrupted run leaves a .part orphan (ignored by skip-if-exists),
              never a truncated .xhtml. Re-running resumes, no flag.
          KEPT from 1.4.x: streaming chunked _download_xhtml with the live ↓ MB/percent bar;
          HEAD size pre-check; _api_get retry/backoff; urllib + certifi SSL.
- 1.4.3 — Unified-scope relocation: _SCOPE_DIR → data/corpora/esef_banks/scopes/.
- 1.4.2 — CLI Output STD conformance (pre-_cli_output_ops): N-of-T lines, ▶ trailing …, alignment.
- 1.4.1 — Fixed default --out to data/corpora/esef_banks/uploads/.
- 1.4.0 — AIStudio_838: --scope flag added.

TERMS OF USE — filings.xbrl.org / XBRL International
Data is retrieved from the filings.xbrl.org public ESEF repository operated by XBRL
International. All filings are public regulatory disclosures (ESEF mandate, ESMA). Use is
subject to the repository's terms; this tool identifies itself in the request headers and
rate-limits between requests.
"""

from __future__ import annotations

import argparse
import json
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path

import yaml

# _scope_common_ops + _cli_output_ops are siblings in scripts/ — scripts/ is on sys.path
# when run directly; insert defensively for -m / odd-cwd invocations (mirrors the SEC path).
sys.path.insert(0, str(Path(__file__).resolve().parent))
import _cli_output as cli  # noqa: E402  shared CLI output (glyph vocabulary)
import _scope_common as _scope  # noqa: E402

try:
    import certifi

    _SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    _SSL_CONTEXT = None

VERSION = "1.5.2"
SCRIPT_NAME = "ais_download_esef"
CORPUS = "esef_banks"
API_BASE = "https://filings.xbrl.org"

# Default membership = the corpus inventory (discover_full). No hardcoded firm list:
# the seed (_esef_banks_metadata_seed_ops.yaml) is the source for AUTHORING the inventory,
# not a runtime fallback — a missing inventory is a hard error with a build hint, never a
# silent default (the failure mode the unified resolver exists to kill).
DEFAULT_SCOPE_REL = "data/corpora/esef_banks/esef_banks_full_scope.yaml"

# The iXBRL entity tag the ingest pipeline reads to recognize an ESEF filing's registrant.
# Distinct from the SEC dei:EntityRegistrantName only in namespace prefix — same local name.
ENTITY_TAG_SUFFIX = "EntityRegistrantName"


def _repo_root() -> Path:
    """scripts/ lives one level under the repo root."""
    return Path(__file__).resolve().parent.parent


# ── API (stdlib urllib + certifi; retry/backoff — kept from 1.4.x, the ESEF I/O win) ──
def _api_get(url: str) -> dict:
    """GET JSON from the filings.xbrl.org API with exponential backoff (3 attempts)."""
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={"Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=30, context=_SSL_CONTEXT) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception as e:
            if attempt < 2:
                time.sleep(2**attempt)
                continue
            raise RuntimeError(str(e)) from e
    return {}


def _find_filings(lei: str, *, max_results: int | None, years: set[int] | None) -> list[dict]:
    """Query filings for an LEI via the fxo_id LIKE filter, newest first, and select by
    EXACTLY ONE mode (mirrors the SEC get_filings contract):
      - max_results=N : the N most-recent filings (by period_end) that have a report_url.
      - years={YYYY,…}: every filing whose period_end year is in the set.
    Returns a list of {name, period_end, year, report_url} dicts (newest first)."""
    filt = json.dumps([{"name": "fxo_id", "op": "like", "val": f"{lei}%"}])
    params = urllib.parse.urlencode(
        {
            "filter": filt,
            "include": "entity",
            "sort": "-period_end",
            "page[size]": "50",
        }
    )
    data = _api_get(f"{API_BASE}/api/filings?{params}")

    lei_to_name: dict[str, str] = {}
    for inc in data.get("included", []):
        if inc.get("type") == "entity":
            attrs = inc.get("attributes", {})
            lei_to_name[attrs.get("identifier", "")] = attrs.get("name", "")

    out: list[dict] = []
    for filing in data.get("data", []):
        attrs = filing["attributes"]
        period = attrs.get("period_end", "")
        if not (period and attrs.get("report_url")):
            continue
        year = int(period[:4]) if period[:4].isdigit() else 0
        if years is not None and year not in years:
            continue
        ent_lei = filing["relationships"]["entity"]["links"]["related"].split("/")[-1]
        out.append(
            {
                "name": lei_to_name.get(ent_lei, ent_lei),
                "period_end": period,
                "year": year,
                "report_url": attrs["report_url"],
            }
        )
        if max_results is not None and len(out) >= max_results:
            break
    return out


def _head_size(report_url: str) -> str:
    """HEAD pre-check → a ` (~NN MB)` hint, or '' on failure. Kept from 1.4.x."""
    try:
        head_req = urllib.request.Request(f"{API_BASE}{report_url}", method="HEAD")
        with urllib.request.urlopen(head_req, timeout=10, context=_SSL_CONTEXT) as h:
            file_size = int(h.headers.get("Content-Length", 0))
        return f" (~{file_size / (1024 * 1024):.0f} MB)" if file_size else ""
    except Exception:
        return ""


def _download_xhtml(report_url: str, dest: Path) -> int:
    """Stream the XHTML to dest with a live ↓ MB/percent bar (the ESEF UX win), via an
    atomic .part temp + Path.replace() (the SEC durability win). Returns bytes written."""
    tmp = dest.with_name(dest.name + ".part")
    req = urllib.request.Request(f"{API_BASE}{report_url}", headers={"Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=120, context=_SSL_CONTEXT) as resp:
        content_length = int(resp.headers.get("Content-Length", 0))
        chunks: list[bytes] = []
        downloaded = 0
        while True:
            chunk = resp.read(65536)
            if not chunk:
                break
            chunks.append(chunk)
            downloaded += len(chunk)
            mb = downloaded / (1024 * 1024)
            if content_length:
                pct = downloaded / content_length * 100
                print(
                    f"  ↓ {mb:.1f} / {content_length / (1024 * 1024):.1f} MB ({pct:.0f}%)",
                    end="\r",
                    flush=True,
                )
            else:
                print(f"  ↓ {mb:.1f} MB", end="\r", flush=True)
        print(" " * 60, end="\r")  # clear the live bar before the result glyph line
    data = b"".join(chunks)
    tmp.write_bytes(data)
    tmp.replace(dest)
    return len(data)


# ── Inventory write-back (the *_full_scope ledger) — LEI-keyed (cf. SEC's CIK-keyed) ──
_INVENTORY_HEADER = (
    "# ESEF banks corpus inventory — the running ledger of every firm downloaded.\n"
    "# Maintained by ais_download_esef: rows are upserted by LEI on each download and the\n"
    "# `last_updated` field is stamped per touched row. Hand-edit lei_corrected (and labels)\n"
    "# as needed — row data round-trips across tool writes, so corrections are preserved.\n"
    "# This file is the default download membership and the entity source for\n"
    "# ais_import_entity_kb_ops (GLEIF). Tool-owned local data (gitignored).\n"
)


def _inventory_path() -> Path:
    """The single stemless esef_banks_full_scope inventory to write firms back into — resolved
    by the SAME function the read side uses (_scope.discover_full). Zero → the canonical
    default, created on first write."""
    try:
        return _scope.discover_full(CORPUS)
    except _scope.ScopeError:
        return _repo_root() / DEFAULT_SCOPE_REL


def _read_inventory_header(path: Path) -> str:
    """Preserve an existing file's leading comment block (everything before `entities:`);
    fall back to the canonical header for a fresh inventory."""
    if path.exists():
        head: list[str] = []
        for ln in path.read_text().splitlines(keepends=True):
            if ln.lstrip().startswith("entities:"):
                break
            head.append(ln)
        if any(h.strip() for h in head):
            return "".join(head)
    return _INVENTORY_HEADER


def _upsert_inventory(learned: list[dict]) -> tuple[Path, int, int]:
    """Merge downloaded firms into the inventory, keyed by LEI. Preserves every existing row
    field (especially hand-corrected lei_corrected / enrichment), only sets label (when
    changed/forced), fills an absent xbrl_name, and stamps last_updated. Returns
    (path, n_added, n_touched). Read-only on any subset scope."""
    path = _inventory_path()
    rows: list[dict] = []
    if path.exists():
        doc = yaml.safe_load(path.read_text()) or {}
        rows = doc.get("entities", []) or []
    by_lei = {lei: r for r in rows if (lei := _scope.entity_lei(r))}
    stamp = datetime.now().isoformat(timespec="seconds")
    added = touched = 0
    for f in learned:
        lei = f["lei"]
        if lei in by_lei:
            r = by_lei[lei]
            if f.get("label"):
                r["label"] = f["label"]
            if f.get("xbrl_name") and not r.get("xbrl_name"):
                r["xbrl_name"] = f["xbrl_name"]
            r["last_updated"] = stamp  # lei_corrected/gleif_*/aliases preserved untouched
            touched += 1
        else:
            rows.append(
                {
                    "label": f.get("label", ""),
                    "lei": lei,
                    "xbrl_name": f.get("xbrl_name", ""),
                    "last_updated": stamp,
                }
            )
            by_lei[lei] = rows[-1]
            added += 1
    header = _read_inventory_header(path)
    body = yaml.safe_dump({"entities": rows}, sort_keys=False, allow_unicode=True)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(header + body)
    return path, added, touched


# ── Targets (the firm set for this run) ─────────────────────────────────────────
def _resolve_targets(scope_arg: str | None, lei_arg: str | None) -> list[dict]:
    """Resolve the run's firm set to a list of {label, lei} dicts.
      --lei            → that single firm.
      --scope <stem>   → scopes/esef_banks_<stem>_scope.yaml (a / or . = literal path).
      neither          → the corpus inventory (discover_full).
    A missing/malformed named scope is a hard ScopeError (no silent fallback)."""
    if lei_arg:
        return [{"label": f"LEI_{lei_arg}", "lei": lei_arg.strip()}]
    if scope_arg:
        is_stem = not any(c in scope_arg for c in "/\\.")
        scope_path = (
            _scope.resolve_scope_file(CORPUS, stem=scope_arg)
            if is_stem
            else _scope.resolve_scope_file(CORPUS, path=scope_arg)
        )
        rows = _scope.load_entities(CORPUS, path=str(scope_path))
    else:
        rows = _scope.load_entities(CORPUS)  # discover_full inventory
    targets: list[dict] = []
    for r in rows:
        label = _scope.entity_name(r) or str(r.get("label", "")).strip()
        lei = _scope.entity_lei(r)
        if not label:
            cli.info(f"scope entry missing a name, skipping: {r}")
            continue
        if not lei:
            cli.info(f"{label}: no LEI in scope row — ESEF discovery needs one, skipping")
            continue
        targets.append({"label": label, "lei": lei})
    return targets


def main(argv=None) -> int:
    # No banner here: the wrapper (ais_download_esef.sh) owns the human-facing banner, and
    # this script must stay silent when called directly in batch mode (per STD CLI Output —
    # .sh owns the banner, .py owns the version). --version still prints below.
    p = argparse.ArgumentParser(prog=SCRIPT_NAME, add_help=False)
    mode = p.add_mutually_exclusive_group()
    mode.add_argument("--lei", help="Single firm by LEI")
    mode.add_argument(
        "--scope",
        default=None,
        help="Scope stem (scopes/esef_banks_<stem>_scope.yaml) or a path. "
        "Absence → the corpus inventory (esef_banks_full_scope.yaml).",
    )
    p.add_argument("--out", default=None, help="Output directory")
    year_sel = p.add_mutually_exclusive_group()
    year_sel.add_argument(
        "--latest",
        dest="latest",
        nargs="?",
        const=1,
        type=int,
        default=None,
        metavar="N",
        help="The N most-recent filings per firm by period_end. "
        "Bare --latest = 1. Default when neither flag is given: 1.",
    )
    year_sel.add_argument(
        "--years",
        dest="years",
        nargs="+",
        type=int,
        default=None,
        metavar="YYYY",
        help="Explicit fiscal year(s) by period_end, e.g. --years 2024 2025. "
        "Mutually exclusive with --latest.",
    )
    p.add_argument(
        "--no-inventory",
        dest="no_inventory",
        action="store_true",
        help="Skip the *_full_scope inventory write-back (throwaway/test runs).",
    )
    p.add_argument("--version", action="store_true")
    args = p.parse_args(argv)

    if args.version:
        print(f"{SCRIPT_NAME} v{VERSION}")
        return 0

    if args.years:
        sel_years: set[int] | None = set(args.years)
        latest_n: int | None = None
        sel_label = "fiscal year(s) " + ", ".join(str(y) for y in sorted(sel_years))
    else:
        sel_years = None
        latest_n = args.latest if args.latest is not None else 1
        sel_label = f"the {latest_n} most-recent filing(s)"

    out_dir = (
        Path(args.out).expanduser()
        if args.out
        else _repo_root() / "data/corpora/esef_banks/uploads"
    )
    out_dir.mkdir(parents=True, exist_ok=True)

    cli.section("Preflight")
    if _SSL_CONTEXT is None:
        cli.partial("certifi not installed — SSL verification disabled (fix: pip3 install certifi)")
    try:
        targets = _resolve_targets(args.scope, args.lei)
    except _scope.ScopeError as e:
        cli.fail(f"scope could not be resolved:\n{e}")
        return 2
    if not targets:
        cli.fail("no firms with an LEI in the resolved scope — nothing to download.")
        return 2
    cli.ok(f"{len(targets)} firm(s) resolved · {sel_label} · source {API_BASE}")

    cli.section("Downloading")
    total = len(targets)
    width = len(str(total))
    total_ok = total_fail = total_fresh = 0
    total_bytes = 0
    t0 = time.time()
    learned: list[dict] = []

    for i, t in enumerate(targets, 1):
        label, lei = t["label"], t["lei"]
        print(f"\n[{i:{width}}/{total}] {label}  ({lei})")
        try:
            filings = _find_filings(lei, max_results=latest_n, years=sel_years)
        except Exception as e:
            cli.fail(f"API error: {e}", indent=2)
            total_fail += 1
            continue

        if not filings:
            cli.fail_recover(
                f"{label}: no filing on filings.xbrl.org for {sel_label}. "
                f"Verify the LEI, or widen the year selection.",
                indent=2,
            )
            total_fail += 1
            continue

        if sel_years:
            got = {f["year"] for f in filings}
            missing = sorted(sel_years - got)
            if missing:
                cli.info(
                    f"{label}: no ESEF filing for fiscal year(s) {', '.join(map(str, missing))}",
                    indent=2,
                )

        firm_ok = False
        firm_name = ""
        for filing in filings:
            year = filing["year"] or "?"
            safe_name = label.replace(" ", "_").replace("/", "_")
            dest = out_dir / f"{safe_name}_ESEF_{year}.xhtml"

            if dest.exists():
                cli.partial(f"{dest.name} — already on disk, no new download", indent=2)
                total_ok += 1
                firm_ok = True
                firm_name = firm_name or filing["name"]
                continue

            size_hint = _head_size(filing["report_url"])
            cli.step(f"{filing['name']} FY{year} → {dest.name}{size_hint}", indent=2)
            try:
                nbytes = _download_xhtml(filing["report_url"], dest)
                cli.ok(f"{dest.name} ({nbytes / (1024 * 1024):.1f} MB)", indent=2)
                total_ok += 1
                total_fresh += 1
                total_bytes += nbytes
                firm_ok = True
                firm_name = firm_name or filing["name"]
            except Exception as e:
                cli.fail(f"download failed: {e}", indent=2)
                if dest.with_name(dest.name + ".part").exists():
                    dest.with_name(dest.name + ".part").unlink()
                total_fail += 1
            time.sleep(0.5)

        if firm_ok:
            learned.append({"label": label, "lei": lei, "xbrl_name": firm_name})

    elapsed = time.time() - t0
    mb = total_bytes / 1_048_576
    print(f"\n{'=' * 50}")
    cli.section("Summary")
    print(
        f"  On disk:  {total_ok} filing(s)  ·  {total_fresh} newly fetched, "
        f"{total_ok - total_fresh} already present"
    )
    if total_fail:
        print(f"  Missing:  {total_fail} firm(s)/filing(s) not retrieved")
    if total_fresh and elapsed > 0:
        print(
            f"  Fetched:  {mb:.1f} MB in {elapsed:.0f}s  ·  {mb / elapsed:.2f} MB/s  ·  "
            f"{mb / total_fresh:.2f} MB/file avg"
        )
    else:
        print(f"  Elapsed:  {elapsed:.0f}s (no new downloads)")
    print(f"  Output:   {out_dir}")

    if learned and not args.no_inventory:
        inv_path, n_added, n_touched = _upsert_inventory(learned)
        try:
            rel = inv_path.relative_to(_repo_root())
        except ValueError:
            rel = inv_path
        print(f"  Inventory: {rel}  (+{n_added} new, {n_touched} updated)")

    print(
        "\nNext steps (all in the Terminal — see TUTORIAL Module 3):"
        "\n   1. ais_import_entity_kb --corpus esef_banks --apply    (build the entity KB)"
        "\n   2. ais_import_glossary_kb --source bis_basel           (build the glossary KB)"
        "\n   3. ais_ingest_esef                                     (ingest into AIStudio)"
        "\nThen query the corpus in the AIStudio UI, or benchmark it with ais_bench --corpus esef_banks."
    )
    return 0 if total_fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
