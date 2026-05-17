#!/bin/bash
# _launcher_ops.sh — AIStudio Launch Agent wrapper
# Version: 1.1.0
# Called by com.aistudio.launcher Launch Agent (launchd context).
# Handles set -e isolation and PATH for non-interactive shell.
# --no-open: suppress browser open in start.sh (desktop app handles opening)
# Operator only — gitignored, never shipped to users directly.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$SCRIPT_DIR"

# Ensure all tools are findable in launchd non-interactive shell
export PATH="/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH"
export HOME="${HOME:-/Users/$(whoami)}"

# Run in subshell with set +e — pass --no-open so browser is opened by the .app instead
( set +e; "$REPO/ais_start.sh" --no-open )

exit 0
