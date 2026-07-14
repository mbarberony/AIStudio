#!/usr/bin/env zsh
# ais_ingest_sec_10k.sh — Ingest the SEC 10-K corpus into AIStudio
# Version: 1.5.0
# Changelog:
#   1.5.0 — AIStudio_1019: export PYTHONUNBUFFERED=1 (after the source guard) so a tee'd ingest
#           streams live progress without the caller prepending it. No other behavior change.
#   1.4.5 — AIS_17 (backend-kill observability, 2026-06-14): preflight now records the PID serving
#           the API port (lsof -nP -iTCP:<port> -sTCP:LISTEN), so a backend that dies mid-ingest
#           isn't silent — you can see what held the port and confirm a restart's new PID. Pairs
#           with the api.py shutdown-log handler (v1.10.2).
#   1.4.4 — AIStudio_908 (Manuel, 2026-06-14): removed the brittle firm count. The Setup banner
#           is now just "· Corpus : sec_10k" (was "(25 firms × 5 filings target)"), and the heredoc
#           corpus_metadata short_description/description/content_summary drop the hardcoded
#           "125 filings / 25 firms" (the count is on-demand-variable — 20 base + adds). NOTE: the
#           LIVE data/corpora/sec_10k/corpus_metadata.yaml still carries the old count until
#           regenerated or hand-edited — fix there too (the stale content_summary, MD_3).
#   1.4.3 — AIStudio_912 (Manuel CLI signature change, 2026-06-14): --files now documents
#           OR-matched substring/regex patterns (matching in engine pipeline.py v1.8.32). Updated
#           usage line, --files option help, the parse comment, and the "To ingest some" footer
#           hint. No shell-side behavior change — the pattern string still passes through to the
#           engine's --files.
#   1.4.2 — AIStudio_909 (Manuel flag A, 2026-06-14): selective-mode count fix. The
#           "▶ Ingesting N filings" line and the time estimate now use INGEST_COUNT — the
#           number of files in --files when selective, else the whole corpus — instead of the
#           full-corpus $FILE_COUNT. (Preflight "✅ N filings ready" still counts all on disk.)
#           Fixes "Ingesting 101 filings · ~27 min" when only 1 file was selected.
#   1.4.1 — CLI-output polish (Manuel flags, 2026-06-13): (a) the "already indexed"
#           incremental-mode line now uses a `·` bullet, not `ℹ` (CLI Output STD v2.4.0:
#           ℹ retired → ·). (b) Dropped the unconditional blank line before "--- Setup" so
#           that line butts directly against the section (STD: no leading blank before a
#           --- header). (c) Removed the stale hardcoded "(pipeline.py v1.7.0)" from the
#           Normalizer banner — a shell echo can't track the engine's real version, so the
#           parenthetical is gone rather than re-hardcoded (AIStudio_909c).
#   1.4.0 — ESEF v1.1.0 parity + selective ingest. (a) Incremental-mode awareness:
#           Qdrant chunk-count check → "already indexed: N chunks — incremental" vs
#           "clean ingest" vs "--force: wiping". (b) Total-bytes/MB accounting in
#           preflight. (c) Metadata-driven time estimate: reads avg_seconds_per_file
#           (tier 2) with a < 2s/file sanity floor that rejects skip-contaminated
#           averages, falling back to a 60s/file seed (tier 3); shows estimate source.
#           (d) New --files <a,b,c> passthrough → engine --files (selective ingest:
#           only those re-embedded, others untouched). (e) --verbose passthrough.
#           (f) Hoisted arg parsing above preflight. (g) Next-steps branches on exit code.
#   1.3.4 — Move --- Important above --- Ingesting per STD §8.
#   1.3.4 — Fix zsh "unmatched quote" error: use ${FORCE_FLAG:+--force} expansion.
#   1.3.3 — STD §8 minimal compliance: wording fixes, --- Important section,
#           ▶ line with · separators + ellipsis, --force flag, --- Next steps.
#   1.3.1 — Wrap ingest with caffeinate -i to prevent macOS sleep during long runs.
#           Updated "leave terminal open" message to clarify "minimized but not closed."
#           Hardware-aware time estimate: Pro vs Air.
#   1.3.0 — Questions YAML v2.0.0: 8 retail-bank-trends questions (cross-firm + temporal)
#   1.2.4 — Heredoc YAML fixes for sec_10k corpus_metadata (25 firms x 5 filings target)
#   1.2.2 — Initial 1.2.x baseline
#   1.2.0 — auto-generate sec_10k_corpus_metadata.yaml on first run (schema v1.0)
#   1.1.0 — auto-generate sec_10k_questions.yaml on first run
# Ingests all .htm files from data/corpora/sec_10k/uploads/ into the sec_10k corpus.
# Requires: AIStudio backend running (ais_start) and files downloaded (ais_download_sec_10k)


