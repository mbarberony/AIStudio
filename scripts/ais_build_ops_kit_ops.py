#!/usr/bin/env python3
"""
ais_build_ops_kit_ops.py — AIStudio Operator Install Kit Builder
Version: 2.1.0
2.1.0: bootstrap path moves to meta/reference/bootstraps/; matches both urCrew (historical)
       and urc (post-2026-05-08) prefixes. INFO File Guide globs removed (type retired Batch C 2026-05-08;
       files renamed to REF). SESS path updated to meta/sessions/ (cross-domain, Batch C). Stale exclude
       for meta/urCrew/ removed (dir deleted Batch A).
2.0.0: rewrite from shell to Python; manifest-driven + filesystem-walk;
       self-maintaining — new operator commands auto-included via manifest

Called by: ais_build_ops_kit_ops.sh (thin wrapper)
Output:    ~/Downloads/AIStudio - Operator Kit - YYYY-MM-DD - HHMM.zip

Selection logic:
  Layer 1 — Manifest: all install:operator entries
  Layer 2 — Meta filesystem walk: STDs, REFs, THINKs, seed files, etc.
  Layer 3 — Root operator scripts not in manifest
  Bootstrap: install_ops, bundle_manifest.yaml, QUICKSTART_OPS.md

Explicit excludes:
  meta/job_hunting/          — personal, iCloud covers this
  meta/bundles/ > last 3     — session history, keep last 3
  meta/packets/ > last 3     — session history, keep last 3
  meta/sessions > last 3 per domain (cross-domain dir post-Batch-C 2026-05-08)
  seed_data/ PDFs            — large, git-tracked
  sec_10k/sec_10k_test_files/ — huge
  *.DS_Store
  epave files (_session_summary.md, session_summary.md, help_manifest_backup.yaml)
  STD - Resume Development - * (superseded)
  (meta/urCrew/ deleted in Batch A 2026-05-08; exclusion no longer needed)
"""

from __future__ import annotations  # isort: skip_file

import argparse
import fnmatch
import os
import re
import sys
import zipfile
from datetime import datetime
from pathlib import Path


# ── Constants ─────────────────────────────────────────────────────────────────

VERSION = "2.0.0"
SCRIPT_NAME = "ais_build_ops_kit_ops"

# How many recent files to keep for session-specific categories
KEEP_LAST_N = 3

# Explicit skip patterns (relative to REPO)
SKIP_PATTERNS = [
    "meta/manual_install/test/*.zip",
    "meta/manual_install/test/*.pdf",
    "meta/manual_install/test/ais_clean_install.sh",  # old name, will be ais_clean_install_ops.sh post-558
    "meta/job_hunting/**",
    "meta/_special_corpus_seed_info/demo/seed_data/**",
    "meta/_special_corpus_seed_info/sec_10k/sec_10k_test_files/**",
    "meta/_session_summary.md",
    "meta/session_summary.md",
    "meta/help_manifest_backup.yaml",
    "meta/standards/STD - Resume Development - *.md",
    "**/.DS_Store",
    "**/__pycache__/**",
    "**/*.pyc",
]

# Versioned files: keep only the latest per glob pattern
GLOB_LATEST_PATTERNS = [
    # Bootstrap — moved to bootstraps/ subdir 2026-05-08; pattern matches both urCrew (historical)
    # and urc (post-rename) prefixes, _glob_latest takes the most recent which is the urc 2026-05-08 file
    "meta/reference/bootstraps/REF - * - New Thread Bootstrap - *.md",
    # File Guides — renamed INFO -> REF in Batch C (2026-05-08); INFO entries no longer match anything
    "meta/reference/REF - AIStudio - File Guide - [0-9]*.md",
    "meta/reference/REF - AIStudio - File Guide - OPS - *.md",
    "meta/reference/REF - JOB - File Guide - *.md",
    "meta/standards/STD - AIStudio - CLI Output - *.md",
    "meta/standards/STD - AIStudio - Command Development*.md",
    "meta/standards/STD - General - Naming Conventions - *.md",
    "meta/standards/STD - JOB - Application Methodology - *.md",
    "meta/standards/STD - JOB - Resume Development - [0-9]*.md",
    "meta/urc/think/THINK - urCrew - Master - Governing*.md",
    "meta/urc/think/THINK - urCrew - Master - Operational Rules*.md",
]

