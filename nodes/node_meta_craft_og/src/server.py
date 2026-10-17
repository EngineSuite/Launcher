# MetaCraft OG Zero-Dependency Server
import http.server
import socketserver
import os
import sys
from pathlib import Path

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8082
PUBLIC_DIR = Path(__file__).resolve().parent.parent / "public"

class SafeHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(PUBLIC_DIR), **kwargs)

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()

def run_server():
    os.chdir(PUBLIC_DIR)
    with socketserver.TCPServer(("", PORT), SafeHandler) as httpd:
        print(f"MetaCraft OG live at http://localhost:{PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    run_server()
