#!/usr/bin/env python3
"""
Zorro Activity Hub - Audio Server with Jenny Neural Voice Integration
Serve audio files over HTTP with Zorro-styled interface
Run this to access at http://localhost:8888
"""

import os
import json
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler
from socketserver import ThreadingMixIn
from urllib.parse import unquote, urlparse
import mimetypes
import re
from datetime import datetime
import sys

# Initialize mimetypes
mimetypes.init()
mimetypes.add_type('audio/mp4', '.m4a')
mimetypes.add_type('audio/mp4', '.mp4')

# Add Audio directory to path for MP4 pipeline
audio_dir = Path(__file__).parent / "Audio"
sys.path.insert(0, str(audio_dir))
# Add Scripts directory for weekly audio pipeline
scripts_dir = Path(__file__).parent / "Audio" / "Scripts"
sys.path.insert(0, str(scripts_dir))

class AudioHandler(SimpleHTTPRequestHandler):
    """Custom HTTP handler for audio files"""
    
    AUDIO_DIR = Path(__file__).parent / "output" / "Audio"
    METADATA_DIR = Path(__file__).parent / "output" / "metadata"
    MP4_OUTPUT_DIR = Path(__file__).parent / "Audio" / "mp4_output"
    
    # Initialize MP4 pipeline on first use
    _mp4_pipeline = None
    
    @classmethod
    def get_pipeline(cls):
        """Lazy-load MP4 pipeline"""
        if cls._mp4_pipeline is None:
            try:
                from mp4_pipeline import MP4Pipeline
                cls._mp4_pipeline = MP4Pipeline()
            except ImportError as e:
                print(f"WARNING: Could not import MP4Pipeline: {e}")
                cls._mp4_pipeline = False
        return cls._mp4_pipeline if cls._mp4_pipeline else None
    
    def do_GET(self):
        """Handle GET requests"""
        # Parse the URL
        parsed = urlparse(self.path)
        path = unquote(parsed.path)

        # Strip the /Zorro/Audio_Message_Hub prefix for hostname-based URL support
        if path.startswith("/Zorro/Audio_Message_Hub"):
            path = path[len("/Zorro/Audio_Message_Hub"):] or "/"
        
        # Serve Spark logo
        if path == "/Spark_Blank.png":
            logo = Path(__file__).parent / "Spark_Blank.png"
            if logo.exists():
                self.serve_file(logo)
            else:
                self.send_error(404, "Logo not found")
            return

        # Serve Jenny Audio generator page
        if path in ("/create-audio", "/create-audio/", "/summarized-audio", "/summarized-audio/"):
            self.serve_jenny_audio_page()
            return
        
        # Serve generated MP4 audio files
        if path.startswith("/audio/"):
            filename = path.replace("/audio/", "")
            filepath = self.MP4_OUTPUT_DIR / filename
            if filepath.exists() and filepath.suffix in ['.mp4', '.m4a']:
                self.serve_file(filepath)
                return
        
        # Serve audio index
        if path == "/" or path == "/index.html":
            try:
                self.serve_index()
            except Exception as e:
                import traceback
                traceback.print_exc()
                self.send_error(500, str(e))
            return
        
        # Serve audio files
        if path.startswith("/audio/"):
            filename = path.replace("/audio/", "")
            filepath = self.AUDIO_DIR / filename
            if filepath.exists() and filepath.suffix in ['.wav', '.mp3', '.m4a', '.mp4', '.txt', '.html']:
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
    
    def do_POST(self):
        """Handle POST requests for Jenny audio generation and file operations"""
        parsed = urlparse(self.path)
        path = unquote(parsed.path)

        # Strip the /Zorro/Audio_Message_Hub prefix for hostname-based URL support
        if path.startswith("/Zorro/Audio_Message_Hub"):
            path = path[len("/Zorro/Audio_Message_Hub"):]
        
        # Handle Jenny audio generation API
        if path == "/api/generate-jenny-audio" or path == "/api/generate-audio":
            self.handle_jenny_generation()
            return
        
        # Handle file deletion
        if path == "/api/delete-file":
            self.handle_delete_file()
            return
        
        # Handle template generation
        if path == "/api/generate-from-template":
            self.handle_template_generation()
            return
        
        # Handle setting Stream URL for an audio file
        if path == "/api/set-audio-link":
            self.handle_set_audio_link()
            return
        
        # Handle sending email report
        if path == "/api/send-email-report":
            self.handle_send_email_report()
            return
        
        # Default 404
        self.send_error(404, "API endpoint not found")
    
    def handle_jenny_generation(self):
        """Handle Jenny MP4 audio generation request"""
        try:
            # Read request body
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            params = json.loads(body)
            
            # Extract parameters
            title = params.get('title', 'Activity Update')
            description = params.get('description', 'New activity message')
            area = params.get('area', 'General')
            activity_type = params.get('type', 'FYI')
            priority = params.get('priority', 'medium')
            
            # Get MP4 pipeline
            pipeline = self.get_pipeline()
            if not pipeline:
                self.send_json_response({'success': False, 'error': 'MP4 pipeline not available'}, 500)
                return
            
            # Build audio script
            priority_text = 'HIGH PRIORITY' if priority.lower() in ['high', '1'] else \
                          'priority message' if priority.lower() in ['medium', '2'] else \
                          'informational message'
            
            audio_script = f"""
            Hello and welcome to Walmart Activity Hub.
            
            This is a {priority_text} announcement from {area}.
            
            {title}
            
            Details: {description}
            
            This announcement is classified as {activity_type}.
            
            Please review this information and ensure your team is aware.
            
            Thank you for your attention.
            """
            
            # Generate MP4
            from mp4_pipeline import Voice
            success, output_file = pipeline.synthesize(audio_script, voice=Voice.JENNY)
            
            if success and output_file:
                output_path = Path(output_file)
                file_size_kb = output_path.stat().st_size / 1024
                filename = output_path.name
                
                response = {
                    'success': True,
                    'audio_url': f'/audio/{filename}',
                    'filename': filename,
                    'size_kb': round(file_size_kb, 1),
                    'voice': 'Jenny Neural',
                    'codec': 'AAC @ 256kbps',
                    'title': title
                }
                self.send_json_response(response, 200)
            else:
                self.send_json_response({'success': False, 'error': 'Audio generation failed'}, 500)
        
        except json.JSONDecodeError:
            self.send_json_response({'success': False, 'error': 'Invalid JSON'}, 400)
        except Exception as e:
            print(f"Error generating Jenny audio: {e}")
            self.send_json_response({'success': False, 'error': str(e)}, 500)
    
    def handle_delete_file(self):
        """Handle file deletion request"""
        try:
            # Read request body
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            params = json.loads(body)
            
            filename = params.get('filename', '')
            
            if not filename:
                self.send_json_response({'success': False, 'error': 'No filename provided'}, 400)
                return
            
            # Determine if file is from output/Audio or Audio/mp4_output
            audio_path = self.AUDIO_DIR / filename
            mp4_path = self.MP4_OUTPUT_DIR / filename
            
            deleted = False
            if audio_path.exists():
                try:
                    audio_path.unlink()
                    deleted = True
                    print(f"Deleted audio file: {filename}")
                except Exception as e:
                    print(f"Error deleting audio file: {e}")
                    self.send_json_response({'success': False, 'error': f'Failed to delete file: {e}'}, 500)
                    return
            elif mp4_path.exists():
                try:
                    mp4_path.unlink()
                    deleted = True
                    print(f"Deleted MP4 file: {filename}")
                except Exception as e:
                    print(f"Error deleting MP4 file: {e}")
                    self.send_json_response({'success': False, 'error': f'Failed to delete file: {e}'}, 500)
                    return
            
            if deleted:
                self.send_json_response({'success': True, 'message': f'File {filename} deleted successfully'}, 200)
            else:
                self.send_json_response({'success': False, 'error': 'File not found'}, 404)
        
        except json.JSONDecodeError:
            self.send_json_response({'success': False, 'error': 'Invalid JSON'}, 400)
        except Exception as e:
            print(f"Error handling file deletion: {e}")
            self.send_json_response({'success': False, 'error': str(e)}, 500)
    
    def handle_template_generation(self):
        """Handle automated weekly message audio generation from BigQuery data.
        
        Supports two-phase VPN workflow:
          phase='fetch'     → Pull BQ data + cache (requires VPN)
          phase='synthesize' → Build audio from cache (requires OFF VPN)
          phase=null/omit   → Auto: try full pipeline, fallback to cache
        """
        try:
            # Read request body
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            params = json.loads(body)
            
            week = params.get('week')  # Required
            fy = params.get('fy')      # Required
            force = params.get('force', False)
            phase = params.get('phase')  # 'fetch', 'synthesize', or None (auto)
            
            # If not forcing and not fetch-only, check if file already exists
            if not force and phase != 'fetch' and week:
                existing = self.AUDIO_DIR / f"Weekly Messages Audio Template - Summarized - Week {week} - Jenny Neural - Vimeo.mp4"
                if existing.exists():
                    file_size_kb = existing.stat().st_size / 1024
                    response = {
                        'success': True,
                        'message': 'Template file already exists. Send force=true to regenerate.',
                        'filename': existing.name,
                        'size_kb': round(file_size_kb, 1)
                    }
                    self.send_json_response(response, 200)
                    return
            
            # Run the pipeline
            from generate_weekly_audio import generate_weekly_message_audio
            print(f"Starting pipeline: week={week}, fy={fy}, phase={phase or 'auto'}")
            result = generate_weekly_message_audio(
                week=int(week) if week else None,
                fy=int(fy) if fy else None,
                voice="Jenny",
                rate=0.95,
                output_dir=str(self.AUDIO_DIR),
                phase=phase
            )
            
            if result.get('success'):
                response = {
                    'success': True,
                    'phase_completed': result.get('phase_completed'),
                    'event_count': result.get('event_count', 0),
                    'review_no_comm_count': result.get('review_no_comm_count', 0),
                    'summarized_count': result.get('summarized_count', 0),
                }
                if result.get('output_file'):
                    output_path = Path(result['output_file'])
                    response['filename'] = output_path.name
                    response['audio_url'] = f'/audio/{output_path.name}'
                    response['size_kb'] = round(output_path.stat().st_size / 1024, 1)
                    response['voice'] = 'Jenny Neural (V2 Enhanced Prosody)'
                    response['codec'] = 'AAC @ 256kbps'
                    response['script_length'] = result.get('script_length', 0)
                    response['duration_seconds'] = result.get('duration_seconds', 0)
                if result.get('email_report'):
                    report_path = Path(result['email_report'])
                    response['email_report_url'] = f'/audio/{report_path.name}'
                self.send_json_response(response, 200)
            else:
                self.send_json_response({
                    'success': False,
                    'error': result.get('error', 'Unknown error'),
                    'event_count': result.get('event_count', 0),
                    'review_no_comm_count': result.get('review_no_comm_count', 0),
                    'summarized_count': result.get('summarized_count', 0),
                }, 500)
        
        except json.JSONDecodeError:
            self.send_json_response({'success': False, 'error': 'Invalid JSON'}, 400)
        except Exception as e:
            print(f"Error in weekly audio pipeline: {e}")
            import traceback
            traceback.print_exc()
            self.send_json_response({'success': False, 'error': str(e)}, 500)
    
    def serve_jenny_audio_page(self):
        """Serve Jenny Neural Voice audio generator page"""
        html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Jenny Neural - Summarized Audio Generator</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #1E3A8A 0%, #1D4ED8 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #1E3A8A 0%, #1D4ED8 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        .header h1 {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 12px;
            font-size: 28px;
            margin-bottom: 8px;
        }
        .header p {
            font-size: 14px;
            opacity: 0.9;
        }
        .content {
            padding: 30px;
        }
        .form-group {
            margin-bottom: 20px;
        }
        .form-group label {
            display: block;
            font-weight: 600;
            margin-bottom: 8px;
            color: #1A202C;
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .form-row {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }
        input, select, textarea {
            width: 100%;
            padding: 10px 12px;
            border: 1px solid #E2E8F0;
            border-radius: 6px;
            font-family: inherit;
            font-size: 14px;
            transition: all 0.3s ease;
        }
        input:focus, select:focus, textarea:focus {
            outline: none;
            border-color: #3B82F6;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
        }
        textarea {
            resize: vertical;
            min-height: 100px;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, monospace;
        }
        .button-group {
            display: flex;
            gap: 12px;
            margin-top: 30px;
            align-items: center;
        }
        button {
            flex: 1;
            padding: 12px 24px;
            background: linear-gradient(135deg, #1E3A8A 0%, #1D4ED8 100%);
            color: white;
            border: none;
            border-radius: 6px;
            font-weight: 600;
            cursor: pointer;
            font-size: 14px;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        button:hover:not(:disabled) {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(30, 58, 138, 0.3);
        }
        button:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }
        button.secondary {
            background: #E2E8F0;
            color: #1A202C;
        }
        button.secondary:hover:not(:disabled) {
            background: #CBD5E0;
        }
        #status {
            font-size: 14px;
            font-weight: 500;
            margin-left: auto;
        }
        .result {
            display: none;
            margin-top: 30px;
            padding: 20px;
            background: #F0FFF4;
            border: 1px solid #9AE6B4;
            border-radius: 8px;
            border-left: 4px solid #38A169;
        }
        .result.show {
            display: block;
            animation: slideIn 0.3s ease;
        }
        .result.error {
            background: #FED7D7;
            border-color: #FC8181;
            border-left-color: #E53E3E;
        }
        @keyframes slideIn {
            from { opacity: 0; transform: translateY(-10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .result h3 {
            color: #38A169;
            margin-bottom: 12px;
            font-size: 16px;
        }
        .result.error h3 {
            color: #E53E3E;
        }
        .result-content {
            font-size: 13px;
            line-height: 1.6;
            color: #2D3748;
        }
        .result-content strong {
            color: #1A202C;
        }
        audio {
            width: 100%;
            margin-top: 16px;
            margin-bottom: 8px;
        }
        .nav-link {
            display: inline-block;
            margin-top: 20px;
            color: #3B82F6;
            text-decoration: none;
            font-size: 13px;
            font-weight: 600;
        }
        .nav-link:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>
                <span>🎤</span>
                <span>Jenny Neural Voice</span>
            </h1>
            <p>Generate MP4 audio messages with Jenny Neural voice</p>
        </div>
        
        <div class="content">
            <form id="audioForm">
                <div class="form-row">
                    <div class="form-group">
                        <label for="title">Activity Title *</label>
                        <input type="text" id="title" placeholder="e.g., Store Remodeling Update" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="area">Store Area</label>
                        <select id="area">
                            <option value="Total Store">Total Store</option>
                            <option value="Admin & Support">Admin & Support</option>
                            <option value="Asset Protection">Asset Protection</option>
                            <option value="Pharmacy">Pharmacy</option>
                            <option value="Fresh">Fresh</option>
                            <option value="Food">Food</option>
                            <option value="Frontend">Frontend</option>
                        </select>
                    </div>
                </div>
                
                <div class="form-row">
                    <div class="form-group">
                        <label for="type">Activity Type</label>
                        <select id="type">
                            <option value="Inform">Inform - FYI</option>
                            <option value="Verification">Verification - Action Required</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label for="priority">Priority</label>
                        <select id="priority">
                            <option value="medium">Medium Priority</option>
                            <option value="high">High - Time Sensitive</option>
                            <option value="low">Low - Reference Only</option>
                        </select>
                    </div>
                </div>
                
                <div class="form-group">
                    <label for="description">Message Description *</label>
                    <textarea id="description" placeholder="Enter the activity message text to be synthesized..." required></textarea>
                </div>
                
                <div class="button-group">
                    <button type="submit" id="generateBtn">🎤 Generate MP4 Audio</button>
                    <button type="reset" class="secondary">🔄 Clear</button>
                    <span id="status"></span>
                </div>
            </form>
            
            <div id="result" class="result">
                <h3 id="resultTitle">✅ Audio Generated Successfully</h3>
                <div class="result-content" id="resultContent"></div>
                <audio id="audioPlayer" controls></audio>
            </div>
            
            <a href="/" class="nav-link">← Back to Audio Library</a>
        </div>
    </div>
    
    <script>
        document.getElementById('audioForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const title = document.getElementById('title').value;
            const description = document.getElementById('description').value;
            const area = document.getElementById('area').value;
            const type = document.getElementById('type').value;
            const priority = document.getElementById('priority').value;
            
            const btn = document.getElementById('generateBtn');
            const status = document.getElementById('status');
            const result = document.getElementById('result');
            const player = document.getElementById('audioPlayer');
            
            // Show loading status
            btn.disabled = true;
            status.textContent = '⏳ Generating audio...';
            status.style.color = '#D69E2E';
            result.classList.remove('show', 'error');
            
            try {
                const response = await fetch('/api/generate-audio', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ title, description, area, type, priority })
                });
                
                const data = await response.json();
                
                if (data.success && data.audio_url) {
                    status.textContent = '✅ Ready to play!';
                    status.style.color = '#38A169';
                    
                    document.getElementById('resultTitle').textContent = '✅ Audio Generated Successfully';
                    result.classList.remove('error');
                    document.getElementById('resultContent').innerHTML = `
                        <p><strong>Title:</strong> ${data.title}</p>
                        <p><strong>File:</strong> ${data.filename}</p>
                        <p><strong>Size:</strong> ${data.size_kb} KB</p>
                        <p><strong>Voice:</strong> ${data.voice}</p>
                        <p><strong>Codec:</strong> ${data.codec}</p>
                    `;
                    
                    player.src = data.audio_url;
                    result.classList.add('show');
                    
                    setTimeout(() => {
                        player.play().catch(e => console.log('Auto-play prevented'));
                    }, 200);
                } else {
                    throw new Error(data.error || 'Unknown error');
                }
            } catch (error) {
                console.error('Error:', error);
                status.textContent = '❌ Error: ' + error.message;
                status.style.color = '#E53E3E';
                
                document.getElementById('resultTitle').textContent = '❌ Audio Generation Failed';
                result.classList.add('show', 'error');
                document.getElementById('resultContent').innerHTML = `<p>${error.message}</p>`;
            } finally {
                btn.disabled = false;
            }
        });
    </script>
