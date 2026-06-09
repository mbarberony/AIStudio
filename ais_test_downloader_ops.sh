#!/usr/bin/env zsh
# Version: 1.0.4
VERSION="1.0.4"
# Changelog: 1.0.4 — fix stale offline assertion: --scope resolution now goes through
#            _scope_common_ops, which raises ScopeError "Scope not found" (was the
#            downloader-local "Scope file not found" in <=1.2.x). Test string realigned.
# Changelog: 1.0.3 — downloader v1.4.0 inventory write-back: network tests pass
#            --no-inventory so throwaway --out runs never mutate the real *_full_scope ledger.
# Changelog: 1.0.2 — downloader v1.3.0 year-flag split: network tests use --latest 1
#            (was --years 1, which now means fiscal year 1). Added offline mutual-exclusion
#            test and a --years YYYY fiscal-year network test.
# Changelog: 1.0.1 — zsh-conform: shebang zsh + REPO via ${0:A:h} (zsh script-dir idiom,
#            replacing the bash-only form). --verbose given its own case branch (was a
#            combined --verbose|-v) so the §8 flag audit sees it implemented; drops -v.
# Changelog: 1.0.0 — Initial: SEC 10-K downloader test harness (offline + --full network).
#
# Test suite for the SEC 10-K downloader (scripts/download_sec_corpus.py).
# Exercises every input mode and outcome (positive + negative) against a throwaway
# output dir, so it never pollutes data/corpora/sec_10k/uploads/. Offline tests run
# always; network tests (real EDGAR fetches) run with --full.
#
# CLI conventions per STD - AIStudio - CLI Output (bold header, --- bundles, ▶/✅/❌/·/ℹ).

set -u
set -o pipefail

CMD="ais_test_downloader_ops"
DESC="Test the SEC 10-K downloader"
FULL=0
VERBOSE=0
SILENT=0
NOSEP=0

# ── Flag parsing ─────────────────────────────────────────────────────────────
while [[ $# -gt 0 ]]; do
  case "$1" in
    --help|-h)
      printf '%s v%s — %s\n\n' "$CMD" "$VERSION" "$DESC"
      printf 'Usage: %s [--full] [--verbose] [--silent] [--no-separator] [--help] [--version]\n\n' "$CMD"
      printf 'Run the SEC 10-K downloader test suite against a throwaway output dir.\n\n'
      printf 'Options:\n'
      printf '  --help          Show this help\n'
      printf '  --version       Show script version\n'
      printf '  --full          Also run network tests (real EDGAR fetches; ~1–2 min)\n'
      printf '  --verbose       Print captured output for failing tests\n'
      printf '  --silent        Suppress all output except failures (for CI / callers)\n'
      printf '  --no-separator  Use blank lines instead of --- Section labels\n\n'
      printf '· Offline tests (arg validation, error paths) always run — no network.\n'
      printf '· Network tests download 1 filing per firm into a temp dir, then discard.\n'
      printf '· Exit 0 if all pass, 1 if any fail.\n'
      exit 0 ;;
    --version)      printf '%s v%s\n' "$CMD" "$VERSION"; exit 0 ;;
    --full)         FULL=1; shift ;;
    --verbose)      VERBOSE=1; shift ;;
    --silent)       SILENT=1; shift ;;
    --no-separator) NOSEP=1; shift ;;
    *) printf '❌ Unknown argument: %s.\n' "$1"; exit 2 ;;
  esac
done

# say: normal output, suppressed under --silent
say() { [[ $SILENT -eq 1 ]] || printf '%s\n' "$1"; }
# sep: section separator (--- Label, or blank line under --no-separator), suppressed under --silent
sep() { [[ $SILENT -eq 1 ]] && return; if [[ $NOSEP -eq 1 ]]; then printf '\n'; else printf -- '--- %s\n' "$1"; fi; }

[[ $SILENT -eq 1 ]] || printf '\033[1m[%s v%s — %s]\033[0m\n' "$CMD" "$VERSION" "$DESC"

# ── Preflight ────────────────────────────────────────────────────────────────
sep "Preflight"
REPO="${0:A:h}"                       # zsh: absolute dir of this script (repo root)
SCRIPT="$REPO/scripts/download_sec_corpus.py"
PYBIN="$REPO/.venv/bin/python"
[[ -x "$PYBIN" ]] || PYBIN="python3"

if [[ ! -f "$SCRIPT" ]]; then
  printf '❌ Downloader not found: %s.\n' "$SCRIPT"; exit 1   # error always shows
fi
say "✅ Downloader found: scripts/download_sec_corpus.py."
say "✅ Python: $PYBIN."

