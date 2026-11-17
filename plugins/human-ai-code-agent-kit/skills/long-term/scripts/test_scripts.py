#!/usr/bin/env python3
"""Self-test for drive.py and check_diff_rules.py. Run: python3 test_scripts.py"""

from __future__ import annotations

import os
import shutil
import signal
import subprocess
import sys
import tempfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent


def git(repo: Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True)


def test_rule_check(tmp: Path) -> None:
    repo = tmp / "repo"
    (repo / "tests").mkdir(parents=True)
    (repo / "tests" / "test_a.py").write_text("def test_a():\n    assert f(1) == 2\n    assert g(1, rtol=1e-6)\n")
    (repo / "README.md").write_text("example: # noqa\n")
    (repo / "my mod.py").write_text("x = 1\n")
    (repo / "数据.py").write_text("x = 1\n")
    (repo / "gap.py").write_text("a = 1\nb = 2\nc = 3\nd = 4\n")
    git(repo, "init", "-q")
    git(repo, "add", ".")
    git(repo, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "base")
    (repo / "tests" / "test_a.py").write_text(
        "import pytest\n@pytest.mark.skip\ndef test_a():\n    assert g(1, rtol=1e-3)\n"
        "@pytest.mark.skipif(not HAS_GPU, reason='gpu')\ndef test_b():\n    pw = pytest.importorskip('pw')\n"
        "    delta = y - x\n    assert_allclose(a, b, rtol=1e-5)\n"
    )
    (repo / "src.py").write_text(
        "x = 1  # noqa: E501\n"
        "try:\n    f()\nexcept:\n    raise\n"
        "try:\n    f()\nexcept ValueError:\n    pass\n"
        "try:\n    f()\nexcept Exception as e:\n    log(e)\n"
        "# TO" "DO later\n"
        "model.fit(features)\n"
        "def fit(self, data):\n    return data\n"
    )
    (repo / "web.ts").write_text("// @ts-" "ignore\nfoo().catch(() => {});\ntry { a() } catch (e) {}\nmodel.fit(x);\n")
    (repo / "web.test.ts").write_text("it.only('a', f);\n")
    (repo / "util.ts").write_text("fit(points);\ncontext.skip(1);\n")  # not a test file: no T1
    # Two hunks two context lines apart: they must not merge into one.
    (repo / "gap.py").write_text("a = 1\nexcept ValueError:\nb = 2\nc = 3\npass\nd = 4\nx = 1  # noqa\n")
    swallow = "x = 1\ntry:\n    f()\nexcept:\n    pass\n"
    (repo / "my mod.py").write_text(swallow)
    (repo / "数据.py").write_text(swallow)
    shutil.copy(HERE / "check_diff_rules.py", repo / "check_diff_rules.py")
    expected = [
        "FAIL T1 tests/test_a.py:2:",
        "REVIEW T1 tests/test_a.py:2: assert f(1) == 2 (assertion removed)",
        "REVIEW T1 tests/test_a.py:3: assert g(1, rtol=1e-6) (tolerance changed)",
        "REVIEW T1 tests/test_a.py:5: @pytest.mark.skipif",
        "REVIEW T1 tests/test_a.py:7:",
        "FAIL C5 src.py:1:",
        "FAIL C2 src.py:4: except:",
        "FAIL C2 src.py:9: pass",
        "REVIEW C1 src.py:12:",
        "REVIEW P2 src.py:14:",
        "FAIL C5 web.ts:1:",
        "FAIL C2 web.ts:2:",
        "FAIL C2 web.ts:3:",
        "FAIL T1 web.test.ts:1:",
        "FAIL C5 gap.py:7:",
        "FAIL C2 my mod.py:4: except:",
        "FAIL C2 数据.py:4: except:",
    ]
    # The result must not depend on the user's diff prefix settings.
    for config in ([], ["diff.mnemonicPrefix=true"], ["diff.noprefix=true"], ["diff.interHunkContext=10"]):
        for item in config:
            git(repo, "config", *item.split("="))
        run = subprocess.run([sys.executable, str(HERE / "check_diff_rules.py")], cwd=repo, capture_output=True, text=True)
        out = run.stdout
        for item in config:
            git(repo, "config", "--unset", item.split("=")[0])
        assert run.returncode == 1, (config, out, run.stderr)
        for item in expected:
            assert item in out, f"{config}: missing {item!r} in:\n{out}"
        for absent in ("README.md", "check_diff_rules.py", "src.py:15:", "src.py:16:", "web.ts:4:", "util.ts", "gap.py:5:",
                       "tests/test_a.py:4:", "tests/test_a.py:8:", "tests/test_a.py:9:"):
            assert absent not in out, f"{config}: unexpected {absent!r} in:\n{out}"
        assert "FAIL T1 tests/test_a.py:5:" not in out and "FAIL T1 tests/test_a.py:7:" not in out, out


