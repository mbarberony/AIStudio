#!/usr/bin/env zsh
# ais_commit — Stage all changes, commit with message, and push
# Usage: ais_commit "your commit message"
# Version: 1.2.0

if [[ -z "$1" ]]; then
    echo "Usage: ais_commit \"commit message\""
    exit 1
fi

REPO="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO"

# ── .gitignore guard ──────────────────────────────────────────────────────────
# meta/ must be gitignored before any commit — prevents leaking operator files
if ! grep -q "^meta/$" .gitignore 2>/dev/null; then
    echo "🚨 STOP — .gitignore does not contain 'meta/' on its own line."
    echo ""
    echo "  This means meta/ files could be committed to GitHub."
    echo "  Fix before committing:"
    echo ""
    echo "    ais_deploy gitignore.txt"
    echo "    git add .gitignore && git commit --no-verify -m \"fix: restore meta/ to .gitignore\""
    echo "    git push"
    echo "    Then re-run ais_commit."
    echo ""
    exit 1
fi

# ── scripts/ guard ────────────────────────────────────────────────────────────
# Operator scripts should never be committed
for script in scripts/deploy_files.sh scripts/generate_packet.sh scripts/bundle_session.sh; do
    if git ls-files --error-unmatch "$script" 2>/dev/null; then
        echo "🚨 STOP — $script is tracked by git and should not be."
        echo "  Run: git rm --cached $script"
        echo "  Then re-run ais_commit."
        exit 1
    fi
done

git add -A
git commit -m "$1"
git push --set-upstream origin main

echo "✅ Committed and pushed: $1"
