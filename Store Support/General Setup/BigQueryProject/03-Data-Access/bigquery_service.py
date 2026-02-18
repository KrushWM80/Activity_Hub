"""
Direct BigQuery Connection Service
Connects directly to wmt-assetprotection-prod.Store_Support_Dev.AMP_Data_Prep
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.parse
import urllib.request
import os
import sys
from datetime import datetime

class BigQueryAPIHandler(BaseHTTPRequestHandler):
    
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
    
    def do_GET(self):
        """Handle GET requests for BigQuery data"""
        if self.path == '/api/bigquery/data':
            self.fetch_bigquery_data()
        elif self.path == '/api/bigquery/auth-url':
            self.get_auth_url()
        else:
            self.send_404()
    
    def do_POST(self):
        """Handle POST requests for authentication"""
        if self.path == '/api/bigquery/authenticate':
            self.handle_authentication()
        else:
            self.send_404()
    
    def fetch_bigquery_data(self):
        """Fetch data directly from BigQuery"""
        try:
            # Check for stored authentication
            auth_token = self.get_auth_token()
            
            if not auth_token:
                self.send_json_response({
                    'error': 'Authentication required',
                    'auth_url': self.get_google_auth_url()
                }, 401)
                return
            
            # BigQuery API endpoint
            project_id = 'wmt-assetprotection-prod'
            
            # SQL query to get real AMP data
            query = """
            SELECT 
                actv_title_home_ofc_nm as title,
                division,
                region,
                market,
                store_nbr,
                store_name,
                week,
                created_date,
                preview_link,
                status,
                verification_status
            FROM `wmt-assetprotection-prod.Store_Support_Dev.AMP_Data_Prep`
            WHERE week = 39 
              AND status = 'Published'
              AND preview_link IS NOT NULL
              AND preview_link != ''
            ORDER BY created_date DESC
            LIMIT 1000
            """
            
            # Make BigQuery API request
            bigquery_url = f'https://bigquery.googleapis.com/bigquery/v2/projects/{project_id}/queries'
            
            request_data = {
                'query': query,
                'useLegacySql': False,
                'maxResults': 1000
            }
            
            headers = {
                'Authorization': f'Bearer {auth_token}',
                'Content-Type': 'application/json'
            }
            
            # Create request
            data = json.dumps(request_data).encode('utf-8')
            req = urllib.request.Request(bigquery_url, data=data, headers=headers, method='POST')
            
            # Execute request
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode('utf-8'))
                
                # Parse BigQuery response
                if 'rows' in result:
                    activities = self.parse_bigquery_rows(result['rows'], result['schema']['fields'])
                    
                    response_data = {
                        'success': True,
                        'data': activities,
                        'count': len(activities),
                        'source': 'wmt-assetprotection-prod.Store_Support_Dev.AMP_Data_Prep',
                        'fetched_at': datetime.now().isoformat(),
                        'week': 39
                    }
                    
                    self.send_json_response(response_data)
                else:
                    self.send_json_response({
                        'error': 'No data returned from BigQuery',
                        'query': query
                    }, 400)
                    
        except Exception as e:
            print(f"Error fetching BigQuery data: {e}")
            self.send_json_response({
                'error': str(e),
                'message': 'Failed to fetch data from BigQuery'
            }, 500)
    
    def parse_bigquery_rows(self, rows, schema):
        """Parse BigQuery response rows into JSON format"""
        activities = []
        field_names = [field['name'] for field in schema]
        
        for row in rows:
            activity = {}
            for i, value in enumerate(row['f']):
                field_name = field_names[i]
                activity[field_name] = value['v'] if value['v'] is not None else ''
            activities.append(activity)
        
        return activities
    
    def get_auth_url(self):
        """Get Google OAuth URL for authentication"""
        auth_url = self.get_google_auth_url()
        self.send_json_response({'auth_url': auth_url})
    
    def get_google_auth_url(self):
        """Generate Google OAuth URL"""
        client_id = 'YOUR_GOOGLE_CLIENT_ID'  # You'll need to configure this
        redirect_uri = 'http://localhost:8081/api/bigquery/callback'
        scope = 'https://www.googleapis.com/auth/bigquery.readonly'
        
        auth_url = (
            f'https://accounts.google.com/o/oauth2/v2/auth?'
            f'client_id={client_id}&'
            f'redirect_uri={urllib.parse.quote(redirect_uri)}&'
            f'scope={urllib.parse.quote(scope)}&'
            f'response_type=code&'
            f'access_type=offline'
        )
        
        return auth_url
    
    def handle_authentication(self):
        """Handle OAuth callback and get access token"""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            auth_code = data.get('code')
            if not auth_code:
                self.send_json_response({'error': 'No authorization code provided'}, 400)
                return
            
            # Exchange code for access token
            token_url = 'https://oauth2.googleapis.com/token'
            token_data = {
                'client_id': 'YOUR_GOOGLE_CLIENT_ID',
                'client_secret': 'YOUR_GOOGLE_CLIENT_SECRET',
                'code': auth_code,
                'grant_type': 'authorization_code',
                'redirect_uri': 'http://localhost:8081/api/bigquery/callback'
            }
            
            # Make token request
            data = urllib.parse.urlencode(token_data).encode('utf-8')
            req = urllib.request.Request(token_url, data=data, method='POST')
            
            with urllib.request.urlopen(req) as response:
                token_result = json.loads(response.read().decode('utf-8'))
                
                if 'access_token' in token_result:
                    # Store the token (in production, use secure storage)
                    self.store_auth_token(token_result['access_token'])
                    self.send_json_response({'success': True, 'message': 'Authentication successful'})
                else:
                    self.send_json_response({'error': 'Failed to get access token'}, 400)
                    
        except Exception as e:
            print(f"Authentication error: {e}")
            self.send_json_response({'error': str(e)}, 500)
    
    def get_auth_token(self):
        """Get stored authentication token"""
        try:
            if os.path.exists('bigquery_token.txt'):
                with open('bigquery_token.txt', 'r') as f:
                    return f.read().strip()
        except:
            pass
        return None
    
    def store_auth_token(self, token):
        """Store authentication token"""
        try:
            with open('bigquery_token.txt', 'w') as f:
                f.write(token)
        except Exception as e:
            print(f"Error storing token: {e}")
    
    def send_json_response(self, data, status_code=200):
        """Send JSON response with CORS headers"""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
        
        response_text = json.dumps(data, indent=2)
        self.wfile.write(response_text.encode('utf-8'))
    
    def send_404(self):
        """Send 404 response"""
        self.send_response(404)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'Not Found')

def run_bigquery_service():
    """Run the BigQuery API service"""
    server_address = ('localhost', 8081)
    httpd = HTTPServer(server_address, BigQueryAPIHandler)
    
    print("🔗 BigQuery API Service Starting...")
    print("📡 Server running at: http://localhost:8081")
    print("🎯 Endpoint: /api/bigquery/data")
    print("🔐 Auth endpoint: /api/bigquery/auth-url")
    print("\n✅ Ready to connect to: wmt-assetprotection-prod.Store_Support_Dev.AMP_Data_Prep")
    print("Press Ctrl+C to stop...")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
        httpd.shutdown()

if __name__ == '__main__':
    run_bigquery_service()