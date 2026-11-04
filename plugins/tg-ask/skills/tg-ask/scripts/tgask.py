#!/usr/bin/env python3
"""tg-ask: a Telegram relay between the human and Claude Code sessions running in tmux.

Python 3.8+ standard library only. External tools: tmux, ps.

Worker side : ask, say, sessions
Relay       : relay, start, stop
Lifecycle   : set-token, pair-start, pair-wait, enable, health, uninstall, selftest
Hook        : hook   (wired by the plugin's hooks/hooks.json; must stay fast and silent)

State lives next to the official Telegram plugin's files so the bot setup stays compatible:
  $TELEGRAM_STATE_DIR (default ~/.claude/channels/telegram)/.env          TELEGRAM_BOT_TOKEN=...
  $TELEGRAM_STATE_DIR/access.json                                         {"allowFrom": [...], ...}
  $TELEGRAM_STATE_DIR/tg-ask/{enabled,requests/,events/,relay.pid,...}    this tool's own state
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import secrets
import shlex
import shutil
import signal
import subprocess
import sys
import threading
import time
import http.client
import socket
from collections import deque
from pathlib import Path

STATE = Path(os.environ.get("TELEGRAM_STATE_DIR") or Path.home() / ".claude" / "channels" / "telegram")
HOME = STATE / "tg-ask"
REQ = HOME / "requests"
EVENTS = HOME / "events"
ENABLED = HOME / "enabled"
PIDF = HOME / "relay.pid"
OFFSET = HOME / "offset"
HEARTBEAT = HOME / "heartbeat"
SAID = HOME / "said.jsonl"
PAIR = HOME / "pair.json"
RELAY_SESSION = "tg-relay"
SELF = Path(__file__).resolve()

# ---------------------------------------------------------------- hook (fast path)

SECRET_RES = [
    (re.compile(r"(?<![0-9])\d{6,12}:[A-Za-z0-9_-]{30,}"), "<bot-token>"),
    (re.compile(r"\b(?:sk|rk|pk)-[A-Za-z0-9_-]{16,}"), "<key>"),
    (re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}"), "<gh-token>"),
    (re.compile(r"\bxox[abprs]-[A-Za-z0-9-]{10,}"), "<slack-token>"),
    (re.compile(r"\bAKIA[0-9A-Z]{16}\b"), "<aws-key>"),
    (re.compile(r"(?i)(bearer\s+)[A-Za-z0-9._~+/=-]{10,}"), r"\1<redacted>"),
    (re.compile(r"(?i)\b((?:api[_-]?key|token|secret|passw(?:or)?d|authorization)\s*[=:]\s*)(\"[^\"]*\"|'[^']*'|\S+)"),
     r"\1<redacted>"),
]
BRIEF_KEYS = ("command", "file_path", "path", "pattern", "url", "description", "query", "prompt")


def redact(s: str) -> str:
    for rx, rep in SECRET_RES:
        s = rx.sub(rep, s)
    return s


def brief(tool_input) -> str:
    v = ""
    if isinstance(tool_input, dict):
        for k in BRIEF_KEYS:
            if tool_input.get(k):
                v = str(tool_input[k])
                break
    return redact(" ".join(v.split()))[:160]


def cmd_hook(_a) -> int:
    # Never block or fail a session: every error is swallowed, nothing is printed.
    try:
        pane = os.environ.get("TMUX_PANE")
        if not pane or not ENABLED.exists():
            return 0
        data = json.load(sys.stdin)
        ev = data.get("hook_event_name", "")
        rec = {"ts": time.time(), "ev": ev}
        if ev == "PreToolUse":
            rec["tool"] = data.get("tool_name", "")
            rec["brief"] = brief(data.get("tool_input"))
        elif ev == "Notification":
            rec["msg"] = redact(str(data.get("message", "")))[:200]
        EVENTS.mkdir(parents=True, exist_ok=True)
        f = EVENTS / (pane.lstrip("%") + ".jsonl")
        with open(f, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
        if f.stat().st_size > 512_000:
            keep = f.read_text(encoding="utf-8").splitlines()[-500:]
            f.write_text("\n".join(keep) + "\n", encoding="utf-8")
    except Exception:
        pass
    return 0

# ---------------------------------------------------------------- utils


def die(msg: str, code: int = 1):
    print(f"tg-ask: {msg}", file=sys.stderr)
    sys.exit(code)


def iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S%z")


def log(msg: str):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def tmux(*args, stdin: str | None = None):
    try:
        p = subprocess.run(["tmux", *args], input=stdin, capture_output=True, text=True)
    except FileNotFoundError:
        return False, ""
    return p.returncode == 0, p.stdout


def ps_table():
    out = subprocess.run(["ps", "-axo", "pid=,ppid=,args="], capture_output=True, text=True).stdout
    kids, args = {}, {}
    for line in out.splitlines():
        parts = line.split(None, 2)
        if len(parts) < 2 or not parts[0].isdigit() or not parts[1].isdigit():
            continue
        pid, ppid = int(parts[0]), int(parts[1])
        args[pid] = parts[2] if len(parts) > 2 else ""
        kids.setdefault(ppid, []).append(pid)
    return kids, args


def is_claude(a: str) -> bool:
    if not a or "--chrome-native-host" in a:
        return False
    return os.path.basename(a.split()[0]) == "claude" or "@anthropic-ai/claude-code" in a


def find_claude(root: int, kids, args):
    stack, seen = [root], set()
    while stack:
        p = stack.pop()
        if p in seen:
            continue
        seen.add(p)
        if is_claude(args.get(p, "")):
            return p
        stack.extend(kids.get(p, []))
    return None


def sessions():
    """Claude Code sessions running in tmux panes, each with a docker-style hex id."""
    ok, out = tmux("list-panes", "-a", "-F", "#{pane_id}\t#{pane_pid}\t#{session_name}\t#{pane_current_path}\t#{pane_title}")
    if not ok:
        return []
    kids, args = ps_table()
    res = []
    for line in out.splitlines():
        pane, ppid, name, cwd, title = (line.split("\t") + [""] * 5)[:5]
        if not ppid.isdigit():
            continue
        cpid = find_claude(int(ppid), kids, args)
        if cpid is None:
            continue
        sid = hashlib.sha1(f"{pane}:{cpid}".encode()).hexdigest()[:12]
        res.append({"sid": sid, "pane": pane, "name": name, "cwd": cwd, "title": title, "pid": cpid})
    return res


def match_prefix(q: str, ss):
    q = q.strip().lower()
    if not q:
        return []
    return [s for s in ss if s["sid"].startswith(q) or s["pane"] == q]


def short_path(p: str) -> str:
    h = str(Path.home())
    return "~" + p[len(h):] if p.startswith(h) else p


# Claude Code TUI heuristics.
# shortcut: screen-scraping Claude Code's TUI (input box = "❯" right under a ─ rule; selection dialogs
# show "❯ 1."); re-check these regexes if a Claude Code release changes the layout.
DIALOG_RE = re.compile(r"❯\s*\d+\.")
INPUT_RE = re.compile(r"─{10,}[ \t]*\n[ \t]*❯")
BUSY_RE = re.compile(r"…\s*\(\d+[hms]")


def screen(pane: str):
    ok, out = tmux("capture-pane", "-p", "-t", pane)
    return out if ok else None


def bottom(scr, n: int = 25) -> str:
    return "\n".join((scr or "").rstrip("\n").splitlines()[-n:])


def ready_for_input(scr) -> bool:
    b = bottom(scr)
    return bool(b) and not DIALOG_RE.search(b) and bool(INPUT_RE.search(b))


def paste(pane: str, text: str):
    """Type text into a pane as one bracketed paste, then submit it."""
    buf = f"tgask-{os.getpid()}"
    tmux("load-buffer", "-b", buf, "-", stdin=text)
    tmux("paste-buffer", "-p", "-d", "-b", buf, "-t", pane)
    time.sleep(0.4)
    tmux("send-keys", "-t", pane, "Enter")

# ---------------------------------------------------------------- telegram


class TgError(Exception):
    pass


def token():
    t = os.environ.get("TELEGRAM_BOT_TOKEN")
    if t:
        return t.strip()
    try:
        for line in (STATE / ".env").read_text().splitlines():
            if line.startswith("TELEGRAM_BOT_TOKEN="):
                return line.split("=", 1)[1].strip()
    except FileNotFoundError:
        pass
    return None


class _Conn(http.client.HTTPSConnection):
    def connect(self):
        # IPv4 first with a short per-address connect timeout: an IPv6 path that black-holes would
        # otherwise stall every call for the full request timeout before falling back.
        infos = sorted(socket.getaddrinfo(self.host, self.port, type=socket.SOCK_STREAM),
                       key=lambda i: i[0] != socket.AF_INET)
        err = None
        for fam, typ, proto, _, addr in infos:
            s = socket.socket(fam, typ, proto)
            s.settimeout(5)
            try:
                s.connect(addr)
            except OSError as e:
                s.close()
                err = e
                continue
            s.settimeout(self.timeout)
            self.sock = self._context.wrap_socket(s, server_hostname=self.host)
            return
        raise err or OSError("no address for api.telegram.org")


_tls = threading.local()  # one keep-alive connection per thread: saves a TLS handshake per call


def api(method: str, _timeout: float = 30, _token: str | None = None, **params):
    t = _token or token()
    if not t:
        raise TgError("no bot token; run /tg-ask:setup")
    body = json.dumps(params).encode()
    for attempt in (1, 2):
        conn = getattr(_tls, "conn", None)
        reused = conn is not None
        if conn is None:
            conn = _tls.conn = _Conn("api.telegram.org", timeout=_timeout)
        conn.timeout = _timeout
        if conn.sock:
            conn.sock.settimeout(_timeout)
        try:
            conn.request("POST", f"/bot{t}/{method}", body, {"Content-Type": "application/json"})
            r = conn.getresponse()
            raw = r.read()
            break
        except (http.client.HTTPException, OSError) as e:  # never echo the URL: it contains the token
            conn.close()
            _tls.conn = None
            # Retry once only when a reused keep-alive socket had gone stale; never after a timeout.
            stale = isinstance(e, (http.client.RemoteDisconnected, BrokenPipeError, ConnectionResetError))
            if attempt == 2 or not (reused and stale):
                raise TgError(f"{method}: network error: {e!r}") from None
    try:
        j = json.loads(raw)
    except ValueError:
        raise TgError(f"{method}: HTTP {r.status}") from None
    if not j.get("ok"):
        raise TgError(f"{method}: {j.get('error_code')} {j.get('description')}")
    return j["result"]


def access() -> dict:
    try:
        return json.loads((STATE / "access.json").read_text())
    except Exception:
        return {}


def owners():
    return [str(x) for x in access().get("allowFrom", [])]


def owner():
    # shortcut: single-user bot; requests and alerts go to the first allowFrom entry. Fan out if this ever has >1 user.
    o = owners()
    return o[0] if o else None


def send_text(chat, text: str, **kw):
    """Send text, split at Telegram's 4096-char cap. Returns the sent messages."""
    out = []
    while True:
        chunk, text = text[:4000], text[4000:]
        out.append(api("sendMessage", chat_id=chat, text=chunk, **kw))
        if not text:
            return out
        kw = {}

