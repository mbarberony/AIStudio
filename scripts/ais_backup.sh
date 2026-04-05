#!/usr/bin/env zsh
# ais_backup.sh — Create timestamped zip backup of AIStudio repo
# Usage: ais_backup
# Version: 1.0.0
#
# Creates a full backup of the repo in:
#   ~/Documents/009 - 010 - ais_backup/<YYYY-MM-DD> - <HHMM>/
#
# Excludes: .venv/, .git/, __pycache__/, qdrant_storage/, node_modules/
#
# Use before risky operations: filter-repo, major refactors, gitignore changes.
# Also run at EOS for an extra safety net beyond git.

set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
BACKUP_ROOT="$HOME/Documents/009 - 010 - ais_backup"
TIMESTAMP="$(date '+%Y-%m-%d') - $(date '+%H%M')"
BACKUP_DIR="$BACKUP_ROOT/$TIMESTAMP"
BACKUP_FILE="$BACKUP_DIR/AIStudio.zip"

echo "💾 AIStudio Backup"
echo ""
echo "  Source : $REPO"
echo "  Dest   : $BACKUP_FILE"
echo ""

# ── Create backup directory ───────────────────────────────────────────────────
mkdir -p "$BACKUP_DIR"

# ── Create zip, excluding heavy/generated directories ────────────────────────
cd "$REPO/.."
zip -r "$BACKUP_FILE" "$(basename "$REPO")" \
    --exclude "$(basename "$REPO")/.venv/*" \
    --exclude "$(basename "$REPO")/.git/*" \
    --exclude "$(basename "$REPO")/__pycache__/*" \
    --exclude "$(basename "$REPO")/.pytest_cache/*" \
    --exclude "$(basename "$REPO")/.ruff_cache/*" \
    --exclude "$(basename "$REPO")/node_modules/*" \
    -q

SIZE=$(du -sh "$BACKUP_FILE" | cut -f1)
echo "  ✓ Backup complete — $SIZE"
echo "  📁 $BACKUP_DIR"
echo ""