# Session files: keep last N sorted by filename (date-encoded names)
GLOB_LAST_N_PATTERNS = {
    # SESS files — migrated to cross-domain meta/sessions/ in Batch C (2026-05-08)
    "meta/sessions/SESS - AIS - *.md": KEEP_LAST_N,
    "meta/sessions/SESS - JOB - *.md": KEEP_LAST_N,
    "meta/sessions/SESS - KRR - *.md": KEEP_LAST_N,
    # Legacy AIS bundles + packets — pending migration to meta/ais/{bundles,packets}/ (Batch F4)
    "meta/bundles/BUNDLE - AIStudio - *.zip": KEEP_LAST_N,
    "meta/packets/PACKET - AIStudio - *.md": KEEP_LAST_N,
}


# ── Helpers ───────────────────────────────────────────────────────────────────

def _should_skip(rel_path: str) -> bool:
    """Return True if this path matches any skip pattern."""
    for pattern in SKIP_PATTERNS:
        if fnmatch.fnmatch(rel_path, pattern):
            return True
        # Also check just the filename
        clean = pattern.replace("**/", "").lstrip("*")
        if fnmatch.fnmatch(Path(rel_path).name, Path(pattern).name) and "/" not in clean:
            return True
    return False


def _glob_latest(repo: Path, pattern: str) -> list[Path]:
    """Resolve a glob pattern and return only the most recent match."""
    matches = sorted(repo.glob(pattern))
    if not matches:
        return []
    return [matches[-1]]  # Last alphabetically = latest date


def _is_new_naming(p: Path) -> bool:
    """Return True if file uses new naming convention: date YYYY-MM-DD before time HHMM.

    New format: BUNDLE - AIStudio - Session - 2026-04-27 - 1400.zip
    Old format: BUNDLE - AIStudio - Session - 0007 - 2026-04-11.zip
    Filter rule: date must appear as YYYY-MM-DD - HHMM (date immediately before 4-digit time).
    """
    return bool(re.search(r"20\d\d-\d\d-\d\d - \d{4}", p.name))


def _date_key(p: Path) -> str:
    """Extract sortable YYYY-MM-DD-HHMM from filename for new-format files."""
    m = re.search(r"(20\d\d-\d\d-\d\d) - (\d{4})", p.name)
    if m:
        return m.group(1) + "-" + m.group(2)
    return "0000-00-00-0000"


def _glob_last_n(repo: Path, pattern: str, n: int) -> list[Path]:
    """Resolve pattern, filter to new naming convention only, return last N by date."""
    all_matches = list(repo.glob(pattern))
    # Only include files with new naming convention (date - time format)
    new_format = [f for f in all_matches if _is_new_naming(f)]
    sorted_matches = sorted(new_format, key=_date_key)
    return sorted_matches[-n:] if len(sorted_matches) >= n else sorted_matches


def _read_manifest(repo: Path) -> dict:
    """Read bundle_manifest.yaml and return parsed content."""
    try:
        import yaml
    except ImportError:
        print("❌ pyyaml not installed — run: pip3 install pyyaml --break-system-packages")
        sys.exit(1)

    manifest_path = repo / "meta" / "bundle_manifest.yaml"
    if not manifest_path.exists():
        print(f"❌ manifest not found: {manifest_path}")
        sys.exit(1)

    with open(manifest_path) as f:
        return yaml.safe_load(f)


def _collect_manifest_operator_files(repo: Path, manifest: dict) -> list[Path]:
    """Collect all install:operator files from the manifest."""
    files = []
    for entry in manifest.get("entries", []):
        if entry.get("install") != "operator":
            continue
        if entry.get("status") == "deprecated":
            continue
        t = entry.get("type", "static")
        path = entry.get("path", "")
        if t == "static":
            p = repo / path
            if p.exists():
                files.append(p)
        elif t == "glob_latest":
            g = entry.get("glob", "")
            if g:
                matches = sorted((repo / "meta").glob(g))
                if not matches:
                    matches = sorted(repo.glob(g))
                if matches:
                    files.append(matches[-1])
    return files