TMP="$(mktemp -d "${TMPDIR:-/tmp}/ais_test_downloader.XXXXXX")"
trap 'rm -rf "$TMP"' EXIT
say "ℹ Temp output: $TMP"

# Fixtures
GOOD_SCOPE="$TMP/good_scope.yaml"
printf 'entities:\n  - { label: Goldman Sachs, cik: "0000886982" }\n' > "$GOOD_SCOPE"
BAD_SCOPE="$TMP/bad_scope.yaml"
printf 'firms:\n  - Goldman Sachs\n' > "$BAD_SCOPE"   # no `entities:` key

PASS=0; FAIL=0

# run <name> <expect: rc0|rcN> <needle> [args...]
#   needle prefixed with ! asserts ABSENCE; empty needle skips the string check.
run() {
  local name="$1" expect="$2" needle="$3"; shift 3
  say "▶ $name..."
  local out rc
  out="$("$PYBIN" "$SCRIPT" --out "$TMP" "$@" 2>&1)"; rc=$?
  local ok=1 why=""
  case "$expect" in
    rc0) [[ $rc -eq 0 ]] || { ok=0; why="expected rc 0, got $rc"; } ;;
    rcN) [[ $rc -ne 0 ]] || { ok=0; why="expected nonzero rc, got 0"; } ;;
  esac
  if [[ -n "$needle" ]]; then
    if [[ "${needle:0:1}" == "!" ]]; then
      grep -qF -- "${needle:1}" <<<"$out" && { ok=0; why="unexpected string present: ${needle:1}"; }
    else
      grep -qF -- "$needle" <<<"$out" || { ok=0; why="missing string: $needle"; }
    fi
  fi
  if [[ $ok -eq 1 ]]; then
    say "✅ $name."; PASS=$((PASS+1))
  else
    printf '❌ %s — %s.\n' "$name" "$why"   # failures always show
    FAIL=$((FAIL+1))
    [[ $VERBOSE -eq 1 ]] && sed 's/^/    /' <<<"$out"
  fi
}

# ── Offline tests (no network) ───────────────────────────────────────────────
sep "Offline tests"
run "help exits clean"                 rc0 "usage:"                      --help
run "mutually exclusive --tkr + --cik" rcN "not allowed with argument"  --tkr GS --cik 0000886982
run "mutually exclusive --latest + --years" rcN "not allowed with argument"  --latest 2 --years 2024
run "scope file not found"             rcN "Scope not found"            --scope "$TMP/nope.yaml"
run "malformed scope (no entities)"    rcN "has no"                     --scope "$BAD_SCOPE"
run "force_name rejected with --scope" rcN "single-firm modes"          --scope "$GOOD_SCOPE" --force_name "X"

# ── Network tests (real EDGAR fetches) ───────────────────────────────────────
sep "Network tests"
if [[ $FULL -eq 0 ]]; then
  say "· skipped (use --full to run real EDGAR fetches)"
else
  run "ticker resolves + verify present (GS)" rc0 "entity tag present"            --tkr GS --latest 1 --no-inventory
  run "CIK mode + verify present (GS)"         rc0 "entity tag present"            --cik 0000886982 --latest 1 --no-inventory
  run "scope download succeeds"                rc0 "Downloaded:"                   --scope "$GOOD_SCOPE" --latest 1 --no-inventory
  run "years mode fetches a fiscal year (GS)" rc0 "entity tag present"            --tkr GS --years 2024 --no-inventory
  run "no-verify suppresses the check"         rc0 "!verify:"                      --tkr GS --latest 1 --no-verify --no-inventory
  run "verify FAIL + coaching (BNY)"           rc0 "no dei:EntityRegistrantName"   --tkr BNY --latest 1 --no-inventory
  run "force_name asserts identity (BNY)"      rc0 "forced"                        --tkr BNY --latest 1 --force_name "The Bank of New York Mellon Corporation" --no-inventory
  run "unknown ticker errors cleanly"          rcN "not found in EDGAR"            --tkr ZZZZ --no-inventory
  run "valid-format CIK with no filings"       rc0 "No 10-K filings found"         --cik 9999999999 --latest 1 --no-inventory
fi

# ── Summary ──────────────────────────────────────────────────────────────────
if [[ $FAIL -eq 0 ]]; then
  sep "Summary"; say "· $PASS passed · $FAIL failed"; say "✅ All downloader tests passed."
  exit 0
else
  if [[ $NOSEP -eq 1 ]]; then printf '\n'; else printf -- '--- Summary\n'; fi
  printf '· %d passed · %d failed\n' "$PASS" "$FAIL"
  printf '❌ %d test(s) failed.\n' "$FAIL"
  exit 1
fi