# ── Source guard: this script must be executed, not sourced ──────────────────
[[ "$ZSH_EVAL_CONTEXT" == *:file* ]] && { echo "❌ Do not source this script — execute it directly."; return 1; }

# AIStudio_1019: line-buffer Python so a tee'd ingest shows live progress. Harmless if already set.
export PYTHONUNBUFFERED=1

VERSION="1.5.0"

SCRIPT_NAME="ais_ingest_sec_10k"
REPO="${0:A:h}"
HELP_FILE="$REPO/ais_command_help.txt"

_show_help() {
    if [[ -f "$HELP_FILE" ]]; then
        awk "/^## $SCRIPT_NAME$/,/^---$/" "$HELP_FILE" | grep -v "^---$" | grep -v "^## "
    else
        echo "$SCRIPT_NAME v$VERSION — Ingest SEC 10-K corpus into AIStudio"
        echo ""
        echo "Usage: $SCRIPT_NAME [--force] [--files <pat1,pat2,...>] [--verbose] [--help] [--version]"
        echo ""
        echo "Options:"
        echo "  --force            Full rebuild — wipe collection, re-ingest all files"
        echo "                     Default (no --force): incremental — only new/changed files"
        echo "  --files <list>     Ingest ONLY files matching these comma-separated patterns (always"
        echo "                     re-embedded). Each pattern is OR-matched against the filename,"
        echo "                     case-insensitively: a literal substring, or a regex if it contains"
        echo "                     regex metacharacters. e.g. --files BlackRock  or  --files 'JPM.*2025,Citi'."
        echo "                     Every non-matching file in uploads/ (indexed or parked) is left untouched"
        echo "  --verbose          Print full JSON result payload after summary"
        echo "  --help             Show this help and exit"
        echo "  --version          Print version and exit"
        echo ""
        echo "Run from: ~/Developer/AIStudio"
    fi
}

if [[ "$1" == "--help" ]]; then _show_help; exit 0; fi
if [[ "$1" == "--version" ]]; then echo "$SCRIPT_NAME v$VERSION"; exit 0; fi

API="http://localhost:8000"
UPLOADS="$REPO/data/corpora/sec_10k/uploads"
BENCH_DIR="$REPO/benchmarks/sec_10k"
CORPUS_DIR="$REPO/data/corpora/sec_10k"
METADATA_FILE="$CORPUS_DIR/sec_10k_corpus_metadata.yaml"

# ── Argument parsing (hoisted so preflight + estimate can see the mode) ────────
FORCE_FLAG=""
VERBOSE_FLAG=""
FILES_ARG=""
while [[ $# -gt 0 ]]; do
    case "$1" in
        --force)   FORCE_FLAG="--force"; shift ;;
        --verbose) VERBOSE_FLAG="--verbose"; shift ;;
        --files)   FILES_ARG="$2"; shift 2 ;;   # comma-separated patterns (substring/regex, OR) → selective ingest
        *) echo "❌ Unknown flag: $1"; echo "· Run: $SCRIPT_NAME --help"; exit 1 ;;
    esac
done

printf "\033[1m[ais_ingest_sec_10k v$VERSION — Ingest SEC 10-K corpus]\033[0m\n"

# --- Preflight
echo "--- Preflight"

if [[ ! -d "$UPLOADS" ]]; then
    echo "❌ Source directory not found: data/corpora/sec_10k/uploads/"
    echo "· Run: ais_download_sec_10k"
    exit 1
fi