def _collect_meta_files(repo: Path) -> list[Path]:
    """Walk meta/ and collect files per the inclusion rules."""
    files = []
    seen_globs: set[str] = set()

    # 1. Glob-latest patterns (versioned files — newest only)
    for pattern in GLOB_LATEST_PATTERNS:
        latest = _glob_latest(repo, pattern)
        for f in latest:
            rel = str(f.relative_to(repo))
            if not _should_skip(rel):
                files.append(f)
                seen_globs.add(rel)

    # 2. Last-N patterns (session files)
    for pattern, n in GLOB_LAST_N_PATTERNS.items():
        for f in _glob_last_n(repo, pattern, n):
            rel = str(f.relative_to(repo))
            if not _should_skip(rel) and rel not in seen_globs:
                files.append(f)
                seen_globs.add(rel)

    # 3. Walk all of meta/ for remaining files
    meta_dir = repo / "meta"
    for root, dirs, filenames in os.walk(meta_dir):
        root_path = Path(root)

        # Skip entire directories
        dirs[:] = [
            d for d in dirs
            if not _should_skip(str((root_path / d).relative_to(repo)) + "/")
            and d not in {"job_hunting", "__pycache__"}
        ]

        for filename in filenames:
            if filename.startswith("."):
                continue
            fpath = root_path / filename
            rel = str(fpath.relative_to(repo))

            # Skip if already added by glob rules
            if rel in seen_globs:
                continue

            # Skip if matches skip patterns
            if _should_skip(rel):
                continue

            # Skip if this is a versioned file handled by glob_latest
            # (older versions of files we only want latest of)
            skip_older = False
            for pattern in GLOB_LATEST_PATTERNS:
                pattern_dir = str(Path(pattern).parent)
                if (str(root_path.relative_to(repo)) == pattern_dir
                        and fnmatch.fnmatch(filename, Path(pattern).name)):
                    skip_older = True
                    break
            if skip_older:
                continue

            files.append(fpath)
            seen_globs.add(rel)

    return files


def _collect_root_operator_scripts(repo: Path) -> list[Path]:
    """Collect root-level operator scripts not captured by manifest."""
    files = []
    for pattern in ["ais_*_ops*", "_ais_*"]:
        for f in repo.glob(pattern):
            if f.is_file() and not f.name.startswith("."):
                files.append(f)
    return files


