"""
Simple HTTP server for DL Selector UI using Python's built-in http.server
No external dependencies required - works with standard Python installation
"""
import http.server
import socketserver
import json
import csv
import os
import glob
from urllib.parse import urlparse, parse_qs
from pathlib import Path

PORT = 5000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class DLAPIHandler(http.server.SimpleHTTPRequestHandler):
    """Custom handler for DL API endpoints and static files"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def end_headers(self):
        """Add CORS headers to allow cross-origin requests"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        # API endpoint: Get all distribution lists
        if path == '/api/distribution-lists':
            self.handle_get_dls()
        
        # API endpoint: Get statistics
        elif path == '/api/stats':
            self.handle_get_stats()
        
        # API endpoint: Search distribution lists
        elif path == '/api/search':
            query_params = parse_qs(parsed_path.query)
            self.handle_search(query_params)
        
        # Serve the main HTML file
        elif path == '/' or path == '/index.html':
            self.serve_html()
        
        # Serve static files (CSS, JS, etc.)
        else:
            super().do_GET()
    
    def do_OPTIONS(self):
        """Handle OPTIONS requests for CORS preflight"""
        self.send_response(200)
        self.end_headers()
    
    def handle_get_dls(self):
        """Return all distribution lists as JSON"""
        try:
            csv_file = self.get_latest_csv()
            if not csv_file:
                self.send_error(404, "No distribution list CSV file found")
                return
            
            dls = []
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    dls.append({
                        'email': row.get('Email', ''),
                        'name': row.get('Name', ''),
                        'description': row.get('Description', ''),
                        'memberCount': int(row.get('MemberCount', 0)),
                        'category': row.get('Category', 'General')
                    })
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(dls).encode('utf-8'))
        
        except Exception as e:
            self.send_error(500, f"Error reading distribution lists: {str(e)}")
    
    def handle_get_stats(self):
        """Return statistics about distribution lists"""
        try:
            csv_file = self.get_latest_csv()
            if not csv_file:
                self.send_error(404, "No distribution list CSV file found")
                return
            
            total_count = 0
            category_counts = {}
            total_members = 0
            
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    total_count += 1
                    category = row.get('Category', 'General')
                    category_counts[category] = category_counts.get(category, 0) + 1
                    total_members += int(row.get('MemberCount', 0))
            
            stats = {
                'totalLists': total_count,
                'categoryCounts': category_counts,
                'totalMembers': total_members,
                'lastUpdated': os.path.getmtime(csv_file)
            }
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(stats).encode('utf-8'))
        
        except Exception as e:
            self.send_error(500, f"Error calculating stats: {str(e)}")
    
    def handle_search(self, query_params):
        """Search and filter distribution lists"""
        try:
            csv_file = self.get_latest_csv()
            if not csv_file:
                self.send_error(404, "No distribution list CSV file found")
                return
            
            # Extract query parameters
            search_query = query_params.get('q', [''])[0].lower()
            category_filter = query_params.get('category', [''])[0]
            size_filter = query_params.get('size', [''])[0]
            
            dls = []
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Apply search filter
                    if search_query:
                        email = row.get('Email', '').lower()
                        name = row.get('Name', '').lower()
                        description = row.get('Description', '').lower()
                        if search_query not in email and search_query not in name and search_query not in description:
                            continue
                    
                    # Apply category filter
                    if category_filter and row.get('Category', '') != category_filter:
                        continue
                    
                    # Apply size filter
                    member_count = int(row.get('MemberCount', 0))
                    if size_filter == 'small' and member_count >= 50:
                        continue
                    elif size_filter == 'medium' and (member_count < 50 or member_count >= 500):
                        continue
                    elif size_filter == 'large' and member_count < 500:
                        continue
                    
                    dls.append({
                        'email': row.get('Email', ''),
                        'name': row.get('Name', ''),
                        'description': row.get('Description', ''),
                        'memberCount': member_count,
                        'category': row.get('Category', 'General')
                    })
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(dls).encode('utf-8'))
        
        except Exception as e:
            self.send_error(500, f"Error searching distribution lists: {str(e)}")
    
    def serve_html(self):
        """Serve the DL selector HTML file"""
        try:
            html_file = os.path.join(DIRECTORY, 'dl_selector.html')
            if not os.path.exists(html_file):
                self.send_error(404, "dl_selector.html not found")
                return
            
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))
        
        except Exception as e:
            self.send_error(500, f"Error serving HTML: {str(e)}")
    
    def get_latest_csv(self):
        """Find the most recent distribution list CSV file"""
        pattern = os.path.join(DIRECTORY, 'all_distribution_lists_*.csv')
        csv_files = glob.glob(pattern)
        if not csv_files:
            return None
        # Return the most recently modified file
        return max(csv_files, key=os.path.getmtime)


def main():
    """Start the HTTP server"""
    handler = DLAPIHandler
    
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"=" * 70)
        print(f"DL Selector Server Started Successfully!")
        print(f"=" * 70)
        print(f"\n📊 Server running at: http://localhost:{PORT}")
        print(f"📁 Serving files from: {DIRECTORY}")
        print(f"\n🔗 API Endpoints:")
        print(f"   • GET /api/distribution-lists  - Get all DLs")
        print(f"   • GET /api/stats               - Get statistics")
        print(f"   • GET /api/search?q=...        - Search DLs")
        print(f"\n🌐 Open in browser: http://localhost:{PORT}")
        print(f"\n⏹️  Press Ctrl+C to stop the server")
        print(f"=" * 70)
        print()
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n🛑 Server stopped by user")
            print("=" * 70)


if __name__ == '__main__':
    main()
