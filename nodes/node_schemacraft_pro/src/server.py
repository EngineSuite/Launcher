# Standalone Zero-Dependency Micro-Server
import http.server
import socketserver
import json
import os
import sys
from pathlib import Path

PORT = int(os.environ.get("PORT", 8080))
NODE_ROOT = Path(__file__).resolve().parent.parent
PUBLIC_DIR = NODE_ROOT / "public"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from schema_engine import SchemaEngine

class EngineHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(PUBLIC_DIR), **kwargs)

    def do_GET(self):
        if self.path == "/api/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps({
                "status": "HEALTHY",
                "node": "schemacraft_pro",
                "upfront_cost": "$0.00",
                "version": "1.0.0"
            }).encode())
            return
        super().do_GET()

    def do_POST(self):
        if self.path == "/api/generate":
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length)
            try:
                data = json.loads(body.decode())
                schema_type = data.get("type", "LocalBusiness")
                if schema_type == "LocalBusiness":
                    res = SchemaEngine.generate_local_business(
                        name=data.get("name", "My Business"),
                        category=data.get("category", "LocalBusiness"),
                        url=data.get("url", "https://example.com"),
                        phone=data.get("phone", ""),
                        address=data.get("address", {}),
                        price_range=data.get("price_range", "$$")
                    )
                else:
                    res = {"@context": "https://schema.org", "@type": schema_type}

                validation = SchemaEngine.validate_schema(res)

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps({"schema": res, "validation": validation}).encode())
            except Exception as e:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode())
            return

def run_server(port=PORT):
    with socketserver.TCPServer(("", port), EngineHandler) as httpd:
        print(f"SchemaCraft Pro server live at http://localhost:{port}")
        httpd.serve_forever()

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else PORT
    run_server(port)
