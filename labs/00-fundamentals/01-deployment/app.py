"""Lab 0 demo app: a page with a visit counter. Standard library only.

Settings, all optional:
  GREETING          environment variable, read once at start
  /config/message   file, read on every request
  REDIS_HOST        database host; without it the page has no counter
  REDIS_PASSWORD    database password
  NODE_NAME         node the pod runs on, from the downward API
"""

import os
import signal
import socket
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

GREETING = os.environ.get("GREETING", "Hello")
MESSAGE_FILE = "/config/message"
UNREADY_FLAG = "/tmp/unready"
hog = []  # memory held by /hog, never released


def count_visit():
    """Add one to the counter in Redis and return the new value."""
    host = os.environ.get("REDIS_HOST")
    if not host:
        return "no database configured"
    try:
        with socket.create_connection((host, 6379), timeout=2) as conn:
            stream = conn.makefile("rwb")

            def command(*parts):
                stream.write(b"*%d\r\n" % len(parts))
                for part in parts:
                    data = part.encode()
                    stream.write(b"$%d\r\n%s\r\n" % (len(data), data))
                stream.flush()
                reply = stream.readline().strip()
                if reply.startswith(b"-"):
                    raise RuntimeError(reply[1:].decode())
                return reply

            password = os.environ.get("REDIS_PASSWORD")
            if password:
                command("AUTH", password)
            return int(command("INCR", "visits")[1:])
    except (OSError, RuntimeError, ValueError) as err:
        return f"database error: {err}"


def read_message():
    try:
        with open(MESSAGE_FILE) as f:
            return f.read().strip()
    except OSError:
        return "no message file"


class Handler(BaseHTTPRequestHandler):
    def reply(self, status, text):
        body = (text + "\n").encode()
        self.send_response(status)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        url = urlparse(self.path)
        if url.path == "/healthz":
            self.reply(200, "ok")
        elif url.path == "/readyz":
            if os.path.exists(UNREADY_FLAG):
                self.reply(503, "not ready")
            else:
                self.reply(200, "ready")
        elif url.path == "/hog":
            megabytes = int(parse_qs(url.query).get("mb", ["50"])[0])
            hog.append(bytearray(megabytes * 1024 * 1024))
            self.reply(200, f"holding {sum(len(b) for b in hog) >> 20} MB")
        elif url.path == "/":
            secret = os.environ.get("REDIS_PASSWORD")
            self.reply(
                200,
                "\n".join(
                    [
                        f"greeting: {GREETING}",
                        f"message:  {read_message()}",
                        f"visits:   {count_visit()}",
                        f"secret:   {'set' if secret else 'not set'}",
                        f"pod:      {socket.gethostname()}",
                        f"node:     {os.environ.get('NODE_NAME', 'unknown')}",
                    ]
                ),
            )
        else:
            self.reply(404, "not found")

    def log_message(self, fmt, *args):
        if self.path not in ("/healthz", "/readyz"):
            super().log_message(fmt, *args)


if __name__ == "__main__":
    # On SIGTERM keep serving for a few seconds, then exit. Kubernetes stops
    # sending traffic to a pod at about the same time as it signals it, so
    # exiting at once would drop requests already on their way.
    signal.signal(
        signal.SIGTERM,
        lambda signum, frame: threading.Timer(3, os._exit, [0]).start(),
    )
    ThreadingHTTPServer(("", 8080), Handler).serve_forever()
