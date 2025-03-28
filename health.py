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
    status_file = 'status.json'  # Default value

    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'healthy'}).encode())
        elif self.path == '/status':
            try:
                # Convert to absolute path if relative
                status_path = os.path.abspath(self.status_file)
                with open(status_path, 'r') as f:
                    status = json.load(f)  # Parse JSON to validate format
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(status).encode())
            except FileNotFoundError:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'Status not available yet'}).encode())
            except json.JSONDecodeError:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'Invalid JSON in status file'}).encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not found')

if __name__ == '__main__':
    args = parser.parse_args()
    HealthHandler.status_file = args.status_file  # Set the status file path as a class variable
    httpd = HTTPServer(('0.0.0.0', args.port), HealthHandler)
    print(f'Starting server on port {args.port}')
    print(f'Using status file: {os.path.abspath(args.status_file)}')
    httpd.serve_forever()