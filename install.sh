#!/usr/bin/env zsh
# AIStudio — User Command Installer
# Installs ais_* user-facing aliases into ~/.zshrc
# Installs 'install_ops' command to /usr/local/bin for operator use
#
# Usage: bash ~/Developer/AIStudio/install.sh
# After running: source ~/.zshrc

REPO="$(cd "$(dirname "$0")" && pwd)"
ZSHRC="$HOME/.zshrc"
MARKER="# ── AIStudio User Commands ──"

if grep -q "$MARKER" "$ZSHRC" 2>/dev/null; then
    echo "✓ AIStudio user aliases already installed in $ZSHRC"
    echo ""
    echo "  To reinstall, remove the block between:"
    echo "    '# ── AIStudio User Commands ──'"
    echo "  and:"
    echo "    '# ── End AIStudio User Commands ──'"
    echo "  then re-run this script."
    exit 0
fi

# Install user aliases into ~/.zshrc
cat >> "$ZSHRC" << BLOCK

# ── AIStudio User Commands ──────────────────────────────────────────────────
alias ais_start='$REPO/scripts/start.sh'
alias ais_stop='$REPO/scripts/stop.sh'
alias ais_bench='$REPO/ais_bench.sh'
alias ais_sec_download='$REPO/ais_sec_download.sh'
alias ais_help='$REPO/ais_help.sh'
# ── End AIStudio User Commands ──────────────────────────────────────────────
BLOCK

# Install 'install_ops' command to /usr/local/bin
sudo ln -sf "$REPO/install_ops.sh" /usr/local/bin/install_ops
sudo chmod +x /usr/local/bin/install_ops

echo ""
echo "✓ AIStudio user commands installed:"
echo "    ais_start        — start all services and open the UI"
echo "    ais_stop         — stop all services"
echo "    ais_bench        — run the demo corpus benchmark"
echo "    ais_sec_download — download SEC 10-K filings from EDGAR"
echo "    ais_help         — show this command reference"
echo ""
echo "Now run:"
echo "    source ~/.zshrc"
echo ""
echo "Then verify:"
echo "    ais_help"
echo ""
echo "Operator? In a new terminal, type:"
echo "    install_ops"
