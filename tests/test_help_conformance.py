"""
test_help_conformance.py — AIStudio Help System Conformance Tests
==================================================================

Verifies that:
1. Every command registered in bundle_manifest.yaml (install: user) has a
   ## <alias> section in ais_command_help.txt
2. Every command registered in bundle_manifest.yaml (install: operator) has a
   ## <alias> section in ais_command_help_ops.txt
3. ais_command_help.txt contains NO operator-only command sections (no ops leak)
4. Every registered script file exists on disk
5. zsh scripts (#!/usr/bin/env zsh) must not use BASH_SOURCE[0] — use ${0:A:h}
6. Every registered script responds to --help (exit 0, non-empty output)
7. Every registered script responds to --version (exit 0, prints version string)
8. ais_help <cmd> resolves correctly for all user commands
9. ais_help_ops <cmd> resolves correctly for all operator commands

All tests are unit/subprocess only — no running services required.
Runs as part of ais_test (pytest -m "not integration").

Usage:
    pytest tests/test_help_conformance.py -v
    pytest tests/test_help_conformance.py -v -k "test_user"
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest
import yaml

# ---------------------------------------------------------------------------
# Fixtures and helpers
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).parent.parent

# Operator-only commands: install: operator in manifest (including historical
# exceptions that lack _ops suffix: ais_deploy, ais_commit, etc.)
# Derived from bundle_manifest.yaml — do not hardcode here.


def _load_manifest() -> dict:
    manifest_path = REPO_ROOT / "meta" / "bundle_manifest.yaml"
    if not manifest_path.exists():
        pytest.skip(f"bundle_manifest.yaml not found at {manifest_path} — meta/ not present")
    with open(manifest_path) as f:
        return yaml.safe_load(f)


def _get_commands(install_tier: str) -> list[dict]:
    """Return all entries with a given install tier that have an alias."""
    manifest = _load_manifest()
    return [
        e
        for e in manifest.get("entries", [])
        if e.get("install") == install_tier and e.get("alias")
    ]


def _parse_help_sections(filepath: Path) -> set[str]:
    """Return set of command names that have a ## <name> section in the file."""
    if not filepath.exists():
        return set()
    sections = set()
    for line in filepath.read_text().splitlines():
        if line.startswith("## "):
            sections.add(line[3:].strip())
    return sections


def _run_cmd(args: list[str], timeout: int = 10) -> subprocess.CompletedProcess:
    """Run a command with the repo venv activated."""
    return subprocess.run(
        args,
        capture_output=True,
        text=True,
        timeout=timeout,
        cwd=str(REPO_ROOT),
    )


# ---------------------------------------------------------------------------
# Derived data — computed once at module load
# ---------------------------------------------------------------------------

USER_COMMANDS = _get_commands("user")
OPERATOR_COMMANDS = _get_commands("operator")
ALL_ALIASED_COMMANDS = USER_COMMANDS + OPERATOR_COMMANDS

USER_HELP_FILE = REPO_ROOT / "ais_command_help.txt"
OPS_HELP_FILE = REPO_ROOT / "ais_command_help_ops.txt"

USER_HELP_SECTIONS = _parse_help_sections(USER_HELP_FILE)
OPS_HELP_SECTIONS = _parse_help_sections(OPS_HELP_FILE)

# Operator aliases — used for leak detection
OPERATOR_ALIASES = {e["alias"] for e in OPERATOR_COMMANDS}
USER_ALIASES = {e["alias"] for e in USER_COMMANDS}


# ---------------------------------------------------------------------------
# 1. Help file section coverage — user commands
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.parametrize("entry", USER_COMMANDS, ids=lambda e: e["alias"])
def test_user_command_has_help_section(entry: dict) -> None:
    """Every user command must have a ## <alias> section in ais_command_help.txt."""
    alias = entry["alias"]
    assert USER_HELP_FILE.exists(), (
        f"ais_command_help.txt not found at {USER_HELP_FILE}. Run: ais_update_help_ops --meta-only"
    )
    assert alias in USER_HELP_SECTIONS, (
        f"No '## {alias}' section found in ais_command_help.txt. "
        f"Add it to ais_command_help_ops.txt then run: ais_update_help_ops --meta-only"
    )


# ---------------------------------------------------------------------------
# 2. Help file section coverage — operator commands
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.parametrize("entry", OPERATOR_COMMANDS, ids=lambda e: e["alias"])
def test_operator_command_has_help_section(entry: dict) -> None:
    """Every operator command must have a ## <alias> section in ais_command_help_ops.txt."""
    alias = entry["alias"]
    assert OPS_HELP_FILE.exists(), f"ais_command_help_ops.txt not found at {OPS_HELP_FILE}."
    assert alias in OPS_HELP_SECTIONS, (
        f"No '## {alias}' section found in ais_command_help_ops.txt. Add the section and redeploy."
    )