def _collect_bootstrap_files(repo: Path) -> list[Path]:
    """Always-included bootstrap files."""
    candidates = [
        repo / "install_ops",
        repo / "meta" / "bundle_manifest.yaml",
        repo / "meta" / "manual_install" / "ops" / "QUICKSTART_OPS.md",
    ]
    return [f for f in candidates if f.exists()]


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        prog=SCRIPT_NAME,
        description="Build AIStudio operator install kit zip"
    )
    parser.add_argument("--version", action="store_true", help="Show version and exit")
    parser.add_argument("--dry-run", action="store_true", help="List files without building zip")
    parser.add_argument("--repo-root", default=None, help="Override repo root path")
    args = parser.parse_args()

    if args.version:
        print(f"{SCRIPT_NAME} v{VERSION}")
        return

    # Resolve repo root
    repo = Path(args.repo_root) if args.repo_root else Path(__file__).parent.parent
    if not (repo / "meta" / "bundle_manifest.yaml").exists():
        print(f"❌ Not a valid AIStudio repo: {repo}")
        sys.exit(1)

    print(f"\033[1m[{SCRIPT_NAME} v{VERSION} — AIStudio Operator Install Kit Builder]\033[0m")
    print(f"  Repo: {repo}")

    if args.dry_run:
        print("  Mode: DRY RUN — no zip will be created")
    print()

    # ── Collect files ─────────────────────────────────────────────────────────
    manifest = _read_manifest(repo)

    print("── Collecting files ─────────────────────────────────────────")

    bootstrap  = _collect_bootstrap_files(repo)
    op_scripts = _collect_manifest_operator_files(repo, manifest)
    root_ops   = _collect_root_operator_scripts(repo)
    meta_files = _collect_meta_files(repo)

    # Deduplicate
    seen: set[Path] = set()
    all_files: list[Path] = []
    for f in bootstrap + op_scripts + root_ops + meta_files:
        if f not in seen:
            seen.add(f)
            all_files.append(f)

    # Sort by relative path for readability
    all_files.sort(key=lambda f: str(f.relative_to(repo)))

    # ── Preflight ─────────────────────────────────────────────────────────────
    missing = [f for f in all_files if not f.exists()]
    if missing:
        print(f"❌ {len(missing)} file(s) not found:")
        for f in missing:
            print(f"  {f.relative_to(repo)}")
        sys.exit(1)

    # ── Report ────────────────────────────────────────────────────────────────
    categories = {
        "Bootstrap":          [f for f in all_files if f.name in {"install_ops", "bundle_manifest.yaml", "QUICKSTART_OPS.md"}],
        "Operator commands":  [f for f in all_files if f.parent == repo and f.name not in {"install_ops"}],
        "meta/standards":     [f for f in all_files if "meta/standards" in str(f)],
        "meta/reference":     [f for f in all_files if "meta/reference" in str(f)],
        "meta/urc/think":     [f for f in all_files if "meta/urc/think" in str(f)],
        "meta/sessions":      [f for f in all_files if "meta/sessions" in str(f)],
        "meta/bundles":       [f for f in all_files if "meta/bundles" in str(f)],
        "meta/packets":       [f for f in all_files if "meta/packets" in str(f)],
        "meta/seed_info":     [f for f in all_files if "_special_corpus_seed_info" in str(f)],
        "meta/other":         [f for f in all_files if "meta/" in str(f.relative_to(repo))
                               and not any(x in str(f) for x in [
                                   "standards", "reference", "urc/think",
                                   "sessions", "bundles", "packets",
                                   "_special_corpus_seed_info"
                               ])],
        "scripts/":           [f for f in all_files if "scripts/" in str(f.relative_to(repo))],
    }

    total_size = sum(f.stat().st_size for f in all_files)

    print(f"  ✅ {len(all_files)} files, {total_size / 1024:.0f} KB total")
    print()

    for cat, cat_files in categories.items():
        if cat_files:
            print(f"  {cat}: {len(cat_files)} files")

    if args.dry_run:
        print()
        print("── File list ────────────────────────────────────────────────")
        for f in all_files:
            size_kb = f.stat().st_size / 1024
            print(f"  {str(f.relative_to(repo)):<70} [{size_kb:.0f}KB]")
        print()
        print(f"Total: {len(all_files)} files, {total_size / 1024:.0f} KB")
        print("(Dry run — no zip created)")
        return

    # ── Build zip ─────────────────────────────────────────────────────────────
    date_str = datetime.now().strftime("%Y-%m-%d")
    time_str = datetime.now().strftime("%H%M")
    zip_name = f"AIStudio - Operator Kit - {date_str} - {time_str}.zip"
    zip_path = Path.home() / "Downloads" / zip_name

    print()
    print("── Building zip ─────────────────────────────────────────────")

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in all_files:
            arcname = str(f.relative_to(repo))
            zf.write(f, arcname)

    zip_size = zip_path.stat().st_size / 1024
    print(f"  ✅ {len(all_files)} files → {zip_name}")
    print(f"  📦 {zip_path} ({zip_size:.0f} KB)")
    print()
    print("── Summary ──────────────────────────────────────────────────")
    print(f"  ✅ Operator kit ready: {zip_name}")
    print()
    print("Next steps:")
    print("  1. Email the zip to yourself")
    print("  2. On the target machine: follow meta/manual_install/ops/QUICKSTART_OPS.md")
    print("  3. Verify: ais_install_ops --verify && ais_test_ops && ais_bench")


if __name__ == "__main__":
    main()
