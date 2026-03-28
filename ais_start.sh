#!/usr/bin/env bash
# ais_start — Start all AIStudio services
# Wrapper around scripts/start.sh for user convenience
exec "$(dirname "$0")/../scripts/start.sh" "$@"
