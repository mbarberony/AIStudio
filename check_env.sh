#!/usr/bin/env bash
# check_env.sh — AIStudio Environment Preflight Check
# Version: 1.0.0
# Validates environment before install. Called by ais_install before proceeding.
# Surfaced by QA_TESTING_LESSONS_LEARNED.md items #1, #8, #10 (AIStudio_101)
#
# Checks:
#   1. Python version (3.10+)
#   2. Homebrew installed
#   3. Qdrant binary in PATH
#   4. Ollama installed
#   5. ~/bin in PATH (required for Qdrant after install)

VERSION="1.0.0"

PASS=0
FAIL=0
WARN=0

ok()   { echo "  ✅ $1"; (( PASS++ )); }
fail() { echo "  ❌ $1"; (( FAIL++ )); }
warn() { echo "  ⚠  $1"; (( WARN++ )); }

echo ""
echo "── Environment Preflight ────────────────────────────────────"

# 1. Python version
PYTHON_BIN=""
for py in python3.14 python3.13 python3.12 python3.11 python3.10 python3; do
    if command -v "$py" > /dev/null 2>&1; then
        VERSION_STR=$("$py" --version 2>&1 | grep -oE '[0-9]+\.[0-9]+')
        MAJOR=$(echo "$VERSION_STR" | cut -d. -f1)
        MINOR=$(echo "$VERSION_STR" | cut -d. -f2)
        if [[ "$MAJOR" -ge 3 && "$MINOR" -ge 10 ]]; then
            PYTHON_BIN="$py"
            ok "Python $VERSION_STR ($py)"
            break
        fi
    fi
done
if [[ -z "$PYTHON_BIN" ]]; then
    fail "Python 3.10+ not found. macOS system Python is 3.9 — install 3.10+ from python.org"
    echo "       · brew install python@3.13"
fi

# 2. Homebrew
if command -v brew > /dev/null 2>&1; then
    ok "Homebrew $(brew --version 2>/dev/null | head -1 | grep -oE '[0-9]+\.[0-9]+\.[0-9]+')"
else
    fail "Homebrew not found. Required for pango, Qdrant, and other dependencies."
    echo "       · /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
fi

# 3. ~/bin in PATH (Qdrant lands here after install)
if echo "$PATH" | grep -q "$HOME/bin"; then
    ok "~/bin in PATH"
else
    warn "~/bin not in PATH — Qdrant binary won't be found after install."
    echo "       · Add to ~/.zshrc: export PATH=\"\$HOME/bin:\$PATH\""
    echo "       · Then: source ~/.zshrc"
fi

# 4. Qdrant binary (may not exist yet on fresh install — that's OK)
if command -v qdrant > /dev/null 2>&1; then
    ok "Qdrant binary found"
else
    warn "Qdrant binary not found (expected on fresh install — will be installed in Step 5)"
fi

# 5. Ollama
if command -v ollama > /dev/null 2>&1; then
    ok "Ollama found"
else
    warn "Ollama not found. Install from https://ollama.com before running ais_start."
fi

# ── Summary ───────────────────────────────────────────────────────
echo ""
if [[ "$FAIL" -gt 0 ]]; then
    echo "  ❌ $FAIL check(s) failed — fix before proceeding with install."
    exit 1
elif [[ "$WARN" -gt 0 ]]; then
    echo "  ⚠  $WARN warning(s) — review above, then continue."
    exit 0
else
    echo "  ✅ All checks passed — environment ready."
    exit 0
fi
