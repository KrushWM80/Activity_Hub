#!/usr/bin/env python3
"""
Simple HTTP Server for AMP Dashboard
Serves the amp_selector_dashboard.html with proper CORS and file access
"""
import http.server
import socketserver
import os
import webbrowser
from pathlib import Path

PORT = 8000
HANDLER = http.server.SimpleHTTPRequestHandler

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()
    
    def do_GET(self):
        if self.path == '/':
            self.path = '/amp_selector_dashboard.html'
        return super().do_GET()

def run_server():
    # Change to the correct directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        print(f"🌐 AMP Dashboard Server Started")
        print(f"📍 http://localhost:{PORT}")
        print(f"📂 Serving from: {script_dir}")
        print(f"✅ Press Ctrl+C to stop")
        
        # Open browser
        webbrowser.open(f'http://localhost:{PORT}')
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n✅ Server stopped")

if __name__ == "__main__":
    run_server()