# ---------------------------------------------------------------- request files


def dump_req(meta: dict, body: str) -> str:
    lines = [f"{k}: {json.dumps(v, ensure_ascii=False)}" for k, v in meta.items() if v is not None]
    return "---\n" + "\n".join(lines) + "\n---\n" + body


def parse_req(text: str):
    m = re.match(r"---\n(.*?)\n---\n?(.*)\Z", text, re.S)
    if not m:
        raise ValueError("no frontmatter")
    meta = {}
    for line in m.group(1).splitlines():
        k, sep, v = line.partition(":")
        if not sep:
            continue
        v = v.strip()
        try:
            meta[k.strip()] = json.loads(v)
        except ValueError:
            meta[k.strip()] = v
    return meta, m.group(2)


def save_req(path: Path, meta: dict, body: str):
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(dump_req(meta, body), encoding="utf-8")
    os.replace(tmp, path)


def all_requests():
    out = []
    for p in sorted(REQ.glob("*.md")) if REQ.exists() else []:
        try:
            meta, body = parse_req(p.read_text(encoding="utf-8"))
            out.append((p, meta, body))
        except Exception:
            continue
    return out


def slug(s: str) -> str:
    return re.sub(r"[\s/\\:*?\"<>|#%]+", "-", s.strip()).strip("-")[:40] or "request"

