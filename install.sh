#!/usr/bin/env zsh
# AIStudio — User alias installer
# Appends ais_* user aliases to ~/.zshrc
# Safe to run multiple times — checks for existing block first
#
# Usage: bash ~/Developer/AIStudio/install.sh

REPO="$(cd "$(dirname "$0")" && pwd)"
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
alias ais_start='$REPO/ais_start.sh'
alias ais_stop='$REPO/ais_stop.sh'
alias ais_bench='$REPO/ais_bench.sh'
alias ais_sec_download='$REPO/ais_sec_download.sh'
alias ais_help='$REPO/ais_help.sh'
alias ais_help_ops='$REPO/ais_help_ops.sh'
alias ais_deploy='$REPO/scripts/deploy_files.sh'
alias ais_packet='$REPO/scripts/generate_packet.sh'
alias ais_bundle='$REPO/scripts/bundle_session.sh'
alias ais_test='cd $REPO && source .venv/bin/activate && make test'
alias ais_check='cd $REPO && source .venv/bin/activate && make check'
alias ais_restore_scripts='source $REPO/scripts/restore_scripts.sh'
# ────────────────────────────────────────────────────────────────
BLOCK

echo "✓ AIStudio aliases added to $ZSHRC"
echo ""
echo "Reload your shell:"
echo "  source ~/.zshrc"
echo ""
echo "Then try:"
echo "  ais_help"
