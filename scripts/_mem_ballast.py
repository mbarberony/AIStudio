# scripts/_mem_ballast.py
# Version: 1.3.1
# Changelog: 1.3.1 — restore the "pages wired down" matcher. The v1.3.0 vocabulary rename hit the
#   literal that parses memory_pressure output, so already-locked memory silently read 0 GB and the
#   suggested target was wrong by the amount the OS holds. A rename must not touch another system's
#   strings; the line now says so.
# Version: 1.3.0
# Changelog: 1.3.0 — vocabulary: "wired" -> "locked" throughout, user-facing and internal. Wired is
#   kernel jargon; locked says what happens (the system cannot reclaim it). Also: when a ballast
#   process is holding the memory, the error now NAMES it instead of attributing it to the OS — a
#   stray 85GB holder read as "the system", which sent the diagnosis in the wrong direction.
# Changelog: 1.2.0 — the lock limit is GLOBAL, not per-process: memory already locked by the OS and
#   running services counts against it. v1.1.0 compared the request against the raw cap and so
#   reported a reachable target that was not (109GB cap, 104GB request, still refused). Headroom is
#   now limit - already_locked - margin, and the suggested target is computed from that.
# Changelog: 1.1.0 — mlock failure now reads as guidance rather than an errno. macOS caps per-process
#   locked memory (EAGAIN/errno 35), so on a 128GB box a 24GB target asks to lock 104GB and is refused.
#   The error now reports the machine's actual lock ceiling and the smallest target it permits.
# Changelog: 1.0.0 — AIStudio_1058: shared memory-ballast utility. Wires RAM with mlock(2) so a
#   large machine can be exercised as if it had less, making real memory scarcity reproducible on
#   the 128 GB box instead of only on the 24 GB one. Consumed by bench.py (--mem) and, once a
#   holder-process lifecycle exists, by ais_start.
#
#   WHY mlock AND NOTHING ELSE. Five prior methods failed, all for one reason: macOS reports
#   "free" memory as everything it could reclaim, and an ordinary allocation is always reclaimable
#   (swappable), so it never moves the reading the fit guard consults. Zeroed pages are absorbed by
#   the compressor; os.urandom is too slow; incompressible random pages get swapped out; and
#   `memory_pressure -p` is jetsam-killed at aggressive targets. LOCKED memory is the only kind the
#   OS cannot take back — hence mlock. Measured 2026-07-19 on M4 Max/128 GB: 20 GB locked moved the
#   reading 95% -> 79%, no sudo required.
"""Constrain visible memory by locking RAM.

The unit of the public API is the machine you want to *emulate*, not the amount
to wire: ``lock_to_target(24)`` makes a 128 GB machine behave like a 24 GB one.
The locked amount is derived (physical - target), so the same call means the same
thing on every machine.
"""

from __future__ import annotations

import ctypes
import mmap
import os
import subprocess
import sys

GIB = 1024**3

# Minimum emulated machine size. A target below this leaves too little for macOS
# itself; locked memory cannot be swapped, so there is no escape valve. Env
# AISTUDIO_MEM_FLOOR_GB. Mirrored as a documented constant in app/config.py —
# the backend declares it for discoverability, this module reads the env directly
# because it must work standalone (ais_start/bench do not import the app package).
FLOOR_GB = float(os.getenv("AISTUDIO_MEM_FLOOR_GB", "8"))
WARN_GB = 16.0


class BallastError(RuntimeError):
    """Raised when a ballast cannot be established. Never returned silently."""


SAFETY_MARGIN_BYTES = 2 * GIB  # never lock right up to the ceiling


def locked_now_bytes() -> int | None:
    """Memory the system already has locked. Counts against the same global cap."""
    try:
        out = subprocess.run(["memory_pressure"], capture_output=True,
                             text=True, check=True).stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None
    page_size = locked_pages = None
    for line in out.splitlines():
        low = line.lower()
        if "page size of" in low:
            tail = low.split("page size of", 1)[1]
            digits = "".join(c for c in tail if c.isdigit())
            page_size = int(digits) if digits else None
        # NOTE: Apple's literal wording. This string is the OS's, not ours — it must not be
        # renamed with the rest of the locked/wired vocabulary (v1.3.0 did exactly that and
        # silently reported 0 GB already locked, corrupting every derived figure).
        elif "pages wired down" in low:
            digits = "".join(c for c in line if c.isdigit())
            locked_pages = int(digits) if digits else None
    if page_size and locked_pages:
        return page_size * locked_pages
    return None


def ballast_holders() -> list[str]:
    """PIDs of ballast processes currently holding memory. Empty if none."""
    try:
        out = subprocess.run(["pgrep", "-f", "ballast"], capture_output=True,
                             text=True, check=False).stdout.strip()
    except FileNotFoundError:
        return []
    me = str(os.getpid())
    return [pid for pid in out.split() if pid and pid != me]


def lock_headroom_bytes() -> int | None:
    """How much MORE can be locked right now: cap - already locked - margin."""
    limit = lock_limit_bytes()
    if not limit:
        return None
    already = locked_now_bytes() or 0
    return max(0, limit - already - SAFETY_MARGIN_BYTES)


