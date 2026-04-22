#!/usr/bin/env bash
# ais_start — Start all AIStudio services
# Wrapper around scripts/start.sh for user convenience
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
exec "$SCRIPT_DIR/scripts/start.sh" "$@"
