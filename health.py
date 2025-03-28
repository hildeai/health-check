from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os
import argparse

# Set up argument parser
parser = argparse.ArgumentParser(description='Health check server')
parser.add_argument('-p', '--port', type=int, default=3033,
                    help='Port to run the server on (default: 3033)')
parser.add_argument('-s', '--status-file', type=str, default='status.json',
                    help='Path to the status.json file (default: status.json)')

class HealthHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.status_file = args[2].status_file if len(args) > 2 else 'status.json'
        super().__init__(*args[:2], **kwargs)

    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'healthy'}).encode())
        elif self.path == '/status':
            try:
                with open(self.status_file, 'r') as f:
                    status = f.read()
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(status.encode())
            except FileNotFoundError:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(json.dumps({'error': f'Status file not found: {self.status_file}'}).encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not found')

if __name__ == '__main__':
    args = parser.parse_args()
    handler = lambda *handler_args: HealthHandler(*handler_args, args)
    httpd = HTTPServer(('0.0.0.0', args.port), handler)
    print(f'Starting server on port {args.port}')
    print(f'Using status file: {args.status_file}')
    httpd.serve_forever()