# ---------------------------------------------------------------- relay process control


def read_pid():
    try:
        return int(PIDF.read_text().strip())
    except Exception:
        return None


def pid_args(pid: int) -> str:
    return subprocess.run(["ps", "-p", str(pid), "-o", "args="], capture_output=True, text=True).stdout.strip()


def relay_pid():
    pid = read_pid()
    if not pid:
        return None
    try:
        os.kill(pid, 0)
    except OSError:
        return None
    a = pid_args(pid)
    return pid if ("tgask.py" in a and a.endswith(" relay")) else None


def ensure_relay() -> bool:
    """Start the relay tmux session unless it is already up. Returns True if it started one."""
    if relay_pid():
        return False
    if tmux("has-session", "-t", "=" + RELAY_SESSION)[0]:
        return False  # its restart loop brings the relay back within seconds
    HOME.mkdir(parents=True, exist_ok=True)
    cmd = f"while true; do {shlex.quote(sys.executable)} {shlex.quote(str(SELF))} relay; sleep 5; done"
    ok, _ = tmux("new-session", "-d", "-s", RELAY_SESSION, "-c", str(HOME), cmd)
    if not ok:
        die("could not start the relay tmux session")
    return True


def cmd_start(_a):
    if not ENABLED.exists():
        die("not set up on this machine; run /tg-ask:setup")
    print("relay started" if ensure_relay() else "relay already running")


def cmd_stop(_a):
    tmux("kill-session", "-t", "=" + RELAY_SESSION)
    pid = relay_pid()
    if pid:
        os.kill(pid, signal.SIGTERM)
    for _ in range(20):
        if not relay_pid():
            break
        time.sleep(0.2)
    PIDF.unlink(missing_ok=True)
    print("relay stopped")

# ---------------------------------------------------------------- worker side


def cmd_ask(a):
    pane = os.environ.get("TMUX_PANE")
    if not pane:
        die("not inside tmux ($TMUX_PANE unset): the relay could not call this session back")
    if not ENABLED.exists():
        die("not set up on this machine; run /tg-ask:setup")
    body = sys.stdin.read()
    if not body.strip():
        die("request body required on stdin")
    rid = time.strftime("%Y%m%d-%H%M%S") + "-" + slug(a.summary)
    REQ.mkdir(parents=True, exist_ok=True)
    path = REQ / f"{rid}.md"
    meta = {"id": rid, "status": "pending", "summary": a.summary.strip(), "pane": pane,
            "options": a.option or [], "created_at": iso()}
    save_req(path, meta, body)
    ensure_relay()
    print(path)


def record_said(mid: int, pane: str):
    SAID.parent.mkdir(parents=True, exist_ok=True)
    with open(SAID, "a") as fh:
        fh.write(json.dumps({"mid": mid, "pane": pane}) + "\n")
    lines = SAID.read_text().splitlines()
    if len(lines) > 1000:
        SAID.write_text("\n".join(lines[-500:]) + "\n")


def said_lookup(mid: int):
    try:
        for line in reversed(SAID.read_text().splitlines()):
            r = json.loads(line)
            if r.get("mid") == mid:
                return r.get("pane")
    except Exception:
        pass
    return None


def cmd_say(a):
    text = a.text if a.text is not None else sys.stdin.read()
    if not text.strip():
        die("nothing to say")
    chat = owner() or die("no allowlisted Telegram user; run /tg-ask:setup")
    pane = os.environ.get("TMUX_PANE")
    me = next((s for s in sessions() if s["pane"] == pane), None) if pane else None
    head = f"💬 {me['sid'][:6]} {me['name']}" if me else "💬"
    try:
        sent = send_text(chat, f"{head}\n{text.strip()}")
    except TgError as e:
        die(str(e))
    if pane:
        for m in sent:
            record_said(m["message_id"], pane)
    print("sent")