FILE_COUNT=$(ls "$UPLOADS"/*.htm 2>/dev/null | wc -l | tr -d ' ')
if [[ "$FILE_COUNT" -eq 0 ]]; then
    echo "❌ No .htm files found in data/corpora/sec_10k/uploads/"
    echo "· Run: ais_download_sec_10k"
    exit 1
fi

# Total size (macOS stat) — matches ESEF accounting
TOTAL_BYTES=0
while IFS= read -r f; do
    sz=$(stat -f%z "$f" 2>/dev/null || echo 0)
    TOTAL_BYTES=$(( TOTAL_BYTES + sz ))
done < <(find "$UPLOADS" -maxdepth 1 -name "*.htm")
TOTAL_MB=$(echo "scale=1; $TOTAL_BYTES / 1048576" | bc)
echo "✅ $FILE_COUNT filings ready · ${TOTAL_MB} MB"

if ! curl -sf "$API/health" > /dev/null 2>&1; then
    echo "❌ Backend not reachable at $API"
    echo "· Run: ais_start"
    exit 1
fi
echo "✅ Backend healthy."
# AIS_17 — backend-kill observability: record which PID is serving the API port now, so if the
# backend dies during a long ingest you can see (in scrollback) what was here and confirm a
# restart brought up a different PID. lsof: -n no DNS, -P numeric ports, -sTCP:LISTEN listener only, -t PID-only.
_PORT="${API##*:}"; _PORT="${_PORT%%/*}"
_HOLDER=$(lsof -nP -iTCP:"${_PORT}" -sTCP:LISTEN -t 2>/dev/null | head -1)
echo "· Backend PID on :${_PORT}: ${_HOLDER:-unknown (health OK but no listener PID found)}"

# Qdrant collection check — info only, no gate (mirrors ESEF v1.1.0)
QDRANT="http://localhost:6333"
COLLECTION="aistudio_sec_10k"
QDRANT_RESPONSE=$(curl -sf "$QDRANT/collections/$COLLECTION" 2>/dev/null)
EXISTING_CHUNKS=""
if [[ -n "$QDRANT_RESPONSE" ]]; then
    EXISTING_CHUNKS=$(echo "$QDRANT_RESPONSE" | python3 -c \
        "import sys,json; d=json.load(sys.stdin); print(d.get('result',{}).get('points_count','?'))" \
        2>/dev/null)
fi
if [[ -n "$EXISTING_CHUNKS" && "$EXISTING_CHUNKS" != "?" && "$EXISTING_CHUNKS" -gt 0 ]]; then
    if [[ "$FORCE_FLAG" == "--force" ]]; then
        echo "⚠ --force: wiping existing collection ($EXISTING_CHUNKS chunks) and re-ingesting all files."
    else
        echo "· Corpus 'sec_10k' already indexed: ${EXISTING_CHUNKS} chunks — incremental ingest (new/changed files only)."
    fi
else
    echo "✅ No existing Qdrant collection — clean ingest."
fi

# --- Setup
echo "--- Setup"
echo "· Corpus     : sec_10k"
echo "· Chunk size : 1200 chars · Overlap: 200 chars"
echo "· Embed model: nomic-embed-text"
echo "· Normalizer : Document-Head Extraction + Temporal Context Injection"
echo "· Source     : $UPLOADS"

# Create benchmarks/sec_10k/ on first run
if [[ ! -d "$BENCH_DIR" ]]; then
    mkdir -p "$BENCH_DIR/reports"
    echo "✅ Created benchmarks/sec_10k/ with reports/ subfolder."
fi

# Write sec_10k_questions.yaml on first run
QUESTIONS_FILE="$BENCH_DIR/sec_10k_questions.yaml"
if [[ ! -f "$QUESTIONS_FILE" ]]; then
    cat > "$QUESTIONS_FILE" << 'EOF'
# AIStudio — SEC 10-K Corpus Benchmark Questions
# Version: 2.0.0
# Auto-generated by ais_ingest_sec_10k on first run
# Corpus: sec_10k — multi-firm financial services corpus
# Focus: Cross-firm retail banking trends and temporal evolution over 5 fiscal years

- topic: AI Risk Evolution
  questions:
    - id: ai_disclosure_evolution
      question: How has AI risk disclosure evolved at major US retail banks from 2022 to 2026? Compare what JPMorgan, Bank of America, and Wells Fargo say about AI risks, and identify which firm started disclosing AI risks earliest.
      keywords: [AI, artificial intelligence, risk, disclosure]
      notes: Cross-firm + temporal trend question — tests retrieval across multiple firms and years

    - id: ai_governance_committees_comparison
      question: Which of JPMorgan, Bank of America, Wells Fargo, or Citigroup have established dedicated AI governance committees, and how do their oversight structures differ?
      keywords: [AI, governance, committee, oversight]
      notes: Cross-firm comparison of governance structures

- topic: Cybersecurity & Operational Risk
  questions:
    - id: cyber_disclosure_2022_vs_2026
      question: Compare how retail banks describe their cybersecurity risk management framework in their 2022 versus 2026 annual reports. What concrete changes in oversight, governance bodies, or response procedures have emerged?
      keywords: [cybersecurity, risk management, governance]
      notes: Temporal comparison — 2022 vs 2026 across retail banks

- topic: Climate & Environmental Risk
  questions:
    - id: climate_risk_evolution
      question: How has climate risk disclosure language and depth evolved in retail bank 10-K filings since 2022? Which firm has the most detailed Net Zero or transition risk framework?
      keywords: [climate, transition risk, Net Zero, sustainability]
      notes: Cross-firm + temporal — climate disclosure has been a major regulatory focus area

- topic: Capital & Financial Position
  questions:
    - id: capital_ratios_trend
      question: How have CET1 capital ratios and total revenues trended at JPMorgan, Bank of America, Wells Fargo, and Citigroup from FY2021 through FY2025? Identify any consistent leaders or laggards.
      keywords: [CET1, capital ratio, revenue, billion]
      notes: Tests financial data extraction across firms and years — must NOT trigger refusal

- topic: Digital Banking & Technology
  questions:
    - id: digital_banking_strategy
      question: How have major retail banks described their digital banking strategy and technology investment priorities over the last 5 years? What major themes emerge across firms?
      keywords: [digital, technology, investment, mobile, online]
      notes: Cross-firm + temporal — digital transformation is a sector-wide theme

- topic: Regulatory & Macro Environment
  questions:
    - id: regulatory_burden_evolution
      question: What new regulatory burdens, capital rules, or compliance requirements have retail banks disclosed in their 2025 and 2026 filings compared to 2022? Are there themes that all firms agree are most challenging?
      keywords: [regulation, capital rules, compliance, Basel]
      notes: Tests recent regulatory disclosures and consensus across firms

- topic: Latency Baseline
  questions:
    - id: latency_test
      question: What is the primary business of the firms in this corpus?
      keywords: [bank, financial, services]
      notes: Simple corpus-grounded query for latency baseline measurement
EOF
    echo "✅ Created benchmarks/sec_10k/sec_10k_questions.yaml"
fi

# Write sec_10k_corpus_metadata.yaml on first run
METADATA_FILE="$CORPUS_DIR/sec_10k_corpus_metadata.yaml"
if [[ ! -f "$METADATA_FILE" ]]; then
    mkdir -p "$CORPUS_DIR"
    cat > "$METADATA_FILE" << 'EOF'
# sec_10k_corpus_metadata.yaml
# Corpus metadata — loaded by api.py at query time
# Auto-generated by ais_ingest_sec_10k on first run

schema_version: "1.0"
corpus_name: sec_10k
short_description: "SEC 10-K filings from major financial services firms"
description: >-
  Annual report (10-K) filings from major financial services firms downloaded
  from SEC EDGAR. Covers bulge-bracket banks, asset managers, exchanges, and
  custody banks. Filings span multiple years — use the Year filter to restrict
  retrieval to a specific filing period.
content_summary: >-
  Filings from major financial services firms: bulge-bracket banks (Goldman Sachs, JPMorgan Chase,
  Morgan Stanley, Bank of America, Citigroup, Wells Fargo), asset managers
  (BlackRock, T. Rowe Price, Franklin Templeton, Invesco, AllianceBernstein),
  exchanges (CME Group, ICE, Nasdaq, CBOE), insurance (AIG, MetLife, Prudential,
  Travelers), custody (BNY Mellon, State Street, Northern Trust), and boutiques
  (Jefferies, Raymond James, Stifel Financial).
search_guidance: |
  Route questions to the most relevant firm and filing year:
  - Always use the Firm filter for firm-specific questions (e.g. "Goldman Sachs")
  - Always use the Year filter for year-specific questions (e.g. "2023")
  - AI risk, AI governance committees → Goldman Sachs, JPMorgan Chase, Morgan Stanley
  - Cybersecurity risk management → JPMorgan Chase, Bank of America, Citigroup
  - Model risk governance → Morgan Stanley, Goldman Sachs
  - Climate risk, ESG → Bank of America, Citigroup, Wells Fargo
  - Revenue and financials → use Year filter + firm name for precision
  - Cross-firm comparisons → leave Firm filter blank, use Year filter only
  When no firm filter is set, answers may blend content from multiple firms.
  The CrossEncoder reranker improves precision — but firm-specific queries benefit
  significantly from the Firm filter applied at the vector layer.
EOF
    echo "✅ Created data/corpora/sec_10k/sec_10k_corpus_metadata.yaml"
fi

# --- Ingesting
echo "--- Important"
echo "· This terminal can be minimized but should not be closed."
echo "· Sleep prevention: caffeinate -i is active for the duration."

# ── Metadata-driven time estimate (cascade: corpus avg → 60s floor) ───────────
# Whole-corpus run can only use the corpus-wide avg (tier 2) or the 60s floor
# (tier 3). Per-file durations (tier 1) apply to selective --files / UI runs.
# IMPORTANT: avg_seconds_per_file can be contaminated by skip-heavy incremental
# runs (duration includes scan time, files_processed counts only new files), so
# we sanity-floor it: a value < 2s/file for SEC XBRL is physically impossible
# (each file is 14–37s), so we reject it and fall back to the 60s seed.
AVG_SECS_PER_FILE=""
if [[ -f "$METADATA_FILE" ]]; then
    AVG_SECS_PER_FILE=$(python3 -c "
import yaml
try:
    d = yaml.safe_load(open('$METADATA_FILE')) or {}
    v = d.get('avg_seconds_per_file')
    # Reject implausible (skip-contaminated) averages for SEC XBRL.
    print(v if (v and float(v) >= 2.0) else '')
except Exception:
    print('')
" 2>/dev/null || echo "")
fi

# Effective count for the time estimate + the ▶ Ingesting line: the SELECTED file count in
# --files mode, else the whole corpus. (Preflight "✅ N filings ready" still counts all on disk.)
if [[ -n "$FILES_ARG" ]]; then
    INGEST_COUNT=$(echo "$FILES_ARG" | tr ',' '\n' | grep -c .)
else
    INGEST_COUNT=$FILE_COUNT
fi

if [[ -n "$AVG_SECS_PER_FILE" && "$AVG_SECS_PER_FILE" != "None" ]]; then
    EST_SRC="corpus avg ${AVG_SECS_PER_FILE}s/file"
    ESTIMATE_PRO=$(python3 -c "v=$AVG_SECS_PER_FILE*$INGEST_COUNT; print(f'{v/60:.0f}' if v>=60 else '< 1')" 2>/dev/null || echo "?")
    ESTIMATE_AIR=$(python3 -c "v=$AVG_SECS_PER_FILE*2.5*$INGEST_COUNT; print(f'{v/60:.0f}' if v>=60 else '< 1')" 2>/dev/null || echo "?")
else
    EST_SRC="60s/file seed (no prior ingest data)"
    ESTIMATE_PRO=$(python3 -c "v=60*$INGEST_COUNT; print(f'{v/60:.0f}')" 2>/dev/null || echo "?")
    ESTIMATE_AIR=$(python3 -c "v=60*2.5*$INGEST_COUNT; print(f'{v/60:.0f}')" 2>/dev/null || echo "?")
fi

# Mode note
if [[ -n "$FILES_ARG" ]]; then
    INGEST_NOTE=" (selective — ${FILES_ARG//,/, } only)"
elif [[ -n "$EXISTING_CHUNKS" && "$EXISTING_CHUNKS" != "?" && "$EXISTING_CHUNKS" -gt 0 && -z "$FORCE_FLAG" ]]; then
    INGEST_NOTE=" (incremental — unchanged files skipped)"
else
    INGEST_NOTE=" (full rebuild)"
fi

echo "--- Ingesting"
echo "▶ Ingesting $INGEST_COUNT filings · ~${ESTIMATE_PRO} min on M4 Pro · ~${ESTIMATE_AIR} min on M4 Air${INGEST_NOTE}"
echo "· estimate from: $EST_SRC · self-corrects from live rate after file 1"

# Parse --force flag
cd "$REPO"
source .venv/bin/activate

INGEST_ARGS=(--corpus sec_10k --root "$UPLOADS")
[[ -n "$FORCE_FLAG"   ]] && INGEST_ARGS+=(--force)
[[ -n "$VERBOSE_FLAG" ]] && INGEST_ARGS+=(--verbose)
[[ -n "$FILES_ARG"    ]] && INGEST_ARGS+=(--files "$FILES_ARG")

caffeinate -i env AISTUDIO_VECTORSTORE=qdrant PYTHONPATH=src \
    python3 -m local_llm_bot.app.ingest "${INGEST_ARGS[@]}"

INGEST_EXIT=$?

echo "--- Next steps"
if [[ "$INGEST_EXIT" -eq 0 ]]; then
    echo "✅ Corpus 'sec_10k' ready."
    echo "· Select 'sec_10k' in the AIStudio corpus dropdown to query."
    echo "· To benchmark    : ais_bench --corpus sec_10k"
    echo "· To add files    : ais_download_sec_10k && $SCRIPT_NAME   (incremental — only new files)"
    echo "· To ingest some  : $SCRIPT_NAME --files BlackRock,Citi   (substring/regex match, OR; others untouched)"
    echo "· To rebuild      : $SCRIPT_NAME --force"
else
    echo "❌ Ingest exited with error code $INGEST_EXIT."
    echo "· Check output above for details."
    echo "· To retry        : $SCRIPT_NAME --force"
fi

exit $INGEST_EXIT
