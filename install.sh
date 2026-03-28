#!/usr/bin/env zsh
# AIStudio — User alias installer
# Appends ais_* user aliases to ~/.zshrc
# Safe to run multiple times — checks for existing block first
#
# Usage: bash ais_scripts/install.sh

REPO="$(cd "$(dirname "$0")/.." && pwd)"
ZSHRC="$HOME/.zshrc"
MARKER="# ── AIStudio User Commands"

if grep -q "$MARKER" "$ZSHRC" 2>/dev/null; then
    echo "✓ AIStudio aliases already installed in $ZSHRC"
    echo "  To reinstall, remove the block between '# ── AIStudio User Commands'"
    echo "  and '# ────────────────────────────────────────────────────────────'"
    echo "  then re-run this script."
    exit 0
fi

cat >> "$ZSHRC" << BLOCK

# ── AIStudio User Commands ────────────────────────────────────────
alias ais_start='$REPO/ais_scripts/ais_start.sh'
alias ais_stop='$REPO/ais_scripts/ais_stop.sh'
alias ais_bench='$REPO/ais_scripts/ais_bench.sh'
alias ais_sec_download='$REPO/ais_scripts/ais_sec_download.sh'
alias ais_help='$REPO/ais_scripts/ais_help.sh'
# ────────────────────────────────────────────────────────────────
BLOCK

echo "✓ AIStudio aliases added to $ZSHRC"
echo ""
echo "Reload your shell:"
echo "  source ~/.zshrc"
echo ""
echo "Then try:"
echo "  ais_help"
