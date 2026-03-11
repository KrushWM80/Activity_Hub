#!/usr/bin/env python3
"""
Zorro Activity Hub - Podcast Server with Jenny Neural Voice Integration
Serve podcast files over HTTP with Zorro-styled interface
Run this to access at http://localhost:8888
"""

import os
import json
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import unquote, urlparse
import mimetypes
import sys

# Initialize mimetypes
mimetypes.init()
mimetypes.add_type('audio/mp4', '.m4a')
mimetypes.add_type('audio/mp4', '.mp4')

# Add Audio directory to path for MP4 pipeline
audio_dir = Path(__file__).parent / "Audio"
sys.path.insert(0, str(audio_dir))

class PodcastHandler(SimpleHTTPRequestHandler):
    """Custom HTTP handler for podcast files"""
    
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
        
        # Serve podcast index
        if path == "/" or path == "/index.html":
            self.serve_index()
            return
        
        # Serve podcast files
        if path.startswith("/podcasts/"):
            filename = path.replace("/podcasts/", "")
            filepath = self.AUDIO_DIR / filename
            if filepath.exists() and filepath.suffix in ['.wav', '.mp3', '.m4a', '.mp4']:
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
        """Handle audio generation from template file"""
        try:
            # Read request body
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            params = json.loads(body)
            
            template_name = params.get('template', 'Weekly Messages Audio Template - Summarized - Week 4')
            
            # Check if template file exists
            template_path = self.AUDIO_DIR / (template_name + '.mp4')
            if not template_path.exists():
                template_path = self.AUDIO_DIR / (template_name + '.mp3')
            if not template_path.exists():
                template_path = self.AUDIO_DIR / (template_name + '.wav')
            
            if not template_path.exists():
                # Generate new audio from Jenny using a standard template message
                pipeline = self.get_pipeline()
                if not pipeline:
                    self.send_json_response({'success': False, 'error': 'MP4 pipeline not available'}, 500)
                    return
                
                audio_script = """
                Hello and welcome to Walmart Activity Hub.
                
                This is your weekly summary for Week 4.
                
                We have several important announcements and updates this week.
                
                Please review the following messages carefully and ensure your team is aware of any operational changes.
                
                This summary has been prepared especially for you. Thank you for your attention and commitment to excellence.
                """
                
                from mp4_pipeline import Voice
                import time
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
                        'codec': 'AAC @ 256kbps'
                    }
                    self.send_json_response(response, 200)
                else:
                    self.send_json_response({'success': False, 'error': 'Audio generation failed'}, 500)
            else:
                # Template file exists, just report it
                file_size_kb = template_path.stat().st_size / 1024
                response = {
                    'success': True,
                    'message': 'Template file already exists',
                    'filename': template_path.name,
                    'size_kb': round(file_size_kb, 1)
                }
                self.send_json_response(response, 200)
        
        except json.JSONDecodeError:
            self.send_json_response({'success': False, 'error': 'Invalid JSON'}, 400)
        except Exception as e:
            print(f"Error generating template audio: {e}")
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
    
    def serve_index(self):
        """Serve Zorro Activity Hub index page with Week 4 Summarized Messages"""
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
    <title>Week 4 Summarized Messages - Zorro Activity Hub</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', sans-serif;
            background: linear-gradient(135deg, #F3F4F6 0%, #E5E7EB 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .header {
            background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%);
            color: white;
            padding: 40px 20px;
            border-radius: 12px;
            margin-bottom: 30px;
            text-align: center;
            box-shadow: 0 10px 30px rgba(99, 102, 241, 0.2);
        }
        
        .header h1 {
            font-size: 28px;
            margin-bottom: 8px;
            font-weight: 700;
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
            border-left: 5px solid #06B6D4;
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
            background: linear-gradient(135deg, #06B6D4 0%, #0891b2 100%);
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
            box-shadow: 0 6px 20px rgba(6, 182, 212, 0.3);
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
        <h1>📊 Week 4 Summarized Messages</h1>
        <p>Your weekly activity announcements and highlights</p>
        <div class="branding">🎤 ZORRO ACTIVITY HUB</div>
    </div>
    
    <div class="container">
        <div class="generator-section">
            <h2>🎤 Generate New Summarized Audio</h2>
            <p>Create a new MP4 audio message with Jenny Neural voice.</p>
            <div style="display: flex; gap: 10px; flex-wrap: wrap;">
                <a href="/create-audio" class="generate-btn">🎤 Custom Audio</a>
                <button class="generate-btn" onclick="generateFromTemplate(event)" style="background: linear-gradient(135deg, #8B5CF6 0%, #6366F1 100%); border: none; cursor: pointer; font-weight: 600;">🎤 Weekly Message Audio</button>
            </div>
        </div>
        
        <div class="files-section">
            <h2>📂 Available Messages</h2>
"""
        
        if audio_files:
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
                    url = f"/podcasts/{filename}"
                file_url = f"http://localhost:8888{url}"
                
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
                
                html += f"""
            <div class="file-card">
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
                    <div class="file-actions">
                        <button class="action-btn copy-btn" onclick="copyURL('{file_url}')">📋 Copy URL</button>
                        <button class="action-btn download-btn" onclick="downloadFile('{url}', '{filename}')">⬇️ Download</button>
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
        
        function generateFromTemplate(event) {
            if (event) {
                event.preventDefault();
                event.target.disabled = true;
                event.target.textContent = '⏳ Generating...';
                const btn = event.target;
            } else {
                const btn = document.querySelector('[onclick="generateFromTemplate(event)"]') || document.querySelector('.generate-btn[style*="8B5CF6"]');
                if (btn) {
                    btn.disabled = true;
                    btn.textContent = '⏳ Generating...';
                }
            }
            
            fetch('/api/generate-from-template', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({template: 'Weekly Messages Audio Template - Summarized - Week 4'})
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert(`Audio generated successfully!\\nFile: ${data.filename}\\nSize: ${data.size_kb}KB\\nVoice: ${data.voice}`);
                    setTimeout(() => location.reload(), 1500);
                } else {
                    alert('Error generating audio: ' + data.error);
                    const btn = event && event.target ? event.target : document.querySelector('.generate-btn[style*="8B5CF6"]');
                    if (btn) {
                        btn.disabled = false;
                        btn.textContent = '🎤 Weekly Message Audio';
                    }
                }
            })
            .catch(err => {
                console.error('Generation error:', err);
                alert('Error generating audio: ' + err.message);
                const btn = event && event.target ? event.target : document.querySelector('.generate-btn[style*="8B5CF6"]');
                if (btn) {
                    btn.disabled = false;
                    btn.textContent = '🎤 Weekly Message Audio';
                }
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
  {PodcastHandler.AUDIO_DIR}

⏹️  Press Ctrl+C to stop the server
    """)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n✋ Server stopped.")
        httpd.server_close()

if __name__ == "__main__":
    start_server(8888)
