# CloudZero Zero-Dependency Micro-Server
import http.server
import socketserver
import json
import os
import sys
from pathlib import Path

PORT = int(os.environ.get("PORT", 8081))
PUBLIC_DIR = Path(__file__).resolve().parent.parent / "public"

class PlaybookHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(PUBLIC_DIR), **kwargs)

    def do_GET(self):
        if self.path == "/api/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "HEALTHY", "node": "dev_cheatsheet_vault", "cost": "$0.00"}).encode())
            return
        super().do_GET()

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else PORT
    with socketserver.TCPServer(("", port), PlaybookHandler) as httpd:
        print(f"CloudZero server live at http://localhost:{port}")
        httpd.serve_forever()