# ---------------------------------------------------------------------------
# 3. No operator commands leaked into user help file
# ---------------------------------------------------------------------------


@pytest.mark.unit
def test_no_operator_leak_in_user_help() -> None:
    """ais_command_help.txt must not contain any operator-only command sections."""
    if not USER_HELP_FILE.exists():
        pytest.skip("ais_command_help.txt not present")
    leaked = USER_HELP_SECTIONS & OPERATOR_ALIASES
    assert not leaked, (
        f"Operator command(s) found in ais_command_help.txt (user file): {sorted(leaked)}. "
        f"These must only appear in ais_command_help_ops.txt. "
        f"Regenerate: ais_update_help_ops --meta-only"
    )


# ---------------------------------------------------------------------------
# 4. Script files exist on disk
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.parametrize("entry", ALL_ALIASED_COMMANDS, ids=lambda e: e["alias"])
def test_script_file_exists(entry: dict) -> None:
    """Every registered script must exist on disk at its declared path."""
    script_path = REPO_ROOT / entry["path"]
    # Operator scripts live in scripts/ (gitignored) — skip if not present
    # rather than fail (they travel via BUNDLE, not git)
    install = entry.get("install", "")
    if not script_path.exists() and install == "operator":
        pytest.skip(
            f"Operator script {entry['path']} not on disk — "
            f"restore from BUNDLE: ais_restore_scripts"
        )
    assert script_path.exists(), (
        f"Script not found: {script_path}. Deploy it: ais_deploy {entry['path']}"
    )


# ---------------------------------------------------------------------------
# 5. zsh scripts must use ${0:A:h} not BASH_SOURCE[0] (AIStudio_499)
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.parametrize("entry", ALL_ALIASED_COMMANDS, ids=lambda e: e["alias"])
def test_zsh_script_no_bash_source(entry: dict) -> None:
    """zsh scripts (#!/usr/bin/env zsh shebang) must not use BASH_SOURCE.

    BASH_SOURCE is bash-only — undefined in zsh. Use ${0:A:h} instead.
    Per STD - AIStudio - Shell Coding Conventions v1.0.1 §2.

    Shell type is read from manifest shell: field if present; falls back to
    reading the shebang line from the script file.
    """
    script_path = REPO_ROOT / entry["path"]
    if not script_path.exists():
        pytest.skip(f"Script not on disk: {entry['path']}")

    # Prefer manifest shell: field for explicit skip messages
    manifest_shell = entry.get("shell", "")

    if manifest_shell == "bash":
        pytest.skip(
            f"{entry['alias']}: shell: bash per manifest — "
            f"BASH_SOURCE[0] is correct for bash scripts"
        )
    if manifest_shell == "python":
        pytest.skip(f"{entry['alias']}: shell: python per manifest — not applicable")

    # For entries without shell: field, fall back to reading the shebang
    if not manifest_shell:
        # Only check shell scripts — skip Python scripts by extension
        if script_path.suffix != ".sh" and script_path.suffix != "":
            pytest.skip(f"Not a shell script (no manifest shell: field): {entry['path']}")

        content = script_path.read_text(encoding="utf-8", errors="replace")
        first_line = content.splitlines()[0] if content.splitlines() else ""

        if "bash" in first_line:
            pytest.skip(
                f"{entry['alias']}: bash shebang detected — "
                f"BASH_SOURCE[0] is correct (add shell: bash to manifest to make explicit)"
            )
        if "zsh" not in first_line:
            pytest.skip(
                f"{entry['alias']}: not a zsh script (shebang: {first_line!r}) — "
                f"add shell: field to manifest entry"
            )
    else:
        # manifest_shell == "zsh" — read content for assertion
        content = script_path.read_text(encoding="utf-8", errors="replace")

    assert "BASH_SOURCE" not in content, (
        f"{entry['alias']} uses BASH_SOURCE in a zsh script ({entry['path']}). "
        f"Replace with ${{0:A:h}} per STD - AIStudio - Shell Coding Conventions §2. "
        f'Example: SCRIPT_DIR="${{0:A:h}}"'
    )


