#!/usr/bin/env zsh
# ais_publish — Deploy a file then commit and push
# Usage: ais_publish <filename> "commit message"

if [[ -z "$1" ]]; then
    echo "Usage: ais_publish <filename> \"commit message\""
    exit 1
fi

REPO="$(cd "$(dirname "$0")/.." && pwd)"

bash "$REPO/scripts/deploy_files.sh" "$1" && \
cd "$REPO" && \
git add -A && \
git commit -m "${2:-docs: update $1}" && \
git push && \
echo "✅ Published: $1"
