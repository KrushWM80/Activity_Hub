#!/usr/bin/env python3
"""
AMP Dashboard - LocalHost Server (No External Dependencies)
Uses Python's built-in http.server module - NO Flask, NO network required
MP4 Audio synthesis with Jenny voice integrated
"""

import http.server
import socketserver
import json
import sys
from pathlib import Path
from datetime import datetime
from urllib.parse import urlparse, parse_qs
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add MP4 Pipeline to path
sys.path.insert(0, str(Path(__file__).parent.parent / "Zorro" / "Audio"))

try:
    from mp4_pipeline import MP4Pipeline, Voice
    MP4_PIPELINE_AVAILABLE = True
    logger.info("✅ MP4 Pipeline (Jenny voice) available")
    mp4_pipeline = MP4Pipeline()
except ImportError as e:
    MP4_PIPELINE_AVAILABLE = False
    logger.warning(f"⚠️  MP4 Pipeline not available: {e}")

PORT = 5000


class DashboardHandler(http.server.SimpleHTTPRequestHandler):
    """Custom HTTP handler for dashboard with MP4 audio API"""
    
    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        # API: Generate audio
        if path.startswith('/api/generate-audio'):
            self.handle_generate_audio()
            return
        
        # API: Serve audio file
        if path.startswith('/api/audio/'):
            filename = path.split('/api/audio/')[-1]
            self.handle_serve_audio(filename)
            return
        
        # API: Health check
        if path == '/health':
            self.send_json_response({
                'status': 'ok',
                'service': 'AMP Dashboard',
                'mp4_pipeline': MP4_PIPELINE_AVAILABLE,
                'timestamp': datetime.utcnow().isoformat()
            })
            return
        
        # API: Root documentation
        if path == '/' or path == '/api':
            self.send_json_response({
                'service': 'AMP Dashboard Local Server',
                'version': '1.0',
                'status': 'online',
                'port': PORT,
                'endpoints': {
                    'GET /health': 'Health check',
                    'POST /api/generate-audio': 'Generate MP4 audio from text',
                    'GET /api/audio/<filename>': 'Download generated MP4',
                    'GET /': 'Dashboard HTML'
                },
                'audio': {
                    'enabled': MP4_PIPELINE_AVAILABLE,
                    'voice': 'Jenny Neural',
                    'format': 'MP4 (AAC @ 256kbps)'
                },
                'timestamp': datetime.utcnow().isoformat()
            })
            return
        
        # Default file serving
        super().do_GET()
    
    def do_POST(self):
        """Handle POST requests"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        # API: Generate audio
        if path == '/api/generate-audio':
            self.handle_generate_audio_post()
            return
        
        self.send_error(404)
    
    def handle_generate_audio(self):
        """Handle audio generation request (GET with query params)"""
        try:
            if not MP4_PIPELINE_AVAILABLE:
                self.send_json_response({
                    'success': False,
                    'error': 'MP4 Pipeline not available'
                }, status=503)
                return
            
            parsed_path = urlparse(self.path)
            params = parse_qs(parsed_path.query)
            
            # Extract parameters
            message_title = params.get('title', ['Activity Update'])[0]
            message_description = params.get('description', ['New activity message'])[0]
            business_area = params.get('area', ['General'])[0]
            activity_type = params.get('type', ['FYI'])[0]
            priority = params.get('priority', ['medium'])[0]
            
            # Build audio script
            priority_text = 'HIGH PRIORITY' if priority.lower() in ['high', '1'] else \
                           'priority' if priority.lower() in ['medium', '2'] else 'informational'
            
            audio_script = f"""
            Hello and welcome to Walmart Activity Hub.
            
            This is a {priority_text} announcement from {business_area}.
            
            {message_title}
            
            Details: {message_description}
            
            This announcement is classified as {activity_type}.
            
            Please review this information and ensure your team is aware.
            
            Thank you for your attention.
            """
            
            logger.info(f"Generating MP4 audio: {message_title}")
            
            # Generate MP4
            success, output_file = mp4_pipeline.synthesize(
                text=audio_script,
                voice=Voice.JENNY
            )
            
            if not success or not output_file:
                self.send_json_response({
                    'success': False,
                    'error': 'Failed to generate audio'
                }, status=500)
                return
            
            # Get file info
            file_path = Path(output_file)
            file_size_kb = file_path.stat().st_size / 1024
            filename = file_path.name
            word_count = len(audio_script.split())
            duration_seconds = int((word_count / 140) * 60)
            
            logger.info(f"✅ Audio generated: {filename} ({file_size_kb:.1f}KB)")
            
            self.send_json_response({
                'success': True,
                'audio_url': f'/api/audio/{filename}',
                'filename': filename,
                'size_kb': round(file_size_kb, 1),
                'duration_seconds': duration_seconds,
                'voice': 'Jenny Neural',
                'codec': 'AAC @ 256kbps',
                'message_title': message_title,
                'timestamp': datetime.utcnow().isoformat()
            })
            
        except Exception as e:
            logger.error(f"❌ Error generating audio: {e}", exc_info=True)
            self.send_json_response({
                'success': False,
                'error': str(e)
            }, status=500)
    
    def handle_generate_audio_post(self):
        """Handle audio generation request (POST with JSON body)"""
        try:
            if not MP4_PIPELINE_AVAILABLE:
                self.send_json_response({
                    'success': False,
                    'error': 'MP4 Pipeline not available'
                }, status=503)
                return
            
            # Read request body
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            data = json.loads(body.decode('utf-8'))
            
            # Extract parameters
            message_title = data.get('message_title', 'Activity Update')
            message_description = data.get('message_description', 'New activity message')
            business_area = data.get('business_area', 'General')
            activity_type = data.get('activity_type', 'FYI')
            priority = data.get('priority', 'medium')
            
            # Build audio script
            priority_text = 'HIGH PRIORITY' if priority.lower() in ['high', '1'] else \
                           'priority' if priority.lower() in ['medium', '2'] else 'informational'
            
            audio_script = f"""
            Hello and welcome to Walmart Activity Hub.
            
            This is a {priority_text} announcement from {business_area}.
            
            {message_title}
            
            Details: {message_description}
            
            This announcement is classified as {activity_type}.
            
            Please review this information and ensure your team is aware.
            
            Thank you for your attention.
            """
            
            logger.info(f"Generating MP4 audio: {message_title}")
            
            # Generate MP4
            success, output_file = mp4_pipeline.synthesize(
                text=audio_script,
                voice=Voice.JENNY
            )
            
            if not success or not output_file:
                self.send_json_response({
                    'success': False,
                    'error': 'Failed to generate audio'
                }, status=500)
                return
            
            # Get file info
            file_path = Path(output_file)
            file_size_kb = file_path.stat().st_size / 1024
            filename = file_path.name
            word_count = len(audio_script.split())
            duration_seconds = int((word_count / 140) * 60)
            
            logger.info(f"✅ Audio generated: {filename} ({file_size_kb:.1f}KB)")
            
            self.send_json_response({
                'success': True,
                'audio_url': f'/api/audio/{filename}',
                'filename': filename,
                'size_kb': round(file_size_kb, 1),
                'duration_seconds': duration_seconds,
                'voice': 'Jenny Neural',
                'codec': 'AAC @ 256kbps',
                'message_title': message_title,
                'timestamp': datetime.utcnow().isoformat()
            })
            
        except Exception as e:
            logger.error(f"❌ Error generating audio: {e}", exc_info=True)
            self.send_json_response({
                'success': False,
                'error': str(e)
            }, status=500)
    
    def handle_serve_audio(self, filename):
        """Serve MP4 audio file"""
        try:
            audio_dir = Path(__file__).parent.parent / "Zorro" / "Audio" / "mp4_output"
            file_path = audio_dir / filename
            
            # Security: ensure file is in mp4_output directory
            if not file_path.resolve().parent == audio_dir.resolve():
                self.send_error(403, 'Forbidden')
                return
            
            if not file_path.exists():
                self.send_error(404, 'Audio file not found')
                return
            
            logger.info(f"Serving audio: {filename}")
            
            # Send file
            self.send_response(200)
            self.send_header('Content-type', 'audio/mp4')
            self.send_header('Content-Length', str(file_path.stat().st_size))
            self.send_header('Content-Disposition', f'attachment; filename="{filename}"')
            self.end_headers()
            
            with open(file_path, 'rb') as f:
                self.wfile.write(f.read())
            
        except Exception as e:
            logger.error(f"❌ Error serving audio: {e}", exc_info=True)
            self.send_error(500, str(e))
    
    def send_json_response(self, data, status=200):
        """Send JSON response"""
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))
    
    def log_message(self, format, *args):
        """Override logging to use our logger"""
        logger.info(f"{self.client_address[0]} - {format % args}")


def run_server():
    """Start the dashboard server"""
    logger.info("\n" + "="*80)
    logger.info("AMP DASHBOARD - LOCAL HOST SERVER")
    logger.info("="*80)
    logger.info(f"🚀 Starting dashboard on http://localhost:{PORT}")
    logger.info(f"🎤 MP4 Audio: {'✅ ENABLED (Jenny voice)' if MP4_PIPELINE_AVAILABLE else '⚠️  DISABLED'}")
    logger.info(f"📊 Built-in HTTP Server (No Flask/Network Required)")
    logger.info("")
    logger.info("API Endpoints:")
    logger.info(f"  GET  http://localhost:{PORT}/health - Health check")
    logger.info(f"  POST http://localhost:{PORT}/api/generate-audio - Generate MP4 audio")
    logger.info(f"  GET  http://localhost:{PORT}/api/audio/<filename> - Download MP4")
    logger.info("")
    logger.info("Open in browser: http://localhost:{PORT}")
    logger.info("="*80 + "\n")
    
    with socketserver.TCPServer(("127.0.0.1", PORT), DashboardHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            logger.info("\n🛑 Server stopped by user")
            httpd.shutdown()


if __name__ == '__main__':
    run_server()
