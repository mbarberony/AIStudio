"""AIStudio_1031 — HOWTO ⊂ HOWTO_OPS subset-invariant guard.

HOWTO_OPS.md is the master; HOWTO.md is its user-facing derivation (strip the
`**[OPS]**`-tagged sections). The 2026-07-12 session found user-facing sections
(Query Settings incl. the renamed "Relevance Threshold", Understanding Citations,
Upgrading) living ONLY in the derived HOWTO.md — the subset invariant had
silently broken. This test locks the fix and catches the regression class:
every user-facing section in HOWTO.md maps to a section in the HOWTO_OPS master,
the mirrored anchors appear in BOTH files, and the dead threshold labels
(AIStudio_1015) stay dead.

HOWTO_OPS.md is gitignored (lives at meta/reference/), so this test SKIPS
gracefully where the master is absent (CI / civilian clone) — same pattern as
tests/test_model_fit.py's optional-dependency skip.
"""
import re
from pathlib import Path

import pytest


def _repo_root():
    for parent in Path(__file__).resolve().parents:
        if (parent / "HOWTO.md").exists():
            return parent
    return None


def _read_first(root, *rel_paths):
    if root is None:
        return None
    for rel in rel_paths:
        p = root / rel
        if p.exists():
            return p.read_text(encoding="utf-8")
    return None


ROOT = _repo_root()
HOWTO = _read_first(ROOT, "HOWTO.md")
# Beast layout: meta/reference/. Bundle layout: reference/. Try both.
HOWTO_OPS = _read_first(ROOT, "meta/reference/HOWTO_OPS.md", "reference/HOWTO_OPS.md")

pytestmark = pytest.mark.skipif(
    not HOWTO or not HOWTO_OPS,
    reason="HOWTO.md and/or HOWTO_OPS.md not present (gitignored master absent in CI/civilian clone)",
)

# Sections that MUST be mirrored master↔derived (the ones that broke).
MIRRORED_ANCHORS = ["## Query Settings", "## Understanding Citations", "## Upgrading AIStudio"]

# The _1015 rename: the user-facing label is "Relevance Threshold"; the old
# labels must not resurface as content (changelog HTML comments excluded).
DEAD_LABELS = ["Score Threshold", "Minimum Score"]

# Legitimate master→derived section renames (documented, NOT violations).
# HOWTO.md title -> HOWTO_OPS master title (None = master scatters it, e.g. troubleshooting).
KNOWN_RENAMES = {
    "Using AIStudio": "User Commands (ais_*)",
    "Installing and Managing LLMs": "Updating LLM Options",
    "Benchmark & Corpus Testing": "Benchmark",
    "Troubleshooting": None,
}


def _strip_html_comments(text):
    return re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)


def _h2_sections(text):
    """Return list of (title, is_ops_tagged) for each `## ` header (not `###`)."""
    out = []
    for line in text.splitlines():
        m = re.match(r"^##\s+(.*)$", line)
        if not m:
            continue
        title = m.group(1).strip()
        is_ops = title.endswith("**[OPS]**")
        if is_ops:
            title = title[: -len("**[OPS]**")].strip()
        out.append((title, is_ops))
    return out


@pytest.mark.parametrize("anchor", MIRRORED_ANCHORS)
def test_mirrored_section_in_both(anchor):
    assert anchor in HOWTO, f"{anchor!r} missing from HOWTO.md"
    assert anchor in HOWTO_OPS, (
        f"{anchor!r} is in HOWTO.md but MISSING from the HOWTO_OPS master "
        f"— subset invariant broken (AIStudio_1031). Port it up (untagged)."
    )


def test_relevance_threshold_label_in_both():
    assert "Relevance Threshold" in HOWTO, "HOWTO.md lost the Relevance Threshold label"
    assert "Relevance Threshold" in HOWTO_OPS, "HOWTO_OPS.md lost the Relevance Threshold label"


@pytest.mark.parametrize("label", DEAD_LABELS)
def test_dead_threshold_labels_gone(label):
    for name, text in (("HOWTO.md", HOWTO), ("HOWTO_OPS.md", HOWTO_OPS)):
        assert label not in _strip_html_comments(text), (
            f"dead label {label!r} resurfaced in {name} — use 'Relevance Threshold' (AIStudio_1015)."
        )


def test_howto_sections_subset_of_ops_master():
    """Every ## section in HOWTO.md maps to a HOWTO_OPS section (direct or known rename)."""
    howto_secs = [t for t, _ in _h2_sections(HOWTO) if t.lower() != "contents"]
    ops_user_secs = {t for t, is_ops in _h2_sections(HOWTO_OPS) if not is_ops}
    missing = [
        s for s in howto_secs
        if s not in ops_user_secs and s not in KNOWN_RENAMES
    ]
    assert not missing, (
        f"HOWTO.md sections absent from the HOWTO_OPS master "
        f"(subset invariant, AIStudio_1031): {missing}. "
        f"Port them up (untagged) or register a documented rename in KNOWN_RENAMES."
    )
