#!/usr/bin/env python3
"""
AMP Dashboard Backend Server (Lite Version)
Uses only Python standard library - no external dependencies needed
Provides BigQuery data access using gcloud authentication
"""

import http.server
import json
import logging
from datetime import datetime, timedelta
from urllib.parse import urlparse, parse_qs
import sys
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# BigQuery Configuration
PROJECT_ID = 'wmt-assetprotection-prod'
DATASET_ID = 'Store_Support_Dev'
TABLE_ID = 'Output - AMP ALL 2'

# Try to import google cloud
try:
    from google.cloud import bigquery
    client = bigquery.Client(project=PROJECT_ID)
    logger.info(f"✅ BigQuery client initialized for project: {PROJECT_ID}")
    bigquery_available = True
except ImportError:
    logger.warning("⚠️  google-cloud-bigquery not installed. Backend will run but return sample data.")
    client = None
    bigquery_available = False
except Exception as e:
    logger.warning(f"⚠️  Failed to initialize BigQuery: {e}")
    client = None
    bigquery_available = False


class AMPRequestHandler(http.server.BaseHTTPRequestHandler):
    """Handle HTTP requests for AMP API"""

    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query_params = parse_qs(parsed_path.query)

        # Add CORS headers
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

        # Route handlers
        if path == '/health':
            self._handle_health()
        elif path == '/StoreActivityandCommunications':
            self._handle_dashboard()
        elif path == '/api/amp-data':
            self._handle_amp_data(query_params)
        elif path == '/api/amp-metrics':
            self._handle_amp_metrics(query_params)
        elif path == '/api/amp-filters':
            self._handle_amp_filters(query_params)
        elif path == '/':
            self._handle_root()
        else:
            self.send_error(404)

    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def _send_json(self, data):
        """Send JSON response"""
        self.wfile.write(json.dumps(data, indent=2, default=str).encode())

    def _handle_health(self):
        """Health check endpoint"""
        response = {
            'status': 'ok',
            'service': 'AMP Dashboard Backend',
            'project': PROJECT_ID,
            'bigquery_connected': bigquery_available,
            'timestamp': datetime.utcnow().isoformat()
        }
        self._send_json(response)
        logger.info(f"Health check: BigQuery={'✅ Connected' if bigquery_available else '❌ Not available'}")

    def _handle_dashboard(self):
        """Serve the AMP Analysis Dashboard at the named route"""
        import os
        try:
            dashboard_path = os.path.join(os.path.dirname(__file__), 'amp_analysis_dashboard.html')
            with open(dashboard_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(html_content.encode('utf-8'))
            logger.info("✅ Dashboard served at /StoreActivityandCommunications")
        except FileNotFoundError:
            logger.error(f"Dashboard file not found")
            self.send_error(404, "Dashboard not found")
        except Exception as e:
            logger.error(f"Error serving dashboard: {e}")
            self.send_error(500, f"Failed to load dashboard: {e}")

    def _handle_root(self):
        """Root endpoint with API documentation"""
        response = {
            'service': 'AMP Dashboard Backend API',
            'version': '1.0',
            'status': 'running',
            'endpoints': {
                '/health': 'Health check and connection status',
                '/api/amp-data': 'Get AMP data with optional filters',
                '/api/amp-metrics': 'Get summary metrics',
                '/api/amp-filters': 'Get filter options'
            },
            'bigquery': {
                'project': PROJECT_ID,
                'dataset': DATASET_ID,
                'table': TABLE_ID,
                'connected': bigquery_available
            },
            'credentials': {
                'type': 'Application Default Credentials (gcloud)',
                'location': os.path.expanduser('~/.config/gcloud/application_default_credentials.json')
            }
        }
        self._send_json(response)

    def _handle_amp_data(self, query_params):
        """Fetch AMP data from BigQuery with optional filters"""
        try:
            if not bigquery_available:
                # Return sample data if BigQuery not available
                data = self._get_sample_data()
                response = {
                    'success': True,
                    'source': 'sample',
                    'count': len(data),
                    'data': data,
                    'message': 'BigQuery not available - showing sample data',
                    'timestamp': datetime.utcnow().isoformat()
                }
                self._send_json(response)
                return

            # Get query parameters
            filters = {
                'division': self._get_param(query_params, 'division'),
                'region': self._get_param(query_params, 'region'),
                'market': self._get_param(query_params, 'market'),
                'facility': self._get_param(query_params, 'facility'),
                'week': self._get_param(query_params, 'week'),
                'activity_type': self._get_param(query_params, 'activity_type'),
                'store_area': self._get_param(query_params, 'store_area'),
                'keyword': self._get_param(query_params, 'keyword')
            }
            
            days = int(self._get_param(query_params, 'days', '90'))
            limit = int(self._get_param(query_params, 'limit', '1000'))

            # Build and execute query
            query = self._build_amp_query(filters, days, limit)
            logger.info(f"Executing BigQuery query with filters: {filters}")
            
            query_job = client.query(query)
            results = query_job.result()

            # Convert results to list of dicts
            data = [dict(row) for row in results]
            
            # Convert datetime objects to ISO strings
            for record in data:
                for key, value in record.items():
                    if isinstance(value, datetime):
                        record[key] = value.isoformat()

            logger.info(f"✅ Retrieved {len(data)} records from BigQuery")
            
            response = {
                'success': True,
                'source': 'bigquery',
                'count': len(data),
                'data': data,
                'filters_applied': filters,
                'timestamp': datetime.utcnow().isoformat()
            }
            self._send_json(response)

        except Exception as e:
            logger.error(f"❌ Error fetching AMP data: {e}", exc_info=True)
            response = {
                'success': False,
                'error': str(e),
                'timestamp': datetime.utcnow().isoformat()
            }
            self._send_json(response)

    def _handle_amp_metrics(self, query_params):
        """Get summary metrics for AMP data"""
        try:
            if not bigquery_available:
                data = self._get_sample_data()
                metrics = {
                    'total_activities': len(data),
                    'completed_activities': sum(1 for d in data if d.get('status') == 'complete'),
                    'in_progress_activities': sum(1 for d in data if d.get('status') == 'incomplete'),
                    'inform_only_activities': sum(1 for d in data if d.get('status') == 'inform'),
                    'completion_rate': 75.5
                }
                response = {
                    'success': True,
                    'source': 'sample',
                    'metrics': metrics,
                    'message': 'Sample metrics',
                    'timestamp': datetime.utcnow().isoformat()
                }
                self._send_json(response)
                return

            days = int(self._get_param(query_params, 'days', '90'))

            query = f"""
                SELECT
                    COUNT(*) as total_activities,
                    COUNTIF(msg_status_id = 'PUBLISHED') as completed_activities,
                    COUNTIF(msg_status_id = 'DRAFT') as in_progress_activities,
                    COUNTIF(msg_status_id NOT IN ('PUBLISHED', 'DRAFT')) as inform_only_activities,
                    SUM(ARRAY_LENGTH(trgt_store_nbr_array)) as total_store_impact,
                    ROUND(100 * COUNTIF(msg_status_id = 'PUBLISHED') / COUNT(*), 2) as completion_rate
                FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`
                WHERE msg_start_dt >= DATE_SUB(CURRENT_DATE(), INTERVAL {days} DAY)
            """

            logger.info(f"Executing metrics query for {days} days")
            
            query_job = client.query(query)
            results = query_job.result()
            
            row = next(results)
            metrics = dict(row)

            logger.info(f"✅ Retrieved metrics: {metrics}")
            
            response = {
                'success': True,
                'source': 'bigquery',
                'metrics': metrics,
                'timestamp': datetime.utcnow().isoformat()
            }
            self._send_json(response)

        except Exception as e:
            logger.error(f"❌ Error fetching metrics: {e}", exc_info=True)
            response = {
                'success': False,
                'error': str(e),
                'timestamp': datetime.utcnow().isoformat()
            }
            self._send_json(response)

    def _handle_amp_filters(self, query_params):
        """Get distinct values for filter dropdowns"""
        try:
            if not bigquery_available:
                filters = {
                    'divisions': ['1', '2', '3', '4'],
                    'regions': ['East', 'West', 'Central', 'South'],
                    'markets': ['Market A', 'Market B', 'Market C'],
                    'facilities': ['Facility 1', 'Facility 2'],
                    'weeks': [1, 2, 3, 4, 5],
                    'activity_types': ['Type A', 'Type B'],
                    'store_areas': ['Area 1', 'Area 2']
                }
                response = {
                    'success': True,
                    'source': 'sample',
                    'filters': filters,
                    'message': 'Sample filters',
                    'timestamp': datetime.utcnow().isoformat()
                }
                self._send_json(response)
                return

            days = int(self._get_param(query_params, 'days', '90'))

            query = f"""
                SELECT
                    ARRAY_AGG(DISTINCT division IGNORE NULLS ORDER BY division) as divisions,
                    ARRAY_AGG(DISTINCT region IGNORE NULLS ORDER BY region) as regions,
                    ARRAY_AGG(DISTINCT market IGNORE NULLS ORDER BY market) as markets,
                    ARRAY_AGG(DISTINCT facility IGNORE NULLS ORDER BY facility) as facilities,
                    ARRAY_AGG(DISTINCT EXTRACT(WEEK FROM msg_start_dt) IGNORE NULLS ORDER BY EXTRACT(WEEK FROM msg_start_dt) DESC) as weeks,
                    ARRAY_AGG(DISTINCT actv_type_nm IGNORE NULLS ORDER BY actv_type_nm) as activity_types,
                    ARRAY_AGG(DISTINCT bus_domain_nm IGNORE NULLS ORDER BY bus_domain_nm) as store_areas
                FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`
                WHERE msg_start_dt >= DATE_SUB(CURRENT_DATE(), INTERVAL {days} DAY)
            """

            logger.info("Fetching filter options...")
            
            query_job = client.query(query)
            results = query_job.result()
            
            row = next(results)
            filter_options = {
                'divisions': row['divisions'] or [],
                'regions': row['regions'] or [],
                'markets': row['markets'] or [],
                'facilities': row['facilities'] or [],
                'weeks': row['weeks'] or [],
                'activity_types': row['activity_types'] or [],
                'store_areas': row['store_areas'] or []
            }

            logger.info(f"✅ Retrieved {len(filter_options)} filter types")
            
            response = {
                'success': True,
                'source': 'bigquery',
                'filters': filter_options,
                'timestamp': datetime.utcnow().isoformat()
            }
            self._send_json(response)

        except Exception as e:
            logger.error(f"❌ Error fetching filters: {e}", exc_info=True)
            response = {
                'success': False,
                'error': str(e),
                'timestamp': datetime.utcnow().isoformat()
            }
            self._send_json(response)

    def _build_amp_query(self, filters, days, limit):
        """Build BigQuery SQL query with filters"""
        
        query = f"""
            WITH amp_data AS (
                SELECT 
                    CAST(EXTRACT(WEEK FROM msg_start_dt) AS INT64) as week_number,
                    actv_title_home_ofc_nm as activity_title,
                    CONCAT('*', COALESCE(CAST(trgt_store_nbr_array[SAFE_OFFSET(0)] AS STRING), 'All Locations')) as location,
                    ARRAY_LENGTH(trgt_store_nbr_array) as total_count,
                    CASE 
                        WHEN msg_status_id = 'PUBLISHED' THEN 'complete'
                        WHEN msg_status_id = 'DRAFT' THEN 'incomplete'
                        ELSE 'inform'
                    END as status,
                    division,
                    region,
                    market,
                    facility,
                    actv_type_nm as activity_type,
                    bus_domain_nm as store_area,
                    msg_status_id = 'PUBLISHED' as published,
                    create_ts,
                    msg_start_dt,
                    msg_end_dt
                FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`
                WHERE 1=1
                    AND msg_start_dt >= DATE_SUB(CURRENT_DATE(), INTERVAL {days} DAY)
                    AND msg_status_id = 'PUBLISHED'
        """

        # Add dynamic filters
        if filters.get('division'):
            query += f" AND division = '{filters['division']}'"
        if filters.get('region'):
            query += f" AND region = '{filters['region']}'"
        if filters.get('market'):
            query += f" AND market = '{filters['market']}'"
        if filters.get('facility'):
            query += f" AND facility = '{filters['facility']}'"
        if filters.get('week'):
            query += f" AND EXTRACT(WEEK FROM msg_start_dt) = {filters['week']}"
        if filters.get('activity_type'):
            query += f" AND actv_type_nm = '{filters['activity_type']}'"
        if filters.get('store_area'):
            query += f" AND bus_domain_nm = '{filters['store_area']}'"
        if filters.get('keyword'):
            keyword = filters['keyword'].lower()
            query += f" AND (LOWER(actv_title_home_ofc_nm) LIKE '%{keyword}%' OR LOWER(actv_type_nm) LIKE '%{keyword}%' OR LOWER(bus_domain_nm) LIKE '%{keyword}%')"

        query += f"""
                )
                SELECT * FROM amp_data
                ORDER BY week_number DESC, total_count DESC
                LIMIT {limit}
            """

        return query

    def _get_sample_data(self):
        """Return sample AMP data for testing"""
        base_date = datetime.utcnow()
        data = []
        for i in range(10):
            data.append({
                'week_number': 8 - (i % 4),
                'activity_title': f'Sample Activity {i+1}',
                'location': f'*{1000 + i}',
                'total_count': 50 + (i * 10),
                'status': ['complete', 'incomplete', 'inform'][i % 3],
                'division': str((i % 4) + 1),
                'region': ['East', 'West', 'Central'][i % 3],
                'market': f'Market {chr(65 + (i % 3))}',
                'facility': f'Facility {i % 5}',
                'activity_type': f'Type {chr(65 + (i % 3))}',
                'store_area': f'Area {i % 3}',
                'published': i % 2 == 0,
                'msg_start_dt': (base_date - timedelta(days=i)).isoformat(),
                'msg_end_dt': (base_date - timedelta(days=i) + timedelta(days=7)).isoformat()
            })
        return data

    def _get_param(self, query_params, key, default=''):
        """Extract query parameter safely"""
        if key in query_params and query_params[key]:
            return query_params[key][0]
        return default

    def log_message(self, format, *args):
        """Suppress default HTTP logging"""
        pass


def run_server(host='localhost', port=5000):
    """Start the HTTP server"""
    server_address = (host, port)
    httpd = http.server.HTTPServer(server_address, AMPRequestHandler)
    logger.info(f"🚀 Starting AMP Dashboard Backend on http://{host}:{port}")
    logger.info(f"📊 BigQuery: {PROJECT_ID}.{DATASET_ID}.{TABLE_ID}")
    logger.info(f"🔐 Using gcloud application default credentials")
    logger.info(f"📖 API docs: http://{host}:{port}/")
    logger.info(f"🟢 BigQuery Status: {'✅ Connected' if bigquery_available else '⚠️  Using sample data'}")
    logger.info(f"Press Ctrl+C to stop server")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.info("\n👋 Server stopped")
        httpd.server_close()
        sys.exit(0)


if __name__ == '__main__':
    run_server()
