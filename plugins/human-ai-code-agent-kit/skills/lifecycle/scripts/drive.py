#!/usr/bin/env python3
"""Outer loop of a lifecycle run: start fresh agent sessions until the run stops.

Usage (from the repository root):
    drive.py --state-dir DIR [--max-stalled N] [--pause SECONDS]
             [--session-timeout SECONDS] [--notify CMD] -- SESSION_COMMAND...

The resume prompt is appended to SESSION_COMMAND as its last argument; the
session gets this driver's pid in LIFECYCLE_DRIVER_PID. Stops on the STOP file,
on a state other than running (checked after the first session), on a missing
state line, or after N stalled sessions in a row (unchanged state line,
non-zero exit, or a session killed at the timeout). Ctrl-C, SIGTERM and
SIGHUP end the running session's process group before the lock is released.
"""

from __future__ import annotations

import argparse
import contextlib
import datetime
import os
import shlex
import shutil
import signal
import subprocess
import sys
import time
from pathlib import Path

RESUME_PROMPT = (
    "Use the lifecycle skill to run one step for the project in the current "
    "directory: recover from its state directory, advance at most one step, "
    "persist the state, and exit."
)


def state_line(state_dir: Path) -> str | None:
    status = state_dir / "STATUS.md"
    if not status.exists():
        return None
    for line in status.read_text(encoding="utf-8").splitlines():
        if line.startswith("lifecycle:"):
            return line.strip()
    return None


def state_of(line: str) -> str:
    for token in line.split()[1:]:
        if token.startswith("state="):
            return token[len("state="):]
    return ""


def notify(command: str | None, message: str) -> None:
    print(message, flush=True)
    if command:
        # A failed notification must not end the run; its stderr stays visible.
        subprocess.run(shlex.split(command) + [message], check=False)


def acquire_lock(lock: Path) -> None:
    try:
        fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        pid = int(lock.read_text().strip())
        try:
            os.kill(pid, 0)
            alive = True
        except ProcessLookupError:
            alive = False
        except PermissionError:
            alive = True  # the process exists under another user
        if alive:
            sys.exit(f"another driver (pid {pid}) holds {lock}")
        lock.unlink()  # stale lock from a dead driver
        return acquire_lock(lock)
    os.write(fd, str(os.getpid()).encode())
    os.close(fd)


def end_session(proc: subprocess.Popen) -> None:
    """Terminate the session's process group: SIGTERM, then SIGKILL after 30 s."""
    with contextlib.suppress(ProcessLookupError):  # the group may already be gone
        os.killpg(proc.pid, signal.SIGTERM)
    try:
        proc.wait(timeout=30)
    except subprocess.TimeoutExpired:
        with contextlib.suppress(ProcessLookupError):
            os.killpg(proc.pid, signal.SIGKILL)
        proc.wait()


def run_session(command: list[str], out, timeout: float) -> str:
    """Run one session in its own process group; return its exit code or 'timeout'."""
    env = {**os.environ, "LIFECYCLE_DRIVER_PID": str(os.getpid())}
    proc = subprocess.Popen(command, stdout=out, stderr=subprocess.STDOUT, env=env, start_new_session=True)
    try:
        return str(proc.wait(timeout=timeout))
    except subprocess.TimeoutExpired:
        end_session(proc)
        return "timeout"
    except BaseException:
        # The driver is exiting (Ctrl-C, SIGTERM, SIGHUP): no session may outlive
        # driver.lock. A second signal must not cut this cleanup short.
        for sig in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP):
            signal.signal(sig, signal.SIG_IGN)
        end_session(proc)
        raise


def drive(state_dir: Path, command: list[str], max_stalled: int, pause: float, timeout: float, notify_cmd: str | None) -> str:
    log = state_dir / "driver.log"
    stalled = 0
    session = 0
    while True:
        if (state_dir / "STOP").exists():
            return "STOP file present"
        before = state_line(state_dir)
        if before is None:
            return "state line missing in STATUS.md"
        if session > 0 and state_of(before) != "running":
            return f"state is {state_of(before)}: {before}"
        session += 1
        with log.open("a", encoding="utf-8") as out:
            out.write(f"\n=== session {session} {datetime.datetime.now().isoformat(timespec='seconds')} ===\n")
            out.flush()
            code = run_session(command + [RESUME_PROMPT], out, timeout)
        after = state_line(state_dir)
        if after is None:
            return f"state line missing after session {session} (exit {code})"
        if code != "0" or after == before:
            stalled += 1
            if stalled >= max_stalled:
                return f"{stalled} stalled sessions in a row (last exit {code}): {after}"
            notify(notify_cmd, f"lifecycle: session {session} stalled ({stalled}/{max_stalled}, exit {code}); pausing {pause:.0f}s")
            time.sleep(pause)
        else:
            stalled = 0


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--state-dir", required=True, type=Path)
    parser.add_argument("--max-stalled", type=int, default=3)
    parser.add_argument("--pause", type=float, default=600)
    parser.add_argument("--session-timeout", type=float, default=14400)
    parser.add_argument("--notify")
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    command = args.command[1:] if args.command[:1] == ["--"] else args.command
    if not command:
        parser.error("session command missing after --")
    if args.notify and not shutil.which(shlex.split(args.notify)[0]):
        parser.error(f"notify command not found: {args.notify}")
    if not args.state_dir.is_dir():
        parser.error(f"{args.state_dir} is not a directory; run lifecycle init first")
    lock = args.state_dir / "driver.lock"
    acquire_lock(lock)
    for sig in (signal.SIGTERM, signal.SIGHUP):
        # Turn the signal into SystemExit so the cleanup runs; keep a SIGHUP that
        # the driver was started to ignore (nohup) ignored.
        if signal.getsignal(sig) is not signal.SIG_IGN:
            signal.signal(sig, lambda signum, _frame: sys.exit(f"lifecycle driver: {signal.Signals(signum).name} received"))
    try:
        reason = drive(args.state_dir, command, args.max_stalled, args.pause, args.session_timeout, args.notify)
    finally:
        lock.unlink()
    notify(args.notify, f"lifecycle driver stopped: {reason}")


if __name__ == "__main__":
    main()