def cmd_sessions(_a):
    for s in sessions():
        print(f"{s['sid']}  {s['pane']:>4}  {s['name']}  {short_path(s['cwd'])}")

# ---------------------------------------------------------------- relay

HELP = """tg-ask commands
/ls — Claude sessions in tmux (id, state)
/watch <id> — live activity of one session
/unwatch — stop the live view
/status <id> — snapshot of the session's screen
/to <id> <text> — type text into a session
/key <id> <key> — press one key (1-9, enter, esc, up, down, tab, stab, y, n)
/pending — open requests
Answer a request: tap a button, or quote-reply it. With exactly one open request a plain message answers it.
Quote-reply a 💬 session message to talk to that session.
<id> = any unique prefix of the hex id, like docker."""

KEYS = {**{str(i): str(i) for i in range(10)}, "enter": "Enter", "esc": "Escape", "escape": "Escape",
        "up": "Up", "down": "Down", "tab": "Tab", "stab": "BTab", "y": "y", "n": "n"}
ICON = {"working": "🦀", "idle": "💤", "waiting": "⏸"}


class Relay:
    def __init__(self):
        self.lock = threading.Lock()
        self.ev_off: dict = {}
        self.ev: dict = {}
        self.watch = None
        self.started = time.time()

    # ---- events from hooks
    def read_events(self):
        if not EVENTS.exists():
            return
        for f in EVENTS.glob("*.jsonl"):
            pane = "%" + f.stem
            first = pane not in self.ev_off
            size = f.stat().st_size
            off = self.ev_off.get(pane, 0)
            if size < off:  # the hook trimmed the file
                off = 0
            if size == off:
                self.ev_off[pane] = off
                continue
            with open(f, encoding="utf-8") as fh:
                fh.seek(off)
                chunk = fh.read()
                self.ev_off[pane] = fh.tell()
            q = self.ev.setdefault(pane, deque(maxlen=40))
            last_ts = q[-1]["ts"] if q else 0
            for line in chunk.splitlines():
                try:
                    e = json.loads(line)
                except ValueError:
                    continue
                if e.get("ts", 0) <= last_ts:
                    continue
                q.append(e)
                if not first and e.get("ev") == "Notification" and "permission" in e.get("msg", "").lower():
                    self.alert_permission(pane, e)

    def alert_permission(self, pane, e):
        s = next((s for s in sessions() if s["pane"] == pane), None)
        chat = owner()
        if not s or not chat:
            return
        sid = s["sid"][:6]
        try:
            api("sendMessage", chat_id=chat,
                text=f"🔔 {sid} {s['name']}\n{e.get('msg', '')}\n\n/status {sid} · /key {sid} 1")
        except TgError as err:
            log(f"alert failed: {err}")

    def state(self, pane, scr) -> str:
        b = bottom(scr)
        # The screen decides: hook events go stale in sessions that started before the plugin loaded.
        if DIALOG_RE.search(b):
            return "waiting"
        return "working" if BUSY_RE.search(b) else "idle"

    def since(self, pane, st) -> str:
        if st != "working":
            return ""
        starts = [e["ts"] for e in self.ev.get(pane, []) if e.get("ev") == "UserPromptSubmit"]
        if not starts:
            return ""
        m = int((time.time() - starts[-1]) // 60)
        return f" {m}m" if m else " <1m"

    # ---- formatting
    def fmt_ls(self) -> str:
        ss = sessions()
        if not ss:
            return "No Claude sessions in tmux."
        out = []
        for s in ss:
            st = self.state(s["pane"], screen(s["pane"]))
            out.append(f"{ICON[st]} {s['sid'][:6]}  {s['name']}  {st}{self.since(s['pane'], st)}\n"
                       f"    📁 {short_path(s['cwd'])}\n    {s['title']}")
        return "\n".join(out)

    def watch_text(self, s) -> str:
        scr = screen(s["pane"])
        st = self.state(s["pane"], scr)
        sid = s["sid"][:6]
        tools = [e for e in self.ev.get(s["pane"], []) if e.get("ev") == "PreToolUse"][-6:]
        lines = [f"▸ {e.get('tool', '')}: {e.get('brief', '')}"[:140] for e in tools] or ["(no tool calls seen yet)"]
        if st == "waiting":
            lines += ["", "⏸ waiting on a dialog:", bottom(scr, 8)]
        return (f"{ICON[st]} {sid} {s['name']} · {st}{self.since(s['pane'], st)}\n📁 {short_path(s['cwd'])}\n\n"
                + "\n".join(lines) + f"\n\n/unwatch · /status {sid}")

    # ---- periodic work
    def tick(self):
        HEARTBEAT.write_text(str(time.time()))
        self.read_events()
        for path, meta, body in all_requests():
            st = meta.get("status")
            try:
                if st == "pending":
                    self.send_request(path, meta, body)
                elif st == "answered":
                    self.callback(path, meta, body)
            except TgError as e:
                log(f"{meta.get('id')}: {e}")
        self.update_watch()

    def send_request(self, path, meta, body):
        chat = owner()
        if not chat:
            log("no allowFrom user; cannot send requests")
            return
        s = next((s for s in sessions() if s["pane"] == meta.get("pane")), None)
        frm = f"from {s['sid'][:6]} {s['name']}\n" if s else ""
        text = f"❓ {meta['id']}\n{frm}\n{body.strip()}"
        if len(text) > 3900:
            text = text[:3800] + f"\n\n… (truncated; full text in {path})"
        opts = meta.get("options") or []
        kw = {}
        if opts:
            kw["reply_markup"] = {"inline_keyboard": [[{"text": str(o)[:60], "callback_data": f"opt:{i}"}]
                                                      for i, o in enumerate(opts)]}
        m = api("sendMessage", chat_id=chat, text=text, **kw)
        meta.update(status="sent", tg_chat_id=chat, tg_message_id=m["message_id"], sent_at=iso())
        save_req(path, meta, body)
        log(f"sent {meta['id']}")

    def callback(self, path, meta, body):
        pane = meta.get("pane", "")
        if not any(s["pane"] == pane for s in sessions()):
            meta["status"] = "orphaned"
            save_req(path, meta, body)
            self.notify(f"⚠️ {meta['id']}: the asking session is gone. The answer is saved in\n{path}")
            log(f"orphaned {meta['id']}")
            return
        if not ready_for_input(screen(pane)):
            if time.time() - meta.get("answered_ts", time.time()) > 600 and not meta.get("stuck_notified"):
                meta["stuck_notified"] = True
                save_req(path, meta, body)
                s = next(s for s in sessions() if s["pane"] == pane)
                self.notify(f"⏳ {meta['id']}: session {s['sid'][:6]} has not been at its input box for 10 min, "
                            f"so the answer is not delivered yet. /status {s['sid'][:6]}")
            return
        paste(pane, f"[tg-ask] the human answered request {meta['id']}. "
                    f"Read the `answer` field in {path} and continue accordingly.")
        meta.update(status="delivered", delivered_at=iso())
        save_req(path, meta, body)
        log(f"delivered {meta['id']}")

    def update_watch(self):
        w = self.watch
        if not w or time.time() - w["at"] < 3:
            return
        s = next((s for s in sessions() if s["pane"] == w["pane"]), None)
        if not s:
            self.edit(w, w["text"] + "\n\n⏹ session ended")
            self.watch = None
            return
        text = self.watch_text(s)
        if text != w["text"]:
            if not self.edit(w, text):
                self.watch = None

    def edit(self, w, text) -> bool:
        w["at"] = time.time()
        try:
            api("editMessageText", chat_id=w["chat"], message_id=w["mid"], text=text[:4000])
            w["text"] = text
            return True
        except TgError as e:
            if "not modified" in str(e):
                return True
            log(f"watch edit failed, dropping watch: {e}")
            return False

    def notify(self, text):
        chat = owner()
        if chat:
            try:
                api("sendMessage", chat_id=chat, text=text)
            except TgError as e:
                log(f"notify failed: {e}")

    # ---- inbound
    def reply(self, chat, text, **kw):
        try:
            send_text(chat, text, **kw)
        except TgError as e:
            log(f"reply failed: {e}")

    def handle(self, u):
        if "callback_query" in u:
            return self.on_button(u["callback_query"])
        m = u.get("message")
        if not m:
            return
        if str(m.get("from", {}).get("id")) not in owners() or m.get("chat", {}).get("type") != "private":
            return  # strangers and groups are dropped silently
        chat = m["chat"]["id"]
        text = (m.get("text") or "").strip()
        if not text:
            return self.reply(chat, "Only text is supported.")
        if text.startswith("/"):
            return self.on_command(chat, text)
        rt = (m.get("reply_to_message") or {}).get("message_id")
        if rt:
            hit = next((r for r in all_requests() if r[1].get("tg_message_id") == rt), None)
            if hit:
                return self.answer(chat, *hit, text, "text")
            pane = said_lookup(rt) or (self.watch["pane"] if self.watch and self.watch["mid"] == rt else None)
            if pane:
                return self.type_into(chat, pane, text)
            return self.reply(chat, "That message is neither an open request nor a session message.")
        open_ = [r for r in all_requests() if r[1].get("status") == "sent"]
        if len(open_) == 1:
            return self.answer(chat, *open_[0], text, "text")
        if not open_:
            return self.reply(chat, "No open request. Use /to <id> <text>, or quote-reply a 💬 session message.")
        return self.reply(chat, f"{len(open_)} open requests; quote-reply the one you are answering:\n"
                          + "\n".join(f"• {r[1]['id']}" for r in open_))

    def answer(self, chat, path, meta, body, text, via):
        if meta.get("status") != "sent":
            return self.reply(chat, f"{meta.get('id')} was already answered ({meta.get('status')}).")
        meta.update(status="answered", answer=text, answered_via=via, answered_at=iso(), answered_ts=time.time())
        save_req(path, meta, body)
        try:
            api("editMessageReplyMarkup", chat_id=meta["tg_chat_id"], message_id=meta["tg_message_id"],
                reply_markup={"inline_keyboard": []})
        except TgError:
            pass
        self.reply(chat, f"✅ {meta['id']}\n→ {text}", reply_to_message_id=meta["tg_message_id"])
        log(f"answered {meta['id']} via {via}")
        self.callback(path, meta, body)

    def on_button(self, q):
        if str(q.get("from", {}).get("id")) not in owners():
            return
        mid = (q.get("message") or {}).get("message_id")
        hit = next((r for r in all_requests() if r[1].get("tg_message_id") == mid), None)
        note = "No matching request."
        if hit:
            path, meta, body = hit
            try:
                choice = meta["options"][int(str(q.get("data", "")).split(":")[1])]
            except (KeyError, IndexError, ValueError):
                choice = None
            if choice is None:
                note = "Unknown option."
            elif meta.get("status") != "sent":
                note = "Already answered."
            else:
                note = f"Chosen: {choice}"
                self.answer(q["message"]["chat"]["id"], path, meta, body, choice, "button")
        try:
            api("answerCallbackQuery", callback_query_id=q["id"], text=note[:190])
        except TgError:
            pass

    def pick(self, chat, q):
        ss = sessions()
        m = match_prefix(q, ss)
        if len(m) == 1:
            return m[0]
        if not m:
            self.reply(chat, f"No session matches '{q}'. /ls")
        else:
            self.reply(chat, f"'{q}' is ambiguous: " + ", ".join(s["sid"][:8] for s in m))
        return None

    def type_into(self, chat, pane, text):
        if not ready_for_input(screen(pane)):
            return self.reply(chat, "That session is not at its input box (a dialog or menu is open). "
                                    "Check /status and answer it with /key.")
        paste(pane, "[tg] " + text)
        self.reply(chat, "⌨️ sent")

    def on_command(self, chat, text):
        head, _, rest = text.partition(" ")
        cmd = head.split("@")[0].lower()
        rest = rest.strip()
        if cmd in ("/start", "/help"):
            return self.reply(chat, HELP)
        if cmd == "/ls":
            return self.reply(chat, self.fmt_ls())
        if cmd == "/pending":
            open_ = [r[1] for r in all_requests() if r[1].get("status") in ("pending", "sent", "answered")]
            return self.reply(chat, "\n".join(f"• {m['id']} ({m['status']})" for m in open_) or "No open requests.")
        if cmd == "/unwatch":
            self.watch = None
            return self.reply(chat, "Stopped watching.")
        arg, _, tail = rest.partition(" ")
        if cmd in ("/status", "/watch", "/to", "/key"):
            if not arg:
                return self.reply(chat, f"Usage: {cmd} <id>" + (" <text>" if cmd == "/to" else " <key>" if cmd == "/key" else ""))
            s = self.pick(chat, arg)
            if not s:
                return
            if cmd == "/status":
                scr = bottom(screen(s["pane"]) or "", 40)[-3800:]
                import html
                return self.reply(chat, f"<b>{s['sid'][:6]} {html.escape(s['name'])}</b>\n<pre>{html.escape(scr)}</pre>",
                                  parse_mode="HTML")
            if cmd == "/watch":
                text0 = self.watch_text(s)
                try:
                    m = api("sendMessage", chat_id=chat, text=text0)
                except TgError as e:
                    return log(f"watch failed: {e}")
                self.watch = {"chat": chat, "pane": s["pane"], "mid": m["message_id"], "text": text0, "at": time.time()}
                return
            if cmd == "/to":
                if not tail.strip():
                    return self.reply(chat, "Usage: /to <id> <text>")
                return self.type_into(chat, s["pane"], tail.strip())
            if cmd == "/key":
                key = KEYS.get(tail.strip().lower())
                if not key:
                    return self.reply(chat, "Allowed keys: " + ", ".join(KEYS))
                tmux("send-keys", "-t", s["pane"], key)
                return self.reply(chat, f"⌨️ {key} → {s['sid'][:6]}")
        return self.reply(chat, HELP)

    # ---- main loops
    def scan_loop(self):
        while True:
            with self.lock:
                try:
                    self.tick()
                except Exception as e:
                    log(f"tick error: {e!r}")
            time.sleep(2)

    def run(self):
        if relay_pid() and relay_pid() != os.getpid():
            log("another relay is already running; exiting")
            time.sleep(10)
            return
        HOME.mkdir(parents=True, exist_ok=True)
        PIDF.write_text(str(os.getpid()))
        try:
            me = api("getMe")
            log(f"relay polling as @{me['username']}")
            cmds = [{"command": c, "description": d} for c, d in [
                ("ls", "List Claude sessions"), ("watch", "Live view: /watch <id>"),
                ("unwatch", "Stop live view"), ("status", "Screen snapshot: /status <id>"),
                ("to", "Type into a session: /to <id> <text>"), ("key", "Press a key: /key <id> <key>"),
                ("pending", "Open requests"), ("help", "Help")]]
            # The official plugin registers its menu under all_private_chats, which outranks the default
            # scope in DMs; overwrite both so the menu shows tg-ask's commands.
            for scope in ({"type": "default"}, {"type": "all_private_chats"}):
                api("setMyCommands", commands=cmds, scope=scope)
        except TgError as e:
            log(f"startup: {e}")
        threading.Thread(target=self.scan_loop, daemon=True).start()
        try:
            off = int(OFFSET.read_text())
        except Exception:
            off = 0
        while True:
            try:
                ups = api("getUpdates", _timeout=40, offset=off, timeout=25,
                          allowed_updates=["message", "callback_query"])
            except TgError as e:
                hint = " (another poller holds this bot: the official telegram plugin, or a second relay?)" if "409" in str(e) else ""
                log(f"{e}{hint}")
                time.sleep(5)
                continue
            for u in ups:
                off = u["update_id"] + 1
                OFFSET.write_text(str(off))  # advance first: a crashing update is skipped, not retried forever
                with self.lock:
                    try:
                        self.handle(u)
                    except Exception as e:
                        log(f"handle error: {e!r}")


def cmd_relay(_a):
    signal.signal(signal.SIGTERM, lambda *_: sys.exit(0))
    try:
        Relay().run()
    finally:
        if read_pid() == os.getpid():
            PIDF.unlink(missing_ok=True)

# ---------------------------------------------------------------- lifecycle


def cmd_set_token(_a):
    t = sys.stdin.read().strip()
    if not re.fullmatch(r"\d+:[A-Za-z0-9_-]{30,}", t):
        die("that does not look like a BotFather token (digits:long-string)")
    try:
        me = api("getMe", _token=t)
    except TgError as e:
        die(f"Telegram rejected the token: {e}")
    STATE.mkdir(parents=True, exist_ok=True, mode=0o700)
    env = STATE / ".env"
    lines = [l for l in (env.read_text().splitlines() if env.exists() else []) if not l.startswith("TELEGRAM_BOT_TOKEN=")]
    tmp = env.with_name(".env.tmp")
    tmp.unlink(missing_ok=True)
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)  # owner-only from the first byte
    with os.fdopen(fd, "w") as fh:
        fh.write("\n".join(lines + [f"TELEGRAM_BOT_TOKEN={t}"]) + "\n")
    os.replace(tmp, env)
    print(f"token saved for @{me['username']} ({env}, mode 600)")


