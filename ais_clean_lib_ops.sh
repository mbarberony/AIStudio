#!/usr/bin/env zsh
# ais_clean_lib_ops.sh — AIStudio Pre-Install Cleanup
# Removes all AIStudio library artifacts from a Mac before a fresh install.
# Operator-only. Gitignored. Install via: ais_install_ops ais_clean_lib_ops
#
# Usage:
#   ais_clean_lib_ops [--dry-run] [--remove-models] [--verbose] [--silent] [--help] [--version]
#
# Flags:
#   --dry-run        Show what would be removed without removing anything
#   --remove-models  Also remove Ollama models (~/.ollama/) — large, slow to re-pull
#   --verbose        Show full output from brew/pip commands
#   --silent         Suppress all output except errors
#   --help           Show this help
#   --version        Show version
#
# What this cleans:
#   1. Ollama service + app (brew uninstall)
#   2. Ollama models (~/.ollama/) — only with --remove-models
#   3. Qdrant binary (~/bin/qdrant)
#   4. Qdrant storage (~/qdrant_storage/)
#   5. AIStudio venv (~/Developer/AIStudio/.venv/)
#   6. Global pip packages installed by AIStudio (cairosvg, weasyprint, sentence-transformers)
#   7. AIStudio aliases from ~/.zshrc (all ais_* lines + ~/bin PATH export)
#   8. Launch Agent + app bundle + Desktop symlink
#
# What this does NOT clean:
#   - ~/Developer/AIStudio/ repo itself (you manage that)
#   - Homebrew itself
#   - Python, git, or other system tools
#   - Any non-AIStudio pip packages
#
# Version: 1.0.1
# 1.0.1: Conformance pass — STD CLI Output + STD CLI Script Help (AIStudio_485)
# 1.0.0: Initial release (AIStudio_485)

# ── --help and --version FIRST — before any logic (Rule 1, STD CLI Script Help) ──
SCRIPT_NAME="ais_clean_lib_ops"
VERSION="1.0.1"
# Version: 1.0.1
DESCRIPTION="Clean AIStudio library artifacts before fresh install"

SCRIPT_DIR="${0:A:h}"
HELP_FILE="$SCRIPT_DIR/ais_command_help_ops.txt"

_show_help() {
    if [[ -f "$HELP_FILE" ]]; then
        awk "/^## ${SCRIPT_NAME}$/,/^---$/" "$HELP_FILE" | grep -v "^---$" | grep -v "^## "
    else
        echo "${SCRIPT_NAME} v${VERSION} — ${DESCRIPTION}"
        echo "Usage: ${SCRIPT_NAME} [--dry-run] [--remove-models] [--verbose] [--silent] [--help] [--version]"
        echo "(inline fallback — deploy ais_command_help_ops.txt for full help)"
    fi
}

if [[ "${1:-}" == "--help" ]];    then _show_help; exit 0; fi
if [[ "${1:-}" == "--version" ]]; then echo "${SCRIPT_NAME} v${VERSION} — ${DESCRIPTION}"; exit 0; fi

set -uo pipefail

# ── ANSI ──────────────────────────────────────────────────────────────────────
BOLD=$'\033[1m'
DIM=$'\e[2m'
ITALIC=$'\e[3m'
RESET=$'\e[0m'

# ── Flags ─────────────────────────────────────────────────────────────────────
DRY_RUN=0
REMOVE_MODELS=0
VERBOSE=0
SILENT=0

for arg in "$@"; do
    case "$arg" in
        --dry-run)       DRY_RUN=1 ;;
        --remove-models) REMOVE_MODELS=1 ;;
        --verbose)       VERBOSE=1 ;;
        --silent)        SILENT=1 ;;
        *)
            echo "❌ Unknown flag: $arg"
            echo "· Usage: ${SCRIPT_NAME} [--dry-run] [--remove-models] [--verbose] [--silent] [--help] [--version]"
            exit 1
            ;;
    esac
done

