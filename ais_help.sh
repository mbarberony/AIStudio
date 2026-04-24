#!/usr/bin/env zsh
# ais_help — AIStudio user command reference

# ── Source guard: this script must be executed, not sourced ──────────────────
[[ "$ZSH_EVAL_CONTEXT" == *:file* ]] && { echo "❌ Do not source this script — execute it directly."; return 1; }

VERSION="2.0.1"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPT_NAME="ais_help"
HELP_FILE="$SCRIPT_DIR/ais_command_help.txt"

_show_help() {
    if [[ -f "$HELP_FILE" ]]; then
        awk "/^## $SCRIPT_NAME$/,/^---$/" "$HELP_FILE" | grep -v "^---$"
    else
        echo "$SCRIPT_NAME v$VERSION"
        echo "Usage: ais_help [<command>]"
    fi
}

if [[ "$1" == "--version" ]]; then echo "$SCRIPT_NAME v$VERSION"; exit 0; fi
if [[ "$1" == "--help" ]]; then _show_help; exit 0; fi

# ais_help <command> — show help for a specific command
if [[ -n "$1" ]]; then
    cmd="$1"
    if [[ -f "$HELP_FILE" ]]; then
        result=$(awk "/^## ${cmd}$/,/^---$/" "$HELP_FILE" | grep -v "^---$")
        if [[ -n "$result" ]]; then
            echo "$result"
        else
            echo "❌ No help found for '$cmd'."
            echo "· Run ais_help to see all available commands."
        fi
    else
        echo "❌ Help file not found: $HELP_FILE"
    fi
    exit 0
fi

# Default: show full reference
printf '\033[1m[ais_help v%s — AIStudio command reference]\033[0m\n' "$VERSION"
echo ""
echo "+==============================================================+"
echo "|              AIStudio — Command Reference                    |"
echo "+==============================================================+"
echo ""
echo "── Setup ────────────────────────────────────────────────────"
echo "  ais_install           Install AIStudio — run once after cloning"
echo "  ais_install <cmd>     Install a single command alias"
echo "  ais_install --verify  Verify all command aliases are active"
echo ""
echo "── Application ──────────────────────────────────────────────"
echo "  ais_start             Start all services (Qdrant, Ollama, FastAPI, opens UI)"
echo "  ais_stop              Stop all services"
echo "  ais_log               Tail live backend log (run in separate tab)"
echo ""
echo "── Corpus & Data ────────────────────────────────────────────"
echo "  ais_download_sec_10k  Download SEC 10-K corpus from EDGAR (~2GB)"
echo "  ais_ingest_sec_10k    Ingest SEC 10-K corpus (~30 min, backend required)"
echo ""
echo "── Benchmarking ─────────────────────────────────────────────"
echo "  ais_bench             Run benchmark on demo corpus (default settings)"
echo ""
echo "── Help ─────────────────────────────────────────────────────"
echo "  ais_help              Show this reference"
echo "  ais_help <command>    Show detailed help for a specific command"
echo ""
echo "· Setup: cd ~/Developer/AIStudio && ./ais_install"
echo "· Docs:  see QUICKSTART.md for full getting-started guide"
echo ""
