# keep_alive_server.py o dentro main.py
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import os

class DummyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running on Render.")

def start_dummy_server():
    port = int(os.environ.get("PORT", 10000))  # Render imposta la PORT env var
    server = HTTPServer(("", port), DummyHandler)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