# ── Output helpers (§4, STD CLI Output) ───────────────────────────────────────
_out() { [[ "$SILENT" -eq 0 ]] && echo "$@" || true; }
_err() { echo "$@"; }  # errors always print

_sep() {
    _out "${DIM}--- ${ITALIC}$1${RESET}"
}

# ── Action helpers ─────────────────────────────────────────────────────────────
_remove() {
    local target="$1"
    local label="${2:-$1}"
    if [[ -e "$target" || -L "$target" ]]; then
        if [[ "$DRY_RUN" -eq 1 ]]; then
            _out "· Would remove: $label"
        else
            /bin/rm -rf "$target"
            _out "✅ Removed: $label"
        fi
    else
        _out "· Not found (skip): $label"
    fi
}

_brew_uninstall() {
    local pkg="$1"
    if /opt/homebrew/bin/brew list --formula "$pkg" &>/dev/null; then
        if [[ "$DRY_RUN" -eq 1 ]]; then
            _out "· Would brew uninstall: $pkg"
        else
            if [[ "$VERBOSE" -eq 1 ]]; then
                /opt/homebrew/bin/brew uninstall --ignore-dependencies "$pkg" \
                    && _out "✅ brew uninstall: $pkg" \
                    || { _err "❌ brew uninstall failed: $pkg"; }
            else
                /opt/homebrew/bin/brew uninstall --ignore-dependencies "$pkg" &>/dev/null \
                    && _out "✅ brew uninstall: $pkg" \
                    || { _err "❌ brew uninstall failed: $pkg"; _err "· Re-run with --verbose for details."; }
            fi
        fi
    else
        _out "· Not installed via brew (skip): $pkg"
    fi
}

_pip_uninstall() {
    local pkg="$1"
    if /usr/bin/pip3 show "$pkg" &>/dev/null 2>&1; then
        if [[ "$DRY_RUN" -eq 1 ]]; then
            _out "· Would pip3 uninstall: $pkg"
        else
            if [[ "$VERBOSE" -eq 1 ]]; then
                /usr/bin/pip3 uninstall -y "$pkg" --break-system-packages \
                    && _out "✅ pip3 uninstall: $pkg" \
                    || _out "· pip3 uninstall no-op: $pkg"
            else
                /usr/bin/pip3 uninstall -y "$pkg" --break-system-packages &>/dev/null \
                    && _out "✅ pip3 uninstall: $pkg" \
                    || _out "· pip3 uninstall no-op: $pkg"
            fi
        fi
    else
        _out "· Not installed globally (skip): $pkg"
    fi
}

_zshrc_clean() {
    local zshrc="$HOME/.zshrc"
    if [[ ! -f "$zshrc" ]]; then
        _out "· ~/.zshrc not found (skip)"
        return
    fi

    # Catches: normal PATH lines, split PATH lines (export PATH= on one line,
    # value on next), and ais_* alias lines
    local ais_count
    ais_count=$(/usr/bin/grep -cE 'alias ais_|export PATH.*HOME/bin|export PATH=$|"[$]HOME/bin' "$zshrc" 2>/dev/null || true)

    if [[ "$ais_count" -eq 0 ]]; then
        _out "· No ais_* aliases or ~/bin PATH found in ~/.zshrc (skip)"
        return
    fi

    if [[ "$DRY_RUN" -eq 1 ]]; then
        _out "· Would remove $ais_count line(s) from ~/.zshrc:"
        /usr/bin/grep -nE 'alias ais_|export PATH.*HOME/bin|export PATH=$|"[$]HOME/bin' "$zshrc" | while IFS= read -r line; do
            _out "  $line"
        done
    else
        /bin/cp "$zshrc" "${zshrc}.bak_ais_clean_$(/bin/date +%Y%m%d_%H%M%S)"
        /usr/bin/sed -i.tmp -E '/^alias ais_/d' "$zshrc"
        /usr/bin/sed -i.tmp -E '/^export PATH=.*HOME\/bin/d' "$zshrc"
        /usr/bin/sed -i.tmp -E '/^export PATH=$/d' "$zshrc"
        /usr/bin/sed -i.tmp -E '/^"\$HOME\/bin:\$PATH"/d' "$zshrc"
        /bin/rm -f "${zshrc}.tmp"
        _out "✅ Removed $ais_count ais_*/PATH line(s) from ~/.zshrc"
        _out "· Backup written: ${zshrc}.bak_ais_clean_*"
    fi
}