def cmd_pair_start(_a):
    me = api("getMe")
    code = secrets.token_hex(3)
    HOME.mkdir(parents=True, exist_ok=True)
    PAIR.write_text(json.dumps({"code": code, "expires": time.time() + 600}))
    print(f"Send this code to @{me['username']} on Telegram: {code}")


def cmd_pair_wait(a):
    try:
        p = json.loads(PAIR.read_text())
    except Exception:
        die("run pair-start first")
    if relay_pid() or tmux("has-session", "-t", "=" + RELAY_SESSION)[0]:
        cmd_stop(a)  # pairing needs the bot's update stream to itself
    deadline = min(p["expires"], time.time() + a.timeout)
    off = 0
    while time.time() < deadline:
        try:
            ups = api("getUpdates", _timeout=30, offset=off, timeout=20, allowed_updates=["message"])
        except TgError as e:
            die(str(e))
        for u in ups:
            off = u["update_id"] + 1
            m = u.get("message") or {}
            if (m.get("text") or "").strip().lower() != p["code"] or m.get("chat", {}).get("type") != "private":
                continue
            uid = str(m["from"]["id"])
            acc = access()
            acc.setdefault("allowFrom", [])
            if uid not in [str(x) for x in acc["allowFrom"]]:
                acc["allowFrom"].append(uid)
            acc["dmPolicy"] = "allowlist"
            acc.setdefault("groups", {})
            acc.setdefault("pending", {})
            (STATE / "access.json").write_text(json.dumps(acc, indent=2) + "\n")
            api("getUpdates", offset=off, timeout=0)  # ack, so the relay does not see the code later
            OFFSET.write_text(str(off))
            PAIR.unlink(missing_ok=True)
            try:
                api("sendMessage", chat_id=m["chat"]["id"], text="✅ Paired with tg-ask.")
            except TgError:
                pass
            print(f"paired Telegram user {uid} (@{m['from'].get('username', '?')}); dmPolicy=allowlist")
            return
    die("timed out waiting for the code; run pair-start again")


