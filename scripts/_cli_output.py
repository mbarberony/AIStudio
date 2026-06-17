#!/usr/bin/env python3
"""
_cli_output.py — Shared CLI output primitives for AIStudio operator commands.

The single source of the STD - AIStudio - CLI Output glyph vocabulary and the
processing-loop format. Imported as a sibling by the ops commands (download, entity/
glossary import, …) so download / enrich / ingest render identically:

    import _cli_output as cli   # when run via `python3 scripts/<cmd>.py`

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

v1.2.0 (2026-06-14): added list_item()/numbered_list()/bullet_list() — aligned sub-item
    rosters per CLI Output STD §9 (right-aligned marker field, stable text column across
    digit-widths, ordered/unordered sibling lists share a column). Tracks STD v2.5.0.

v1.2.1 (2026-06-14): added the VERSION code constant (911c) — urc_deploy's new no-VERSION
    warn (deploy_ops v3.4.0) surfaced that this versionless module printed no [v] on deploy.

NOT a command (underscore-prefixed, no alias) per Naming STD §14.
Version: 1.2.1
"""

from __future__ import annotations

import sys

VERSION = "1.2.1"  # single source of truth for urc_deploy's [v] tag (AIStudio_911c)

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


# ── Sub-item lists (STD - AIStudio - CLI Output §9) ─────────────────────────────
def list_item(text: str, *, index: int | None = None, total: int | None = None,
              indent: int = 2) -> None:
    """Render one aligned list line (STD §9). Ordered when `index` is given (renders
    "N."), unordered otherwise (renders "*"). The marker is right-aligned in a field
    sized by `total` (the largest index in the list), so the text column stays put as
    the count grows into multiple digits and ordered/unordered sibling lists share a
    text column. Pass `total` even for bullets so they align with a same-length
    numbered list."""
    width = len(str(total)) if total else 1            # digit-width of the largest index
    marker = f"{index:>{width}}." if index is not None else f"{'*':>{width + 1}}"
    print(f"{' ' * indent}{marker} {text}")


def numbered_list(items: list[str], *, indent: int = 2) -> None:
    """Render an ordered list with right-aligned numbers (STD §9)."""
    total = len(items)
    for i, text in enumerate(items, 1):
        list_item(text, index=i, total=total, indent=indent)


def bullet_list(items: list[str], *, indent: int = 2) -> None:
    """Render an unordered list whose text column aligns with a same-length numbered
    list (STD §9)."""
    total = len(items)
    for text in items:
        list_item(text, total=total, indent=indent)