_launchagent_clean() {
    local plist="$HOME/Library/LaunchAgents/com.aistudio.launcher.plist"
    if [[ -f "$plist" ]]; then
        if [[ "$DRY_RUN" -eq 1 ]]; then
            _out "· Would unload + remove: com.aistudio.launcher.plist"
        else
            /bin/launchctl unload "$plist" 2>/dev/null || true
            rm -f "$plist"
            _out "✅ Launch Agent unloaded + removed"
        fi
    else
        _out "· Launch Agent plist not found (skip)"
    fi
}

# ── Header (§1, STD CLI Output) ───────────────────────────────────────────────
printf "${BOLD}[%s v%s — %s]${RESET}\n" "$SCRIPT_NAME" "$VERSION" "$DESCRIPTION"

if [[ "$DRY_RUN" -eq 1 ]];       then _out "ℹ Dry run — nothing will be removed"; fi
if [[ "$REMOVE_MODELS" -eq 1 ]]; then _out "ℹ --remove-models — Ollama models will also be removed"; fi

# ── 1. Ollama ─────────────────────────────────────────────────────────────────
_sep "1. Ollama (brew)"
_brew_uninstall "ollama"

# ── 2. Ollama models ──────────────────────────────────────────────────────────
_sep "2. Ollama models"
if [[ "$REMOVE_MODELS" -eq 1 ]]; then
    _remove "$HOME/.ollama" "~/.ollama/ (all models + config)"
else
    _out "· Skipped — use --remove-models to include"
    _out "· Models live at ~/.ollama/models/ (~8–20GB)"
fi

# ── 3. Qdrant binary ──────────────────────────────────────────────────────────
_sep "3. Qdrant binary"
_remove "$HOME/bin/qdrant" "~/bin/qdrant"

# ── 4. Qdrant storage ─────────────────────────────────────────────────────────
_sep "4. Qdrant storage"
_remove "$HOME/qdrant_storage" "~/qdrant_storage/ (all collections + WAL)"

# ── 5. Python venv ────────────────────────────────────────────────────────────
_sep "5. Python venv"
_remove "$HOME/Developer/AIStudio/.venv" "~/Developer/AIStudio/.venv/"

# ── 6. Global pip packages ────────────────────────────────────────────────────
_sep "6. Global pip packages"
_pip_uninstall "cairosvg"
_pip_uninstall "weasyprint"
_pip_uninstall "sentence-transformers"

# ── 7. ~/.zshrc ───────────────────────────────────────────────────────────────
_sep "7. ~/.zshrc aliases + PATH"
_zshrc_clean

# ── 8. Launch Agent + app bundle + Desktop symlink ───────────────────────────
_sep "8. Launch Agent + app bundle + Desktop symlink"
_launchagent_clean
_remove "$HOME/Applications/AIStudio.app" "~/Applications/AIStudio.app"
_remove "$HOME/Desktop/AIStudio" "~/Desktop/AIStudio (symlink)"

# ── Done (§7, STD CLI Output) ─────────────────────────────────────────────────
_out ""
if [[ "$DRY_RUN" -eq 1 ]]; then
    _out "✅ Dry run complete — re-run without --dry-run to apply."
else
    _out "✅ AIStudio library artifacts removed."
    _out "· Next: source ~/.zshrc"
    _out "· Then: git clone git@github.com:mbarberony/AIStudio.git"
    _out "· Then: follow QUICKSTART.md from Step 1"
fi