def cmd_enable(_a):
    for d in (HOME, REQ, EVENTS):
        d.mkdir(parents=True, exist_ok=True)
    ENABLED.write_text(iso() + "\n")
    print(f"enabled ({ENABLED})")


def official_plugin_conflict() -> str:
    cfg = Path(os.environ.get("CLAUDE_CONFIG_DIR") or Path.home() / ".claude") / "settings.json"
    try:
        enabled = json.loads(cfg.read_text()).get("enabledPlugins", {})
        on = [k for k, v in enabled.items() if k.startswith("telegram@") and v]
        if on:
            return f"official plugin enabled in settings: {', '.join(on)}"
    except Exception:
        pass
    _, args = ps_table()
    if any("/telegram/" in a and "server.ts" in a for a in args.values()):
        return "official telegram plugin server.ts is running"
    return ""


def cmd_health(a):
    res = []

    def add(level, name, detail=""):
        res.append((level, name, detail))

    add("OK", "python", sys.version.split()[0]) if sys.version_info >= (3, 8) else add("FAIL", "python", "need 3.8+")
    add("OK", "tmux", shutil.which("tmux")) if shutil.which("tmux") else add("FAIL", "tmux", "not on PATH")
    add("OK", "setup", str(HOME)) if ENABLED.exists() else add("FAIL", "setup", "not enabled; run /tg-ask:setup")
    if not token():
        add("FAIL", "token", f"no TELEGRAM_BOT_TOKEN in {STATE / '.env'}")
    else:
        try:
            add("OK", "token", "@" + api("getMe", _timeout=10)["username"])
            wh = api("getWebhookInfo", _timeout=10).get("url")
            add("WARN", "webhook", f"set to {wh}; getUpdates will fail") if wh else add("OK", "webhook", "none")
        except TgError as e:
            add("FAIL", "token", str(e))
    add("OK", "allowlist", ", ".join(owners())) if owners() else add("FAIL", "allowlist", "empty; pair first")
    c = official_plugin_conflict()
    add("FAIL", "plugin-conflict", c + " (disable it: two pollers fight over one bot)") if c else add("OK", "plugin-conflict", "none")

    pid = relay_pid()
    if not pid:
        if a.fix and not any(l == "FAIL" for l, _, _ in res):
            ensure_relay()
            time.sleep(3)
            pid = relay_pid()
        add("OK", "relay", f"started (pid {pid})") if pid else add("FAIL", "relay", "not running")
    else:
        stale = str(SELF) not in pid_args(pid)
        if stale and a.fix:
            cmd_stop(a)
            ensure_relay()
            time.sleep(3)
            pid, stale = relay_pid(), False
        add("WARN", "relay", f"pid {pid} runs an older copy of tgask.py; rerun with --fix") if stale else add("OK", "relay", f"pid {pid}")
    if pid:
        try:
            age = time.time() - float(HEARTBEAT.read_text())
            add("OK", "heartbeat", f"{age:.0f}s ago") if age < 30 else add("WARN", "heartbeat", f"{age:.0f}s ago (relay stuck?)")
        except Exception:
            add("WARN", "heartbeat", "none yet")

    recent = [f for f in EVENTS.glob("*.jsonl") if time.time() - f.stat().st_mtime < 86400] if EVENTS.exists() else []
    add("OK", "hooks", f"events from {len(recent)} pane(s) in 24h") if recent else \
        add("WARN", "hooks", "no events in 24h; sessions started before the plugin was enabled do not report activity")
    reqs = all_requests()
    stuck = [m["id"] for _, m, _ in reqs if m.get("status") == "answered"]
    orphan = [m["id"] for _, m, _ in reqs if m.get("status") == "orphaned"]
    waiting = [m["id"] for _, m, _ in reqs if m.get("status") in ("pending", "sent")]
    add("WARN" if stuck else "OK", "requests",
        f"{len(waiting)} open, {len(stuck)} answered-undelivered, {len(orphan)} orphaned" + (f": {', '.join(stuck)}" if stuck else ""))
    if a.ping and not any(l == "FAIL" for l, n, _ in res if n in ("token", "allowlist")):
        try:
            api("sendMessage", chat_id=owner(), text="🏓 tg-ask health check: the relay can reach you.")
            add("OK", "ping", "sent")
        except TgError as e:
            add("FAIL", "ping", str(e))
    for level, name, detail in res:
        print(f"{level:4}  {name:16} {detail}")
    return 1 if any(l == "FAIL" for l, _, _ in res) else 0


