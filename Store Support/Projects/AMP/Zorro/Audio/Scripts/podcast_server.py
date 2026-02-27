"""Simple HTTP server for streaming generated podcasts."""

import os
import json
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs, unquote
import mimetypes

PODCASTS_DIR = Path("../output/podcasts")
METADATA_DIR = Path("../output/metadata")

class PodcastHandler(SimpleHTTPRequestHandler):
    """Custom HTTP handler for podcast server."""
    
    def do_GET(self):
        """Handle GET requests."""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        # Root path - serve HTML player
        if path == "/" or path == "":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(self.get_html_audio_player().encode())
            return
        
        # Podcasts list API
        if path == "/api/podcasts":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            podcasts = self.get_podcasts_list()
            self.wfile.write(json.dumps(podcasts).encode())
            return
        
        # Delete podcast file
        if path.startswith("/api/delete/"):
            filename = unquote(path.split("/api/delete/")[-1])
            filepath = PODCASTS_DIR / filename
            
            if filepath.exists() and filepath.is_file():
                try:
                    filepath.unlink()
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({"status": "deleted", "filename": filename}).encode())
                    return
                except Exception as e:
                    self.send_response(500)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": str(e)}).encode())
                    return
            else:
                self.send_response(404)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "File not found"}).encode())
                return
        
        # Serve podcast file
        if path.startswith("/podcasts/"):
            filename = unquote(path.split("/")[-1])
            filepath = PODCASTS_DIR / filename
            
            if filepath.exists() and filepath.is_file():
                self.send_response(200)
                mime_type, _ = mimetypes.guess_type(str(filepath))
                self.send_header("Content-type", mime_type or "audio/wav")
                self.send_header("Content-Length", str(filepath.stat().st_size))
                self.end_headers()
                
                with open(filepath, "rb") as f:
                    self.wfile.write(f.read())
                return
        
        # 404
        self.send_response(404)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"<h1>404 - File not found</h1>")
    
    def get_podcasts_list(self):
        """Get list of available podcasts (WAV, MP4, MP3)."""
        podcasts = []
        if PODCASTS_DIR.exists():
            # Get WAV, MP4, and MP3 files (supports SAPI5 and Cloud voices)
            all_files = (list(PODCASTS_DIR.glob("*.wav")) + 
                        list(PODCASTS_DIR.glob("*.mp4")) + 
                        list(PODCASTS_DIR.glob("*.mp3")))
            for file in sorted(all_files, key=os.path.getmtime, reverse=True):
                podcasts.append({
                    "filename": file.name,
                    "size_mb": round(file.stat().st_size / 1024 / 1024, 2),
                    "url": f"/podcasts/{file.name}"
                })
        return podcasts
    
    def get_html_audio_player(self):
        """Return HTML for audio player interface."""
        return """
<!DOCTYPE html>
<html>
<head>
    <title>Zorro - AMP Audio Content</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
        }
        h1 {
            color: white;
            text-align: center;
            margin-bottom: 5px;
            font-size: 28px;
        }
        .breadcrumb {
            text-align: center;
            color: rgba(255,255,255,0.8);
            margin-bottom: 8px;
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .subtitle {
            text-align: center;
            color: rgba(255,255,255,0.9);
            margin-bottom: 30px;
            font-size: 15px;
            font-weight: 500;
        }
        .podcast-list {
            display: grid;
            gap: 15px;
        }
        .podcast-item {
            background: white;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .podcast-item:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(0,0,0,0.3);
        }
        .podcast-title {
            font-weight: 600;
            color: #333;
            margin-bottom: 10px;
            font-size: 16px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .voice-badge {
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
        }
        .podcast-info {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
            font-size: 12px;
            color: #666;
        }
        audio {
            width: 100%;
            margin-bottom: 10px;
            height: 40px;
        }
        .controls {
            display: flex;
            gap: 10px;
        }
        button {
            flex: 1;
            padding: 10px;
            border: none;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 600;
            cursor: pointer;
            transition: background 0.2s;
        }
        .download-btn {
            background: #667eea;
            color: white;
        }
        .download-btn:hover {
            background: #5568d3;
        }
        .copy-btn {
            background: #e0e0e0;
            color: #333;
        }
        .copy-btn:hover {
            background: #d0d0d0;
        }
        .delete-btn {
            background: #ff6b6b;
            color: white;
        }
        .delete-btn:hover {
            background: #ff5252;
        }
        .empty {
            text-align: center;
            color: rgba(255,255,255,0.7);
            padding: 40px;
            font-size: 16px;
        }
        .loading {
            text-align: center;
            color: rgba(255,255,255,0.7);
            padding: 20px;
        }
        .product-type {
            display: inline-block;
            background: rgba(255,255,255,0.2);
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 11px;
            color: rgba(255,255,255,0.9);
            margin-bottom: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="breadcrumb">📍 Zorro Activity Hub</div>
        <h1>Week 4 Summarized Messages</h1>
        <div class="product-type">🔊 Audio Format</div>
        <div class="subtitle">Narrated by: David, Zira</div>
        <div id="audio-list" class="podcast-list">
            <div class="loading">Loading audio files...</div>
        </div>
    </div>

    <script>
        async function loadAudioFiles() {
            try {
                const response = await fetch("/api/podcasts");
                const podcasts = await response.json();
                const container = document.getElementById("audio-list");
                
                if (podcasts.length === 0) {
                    container.innerHTML = '<div class="empty">No audio files available yet.</div>';
                    return;
                }
                
                container.innerHTML = podcasts.map(podcast => {
                    // Extract voice name and format from filename
                    const voiceName = podcast.filename.includes("David") ? "David" : podcast.filename.includes("Zira") ? "Zira" : "Unknown";
                    const fileExt = podcast.filename.split(".").pop().toUpperCase();
                    const audioType = fileExt === "MP4" ? "audio/mp4" : "audio/wav";
                    const voiceBadge = `<span class="voice-badge">${voiceName}</span>`;
                    
                    // Use filename as title to show clear differences
                    const displayTitle = podcast.filename.replace(/\\.(wav|mp4|mp3)$/i, '');
                    
                    return `
                    <div class="podcast-item">
                        <div class="podcast-title">
                            ${displayTitle} ${voiceBadge}
                        </div>
                        <div class="podcast-info">
                            <span>Size: ${podcast.size_mb} MB</span>
                            <span>Format: ${fileExt} (16-bit)</span>
                        </div>
                        <audio controls>
                            <source src="${podcast.url}" type="${audioType}">
                            Your browser does not support the audio element.
                        </audio>
                        <div class="controls">
                            <button class="download-btn" onclick="downloadAudio('${podcast.url}', '${podcast.filename}')">
                                ⬇️ Download
                            </button>
                            <button class="copy-btn" onclick="copyURL('${window.location.origin}${podcast.url}')">
                                📋 Copy Link
                            </button>
                            <button class="delete-btn" onclick="deleteAudio('${podcast.filename}')">
                                🗑️ Delete
                            </button>
                        </div>
                    </div>
                `}).join("");
            } catch (error) {
                document.getElementById("audio-list").innerHTML = 
                    `<div class="empty">Error loading audio: ${error.message}</div>`;
            }
        }
        
        function downloadAudio(url, filename) {
            const link = document.createElement("a");
            link.href = url;
            link.download = filename;
            link.click();
        }
        
        function copyURL(url) {
            navigator.clipboard.writeText(url).then(() => {
                alert("URL copied to clipboard!");
            });
        }
        
        function deleteAudio(filename) {
            if (!confirm(`Are you sure you want to delete: ${filename}?`)) {
                return;
            }
            
            fetch(`/api/delete/${encodeURIComponent(filename)}`, {
                method: 'GET'
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'deleted') {
                    alert(`Deleted: ${filename}`);
                    loadAudioFiles();
                } else {
                    alert(`Error: ${data.error}`);
                }
            })
            .catch(error => {
                alert(`Error deleting file: ${error.message}`);
            });
        }
        
        // Load audio files on page load
        loadAudioFiles();
        
        // Refresh every 5 seconds to pick up new files
        setInterval(loadAudioFiles, 5000);
    </script>
</body>
</html>
"""
    
    def log_message(self, format, *args):
        """Suppress default logging."""
        pass

if __name__ == "__main__":
    import sys
    
    # Change to script directory for relative paths
    script_dir = Path(__file__).parent.parent
    os.chdir(script_dir)
    
    server_address = ("", 8888)
    httpd = HTTPServer(server_address, PodcastHandler)
    print("=" * 70)
    print("PODCAST SERVER RUNNING")
    print("=" * 70)
    print()
    print("🎙️  Access at: http://localhost:8888")
    print()
    print("Serving podcasts from:")
    print(f"  {PODCASTS_DIR.absolute()}")
    print()
    print("Press Ctrl+C to stop")
    print()
    httpd.serve_forever()
