#!/usr/bin/env zsh
# ais_commit — Stage all changes, commit with message, and push
# Usage: ais_commit "your commit message"
# Version: 1.2.0
# 1.2.0: --dry-run — stage, run all guards, show what WOULD commit, then unstage
#        and exit without committing or pushing. Safe inspection of git add -A.
# 1.1.0: KRR_085 — staged-content guard. After `git add -A`, inspect what was
#        actually staged and HALT (unstage) if it swept in artifacts that must
#        never reach the public repo (bundle zips, _ops files, meta/, PACKET/
#        BUNDLE/.backup). Empty stage → honest clean exit, not a commit error.
#        (Silent-failure antipattern: work done ≠ work requested → HALT.)
# 1.0.3: prior — meta/ gitignore guard + three-script tracked guard.


# ── Source guard: this script must be executed, not sourced ──────────────────
[[ "$ZSH_EVAL_CONTEXT" == *:file* ]] && { echo "❌ Do not source this script — execute it directly."; return 1; }

VERSION="1.2.0"

SCRIPT_NAME="ais_commit"
HELP_FILE="$SCRIPT_DIR/../ais_command_help_ops.txt"

_show_help() {
    if [[ -f "$HELP_FILE" ]]; then
        awk "/^## $SCRIPT_NAME$/,/^---$/" "$HELP_FILE" | grep -v "^---$"
    else
        echo "$SCRIPT_NAME v$VERSION"
        echo ""
        echo "Usage: $SCRIPT_NAME [--help] [--version] [--dry-run] \"<message>\""
        echo ""
        echo "Run from: ~/Developer/AIStudio"
    fi
}

if [[ "$1" == "--help" ]]; then _show_help; exit 0; fi
if [[ "$1" == "--version" ]]; then echo "$SCRIPT_NAME v$VERSION"; exit 0; fi

# ── --dry-run flag (may precede the message) ─────────────────────────────────
DRY_RUN=0
if [[ "$1" == "--dry-run" ]]; then DRY_RUN=1; shift; fi

printf '\033[1m[ais_commit v%s — Lint, commit, and push changes to git%s]\033[0m\n' "$VERSION" "$( [[ $DRY_RUN -eq 1 ]] && echo ' — DRY RUN' )"

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
    echo "    urc_deploy gitignore.txt"
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

# ── staged-content guard (KRR_085) ───────────────────────────────────────────
# git add -A stages everything not ignored. Inspect what landed and HALT if it
# swept in artifacts that must never reach the public repo. Loud failure, not a
# silent push. (Antipattern: silent failure — work done ≠ work requested → HALT.)
STAGED="$(git diff --cached --name-only)"
if [[ -z "$STAGED" ]]; then
    echo "ℹ Nothing staged — working tree clean. Nothing to commit or push."
    exit 0
fi
BAD="$(printf '%s\n' "$STAGED" | grep -E '\.zip$|_ops\.|_ops$|(^|/)meta/|PACKET|BUNDLE|\.backup' || true)"
if [[ -n "$BAD" ]]; then
    echo "🚨 STOP — git add -A staged files that must NOT be committed to the public repo:"
    printf '   • %s\n' ${(f)BAD}
    echo ""
    echo "  Unstaging everything (git reset). If you meant to commit specific files,"
    echo "  stage them explicitly: git add <file>   then re-run ais_commit."
    git reset -q
    exit 1
fi
echo "· Staged (clean — no zip/_ops/meta/PACKET/BUNDLE/backup):"
printf '   • %s\n' ${(f)STAGED}

if [[ $DRY_RUN -eq 1 ]]; then
    echo ""
    echo "🔍 DRY RUN — the above would be committed with message: \"${1:-<none given>}\""
    echo "   No commit, no push. Unstaging now (git reset)."
    git reset -q
    exit 0
fi

git commit -m "$1"
git push --set-upstream origin main

echo "✅ Committed and pushed: $1"
