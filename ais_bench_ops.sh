#!/usr/bin/env zsh
# ais_bench_ops.sh — AIStudio Benchmark Operator Command
# Version: 1.0.0
# Runs benchmark, then copies latest PDF to demo corpus and triggers re-ingest

VERSION="1.0.0"
REPO="$(cd "$(dirname "$0")" && pwd)"
API="http://localhost:8000"
CORPUS="demo"
BENCH_PDF_NAME="AIStudio - Benchmark Data.pdf"

printf "\033[1m[ais_bench_ops v$VERSION — Run benchmark and publish to demo corpus]\033[0m\n"

if [[ "$1" == "--version" ]]; then
    exit 0
fi

if [[ "$1" == "--help" ]]; then
    echo ""
    echo "Usage: ais_bench_ops [ais_bench options]"
    echo ""
    echo "Runs the AIStudio benchmark (same as ais_bench) then automatically:"
    echo "  · Copies latest PDF report as '$BENCH_PDF_NAME'"
    echo "  · Deploys to data/corpora/demo/uploads/"
    echo "  · Triggers demo corpus re-ingest"
    echo ""
    echo "All ais_bench flags are supported:"
    echo "  --top-k N  --temperature F  --model NAME  --no-markdown  --full"
    echo ""
    echo "· Reports written to benchmarks/demo/reports/"
    echo "· Requires backend running: ais_start"
    exit 0
fi

# Check backend
if ! curl -sf "$API/health" > /dev/null 2>&1; then
    echo "❌ Backend not reachable at $API"
    echo "· Run: ais_start"
    exit 1
fi

# --- Benchmark
echo "--- Benchmark"
cd "$REPO"
source .venv/bin/activate
python3 benchmarks/bench.py "$@"
BENCH_EXIT=$?

if [[ $BENCH_EXIT -ne 0 ]]; then
    echo "❌ Benchmark failed — aborting publish."
    exit 1
fi

# --- Publish
echo ""
echo "--- Publish"

# Find latest PDF in benchmarks/demo/reports/
REPORTS_DIR="$REPO/benchmarks/demo/reports"
LATEST_PDF=$(ls -t "$REPORTS_DIR"/benchmark_demo_*.pdf 2>/dev/null | head -1)

if [[ -z "$LATEST_PDF" ]]; then
    echo "⚠ No PDF report found in $REPORTS_DIR — skipping publish."
    echo "· Install pandoc to enable PDF generation: brew install pandoc"
    exit 0
fi

# Copy to demo corpus uploads
DEST="$REPO/data/corpora/demo/uploads/$BENCH_PDF_NAME"
cp "$LATEST_PDF" "$DEST"
echo "✅ $BENCH_PDF_NAME → data/corpora/demo/uploads/"

# Trigger re-ingest via API
echo "▶ Triggering demo corpus re-ingest..."
RESPONSE=$(curl -sf -X POST "$API/corpus/demo/ingest" 2>&1)
if [[ $? -eq 0 ]]; then
    echo "✅ Demo corpus re-ingest triggered."
    echo "· Benchmark results are now searchable in the demo corpus."
else
    echo "⚠ Re-ingest trigger failed — run manually: select demo corpus → Add → upload $BENCH_PDF_NAME"
fi
