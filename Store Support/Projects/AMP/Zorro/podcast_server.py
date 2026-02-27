#!/usr/bin/env python3
"""
Local Podcast Server - Serve podcast files over HTTP
Run this to access podcasts at http://localhost:8888
"""

import os
import json
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import unquote, urlparse
import mimetypes

class PodcastHandler(SimpleHTTPRequestHandler):
    """Custom HTTP handler for podcast files"""
    
    PODCAST_DIR = Path(__file__).parent / "output" / "podcasts"
    METADATA_DIR = Path(__file__).parent / "output" / "metadata"
    
    def do_GET(self):
        """Handle GET requests"""
        # Parse the URL
        parsed = urlparse(self.path)
        path = unquote(parsed.path)
        
        # Serve podcast index
        if path == "/" or path == "/index.html":
            self.serve_index()
            return
        
        # Serve podcast files
        if path.startswith("/podcasts/"):
            filename = path.replace("/podcasts/", "")
            filepath = self.PODCAST_DIR / filename
            if filepath.exists() and filepath.suffix in ['.wav', '.mp3', '.m4a']:
                self.serve_file(filepath)
                return
        
        # Serve metadata
        if path.startswith("/metadata/"):
            filename = path.replace("/metadata/", "")
            filepath = self.METADATA_DIR / filename
            if filepath.exists() and filepath.suffix == '.json':
                self.serve_json(filepath)
                return
        
        # Default 404
        self.send_error(404, "File not found")
    
    def serve_index(self):
        """Serve HTML index page"""
        podcasts = list(self.PODCAST_DIR.glob("*.wav")) + list(self.PODCAST_DIR.glob("*.mp3"))
        
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>AMP Podcast Server</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
        .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #0071ce; margin-bottom: 30px; }}
        .podcast {{ background: #f9f9f9; padding: 20px; margin: 15px 0; border-left: 4px solid #0071ce; border-radius: 4px; }}
        .podcast h3 {{ margin: 0 0 10px 0; color: #333; }}
        .controls {{ display: flex; gap: 10px; margin: 15px 0; flex-wrap: wrap; }}
        audio {{ width: 100%; margin: 10px 0; }}
        button {{ background: #0071ce; color: white; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer; }}
        button:hover {{ background: #005aa3; }}
        .info {{ font-size: 12px; color: #666; margin: 10px 0; }}
        .copy-btn {{ background: #4CAF50; }}
        .copy-btn:hover {{ background: #45a049; }}
        code {{ background: #f0f0f0; padding: 2px 6px; border-radius: 3px; font-family: monospace; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🎙️ AMP Podcast Server</h1>
        <p>Server running on <strong>http://localhost:8888</strong></p>
        <hr>
        
        <h2>Available Podcasts ({len(podcasts)})</h2>
"""
        
        for filepath in sorted(podcasts, reverse=True):
            filename = filepath.name
            file_size = filepath.stat().st_size / (1024 * 1024)
            
            # Try to load metadata
            metadata_file = self.METADATA_DIR / f"{filepath.stem}.json"
            if metadata_file.exists():
                with open(metadata_file) as f:
                    meta = json.load(f)
                    title = meta.get('title', filename)
                    tracking_id = meta.get('tracking_id', 'N/A')
            else:
                title = filename
                tracking_id = 'N/A'
            
            url = f"/podcasts/{filename}"
            file_url = f"http://localhost:8888{url}"
            
            html += f"""
        <div class="podcast">
            <h3>{title}</h3>
            <div class="info">
                <p><strong>File:</strong> {filename}</p>
                <p><strong>Size:</strong> {file_size:.2f} MB | <strong>Tracking ID:</strong> {tracking_id}</p>
            </div>
            <audio controls>
                <source src="{url}" type="audio/wav">
                Your browser does not support the audio element.
            </audio>
            <div class="controls">
                <button onclick="copyToClipboard('{file_url}')">📋 Copy URL</button>
                <button onclick="downloadFile('{url}', '{filename}')">⬇️ Download</button>
            </div>
            <div class="info" style="color: #0071ce;">
                <code>http://localhost:8888{url}</code>
            </div>
        </div>
"""
        
        html += """
    </div>
    <script>
        function copyToClipboard(text) {
            navigator.clipboard.writeText(text).then(() => {
                alert('URL copied to clipboard!');
            });
        }
        function downloadFile(url, filename) {
            const link = document.createElement('a');
            link.href = url;
            link.download = filename;
            link.click();
        }
    </script>
</body>
</html>
"""
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())
    
    def serve_file(self, filepath):
        """Serve audio file"""
        try:
            with open(filepath, 'rb') as f:
                content = f.read()
            
            mime_type, _ = mimetypes.guess_type(str(filepath))
            if not mime_type:
                mime_type = 'audio/wav'
            
            self.send_response(200)
            self.send_header('Content-type', mime_type)
            self.send_header('Content-Length', len(content))
            self.send_header('Accept-Ranges', 'bytes')
            self.end_headers()
            self.wfile.write(content)
        except Exception as e:
            self.send_error(500, str(e))
    
    def serve_json(self, filepath):
        """Serve JSON metadata"""
        try:
            with open(filepath, 'r') as f:
                content = f.read()
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(content.encode())
        except Exception as e:
            self.send_error(500, str(e))
    
    def log_message(self, format, *args):
        """Custom logging"""
        print(f"[{self.client_address[0]}] {format % args}")

def start_server(port=8888):
    """Start the podcast server"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, PodcastHandler)
    
    print(f"""
╔════════════════════════════════════════════════════════╗
║          🎙️  AMP PODCAST SERVER STARTED 🎙️           ║
╚════════════════════════════════════════════════════════╝

✅ Server Running on: http://localhost:{port}

📚 Available URLs:
  • Web Player: http://localhost:{port}
  • Download: http://localhost:{port}/podcasts/[filename]
  • Metadata: http://localhost:{port}/metadata/[json]

📁 Serving from:
  {PodcastHandler.PODCAST_DIR}

⏹️  Press Ctrl+C to stop the server
    """)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n✋ Server stopped.")
        httpd.server_close()

if __name__ == "__main__":
    start_server(8888)
