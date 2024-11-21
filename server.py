import ssl
from http.server import SimpleHTTPRequestHandler, HTTPServer
import os

class BrotliHTTPRequestHandler(SimpleHTTPRequestHandler):
    def guess_type(self, path):
        """Add Brotli support for JavaScript files."""
        if path.endswith(".js.br"):
            return "application/javascript"
        return super().guess_type(path)
        
    def end_headers(self):
        if self.path.endswith(".br"):
            self.send_header("Content-Encoding", "br")
        super().end_headers()

if __name__ == "__main__":
    port = 3000
    httpd = HTTPServer(("localhost", port), BrotliHTTPRequestHandler)
    httpd.socket = ssl.wrap_socket(
        httpd.socket, 
        keyfile="key.pem", 
        certfile="cert.pem", 
        server_side=True
    )
    print(f"Starting server at https://localhost:{port}")
    httpd.serve_forever()
