#!/usr/bin/env bash
# =============================================================================
# validate.sh — AIStudio full validation script
# =============================================================================
# Runs all test suites in sequence and reports a combined result.
#
# Usage:
#   ./validate.sh                  # full validation (Ollama + backend optional)
#   ./validate.sh --unit-only      # pytest unit tests only, no live services
#
# What it runs:
#   Phase 1 — Unit tests (pytest, no live services required)
#   Phase 2 — Integration tests (pytest, Ollama required if available)
#   Phase 3 — Live API tests (test_aistudio.py, backend + Ollama required)
#
# =============================================================================

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

UNIT_ONLY=false
for arg in "$@"; do
    [[ "$arg" == "--unit-only" ]] && UNIT_ONLY=true
done

# ── Colours ───────────────────────────────────────────────────────────────────
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
DIM='\033[2m'
NC='\033[0m'

PASS=0
FAIL=0
SKIP=0

# ── Helpers ───────────────────────────────────────────────────────────────────
divider() {
    echo -e "${DIM}────────────────────────────────────────────────────────────${NC}"
}

phase_header() {
    echo ""
    divider
    echo -e "${CYAN}${BOLD}  Phase $1 — $2${NC}"
    echo -e "${DIM}  $3${NC}"
    divider
    echo ""
}

result_line() {
    if [[ "$1" == "pass" ]]; then
        echo -e "  ${GREEN}✓ $2${NC}"
    elif [[ "$1" == "fail" ]]; then
        echo -e "  ${RED}✗ $2${NC}"
    else
        echo -e "  ${YELLOW}⚠ $2${NC}"
    fi
}

# ── Header ────────────────────────────────────────────────────────────────────
echo ""
echo -e "${BOLD}============================================================${NC}"
echo -e "${BOLD}  AIStudio — Validation Suite${NC}"
echo -e "${DIM}  $(date '+%Y-%m-%d %H:%M')  ·  $(python3 --version 2>&1)${NC}"
echo -e "${BOLD}============================================================${NC}"

# ── Activate venv ─────────────────────────────────────────────────────────────
if [[ ! -f "$REPO_ROOT/.venv/bin/activate" ]]; then
    echo ""
    echo -e "${RED}✗ .venv not found.${NC}"
    echo -e "  Run: python3.13 -m venv .venv && pip install -r requirements.txt"
    echo ""
    exit 1
fi
source "$REPO_ROOT/.venv/bin/activate"
cd "$REPO_ROOT"

# ── Phase 1 — Unit tests ──────────────────────────────────────────────────────
phase_header "1" "Unit tests" "No live services required — runs anywhere"

if PYTHONPATH=src pytest -v -m "not integration"; then
    result_line "pass" "Unit tests passed"
    ((PASS++))
else
    result_line "fail" "Unit tests failed"
    ((FAIL++))
fi

# ── Phase 2 — Integration tests ───────────────────────────────────────────────
phase_header "2" "Integration tests" "Ollama required — skips gracefully if not running"

if [[ "$UNIT_ONLY" == true ]]; then
    result_line "skip" "Skipped (--unit-only)"
    ((SKIP++))
else
    if PYTHONPATH=src pytest -v -m "integration"; then
        result_line "pass" "Integration tests passed (or skipped gracefully)"
        ((PASS++))
    else
        result_line "fail" "Integration tests failed"
        ((FAIL++))
    fi
fi

# ── Phase 3 — Live API tests ──────────────────────────────────────────────────
phase_header "3" "Live API tests (test_aistudio.py)" "Backend + Ollama + demo corpus required"

if [[ "$UNIT_ONLY" == true ]]; then
    result_line "skip" "Skipped (--unit-only)"
    ((SKIP++))
else
    if ! curl -sf http://localhost:8000/health > /dev/null 2>&1; then
        result_line "skip" "Backend not running — skipping live API tests"
        echo -e "${DIM}  Start with: PYTHONPATH=src uvicorn local_llm_bot.app.api:app --port 8000${NC}"
        ((SKIP++))
    else
        echo -e "  ${DIM}Backend reachable at localhost:8000 ✓${NC}"
        echo ""
        if PYTHONPATH=src python tests/test_aistudio.py; then
            result_line "pass" "Live API tests passed"
            ((PASS++))
        else
            result_line "fail" "Live API tests failed"
            ((FAIL++))
        fi
    fi
fi

# ── Summary ───────────────────────────────────────────────────────────────────
echo ""
echo -e "${BOLD}============================================================${NC}"
TOTAL=$((PASS + FAIL + SKIP))
if [[ $FAIL -eq 0 ]]; then
    echo -e "${GREEN}${BOLD}  ALL CLEAR — $PASS passed, $SKIP skipped, 0 failed${NC}"
else
    echo -e "${RED}${BOLD}  FAILED — $PASS passed, $SKIP skipped, $FAIL failed${NC}"
fi
echo -e "${DIM}  $TOTAL suites evaluated${NC}"
echo -e "${BOLD}============================================================${NC}"
echo ""

[[ $FAIL -eq 0 ]]
