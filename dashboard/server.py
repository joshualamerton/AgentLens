from core.event_stream import get_events
from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        events = get_events()

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        self.wfile.write(json.dumps(events).encode())

def run():
    server = HTTPServer(("localhost", 8080), Handler)
    print("Dashboard running at http://localhost:8080")
    server.serve_forever()

if __name__ == "__main__":
    run()
