#!/usr/bin/env python3
"""
Web Server for Digital Egg Hunt Frontend
Serves the frontend interface and assets on port 4326
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import os
import sys

PORT = 4326

class MyHTTPRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        # Change working directory to the directory containing this script
        script_dir = Path(__file__).parent / "frontend"
        super().__init__(*args, directory=str(script_dir), **kwargs)
    
    def do_GET(self):
        """Handle GET requests, route /Digital_Egg_Hunt to index.html"""
        if self.path == '/' or self.path == '/Digital_Egg_Hunt' or self.path.startswith('/Digital_Egg_Hunt?'):
            self.path = '/index.html'
        return super().do_GET()
    
    def log_message(self, format, *args):
        """Custom log messages"""
        print(f"[{self.log_date_time_string()}] {format % args}")

def main():
    frontend_dir = Path(__file__).parent / "frontend"
    
    if not frontend_dir.exists():
        print(f"❌ ERROR: Frontend directory not found: {frontend_dir}")
        sys.exit(1)
    
    os.chdir(frontend_dir)
    
    server_address = ('', PORT)
    httpd = HTTPServer(server_address, MyHTTPRequestHandler)
    
    print("=" * 70)
    print("🥚 Digital Egg Hunt - Web Server 🥚")
    print("=" * 70)
    print(f"✅ Server starting on port {PORT}")
    print(f"📍 Access at: http://weus42608431466:{PORT}/Digital_Egg_Hunt")
    print(f"📁 Serving from: {frontend_dir}")
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 70)
    print()
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
        sys.exit(0)

if __name__ == "__main__":
    main()