def lock_limit_bytes() -> int | None:
    """How much memory this machine will let one process wire. None if unreadable."""
    for key in ("vm.global_user_wire_limit", "vm.user_wire_limit"):
        try:
            out = subprocess.run(["sysctl", "-n", key], capture_output=True,
                                 text=True, check=True).stdout.strip()
            if out.isdigit() and int(out) > 0:
                return int(out)
        except (subprocess.CalledProcessError, FileNotFoundError):
            continue
    return None


def physical_ram_bytes() -> int:
    """Total installed RAM, from sysctl. Raises rather than guessing."""
    try:
        out = subprocess.run(
            ["sysctl", "-n", "hw.memsize"], capture_output=True, text=True, check=True
        ).stdout.strip()
        return int(out)
    except (subprocess.CalledProcessError, FileNotFoundError, ValueError) as exc:
        raise BallastError(f"could not read hw.memsize: {exc}") from exc


def free_pct() -> int | None:
    """OS-reported free memory percentage — the same figure the fit guard reads.

    Returns None if unavailable; callers must treat None as 'unknown', never as 0.
    """
    try:
        out = subprocess.run(
            ["memory_pressure"], capture_output=True, text=True, check=True
        ).stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None
    for line in out.splitlines():
        if "free percentage" in line.lower():
            digits = "".join(c for c in line if c.isdigit())
            return int(digits) if digits else None
    return None


class Ballast:
    """A held block of locked memory. Release with .release() or use as a context manager."""

    def __init__(self, buf: mmap.mmap, libc: ctypes.CDLL, addr: int, nbytes: int) -> None:
        self._buf = buf
        self._libc = libc
        self._addr = addr
        self.locked_bytes = nbytes
        self._released = False

    @property
    def locked_gb(self) -> float:
        return self.locked_bytes / GIB

    def release(self) -> None:
        if self._released:
            return
        self._libc.munlock(ctypes.c_void_p(self._addr), ctypes.c_size_t(self.locked_bytes))
        self._buf.close()
        self._released = True

    def __enter__(self) -> Ballast:
        return self

    def __exit__(self, *exc: object) -> None:
        self.release()


def lock_to_target(target_gb: float) -> Ballast | None:
    """Wire memory so that roughly ``target_gb`` remains visible to the system.

    Returns None when no ballast is needed (target >= physical RAM) — that is a
    legitimate no-op on a machine already at or below the target, not a failure.
    Raises BallastError on anything else, so a failed ballast can never be
    mistaken for a successful one (the _1050 antipattern).
    """
    if sys.platform != "darwin":
        raise BallastError("memory ballast is macOS-only (uses libc mlock via sysctl sizing)")
    if target_gb < FLOOR_GB:
        raise BallastError(
            f"target {target_gb:g} GB is below the {FLOOR_GB:g} GB floor — "
            "locked memory cannot be swapped, so the machine would have no headroom"
        )

    total = physical_ram_bytes()
    target_bytes = int(target_gb * GIB)
    if target_bytes >= total:
        return None

    nbytes = total - target_bytes
    before = free_pct()

    buf = mmap.mmap(-1, nbytes)
    libc = ctypes.CDLL("libc.dylib", use_errno=True)
    addr = ctypes.addressof(ctypes.c_char.from_buffer(buf))
    rc = libc.mlock(ctypes.c_void_p(addr), ctypes.c_size_t(nbytes))
    if rc != 0:
        err = ctypes.get_errno()
        buf.close()
        headroom = lock_headroom_bytes()
        holders = ballast_holders()
        if headroom:
            lowest = (total - headroom) / GIB
            raise BallastError(
                f"this machine cannot reserve {nbytes / GIB:.0f} GB right now.\n"
                f"  · macOS caps total reserved memory, and about "
                f"{(locked_now_bytes() or 0) / GIB:.0f} GB is already reserved by the system "
                f"and running services — leaving roughly {headroom / GIB:.0f} GB.\n"
                f"  · So the smallest machine you can emulate here is about "
                f"{lowest:.0f} GB — try --emulate-ram {lowest + 1:.0f} or higher."
                + (f"\n  · A ballast process is still holding memory (pid "
                   f"{', '.join(holders)}). Release it first: pkill -f ballast"
                   if holders else "")
            )
        raise BallastError(
            f"this machine would not reserve {nbytes / GIB:.0f} GB (system error {err}).\n"
            "  · Try a larger --emulate-ram value, which reserves less."
        )

    ballast = Ballast(buf, libc, addr, nbytes)

    # Verify the locking actually moved the reading the guard consults. A ballast
    # that allocates but does not register is indistinguishable from none at all,
    # and every prior method failed in exactly that way.
    after = free_pct()
    if before is not None and after is not None and after >= before:
        ballast.release()
        raise BallastError(
            f"locked {nbytes / GIB:.0f} GB but free memory did not move "
            f"({before}% -> {after}%) — the ballast had no effect"
        )
    return ballast


def describe(target_gb: float) -> str:
    """One-line preflight summary. Callers print this; the module never prints."""
    total_gb = physical_ram_bytes() / GIB
    if target_gb >= total_gb:
        return f"no ballast needed — this machine has {total_gb:.0f} GB"
    warn = "  ⚠️ very tight" if target_gb < WARN_GB else ""
    return (
        f"emulating a {target_gb:g} GB machine "
        f"({total_gb - target_gb:.0f} GB of {total_gb:.0f} GB locked){warn}"
    )
