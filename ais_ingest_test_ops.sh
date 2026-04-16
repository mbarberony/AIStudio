#!/usr/bin/env zsh
# ais_ingest_test_ops.sh — AIStudio Ingest Pipeline Test (Operator only)
# Version: 1.0.0

VERSION="1.0.0"
REPO="$(cd "$(dirname "$0")" && pwd)"

printf "\033[1m[ais_ingest_test_ops v$VERSION — Validate ingest pipeline end-to-end]\033[0m\n"

if [[ "$1" == "--version" ]]; then
    exit 0
fi

if [[ "$1" == "--help" ]]; then
    echo ""
    echo "Usage: ais_ingest_test_ops [--test N] [--no-cleanup] [--model NAME] [--seed] [--list-sets]"
    echo ""
    echo "Validates the AIStudio ingest pipeline end-to-end."
    echo ""
    echo "Test modes:"
    echo "  --test 1  (default) Fresh ingest → MD5 → skip regression → thematic query"
    echo "  --test 2  Ingest 6 → upload 6+4 (skip 6, ingest 4 new)"
    echo "  --test 3  Ingest 6 → upload 6+4 (reingest all 10)"
    echo "  --test 4  Mixed: skip/reingest/new pattern"
    echo ""
    echo "Options:"
    echo "  --no-cleanup    Leave corpus after test"
    echo "  --model NAME    Override query model"
    echo "  --seed          Seed fixtures from sec_10k corpus"
    echo "  --list-sets     List available test sets"
    echo ""
    echo "· Reports written to tests/reports/"
    echo "· Fixtures required in tests/fixtures/ — seed with: ais_ingest_test_ops --seed"
    exit 0
fi

cd "$REPO"
source .venv/bin/activate
PYTHONPATH="$REPO/src" python3 "$REPO/tests/ingest_test_ops.py" "$@"
