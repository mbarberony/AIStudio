#!/usr/bin/env python3
"""
_cli_output_ops.py — Shared CLI output primitives for AIStudio operator commands.

The single source of the STD - AIStudio - CLI Output glyph vocabulary and the
processing-loop format. Imported as a sibling by the ops commands (download, entity/
glossary import, …) so download / enrich / ingest render identically:

    import _cli_output_ops as cli   # when run via `python3 scripts/<cmd>.py`

Glyph vocabulary (foreground glyph on the default background; block only for hard fail):
    ok(...)           ✅              success, full / verified
    partial(...)      yellow ✓        succeeded but degraded — skip, fallback, name-search-
                                      not-LEI, Wikidata-partial (NOT a failure; no block)
    fail(...)         white ✗ / red   failure (block)
    fail_recover(...) yellow ✗        failure, recovery possible — see note (no block)
    info(...)         ·               passive info / auto-resolution bullet (was ℹ)

Structure:
    section("Resolve")              -> "--- Resolve"
    step("Resolving 20 row(s)")     -> "  ▶ Resolving 20 row(s)..."   (working; trailing …)
    done(ok, "Resolved 20/20")      -> "  ✅ Resolved 20/20"          (finished)

v1.1.0 (2026-06-13): partial glyph → yellow ✓, no block (was white-✓-on-yellow-block);
    info() bullet → `·` (was `ℹ`), unifying passive info + auto-resolution. Tracks CLI
    Output STD v2.4.0.

NOT a command (underscore-prefixed, no alias) per Naming STD §14.
Version: 1.1.0
"""

from __future__ import annotations

import sys

# ── ANSI ────────────────────────────────────────────────────────────────────────
# Colour only when stdout is a TTY; otherwise emit plain glyphs so piped/captured
# output (the ais_update_*_ops JSON-capture path) stays clean.
_TTY = sys.stdout.isatty()


def _wrap(code: str, text: str) -> str:
    return f"\033[{code}m{text}\033[0m" if _TTY else text


# Foreground glyph on the default (black) terminal background — no colored blocks except hard fail.
GLYPH_OK = "✅"                                  # success, full / verified
GLYPH_PARTIAL = _wrap("93", "✓")                 # bright-yellow ✓, no block (soft/degraded success)
GLYPH_FAIL = _wrap("97;101", " ✗ ")              # bright-white ✗ on bright-red block (hard failure)
GLYPH_FAIL_RECOVER = _wrap("93", "✗")            # bright-yellow ✗, no block (recoverable)

_TRIANGLE = "▶"


def section(name: str) -> None:
    """A top-level activity header: `--- Name`. No leading blank line (loops stay dense)."""
    print(f"--- {name}")


def step(msg: str, *, indent: int = 2) -> None:
    """An activity START — triangle + trailing ellipsis (work in progress)."""
    print(f"{' ' * indent}{_TRIANGLE} {msg}...", flush=True)


def info(msg: str, *, indent: int = 2) -> None:
    """A neutral declaration line — a `·` bullet (passive info / auto-resolution), not a
    success or failure. (Was `ℹ`; unified to `·` per CLI Output STD v2.4.0.)"""
    print(f"{' ' * indent}\u00b7 {msg}")


def done(glyph: str, msg: str, *, indent: int = 2) -> None:
    """An activity RESULT line, indented under its step."""
    print(f"{' ' * indent}{glyph} {msg}")


def ok(msg: str, *, indent: int = 2) -> None:
    done(GLYPH_OK, msg, indent=indent)


def partial(msg: str, *, indent: int = 2) -> None:
    done(GLYPH_PARTIAL, msg, indent=indent)


def fail(msg: str, *, indent: int = 2) -> None:
    done(GLYPH_FAIL, msg, indent=indent)


def fail_recover(msg: str, *, indent: int = 2) -> None:
    done(GLYPH_FAIL_RECOVER, msg, indent=indent)
