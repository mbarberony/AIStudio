#!/usr/bin/env bash
# ais_stop — Stop AIStudio services
# Wrapper around scripts/stop.sh for user convenience
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
exec "$SCRIPT_DIR/scripts/stop.sh" "$@"
