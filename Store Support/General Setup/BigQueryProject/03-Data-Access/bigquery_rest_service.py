"""
Simplified BigQuery REST API Service
Uses Google Cloud REST API directly without external dependencies
Connects to: wmt-assetprotection-prod.Store_Support_Dev.AMP_Data_Prep
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.parse
import urllib.request
import webbrowser
import os
import sys
from datetime import datetime

class BigQueryRESTHandler(BaseHTTPRequestHandler):
    
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
    
    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/api/bigquery/data':
            self.fetch_bigquery_data()
        elif self.path == '/api/bigquery/auth-url':
            self.get_auth_url()
        elif self.path.startswith('/api/bigquery/callback'):
            self.handle_oauth_callback()
        elif self.path == '/api/status':
            self.get_service_status()
        else:
            self.send_404()
    
    def do_POST(self):
        """Handle POST requests"""
        if self.path == '/api/bigquery/authenticate':
            self.handle_authentication()
        else:
            self.send_404()
    
    def fetch_bigquery_data(self):
        """Fetch data directly from BigQuery REST API"""
        try:
            # Check for authentication
            access_token = self.get_stored_token()
            
            if not access_token:
                self.send_json_response({
                    'error': 'Authentication required',
                    'message': 'Please authenticate first',
                    'auth_url': self.get_google_auth_url()
                }, 401)
                return
            
            # BigQuery REST API endpoint
            project_id = 'wmt-assetprotection-prod'
            
            # SQL Query for AMP data
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
            
            # BigQuery jobs endpoint
            jobs_url = f'https://bigquery.googleapis.com/bigquery/v2/projects/{project_id}/queries'
            
            request_data = {
                'query': query,
                'useLegacySql': False,
                'maxResults': 1000
            }
            
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
            
            print(f"🔗 Querying BigQuery: {project_id}")
            print(f"📊 Query: {query[:100]}...")
            
            # Execute BigQuery request
            data = json.dumps(request_data).encode('utf-8')
            req = urllib.request.Request(jobs_url, data=data, headers=headers, method='POST')
            
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode('utf-8'))
                
                if 'rows' in result and result['rows']:
                    # Parse BigQuery results
                    activities = self.parse_bigquery_results(result)
                    
                    # Save results locally
                    with open('real_bigquery_data.json', 'w') as f:
                        json.dump(activities, f, indent=2)
                    
                    response_data = {
                        'success': True,
                        'data': activities,
                        'count': len(activities),
                        'source': 'wmt-assetprotection-prod.Store_Support_Dev.AMP_Data_Prep',
                        'fetched_at': datetime.now().isoformat(),
                        'message': f'Successfully fetched {len(activities)} activities'
                    }
                    
                    print(f"✅ Successfully fetched {len(activities)} records")
                    self.send_json_response(response_data)
                    
                else:
                    self.send_json_response({
                        'error': 'No data found',
                        'message': 'Query returned no results. Check filters and permissions.',
                        'query_info': result.get('jobReference', {})
                    }, 404)
                    
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8')
            print(f"❌ BigQuery HTTP Error: {e.code} - {error_body}")
            
            self.send_json_response({
                'error': f'BigQuery API Error: {e.code}',
                'message': 'Check authentication and permissions',
                'details': error_body
            }, e.code)
            
        except Exception as e:
            print(f"❌ Error fetching BigQuery data: {e}")
            self.send_json_response({
                'error': str(e),
                'message': 'Failed to connect to BigQuery'
            }, 500)
    
    def parse_bigquery_results(self, result):
        """Convert BigQuery result format to JSON"""
        activities = []
        
        if 'schema' in result and 'fields' in result['schema']:
            field_names = [field['name'] for field in result['schema']['fields']]
            
            for row in result['rows']:
                activity = {}
                for i, field in enumerate(row['f']):
                    field_name = field_names[i] if i < len(field_names) else f'field_{i}'
                    activity[field_name] = field['v'] if field and field.get('v') is not None else ''
                activities.append(activity)
        
        return activities
    
    def get_auth_url(self):
        """Generate Google OAuth URL"""
        # You'll need to replace these with your actual OAuth credentials
        # Get them from: https://console.cloud.google.com/apis/credentials
        
        client_id = 'YOUR_GOOGLE_CLIENT_ID_HERE'  # Replace with actual client ID
        redirect_uri = 'http://localhost:8081/api/bigquery/callback'
        scope = 'https://www.googleapis.com/auth/bigquery.readonly'
        
        if client_id == 'YOUR_GOOGLE_CLIENT_ID_HERE':
            self.send_json_response({
                'error': 'OAuth not configured',
                'message': 'Please configure Google OAuth credentials',
                'instructions': [
                    '1. Go to https://console.cloud.google.com/apis/credentials',
                    '2. Create OAuth 2.0 Client ID',
                    '3. Add http://localhost:8081/api/bigquery/callback as redirect URI',
                    '4. Update bigquery_rest_service.py with your client_id and client_secret'
                ]
            }, 400)
            return
        
        auth_url = (
            f'https://accounts.google.com/o/oauth2/v2/auth?'
            f'client_id={client_id}&'
            f'redirect_uri={urllib.parse.quote(redirect_uri)}&'
            f'scope={urllib.parse.quote(scope)}&'
            f'response_type=code&'
            f'access_type=offline&'
            f'prompt=consent'
        )
        
        self.send_json_response({
            'auth_url': auth_url,
            'message': 'Open this URL to authenticate'
        })
    
    def handle_oauth_callback(self):
        """Handle OAuth callback and exchange code for token"""
        try:
            # Parse URL parameters
            url_parts = urllib.parse.urlparse(self.path)
            params = urllib.parse.parse_qs(url_parts.query)
            
            if 'code' in params:
                auth_code = params['code'][0]
                
                # Exchange code for access token
                success = self.exchange_code_for_token(auth_code)
                
                if success:
                    # Send success page
                    self.send_response(200)
                    self.send_header('Content-Type', 'text/html')
                    self.end_headers()
                    
                    success_html = """
                    <html><body>
                        <h2>✅ Authentication Successful!</h2>
                        <p>You can now close this window and return to the dashboard.</p>
                        <script>setTimeout(() => window.close(), 3000);</script>
                    </body></html>
                    """
                    self.wfile.write(success_html.encode('utf-8'))
                else:
                    self.send_error_page('Authentication failed')
            else:
                self.send_error_page('No authorization code received')
                
        except Exception as e:
            print(f"❌ OAuth callback error: {e}")
            self.send_error_page(f'Error: {e}')
    
    def exchange_code_for_token(self, auth_code):
        """Exchange authorization code for access token"""
        try:
            # Token exchange endpoint
            token_url = 'https://oauth2.googleapis.com/token'
            
            token_data = {
                'client_id': 'YOUR_GOOGLE_CLIENT_ID_HERE',      # Replace with actual
                'client_secret': 'YOUR_GOOGLE_CLIENT_SECRET',    # Replace with actual
                'code': auth_code,
                'grant_type': 'authorization_code',
                'redirect_uri': 'http://localhost:8081/api/bigquery/callback'
            }
            
            # Make token request
            data = urllib.parse.urlencode(token_data).encode('utf-8')
            req = urllib.request.Request(token_url, data=data, method='POST')
            req.add_header('Content-Type', 'application/x-www-form-urlencoded')
            
            with urllib.request.urlopen(req) as response:
                token_result = json.loads(response.read().decode('utf-8'))
                
                if 'access_token' in token_result:
                    # Store the token
                    self.store_token(token_result['access_token'])
                    print("✅ Access token obtained and stored")
                    return True
                else:
                    print(f"❌ Token exchange failed: {token_result}")
                    return False
                    
        except Exception as e:
            print(f"❌ Token exchange error: {e}")
            return False
    
    def get_stored_token(self):
        """Get stored access token"""
        try:
            if os.path.exists('bigquery_token.txt'):
                with open('bigquery_token.txt', 'r') as f:
                    return f.read().strip()
        except:
            pass
        return None
    
    def store_token(self, token):
        """Store access token"""
        try:
            with open('bigquery_token.txt', 'w') as f:
                f.write(token)
        except Exception as e:
            print(f"❌ Error storing token: {e}")
    
    def get_service_status(self):
        """Get service status"""
        token = self.get_stored_token()
        
        status = {
            'service': 'BigQuery REST API',
            'status': 'running',
            'authenticated': bool(token),
            'endpoints': {
                'data': '/api/bigquery/data',
                'auth': '/api/bigquery/auth-url',
                'status': '/api/status'
            }
        }
        
        self.send_json_response(status)
    
    def get_google_auth_url(self):
        """Generate auth URL"""
        return 'http://localhost:8081/api/bigquery/auth-url'
    
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
    
    def send_error_page(self, error_message):
        """Send error HTML page"""
        self.send_response(400)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        
        error_html = f"""
        <html><body>
            <h2>❌ Error</h2>
            <p>{error_message}</p>
            <p><a href="javascript:window.close()">Close Window</a></p>
        </body></html>
        """
        self.wfile.write(error_html.encode('utf-8'))
    
    def send_404(self):
        """Send 404 response"""
        self.send_response(404)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        
        error_response = {'error': 'Endpoint not found'}
        self.wfile.write(json.dumps(error_response).encode('utf-8'))

def run_bigquery_rest_service():
    """Start the BigQuery REST API service"""
    server_address = ('localhost', 8081)
    httpd = HTTPServer(server_address, BigQueryRESTHandler)
    
    print("🔗 BigQuery REST API Service")
    print("=" * 40)
    print(f"📡 Server: http://localhost:8081")
    print(f"🎯 BigQuery Table: wmt-assetprotection-prod.Store_Support_Dev.AMP_Data_Prep")
    print(f"📋 Status: http://localhost:8081/api/status")
    print(f"🔐 Auth: http://localhost:8081/api/bigquery/auth-url")
    print(f"📊 Data: http://localhost:8081/api/bigquery/data")
    print()
    print("✅ Ready to connect! Press Ctrl+C to stop...")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Service stopped")
        httpd.shutdown()

if __name__ == '__main__':
    print("🚀 Starting BigQuery REST API Service...")
    run_bigquery_rest_service()