def test_driver(tmp: Path) -> None:
    state = tmp / "state"
    state.mkdir()
    status = state / "STATUS.md"
    line = "lifecycle: state=running cycle=1 stage=cycle-planning step=- last=init"
    # Session 1 advances, session 2 sets idle; the driver must stop after session 2.
    session = (
        "import sys, pathlib\n"
        f"p = pathlib.Path({str(status)!r})\n"
        "t = p.read_text()\n"
        "t = t.replace('last=init', 'last=C1-plan') if 'last=init' in t else t.replace('state=running', 'state=idle')\n"
        "p.write_text(t)\n"
    )
    status.write_text(f"# STATUS\n{line}\n")
    (state / "driver.lock").write_text("99999999")  # left by a dead driver: blocks nobody
    run = subprocess.run(
        [sys.executable, str(HERE / "drive.py"), "--state-dir", str(state), "--pause", "0", "--", sys.executable, "-c", session],
        capture_output=True, text=True,
    )
    assert run.returncode == 0, run.stderr
    assert "state is idle" in run.stdout, run.stdout
    assert (state / "driver.log").read_text().count("=== session") == 2
    assert not (state / "driver.lock").exists()

    # A session that changes nothing stalls; the driver stops at the limit.
    status.write_text(f"# STATUS\n{line}\n")
    run = subprocess.run(
        [sys.executable, str(HERE / "drive.py"), "--state-dir", str(state), "--pause", "0", "--max-stalled", "2", "--", sys.executable, "-c", "pass"],
        capture_output=True, text=True,
    )
    assert "2 stalled sessions in a row" in run.stdout, run.stdout

    # The session sees the driver's pid; a hung session is killed and counts as stalled.
    hang = "import os, time; print('pid', os.environ['LIFECYCLE_DRIVER_PID'], flush=True); time.sleep(60)"
    run = subprocess.run(
        [sys.executable, str(HERE / "drive.py"), "--state-dir", str(state), "--pause", "0", "--max-stalled", "1",
         "--session-timeout", "1", "--", sys.executable, "-c", hang],
        capture_output=True, text=True, timeout=50,
    )
    assert "1 stalled sessions in a row (last exit timeout)" in run.stdout, run.stdout
    assert "\npid " in (state / "driver.log").read_text()

    # An unresolvable notify command is rejected before any session starts.
    run = subprocess.run(
        [sys.executable, str(HERE / "drive.py"), "--state-dir", str(state), "--notify", "no-such-notifier --x", "--", "true"],
        capture_output=True, text=True,
    )
    assert run.returncode == 2 and "notify command not found" in run.stderr, run.stderr

    # Ctrl-C or a hangup of the driver ends the running session before the lock goes.
    pid_file = tmp / "session.pid"
    wait = f"import os, time, pathlib; pathlib.Path({str(pid_file)!r}).write_text(str(os.getpid())); time.sleep(60)"
    for sig in (signal.SIGINT, signal.SIGHUP):
        pid_file.unlink(missing_ok=True)
        status.write_text(f"# STATUS\n{line}\n")
        driver = subprocess.Popen(
            [sys.executable, str(HERE / "drive.py"), "--state-dir", str(state), "--", sys.executable, "-c", wait],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            # Test runners may start us with SIGINT ignored; the driver must see the default.
            preexec_fn=lambda: [signal.signal(s, signal.SIG_DFL) for s in (signal.SIGINT, signal.SIGHUP)],
        )
        for _ in range(100):
            if pid_file.exists() and pid_file.read_text():
                break
            time.sleep(0.1)
        os.kill(driver.pid, sig)
        driver.wait(timeout=40)
        assert not (state / "driver.lock").exists(), sig
        try:
            os.kill(int(pid_file.read_text()), 0)
            raise AssertionError(f"session survived {sig.name}")
        except ProcessLookupError:
            pass

    # A second driver exits at once and leaves the first one running; SIGKILL of the
    # first leaves the file, and the next driver takes the lock anyway.
    pid_file.unlink(missing_ok=True)
    status.write_text(f"# STATUS\n{line}\n")
    first = subprocess.Popen(
        [sys.executable, str(HERE / "drive.py"), "--state-dir", str(state), "--", sys.executable, "-c", wait],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    for _ in range(100):
        if pid_file.exists() and pid_file.read_text():
            break
        time.sleep(0.1)
    second = subprocess.run(
        [sys.executable, str(HERE / "drive.py"), "--state-dir", str(state), "--", sys.executable, "-c", "pass"],
        capture_output=True, text=True, timeout=20,
    )
    assert second.returncode != 0 and "another driver holds" in second.stderr, second.stderr
    assert first.poll() is None and (state / "driver.lock").read_text() == str(first.pid)
    first.kill()
    first.wait()
    os.kill(int(pid_file.read_text()), signal.SIGKILL)  # the session may outlive a killed driver
    assert (state / "driver.lock").exists()
    run = subprocess.run(
        [sys.executable, str(HERE / "drive.py"), "--state-dir", str(state), "--pause", "0", "--max-stalled", "1", "--", sys.executable, "-c", "pass"],
        capture_output=True, text=True, timeout=20,
    )
    assert run.returncode == 0 and "1 stalled sessions in a row" in run.stdout, run.stdout + run.stderr
    assert not (state / "driver.lock").exists()

    # STOP prevents any session.
    (state / "STOP").write_text("human stop\n")
    run = subprocess.run(
        [sys.executable, str(HERE / "drive.py"), "--state-dir", str(state), "--", sys.executable, "-c", "raise SystemExit(9)"],
        capture_output=True, text=True,
    )
    assert "STOP file present" in run.stdout, run.stdout


if __name__ == "__main__":
    with tempfile.TemporaryDirectory() as d:
        test_rule_check(Path(d))
        test_driver(Path(d))
    print("ok")
