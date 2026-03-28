#!/usr/bin/env bash
# ais_stop — Stop AIStudio services
# Wrapper around scripts/stop.sh for user convenience
exec "$(dirname "$0")/../scripts/stop.sh" "$@"