def cmd_uninstall(a):
    cmd_stop(a)
    ENABLED.unlink(missing_ok=True)
    print("disabled: hooks are now no-ops, relay stopped")
    if a.purge and HOME.exists():
        shutil.rmtree(HOME)
        print(f"removed {HOME}")
    if a.forget_bot:
        for f in (STATE / ".env", STATE / "access.json"):
            if f.exists():
                f.unlink()
                print(f"removed {f}")

# ---------------------------------------------------------------- selftest


def cmd_selftest(_a):
    meta = {"id": "x", "status": "answered", "options": ["A: 跑", "B"], "answer": "多行\n回复: \"引号\""}
    m2, b2 = parse_req(dump_req(meta, "## body\n---\nline"))
    assert m2 == meta and b2 == "## body\n---\nline", (m2, b2)
    rule = "─" * 40
    assert ready_for_input(f"out\n{rule}\n❯ \n{rule}\n  status")
    assert not ready_for_input(f"Do you want to proceed?\n❯ 1. Yes\n  2. No\n{rule}\n❯ ")
    assert not ready_for_input("plain zsh prompt %")
    assert BUSY_RE.search("✽ Kerfuffling… (40s · ↓ 3.3k tokens)")
    assert "<bot-token>" in redact("curl api.telegram.org/bot123456789:" + "x" * 35 + "/getMe")
    assert redact("export API_KEY=abc123") == "export API_KEY=<redacted>"
    assert "ghp_" not in redact("ghp_" + "a" * 30)
    ss = [{"sid": "abc123", "pane": "%1"}, {"sid": "abd999", "pane": "%2"}]
    assert len(match_prefix("ab", ss)) == 2 and match_prefix("abc", ss)[0]["pane"] == "%1"
    assert match_prefix("%2", ss)[0]["sid"] == "abd999" and match_prefix("", ss) == []
    assert slug(" lut / export: 格式?") == "lut-export-格式"
    assert brief({"command": "ls   -la\n x"}) == "ls -la x"
    print("selftest ok")

