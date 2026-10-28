"""Tiny HTTP service used to demonstrate a CI/CD pipeline."""

import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer


def greeting(name: str = "world") -> str:
    """Return a greeting for the given name."""
    cleaned = name.strip() or "world"
    return f"Hello, {cleaned}!"


class Handler(BaseHTTPRequestHandler):
    def _send_json(self, status: int, payload: dict) -> None:
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):  # noqa: N802 (name required by BaseHTTPRequestHandler)
        if self.path == "/health":
            self._send_json(200, {"status": "ok"})
        elif self.path == "/":
            self._send_json(200, {"message": greeting()})
        else:
            self._send_json(404, {"error": "not found"})

    def log_message(self, fmt, *args):
        # Keep container logs quiet; real services would log structured output.
        return


def main() -> None:
    port = int(os.environ.get("PORT", "8080"))
    server = HTTPServer(("0.0.0.0", port), Handler)
    print(f"Listening on port {port}")
    server.serve_forever()


if __name__ == "__main__":
    main()
