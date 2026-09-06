"""
Unit tests for the v3.9.0 Electron ("_N") de-fork path in `urc.deploy_ops`.

VERSION = "1.0.0"

⛔ WHY THIS FILE EXISTS. On 2026-08-23 a byte-exact workbook deployed as
`WIP - KRR - File Usage Tracking_4.xlsx` — a FOURTH copy beside the original rather than
an update of it. Third recorded instance on that one file. The hash was right every time;
the NAME was wrong, and hash-checking is structurally blind to that.

⭐ These tests cover the guard boundaries, not just the happy path — a de-fork that fires
when it should not is worse than the bug it fixes, because it OVERWRITES a real file.

Partial cover for AIStudio_594 (unit tests for deploy_ops resolvers).
Run: .venv/bin/python3 -m pytest tests/test_deploy_ops_defork.py -q
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from urc.deploy_ops import _defork, canonical_name, strip_electron_fork  # noqa: E402


# ── strip_electron_fork: the pure string layer ───────────────────────────────


@pytest.mark.parametrize(
    "given,expected",
    [
        # the bug this was written for
        ("WIP - KRR - File Usage Tracking_4.xlsx", "WIP - KRR - File Usage Tracking.xlsx"),
        ("notes_2.md", "notes.md"),
        ("a_1.py", "a.py"),
        ("notes_20.md", "notes.md"),  # upper bound, inclusive
        # ── must NOT strip ──
        ("notes_0.md", "notes_0.md"),  # counters start at 1
        ("notes_21.md", "notes_21.md"),  # above the counter range
        ("notes_2026.md", "notes_2026.md"),  # 4 digits — a year, not a counter
        ("part_99.csv", "part_99.csv"),  # 99 > 20
        ("archive.tar.gz", "archive.tar.gz"),  # no suffix at all
        ("install_ops", "install_ops"),  # extensionless
        ("_4.xlsx", "_4.xlsx"),  # nothing left if stripped — refuse
        ("foo (3).md", "foo (3).md"),  # Safari's form is canonical_name's job
    ],
)
def test_strip_electron_fork(given: str, expected: str) -> None:
    assert strip_electron_fork(given) == expected


# ── canonical_name: must be UNCHANGED by v3.9.0 ──────────────────────────────
# It has 14 call sites. A regression here is a repo-wide misroute, so it is pinned.


@pytest.mark.parametrize(
    "given,expected",
    [
        ("rag_studio (1).html", "rag_studio.html"),
        ("BUNDLE - JOB (3).zip", "BUNDLE - JOB.zip"),
        ("PIPELINE - 2026-06-20T155951.759.md", "PIPELINE.md"),
        ("gitignore.txt", ".gitignore"),
        # ⭐ the dated-file suffix must SURVIVE — it has no 'T' and is part of the name
        (
            "SESS - KRR - Session Summary - 2026-08-23 - 1320.md",
            "SESS - KRR - Session Summary - 2026-08-23 - 1320.md",
        ),
        # ⭐ canonical_name deliberately does NOT strip '_N' — that is _defork's call
        ("WIP - KRR - File Usage Tracking_4.xlsx", "WIP - KRR - File Usage Tracking_4.xlsx"),
    ],
)
def test_canonical_name_unchanged(given: str, expected: str) -> None:
    assert canonical_name(given) == expected


# ── _defork: the guarded layer ───────────────────────────────────────────────


def _manifest(glob_pattern: str = "meta/krr/wip/WIP - KRR - *") -> dict:
    """Minimal manifest routing anything matching the glob into meta/krr/wip/."""
    return {
        "entries": [
            {
                "type": "glob_all",
                "glob": glob_pattern,
                "deploy_to": "meta/krr/wip",
                "status": "active",
            }
        ]
    }


@pytest.fixture()
def repo(tmp_path: Path) -> Path:
    (tmp_path / "meta" / "krr" / "wip").mkdir(parents=True)
    return tmp_path


FORKED = "WIP - KRR - File Usage Tracking_4.xlsx"
CLEAN = "WIP - KRR - File Usage Tracking.xlsx"


def test_defork_collapses_when_the_original_is_there(repo: Path) -> None:
    """The bug case: `_4` arrives, the un-suffixed file already exists → collapse."""
    (repo / "meta/krr/wip" / CLEAN).write_bytes(b"old")
    assert _defork(FORKED, _manifest(), repo) == CLEAN


def test_defork_leaves_it_alone_when_there_is_nothing_to_update(repo: Path) -> None:
    """Guard (d): no un-suffixed file at the destination → this is not a fork."""
    assert _defork(FORKED, _manifest(), repo) == FORKED


def test_defork_leaves_a_real_tracked_underscore_file_alone(repo: Path) -> None:
    """⭐ Guard (c), the dangerous case. `X_4` is itself a tracked file — redeploying it
    must NOT overwrite `X`, even though `X` also exists beside it."""
    (repo / "meta/krr/wip" / CLEAN).write_bytes(b"clean")
    (repo / "meta/krr/wip" / FORKED).write_bytes(b"legitimately named _4")
    assert _defork(FORKED, _manifest(), repo) == FORKED


def test_defork_is_a_no_op_without_a_suffix(repo: Path) -> None:
    (repo / "meta/krr/wip" / CLEAN).write_bytes(b"x")
    assert _defork(CLEAN, _manifest(), repo) == CLEAN


def test_defork_respects_the_counter_range(repo: Path) -> None:
    """`_2026` is a year. Even with the stripped file present, it must not fire."""
    (repo / "meta/krr/wip" / "WIP - KRR - Thing.md").write_bytes(b"x")
    assert (
        _defork("WIP - KRR - Thing_2026.md", _manifest(), repo) == "WIP - KRR - Thing_2026.md"
    )


def test_defork_does_not_fire_when_the_name_routes_nowhere(repo: Path) -> None:
    """No manifest route and no repo match → resolve_destination returns None → no-op."""
    assert _defork("Unrouted Thing_3.md", _manifest(), repo) == "Unrouted Thing_3.md"
