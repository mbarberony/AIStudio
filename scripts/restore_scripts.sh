#!/usr/bin/env zsh
# restore_scripts.sh — Restore operator scripts from latest AIStudio BUNDLE zip
# Usage: ais_restore_scripts
# Version: 1.0.0
#
# Use after git filter-repo (which deletes scripts/ from disk) or any other
# situation where operator scripts are missing. Extracts deploy_files.sh,
# generate_packet.sh, and bundle_session.sh from the latest BUNDLE zip in
# ~/Downloads and places them in scripts/.

set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
SCRIPTS_DIR="$REPO/scripts"
DOWNLOADS="$HOME/Downloads"

echo "🔧 AIStudio — Restore Operator Scripts"
echo ""

# ── Find latest BUNDLE zip ────────────────────────────────────────────────────
BUNDLE=$(ls -t "$DOWNLOADS"/BUNDLE\ -\ AIStudio\ -\ Session\ -\ *.zip 2>/dev/null | head -1)

if [[ -z "$BUNDLE" ]]; then
    echo "❌ No AIStudio BUNDLE zip found in ~/Downloads."
    echo "   Download the latest BUNDLE and try again."
    exit 1
fi

echo "  📦 Found: $(basename "$BUNDLE")"
echo ""

# ── Extract scripts ───────────────────────────────────────────────────────────
mkdir -p "$SCRIPTS_DIR"

for script in deploy_files.sh generate_packet.sh bundle_session.sh; do
    if unzip -p "$BUNDLE" "scripts/$script" > "$SCRIPTS_DIR/$script" 2>/dev/null; then
        chmod +x "$SCRIPTS_DIR/$script"
        echo "  ✓ $script → scripts/$script"
    else
        echo "  ⚠  $script not found in bundle — skipping"
    fi
done

echo ""

# ── Refresh shell hash table ──────────────────────────────────────────────────
hash -r 2>/dev/null || true

echo "✅ Scripts restored. Run: source ~/.zshrc"
echo "   Then verify: ais_deploy --help"