# ---------------------------------------------------------------------------
# 6. --help flag — exit 0, non-empty output
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.parametrize("entry", ALL_ALIASED_COMMANDS, ids=lambda e: e["alias"])
def test_script_help_flag(entry: dict) -> None:
    """Every registered script must respond to --help with exit 0 and non-empty output."""
    script_path = REPO_ROOT / entry["path"]
    if not script_path.exists():
        pytest.skip(f"Script not on disk: {entry['path']}")

    result = _run_cmd([str(script_path), "--help"])
    output = (result.stdout + result.stderr).strip()

    assert result.returncode == 0, (
        f"{entry['alias']} --help returned exit code {result.returncode}. Output: {output[:200]}"
    )
    assert output, (
        f"{entry['alias']} --help produced no output. "
        f"Check _show_help() implementation per STD - AIStudio - CLI Script Help."
    )


# ---------------------------------------------------------------------------
# 7. --version flag — exit 0, version string in output
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.parametrize("entry", ALL_ALIASED_COMMANDS, ids=lambda e: e["alias"])
def test_script_version_flag(entry: dict) -> None:
    """Every registered script must respond to --version with exit 0 and a version string."""
    script_path = REPO_ROOT / entry["path"]
    if not script_path.exists():
        pytest.skip(f"Script not on disk: {entry['path']}")

    result = _run_cmd([str(script_path), "--version"])
    output = (result.stdout + result.stderr).strip()

    assert result.returncode == 0, (
        f"{entry['alias']} --version returned exit code {result.returncode}. Output: {output[:200]}"
    )
    # Version string must contain a digit (e.g. "1.0.0", "v1.2.3", "ais_start v1.6.12")
    import re

    assert re.search(r"\d+\.\d+", output), (
        f"{entry['alias']} --version output doesn't look like a version string: {output!r}. "
        f"Expected format: '<command> v<N>.<N>' per STD - AIStudio - CLI Output."
    )


# ---------------------------------------------------------------------------
# 8. ais_help <cmd> resolves user commands correctly
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.parametrize("entry", USER_COMMANDS, ids=lambda e: e["alias"])
def test_ais_help_resolves_user_command(entry: dict) -> None:
    """ais_help <cmd> must return exit 0 and output matching the help section."""
    ais_help = REPO_ROOT / "ais_help.sh"
    if not ais_help.exists():
        pytest.skip("ais_help.sh not on disk")
    if not USER_HELP_FILE.exists():
        pytest.skip("ais_command_help.txt not present")
    if entry["alias"] not in USER_HELP_SECTIONS:
        pytest.skip(f"No section for {entry['alias']} in help file — covered by test 1")

    result = _run_cmd([str(ais_help), entry["alias"]])
    output = (result.stdout + result.stderr).strip()

    assert result.returncode == 0, (
        f"ais_help {entry['alias']} returned exit code {result.returncode}. Output: {output[:200]}"
    )
    assert entry["alias"] in output, (
        f"ais_help {entry['alias']} output doesn't mention the command name. Output: {output[:200]}"
    )
    # Must not show the "not found" error message
    assert "No help found" not in output, (
        f"ais_help {entry['alias']} returned 'No help found' — "
        f"HELP_FILE path may be wrong (check SCRIPT_DIR in ais_help.sh)"
    )


# ---------------------------------------------------------------------------
# 9. ais_help_ops <cmd> resolves operator commands correctly
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.parametrize("entry", OPERATOR_COMMANDS, ids=lambda e: e["alias"])
def test_ais_help_ops_resolves_operator_command(entry: dict) -> None:
    """ais_help_ops <cmd> must return exit 0 and output matching the ops help section."""
    ais_help_ops = REPO_ROOT / "ais_help_ops.sh"
    if not ais_help_ops.exists():
        pytest.skip("ais_help_ops.sh not on disk")
    if not OPS_HELP_FILE.exists():
        pytest.skip("ais_command_help_ops.txt not present")
    if entry["alias"] not in OPS_HELP_SECTIONS:
        pytest.skip(f"No section for {entry['alias']} in ops help file — covered by test 2")

    result = _run_cmd([str(ais_help_ops), entry["alias"]])
    output = (result.stdout + result.stderr).strip()

    assert result.returncode == 0, (
        f"ais_help_ops {entry['alias']} returned exit code {result.returncode}. "
        f"Output: {output[:200]}"
    )
    assert entry["alias"] in output, (
        f"ais_help_ops {entry['alias']} output doesn't mention the command name. "
        f"Output: {output[:200]}"
    )
    assert "No help found" not in output, (
        f"ais_help_ops {entry['alias']} returned 'No help found' — "
        f"check SCRIPT_DIR in ais_help_ops.sh"
    )
