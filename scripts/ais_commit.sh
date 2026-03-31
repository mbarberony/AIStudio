#!/usr/bin/env zsh
# ais_commit — Stage all changes, commit with message, and push
# Usage: ais_commit "your commit message"

if [[ -z "$1" ]]; then
    echo "Usage: ais_commit \"commit message\""
    exit 1
fi

REPO="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO"

git add -A
git commit -m "$1"
git push

echo "✅ Committed and pushed: $1"