# ---------------------------------------------------------------- main


def main():
    ap = argparse.ArgumentParser(prog="tgask.py", description=__doc__.split("\n")[0])
    sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("ask", help="file a request for the human (body on stdin)")
    p.add_argument("--summary", required=True)
    p.add_argument("--option", action="append", help="button label; repeat for each option")
    p = sp.add_parser("say", help="send a message to the human")
    p.add_argument("text", nargs="?")
    sp.add_parser("sessions", help="list Claude sessions in tmux")
    sp.add_parser("hook")
    sp.add_parser("relay")
    sp.add_parser("start")
    sp.add_parser("stop")
    sp.add_parser("set-token", help="read a BotFather token on stdin, verify, save")
    sp.add_parser("pair-start")
    p = sp.add_parser("pair-wait")
    p.add_argument("--timeout", type=int, default=300)
    sp.add_parser("enable")
    p = sp.add_parser("health")
    p.add_argument("--fix", action="store_true", help="start or restart the relay when needed")
    p.add_argument("--ping", action="store_true", help="send a test message")
    p = sp.add_parser("uninstall")
    p.add_argument("--purge", action="store_true", help="also delete requests and events")
    p.add_argument("--forget-bot", action="store_true", help="also delete the bot token and allowlist")
    sp.add_parser("selftest")
    a = ap.parse_args()
    fn = globals()["cmd_" + a.cmd.replace("-", "_")]
    sys.exit(fn(a) or 0)


if __name__ == "__main__":
    main()