</body>
</html>
"""
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())
    
    def send_json_response(self, data, status_code=200):
        """Send JSON response"""
        response = json.dumps(data)
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(response.encode())
    
    # ── Audio Link (Stream URL) persistence ──────────────────────────
    LINKS_FILE = Path(__file__).parent / "output" / "Audio" / "audio_links.json"
    
    @classmethod
    def _load_audio_links(cls):
        if cls.LINKS_FILE.exists():
            with open(cls.LINKS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    @classmethod
    def _save_audio_links(cls, links):
        cls.LINKS_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(cls.LINKS_FILE, 'w', encoding='utf-8') as f:
            json.dump(links, f, indent=2)
    
    def handle_set_audio_link(self):
        """Save a Stream/SharePoint URL for an audio file."""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            params = json.loads(body)
            
            filename = params.get('filename', '').strip()
            link = params.get('link', '').strip()
            
            if not filename:
                self.send_json_response({'success': False, 'error': 'filename is required'}, 400)
                return
            
            links = self._load_audio_links()
            if link:
                links[filename] = link
            else:
                links.pop(filename, None)
            self._save_audio_links(links)
            
            self.send_json_response({'success': True, 'filename': filename, 'link': link})
        except Exception as e:
            self.send_json_response({'success': False, 'error': str(e)}, 500)
    
    def handle_send_email_report(self):
        """Send the Weekly Messages Audio Report email via Outlook COM."""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            params = json.loads(body)
            
            week = params.get('week')
            fy = params.get('fy', 2027)
            to = params.get('to', 'kendall.rush@walmart.com')
            
            if not week:
                self.send_json_response({'success': False, 'error': 'week is required'}, 400)
                return
            
            recipients = [r.strip() for r in to.split(';') if r.strip()]
            
            from generate_weekly_audio import send_audio_report_email
            result = send_audio_report_email(int(week), int(fy), to_recipients=recipients)
            
            status_code = 200 if result.get('success') else 500
            self.send_json_response(result, status_code)
        except Exception as e:
            print(f"Error sending email report: {e}")
            import traceback
            traceback.print_exc()
            self.send_json_response({'success': False, 'error': str(e)}, 500)
    
    def serve_index(self):
        """Serve Audio Message Hub index page"""
        # Collect audio files from both /output/Audio/ and /Audio/mp4_output/
        audio_files = []
        
        # Collect from main audio directory
        if self.AUDIO_DIR.exists():
            mp4_files = list(self.AUDIO_DIR.glob("*.mp4"))
            mp3_files = list(self.AUDIO_DIR.glob("*.mp3"))
            wav_files = list(self.AUDIO_DIR.glob("*.wav"))
            audio_files.extend(mp4_files + mp3_files + wav_files)
        
        # Collect from MP4 output directory (newly generated files)
        if self.MP4_OUTPUT_DIR.exists():
            mp4_output_files = list(self.MP4_OUTPUT_DIR.glob("*.mp4"))
            audio_files.extend(mp4_output_files)
        
        # Remove duplicates and sort by date (newest first)
        audio_files = sorted(set(audio_files), key=lambda x: x.stat().st_mtime, reverse=True)
        
        # Function to extract voice from filename
        def get_voice_from_filename(filename):
            filename_lower = filename.lower()
            if 'jenny' in filename_lower:
                return 'JENNY'
            elif 'david' in filename_lower:
                return 'DAVID'
            elif 'zira' in filename_lower:
                return 'ZIRA'
            else:
                return 'UNKNOWN'
        
        # Function to get badge color and emoji
        def get_voice_badge(voice):
            badges = {
                'JENNY': ('🎤 JENNY', '#06B6D4', '#0891b2'),  # cyan
                'DAVID': ('🎙️ DAVID', '#A855F7', '#9333ea'),  # purple
                'ZIRA': ('🗣️ ZIRA', '#EC4899', '#be185d'),    # pink
                'UNKNOWN': ('❓ UNKNOWN', '#6B7280', '#4b5563') # gray
            }
            label, bg_color, hover_color = badges.get(voice, badges['UNKNOWN'])
            return label, bg_color, hover_color
        
        html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Audio Message Hub - Zorro Activity Hub</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
            background: #F7FAFC;
            min-height: 100vh;
            padding: 20px;
        }
        
        .header {
            background: linear-gradient(135deg, #1E3A8A 0%, #1D4ED8 100%);
            color: white;
            padding: 32px 24px;
            border-radius: 12px;
            margin-bottom: 30px;
            text-align: center;
            box-shadow: 0 4px 20px rgba(30, 58, 138, 0.25);
        }

        .header-logo {
            height: 48px;
            vertical-align: middle;
            margin-bottom: 8px;
        }
        
        .header h1 {
            font-size: 26px;
            margin-bottom: 6px;
            font-weight: 700;
            color: white;
        }
        
        .header p {
            font-size: 14px;
            opacity: 0.95;
            margin-bottom: 15px;
        }
        
        .header .branding {
            font-size: 12px;
            opacity: 0.85;
            font-weight: 500;
            color: #BFDBFE;
        }
        
        .container {
            max-width: 1000px;
            margin: 0 auto;
        }
        
        .generator-section {
            background: white;
            padding: 25px;
            border-radius: 12px;
            margin-bottom: 30px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            border-left: 5px solid #3B82F6;
        }
        
        .generator-section h2 {
            color: #1F2937;
            margin-bottom: 15px;
            font-size: 18px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .generator-section p {
            color: #6B7280;
            margin-bottom: 15px;
            font-size: 14px;
        }
        
        .generate-btn {
            display: inline-block;
            background: linear-gradient(135deg, #3B82F6 0%, #1D4ED8 100%);
            color: white;
            padding: 12px 28px;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 600;
            transition: all 0.3s ease;
            border: none;
            cursor: pointer;
            font-size: 14px;
        }
        
        .generate-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(29, 78, 216, 0.3);
        }
        
        .files-section h2 {
            color: #1F2937;
            margin-bottom: 20px;
            font-size: 20px;
            font-weight: 700;
        }
        
        .files-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .file-card {
            background: white;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            transition: all 0.3s ease;
            border-top: 4px solid #E5E7EB;
        }
        
        .file-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.12);
        }
        
        .file-header {
            padding: 15px;
            background: #F9FAFB;
            border-bottom: 1px solid #E5E7EB;
        }
        
        .voice-badge {
            display: inline-block;
            padding: 6px 12px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 600;
            color: white;
            margin-bottom: 10px;
        }
        
        .file-title {
            color: #1F2937;
            font-size: 14px;
            font-weight: 600;
            margin-bottom: 8px;
            word-break: break-word;
            max-height: 40px;
            overflow: hidden;
        }
        
        .file-meta {
            color: #6B7280;
            font-size: 12px;
            line-height: 1.6;
        }
        
        .file-content {
            padding: 15px;
        }
        
        .audio-player {
            width: 100%;
            margin-bottom: 12px;
            border-radius: 4px;
        }
        
        .file-actions {
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
        }
        
        .action-btn {
            flex: 1;
            min-width: 70px;
            padding: 8px 12px;
            border: none;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
            background: #F3F4F6;
            color: #374151;
        }
        
        .action-btn:hover {
            background: #E5E7EB;
            transform: translateY(-1px);
        }
        
        .download-btn {
            background: #10B981;
            color: white;
        }
        
        .download-btn:hover {
            background: #059669;
        }
        
        .copy-btn {
            background: #3B82F6;
            color: white;
        }
        
        .copy-btn:hover {
            background: #2563EB;
        }
        
        .script-btn {
            background: #1D4ED8;
            color: white;
        }
        
        .script-btn:hover {
            background: #1E3A8A;
        }
        
        .report-btn {
            background: #EA580C;
            color: white;
        }
        
        .report-btn:hover {
            background: #C2410C;
        }
        
        .setlink-btn {
            background: #0891B2;
            color: white;
            white-space: nowrap;
        }
        
        .setlink-btn:hover {
            background: #0E7490;
        }
        
        .delete-btn {
            background: #EF4444;
            color: white;
        }
        
        .delete-btn:hover {
            background: #DC2626;
        }
        
        .empty-state {
            background: white;
            padding: 40px;
            border-radius: 12px;
            text-align: center;
            color: #6B7280;
        }
        
        .empty-state p {
            margin-bottom: 20px;
            font-size: 14px;
        }
        
        .footer {
            text-align: center;
            color: #6B7280;
            font-size: 12px;
            margin-top: 30px;
            padding: 20px;
        }
        
        @media (max-width: 768px) {
            .header h1 {
                font-size: 22px;
            }
            
            .files-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="header">
        <img src="/Spark_Blank.png" alt="Spark" class="header-logo"><br>
        <h1>Audio Message Hub</h1>
        <p>Creating Audio Activity for WM US Stores</p>
        <div class="branding">ZORRO ACTIVITY HUB</div>
    </div>
    
    <div class="container">
        <div class="generator-section">
            <h2>🎤 Generate New Audio</h2>
            <p>Create a new MP4 audio message with Jenny Neural voice.</p>
            <div style="display: flex; gap: 10px; flex-wrap: wrap; align-items: center;">
                <a href="/create-audio" class="generate-btn">🎤 Custom Audio</a>
                <button class="generate-btn" id="btn-weekly" onclick="openWeeklyAudioModal()" style="background: linear-gradient(135deg, #1D4ED8 0%, #1E3A8A 100%); border: none; cursor: pointer; font-weight: 600;">🎤 Weekly Message Audio</button>
            </div>
            <div id="pipeline-status" style="margin-top: 12px; padding: 10px; border-radius: 8px; display: none; font-size: 0.9em;"></div>
        </div>

        <!-- Weekly Message Audio Modal -->
        <div id="weekly-modal" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.7); z-index:1000; justify-content:center; align-items:center;">
            <div style="background:#1F2937; border-radius:16px; padding:30px; max-width:520px; width:90%; box-shadow: 0 20px 60px rgba(0,0,0,0.5); border: 1px solid #374151;">
                <h2 style="margin:0 0 8px; color:#F9FAFB; font-size:1.3em;">🎤 Weekly Message Audio</h2>
                <p style="color:#9CA3AF; margin:0 0 12px; font-size:0.9em;">Two-step process based on network requirements</p>
                
                <div style="display:flex; gap:12px; margin-bottom:16px; align-items:center;">
                    <div style="flex:1;">
                        <label style="color:#9CA3AF; font-size:0.8em; display:block; margin-bottom:4px;">WM Week</label>
                        <input id="wm-week" type="number" min="1" max="52" value="4" style="width:100%; padding:8px 12px; border-radius:8px; border:1px solid #4B5563; background:#111827; color:#F9FAFB; font-size:1em; text-align:center;">
                    </div>
                    <div style="flex:1;">
                        <label style="color:#9CA3AF; font-size:0.8em; display:block; margin-bottom:4px;">Fiscal Year</label>
                        <input id="wm-fy" type="number" min="2025" max="2030" value="2027" style="width:100%; padding:8px 12px; border-radius:8px; border:1px solid #4B5563; background:#111827; color:#F9FAFB; font-size:1em; text-align:center;">
                    </div>
                </div>

                <div style="display:flex; flex-direction:column; gap:14px;">
                    <!-- Step 1 -->
                    <div id="step1-card" style="background:#111827; border:1px solid #374151; border-radius:12px; padding:16px;">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                            <span style="color:#10B981; font-weight:700; font-size:1em;">Step 1: Fetch Data</span>
                            <span style="background:#064E3B; color:#6EE7B7; padding:3px 10px; border-radius:6px; font-size:0.75em; font-weight:600;">Requires Eagle WiFi / VPN</span>
                        </div>
                        <p style="color:#9CA3AF; margin:0 0 12px; font-size:0.85em;">Queries BigQuery for Weekly Messages (Review for Publish - No Comm), extracts Summarized text, and caches the script locally.</p>
                        <button id="modal-fetch-btn" onclick="modalFetchData()" style="width:100%; padding:10px; border-radius:8px; border:none; cursor:pointer; font-weight:600; font-size:0.95em; background:linear-gradient(135deg, #10B981 0%, #059669 100%); color:white;">📡 Fetch Data from BigQuery</button>
                        <div id="step1-status" style="margin-top:10px; display:none; padding:8px; border-radius:6px; font-size:0.85em;"></div>
                    </div>

                    <!-- Step 2 -->
                    <div id="step2-card" style="background:#111827; border:1px solid #374151; border-radius:12px; padding:16px;">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                            <span style="color:#1D4ED8; font-weight:700; font-size:1em;">Step 2: Generate Audio</span>
                            <span style="background:#1E1B4B; color:#A78BFA; padding:3px 10px; border-radius:6px; font-size:0.75em; font-weight:600;">Requires Walmart WiFi</span>
                        </div>
                        <p style="color:#9CA3AF; margin:0 0 12px; font-size:0.85em;">Synthesizes the cached script with Jenny Neural voice into an MP4 file. Must be off Eagle WiFi / VPN.</p>
                        <button id="modal-synth-btn" onclick="modalSynthesizeAudio()" style="width:100%; padding:10px; border-radius:8px; border:none; cursor:pointer; font-weight:600; font-size:0.95em; background:linear-gradient(135deg, #1D4ED8 0%, #1E3A8A 100%); color:white;">🎤 Generate Audio with Jenny Neural</button>
                        <div id="step2-status" style="margin-top:10px; display:none; padding:8px; border-radius:6px; font-size:0.85em;"></div>
                    </div>
                </div>

                <button onclick="closeModal()" style="margin-top:18px; width:100%; padding:8px; border-radius:8px; border:1px solid #4B5563; background:transparent; color:#9CA3AF; cursor:pointer; font-size:0.9em;">Close</button>
            </div>
        </div>
        
        <div class="files-section">
            <h2>📂 Available Messages</h2>
"""
        
        if audio_files:
            audio_links = self._load_audio_links()
            html += '<div class="files-grid">'
            for filepath in audio_files:
                filename = filepath.name
                file_size = filepath.stat().st_size
                
                # Format file size
                if file_size > 1024 * 1024:
                    size_str = f"{file_size / (1024 * 1024):.1f} MB"
                elif file_size > 1024:
                    size_str = f"{file_size / 1024:.1f} KB"
                else:
                    size_str = f"{file_size} bytes"
                
                # Get file extension
                ext = filepath.suffix.lower().strip('.')
                format_str = ext.upper()
                
                # Get voice from filename
                voice = get_voice_from_filename(filename)
                voice_label, badge_bg, badge_hover = get_voice_badge(voice)
                
                # Create URL based on file location
                if filepath.parent == self.MP4_OUTPUT_DIR:
                    url = f"/audio/{filename}"
                else:
                    url = f"/audio/{filename}"
                
                # Clean up filename for display
                display_name = filename.rsplit('.', 1)[0]  # Remove extension
                
                # Map extension to MIME type
                mime_type_map = {
                    'mp3': 'audio/mpeg',
                    'mp4': 'audio/mp4',
                    'm4a': 'audio/mp4',
                    'wav': 'audio/wav',
                    'ogg': 'audio/ogg',
                    'flac': 'audio/flac'
                }
                mime_type = mime_type_map.get(ext, f'audio/{ext}')
                
                # Check for matching TTS script .txt file
                wk_match = re.search(r'Week (\d+)', filename)
                script_btn = ''
                report_btn = ''
                if wk_match:
                    script_name = f"Week {wk_match.group(1)} - Weekly Messages Audio Script.txt"
                    inflection_name = f"Week {wk_match.group(1)} - Weekly Messages Audio Script (Inflection).txt"
                    script_path = self.AUDIO_DIR / script_name
                    inflection_path = self.AUDIO_DIR / inflection_name
                    has_standard = script_path.exists()
                    has_inflection = inflection_path.exists()
                    if has_standard or has_inflection:
                        from urllib.parse import quote
                        script_url = f"/audio/{quote(script_name)}" if has_standard else ''
                        inflection_url = f"/audio/{quote(inflection_name)}" if has_inflection else ''
                        # Escape for safe JS embedding (parentheses in filenames)
                        esc = lambda s: s.replace("'", "\\'")
                        script_btn = f'<button class="action-btn script-btn" onclick="chooseScript(\'{esc(script_url)}\', \'{esc(script_name)}\', \'{esc(inflection_url)}\', \'{esc(inflection_name)}\')">📝 Script</button>'
                    report_name = f"Week {wk_match.group(1)} - Weekly Messages Audio Report.html"
                    report_path = self.AUDIO_DIR / report_name
                    if report_path.exists():
                        report_url = f"/audio/{report_name}"
                        wk_num = wk_match.group(1)
                        report_btn = f'<button class="action-btn report-btn" onclick="sendEmailReport({wk_num}, this)">📧 Email Report</button>'
                
                # Auto-generate the enablement Walmart CMS URL from the week number
                if wk_match:
                    _wk = wk_match.group(1)
                    _yr = datetime.now().year
                    cms_url = f'https://enablement.walmart.com/content/store-communications/home/merchandise/weekly-messages/{_yr}/week-{_wk}/weekly_messages_audiowk{_wk}.html'
                    # Auto-save to audio_links.json for BQ publish
                    audio_links = self._load_audio_links()
                    if audio_links.get(filename) != cms_url:
                        audio_links[filename] = cms_url
                        self._save_audio_links(audio_links)
                else:
                    cms_url = ''
                
                import html as html_mod
                html_escaped_cms = html_mod.escape(cms_url) if cms_url else ''
                copy_disabled = '' if cms_url else ' disabled title="No week detected in filename"'
                copy_style = 'opacity:0.4;cursor:not-allowed;' if not cms_url else ''
                
                html += f"""
            <div class="file-card" id="card-{hash(filename) & 0xFFFFFFFF}">
                <div class="file-header">
                    <div class="voice-badge" style="background-color: {badge_bg};">{voice_label}</div>
                    <div class="file-title">{display_name}</div>
                    <div class="file-meta">
                        <div>📦 {size_str} | {format_str}</div>
                    </div>
                </div>
                <div class="file-content">
                    <audio class="audio-player" controls preload="metadata">
                        <source src="{url}" type="{mime_type}">
                        Your browser does not support the audio element.
                    </audio>
                    <div class="link-row" style="margin:6px 0;display:flex;gap:6px;align-items:center;">
                        <span style="font-size:0.82em;color:#6B7280;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;" title="{html_escaped_cms}">🔗 {html_escaped_cms}</span>
                    </div>
                    <div class="file-actions">
                        <button class="action-btn copy-btn"
                                onclick="copyStreamURL(this)"{copy_disabled}
                                style="{copy_style}">📋 Copy URL</button>
                        <button class="action-btn download-btn" onclick="downloadFile('{url}', '{filename}')">⬇️ Download</button>
                        {script_btn}
                        {report_btn}
                        <button class="action-btn delete-btn" onclick="deleteFile('{filename}')">🗑️ Delete</button>
                    </div>
                </div>
            </div>
"""
            html += '</div>'
        else:
            html += """
            <div class="empty-state">
                <p>📭 No audio messages available yet</p>
                <p>Generate your first audio message with Jenny Neural voice using the button above.</p>
            </div>
"""
        
        html += """
        </div>
    </div>
    
    <div class="footer">
        <p>🎙️ Narrated by: Jenny Neural Voice | Powered by Zorro Activity Hub</p>
        <p style="font-size: 11px; margin-top: 10px; opacity: 0.7;">Server: http://localhost:8888</p>
    </div>
    
    <script>
        function copyStreamURL(btn) {
            const card = btn.closest('.file-card');
            const span = card.querySelector('.link-row span');
            const url = span ? span.textContent.replace(/^.*?https/, 'https').trim() : '';
            if (!url) {
                alert('No CMS URL available (week number not detected in filename).');
                return;
            }
            navigator.clipboard.writeText(url).then(() => {
                const orig = btn.textContent;
                btn.textContent = '✅ Copied!';
                setTimeout(() => btn.textContent = orig, 1500);
            }).catch(err => {
                console.error('Failed to copy:', err);
            });
        }
        
        function sendEmailReport(week, btn) {
            if (!confirm('Send Weekly Messages Audio Report email for Week ' + week + '?')) return;
            const orig = btn.textContent;
            btn.disabled = true;
            btn.textContent = '⏳ Sending...';
            fetch('/api/send-email-report', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({week: week, fy: 2027})
            })
            .then(r => r.json())
            .then(data => {
                btn.disabled = false;
                if (data.success) {
                    btn.textContent = '✅ Sent!';
                    setTimeout(() => btn.textContent = orig, 3000);
                } else {
                    btn.textContent = orig;
                    alert('Email failed: ' + (data.error || 'Unknown error'));
                }
            })
            .catch(err => {
                btn.disabled = false;
                btn.textContent = orig;
                alert('Email error: ' + err.message);
            });
        }
        
        function copyURL(text) {
            navigator.clipboard.writeText(text).then(() => {
                alert('URL copied to clipboard!');
            }).catch(err => {
                console.error('Failed to copy:', err);
            });
        }
        
        function downloadFile(url, filename) {
            const link = document.createElement('a');
            link.href = url;
            link.download = filename;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }

        function chooseScript(stdUrl, stdName, infUrl, infName) {
            // Remove any existing popup
            const old = document.getElementById('script-choice-popup');
            if (old) old.remove();

            const overlay = document.createElement('div');
            overlay.id = 'script-choice-popup';
            overlay.style.cssText = 'position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.5);display:flex;align-items:center;justify-content:center;z-index:9999;';
            overlay.innerHTML = `
                <div style="background:white;border-radius:12px;padding:28px 32px;max-width:400px;width:90%;box-shadow:0 8px 30px rgba(0,0,0,0.25);text-align:center;">
                    <div style="font-size:24px;margin-bottom:8px;">📝</div>
                    <h3 style="margin:0 0 6px;font-size:18px;color:#111827;">Download Script</h3>
                    <p style="font-size:13px;color:#6B7280;margin:0 0 20px;">Choose which version to download:</p>
                    <div style="display:flex;flex-direction:column;gap:10px;">
                        ${stdUrl ? `<button onclick="downloadFile('${stdUrl}','${stdName}');document.getElementById('script-choice-popup').remove();" style="padding:12px 16px;border:1px solid #D1D5DB;border-radius:8px;background:white;cursor:pointer;font-size:14px;text-align:left;transition:background 0.15s;">
                            <strong>📄 Standard Script</strong><br>
                            <span style="font-size:12px;color:#6B7280;">Clean text — no annotations</span>
                        </button>` : ''}
                        ${infUrl ? `<button onclick="downloadFile('${infUrl}','${infName}');document.getElementById('script-choice-popup').remove();" style="padding:12px 16px;border:1px solid #D1D5DB;border-radius:8px;background:white;cursor:pointer;font-size:14px;text-align:left;transition:background 0.15s;">
                            <strong>🎭 Script with Inflection</strong><br>
                            <span style="font-size:12px;color:#6B7280;">Includes prosody markings [WARM, PERSONAL] etc.</span>
                        </button>` : ''}
                    </div>
                    <button onclick="document.getElementById('script-choice-popup').remove();" style="margin-top:16px;padding:8px 20px;border:none;background:#F3F4F6;border-radius:6px;cursor:pointer;font-size:13px;color:#6B7280;">Cancel</button>
                </div>
            `;
            document.body.appendChild(overlay);
            overlay.addEventListener('click', function(e) { if (e.target === overlay) overlay.remove(); });
        }
        
        function deleteFile(filename) {
            if (confirm(`Are you sure you want to delete "${filename}"? This action cannot be undone.`)) {
                fetch('/api/delete-file', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({filename: filename})
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        alert('File deleted successfully');
                        location.reload();
                    } else {
                        alert('Error deleting file: ' + data.error);
                    }
                })
                .catch(err => {
                    console.error('Delete error:', err);
                    alert('Error deleting file');
                });
            }
        }
        
        function openWeeklyAudioModal() {
            document.getElementById('weekly-modal').style.display = 'flex';
            // Reset statuses
            document.getElementById('step1-status').style.display = 'none';
            document.getElementById('step2-status').style.display = 'none';
        }

        function closeModal() {
            document.getElementById('weekly-modal').style.display = 'none';
        }

        // Close modal on backdrop click
        document.getElementById('weekly-modal').addEventListener('click', function(e) {
            if (e.target === this) closeModal();
        });

        function stepStatus(step, html, type) {
            const el = document.getElementById('step' + step + '-status');
            el.innerHTML = html;
            el.style.display = 'block';
            el.style.background = type === 'success' ? '#064E3B' : type === 'error' ? '#7F1D1D' : '#1E3A5F';
            el.style.color = '#F3F4F6';
            el.style.border = '1px solid ' + (type === 'success' ? '#10B981' : type === 'error' ? '#EF4444' : '#3B82F6');
        }

        function getWeekFY() {
            return {
                week: parseInt(document.getElementById('wm-week').value) || 4,
                fy: parseInt(document.getElementById('wm-fy').value) || 2027
            };
        }

        function modalFetchData() {
            const {week, fy} = getWeekFY();
            const btn = document.getElementById('modal-fetch-btn');
            btn.disabled = true;
            btn.textContent = '⏳ Fetching WK ' + week + ' from BigQuery...';
            stepStatus(1, 'Connecting to BigQuery for WK ' + week + ' FY' + fy + '...', 'info');

            fetch('/api/generate-from-template', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({week: week, fy: fy, phase: 'fetch'})
            })
            .then(r => r.json())
            .then(data => {
                btn.disabled = false;
                btn.textContent = '📡 Fetch Data from BigQuery';
                if (data.success) {
                    stepStatus(1,
                        '<strong>✅ Data Cached!</strong><br>' +
                        '<table style="margin-top:4px;font-size:0.9em;">' +
                        '<tr><td>Review for Publish - No Comm:</td><td style="padding-left:8px;font-weight:bold;">' + data.review_no_comm_count + '</td></tr>' +
                        '<tr><td>With Summarized text:</td><td style="padding-left:8px;font-weight:bold;">' + data.summarized_count + '</td></tr>' +
                        '</table>' +
                        '<br><em>Now switch to Walmart WiFi and run Step 2 ↓</em>',
                        'success'
                    );
                } else {
                    stepStatus(1, '<strong>❌ Fetch Failed:</strong> ' + data.error + '<br><em>Make sure you are on Eagle WiFi / VPN.</em>', 'error');
                }
            })
            .catch(err => {
                btn.disabled = false;
                btn.textContent = '📡 Fetch Data from BigQuery';
                stepStatus(1, '<strong>❌ Network Error:</strong> ' + err.message, 'error');
            });
        }

        function modalSynthesizeAudio() {
            if (!confirm('⚠️ Have you come off Eagle WiFi and onto Walmart WiFi?\\n\\nJenny Neural voice requires Walmart WiFi (off VPN) to synthesize audio.')) {
                return;
            }
            const {week, fy} = getWeekFY();
            const btn = document.getElementById('modal-synth-btn');
            btn.disabled = true;
            btn.textContent = '⏳ Synthesizing WK ' + week + ' (~2-4 min)...';
            stepStatus(2, 'Building WK ' + week + ' script and synthesizing with Jenny Neural...', 'info');

            fetch('/api/generate-from-template', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({week: week, fy: fy, phase: 'synthesize', force: true})
            })
            .then(r => r.json())
            .then(data => {
                btn.disabled = false;
                btn.textContent = '🎤 Generate Audio with Jenny Neural';
                if (data.success) {
                    stepStatus(2,
                        '<strong>✅ Audio Generated!</strong><br>' +
                        '<table style="margin-top:4px;font-size:0.9em;">' +
                        '<tr><td>File:</td><td style="padding-left:8px;">' + data.filename + '</td></tr>' +
                        '<tr><td>Size:</td><td style="padding-left:8px;">' + data.size_kb + ' KB</td></tr>' +
                        '<tr><td>Voice:</td><td style="padding-left:8px;">' + data.voice + '</td></tr>' +
                        '<tr><td>Events:</td><td style="padding-left:8px;font-weight:bold;">' + data.summarized_count + '</td></tr>' +
                        '</table>',
                        'success'
                    );
                    setTimeout(() => { closeModal(); location.reload(); }, 3000);
                } else {
                    let hint = '';
                    if (data.error && data.error.includes('No cached data')) hint = '<br><em>Run Step 1 on Eagle WiFi first.</em>';
                    else if (data.error && data.error.includes('synthesis failed')) hint = '<br><em>Make sure you are on Walmart WiFi (off VPN).</em>';
                    stepStatus(2, '<strong>❌ Synthesis Failed:</strong> ' + data.error + hint, 'error');
                }
            })
            .catch(err => {
                btn.disabled = false;
                btn.textContent = '🎤 Generate Audio with Jenny Neural';
                stepStatus(2, '<strong>❌ Network Error:</strong> ' + err.message, 'error');
            });
        }
    </script>
</body>
</html>
"""
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))
    
    def serve_file(self, filepath):
        """Serve audio file with Range request support for browser playback"""
        try:
            file_size = filepath.stat().st_size
            
            # Determine MIME type based on file extension
            ext = filepath.suffix.lower()
            mime_types = {
                '.mp3': 'audio/mpeg',
                '.mp4': 'audio/mp4',
                '.m4a': 'audio/mp4',
                '.wav': 'audio/wav',
                '.ogg': 'audio/ogg',
                '.flac': 'audio/flac'
            }
            mime_type = mime_types.get(ext, 'audio/mpeg')
            
            # Handle Range requests (required for browser audio/video playback)
            range_header = self.headers.get('Range')
            if range_header:
                # Parse Range: bytes=start-end
                range_spec = range_header.replace('bytes=', '')
                parts = range_spec.split('-')
                start = int(parts[0]) if parts[0] else 0
                end = int(parts[1]) if parts[1] else file_size - 1
                end = min(end, file_size - 1)
                content_length = end - start + 1
                
                with open(filepath, 'rb') as f:
                    f.seek(start)
                    content = f.read(content_length)
                
                self.send_response(206)  # Partial Content
                self.send_header('Content-type', mime_type)
                self.send_header('Content-Length', content_length)
                self.send_header('Content-Range', f'bytes {start}-{end}/{file_size}')
                self.send_header('Accept-Ranges', 'bytes')
                self.send_header('Cache-Control', 'public, max-age=3600')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(content)
            else:
                with open(filepath, 'rb') as f:
                    content = f.read()
                
                self.send_response(200)
                self.send_header('Content-type', mime_type)
                self.send_header('Content-Length', file_size)
                self.send_header('Accept-Ranges', 'bytes')
                self.send_header('Cache-Control', 'public, max-age=3600')
                self.send_header('Access-Control-Allow-Origin', '*')
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

class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True

def start_server(port=8888):
    """Start the audio server"""
    server_address = ('', port)
    httpd = ThreadingHTTPServer(server_address, AudioHandler)
    
    print(f"""
========================================================
       AMP AUDIO SERVER STARTED
========================================================

Server Running on: http://localhost:{port}

Available URLs:
  Web Player: http://localhost:{port}
  Download:   http://localhost:{port}/audio/[filename]
  Metadata:   http://localhost:{port}/metadata/[json]

Serving from:
  {AudioHandler.AUDIO_DIR}

Press Ctrl+C to stop the server
    """)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n✋ Server stopped.")
        httpd.server_close()

if __name__ == "__main__":
    start_server(8888)
