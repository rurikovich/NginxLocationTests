from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class H(BaseHTTPRequestHandler):
    def do_GET(self):
        body = {
            "path": self.path,
            "headers": {k: v for k, v in self.headers.items()}
        }
        self.send_response(200)
        self.send_header("Content-Type","application/json")
        self.end_headers()
        self.wfile.write(json.dumps(body).encode())

HTTPServer(("0.0.0.0", 9000), H).serve_forever()
