#!/bin/bash
# ais_launcher.sh — AIStudio Launch Agent backing (TRACKED — ships on every clone)
# Version: 1.0.0
# Changelog:
#   1.0.0 — Created for AIStudio_A1. Tracked replacement for the gitignored operator twin
#           `_ais_create_shortcut_ops.sh` (a.k.a. _launcher_ops.sh), which the desktop
#           shortcut's Launch Agent pointed at — so on a fresh public clone the target was
#           missing and the icon opened a dead UI ("Ollama not running"). Faithful port:
#           launchd PATH + `set +e` isolation + `ais_start.sh --no-open`. No alias (launchd
#           calls it by path); not a user command → no help.txt section (mirrors ais_start.py).
#
# Called by the com.aistudio.launcher Launch Agent that `ais_create_shortcut` installs.
# Double-clicking the Desktop/Dock AIStudio icon kickstarts that agent, which runs this.
#
# Job: (1) give launchd's bare non-interactive shell a real PATH, (2) isolate `set -e`
# (ais_start.sh runs under `set -euo pipefail` and has non-fatal steps — lsof on a free
# port, optional PDF generation — that must not abort the launch), (3) start services with
# browser-open suppressed (the .app executable opens the browser itself once /health is up).

VERSION="1.0.0"

# launchd starts with a minimal PATH — restore the tools ais_start.sh needs (brew, curl, python…).
# (The Launch Agent plist also sets PATH; this is belt-and-suspenders if ever run outside launchd.)
export PATH="/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH"
export HOME="${HOME:-/Users/$(whoami)}"

# REPO = parent of scripts/ (this file lives in scripts/). ${BASH_SOURCE[0]:-$0} is zsh/bash-safe;
# launchd invokes via /bin/bash so BASH_SOURCE is set, but the fallback keeps REPO correct even
# if this is ever run under zsh.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
REPO="$(dirname "$SCRIPT_DIR")"

# set +e subshell: swallow errexit so a benign non-zero during startup (free-port lsof, optional
# PDF step) doesn't make launchd report the whole launch as failed and back off future relaunches.
( set +e; "$REPO/ais_start.sh" --no-open )

exit 0
