"""
V.E.T. Dashboard Backend - Executive Report
Fetches TDA data with Dallas POC focus and Implementation Week from Intake Hub
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Any
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from google.cloud import bigquery
import logging
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import sample data
from sample_data import SAMPLE_DATA_49_PROJECTS

# Configuration
app = Flask(__name__, static_folder=os.path.dirname(__file__), static_url_path='/static')
CORS(app)

# Logging — send ALL log output to stdout so PowerShell doesn't kill the process
logging.basicConfig(level=logging.INFO, stream=sys.stdout,
                    format='%(levelname)s:%(name)s:%(message)s')
logger = logging.getLogger(__name__)

# Ensure werkzeug/Flask logs also go to stdout
for _log_name in ('werkzeug', 'google', 'google.auth', 'urllib3'):
    _l = logging.getLogger(_log_name)
    _l.handlers = [logging.StreamHandler(sys.stdout)]
    _l.propagate = False

# Import PPT service (after logger is initialized)
try:
    from ppt_service import register_ppt_routes
except Exception as e:
    logger.warning(f"PPT service not available: {e}")
    register_ppt_routes = None

# BigQuery Configuration
PROJECT_ID = "wmt-assetprotection-prod"
DATASET_ID = "Store_Support_Dev"
TABLE_ID = "Output- TDA Report"  # Table name with space
INTAKE_HUB_TABLE = "IH_Intake_Data"
FULL_TABLE_ID = f"`{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`"
FULL_INTAKE_HUB_ID = f"`{PROJECT_ID}.{DATASET_ID}.{INTAKE_HUB_TABLE}`"

# V.E.T. Dashboard specific config
# BQ data now uses "Dallas VET" as TDA_Ownership value (renamed from "Dallas POC")
BQ_OWNERSHIP_FILTER = "Dallas VET"
DISPLAY_OWNERSHIP_NAME = "Dallas VET"

# Phase normalization (until BQ data reflects new names)
_PHASE_MAP = {'POC/POT': 'Vet', 'Mkt Scale': 'Test Markets'}
def _normalize_phase(phase):
    return _PHASE_MAP.get(phase, phase)

def _init_bigquery_client():
    """Try to initialize a BigQuery client. Returns client or None."""
    _creds_path = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS',
        r'C:\Users\krush\AppData\Roaming\gcloud\application_default_credentials.json')
    if _creds_path and os.path.exists(_creds_path):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = _creds_path
    try:
        bq_client = bigquery.Client(project=PROJECT_ID)
        logger.info(f"[OK] BigQuery client initialized for project: {PROJECT_ID}")
        return bq_client
    except Exception as e1:
        logger.warning(f"[WARN] ADC failed: {e1}")
        if _creds_path and os.path.exists(_creds_path):
            try:
                from google.oauth2 import service_account
                credentials = service_account.Credentials.from_service_account_file(_creds_path)
                bq_client = bigquery.Client(credentials=credentials, project=PROJECT_ID)
                logger.info(f"[OK] BigQuery client initialized with service account from: {_creds_path}")
                return bq_client
            except Exception as e2:
                logger.error(f"[ERROR] Service account credentials failed: {e2}")
    return None

# Initialize BigQuery client
client = _init_bigquery_client()
if not client:
    logger.warning("[WARN] BigQuery not available at startup - will retry on data request")


class VETDataManager:
    """Manages V.E.T. Dashboard data from BigQuery with Intake Hub integration"""
    
    def __init__(self, bigquery_client):
        self.client = bigquery_client
        self._data_cache = None
        self._cache_timestamp = None
    
    def fetch_all_data(self, force_refresh=False) -> List[Dict[str, Any]]:
        """Fetch V.E.T. data from BigQuery with Intake Hub join and caching"""
        
        # Return cached data if available (less than 5 minutes old)
        if self._data_cache and not force_refresh:
            if self._cache_timestamp:
                age = (datetime.now() - self._cache_timestamp).total_seconds()
                if age < 300:  # 5 minutes
                    logger.info(f"Returning cached data (age: {age:.0f}s)")
                    return self._data_cache
        
        if not self.client:
            # Retry BQ initialization — credentials may now be available
            self.client = _init_bigquery_client()
        
        if not self.client:
            logger.warning(f"BigQuery client not initialized - using {len(SAMPLE_DATA_49_PROJECTS)} sample projects")
            for row in SAMPLE_DATA_49_PROJECTS:
                row['Phase'] = _normalize_phase(row.get('Phase', 'Unknown'))
            self._data_cache = SAMPLE_DATA_49_PROJECTS
            self._cache_timestamp = datetime.now()
            return SAMPLE_DATA_49_PROJECTS
        
        try:
            query = f"""
            SELECT 
                tda.Topic AS `Initiative - Project Title`,
                tda.Health_Update AS `Health Status`,
                tda.Phase,
                SUM(CASE 
                    WHEN tda.Phase = tda.Facility_Phase THEN tda.Facility 
                    ELSE 0 
                END) AS `# of Stores`,
                tda.Dallas_POC AS `Executive Notes`,
                tda.TDA_Ownership,
                tda.Intake_Card_Nbr AS `Project ID`,
                tda.Intake_n_Testing AS `Intake & Testing`,
                tda.Deployment,
                COALESCE(CAST(MIN(intake.WM_Week) AS STRING), 'TBD') AS `WM Week`
            FROM 
                {FULL_TABLE_ID} tda
            LEFT JOIN 
                {FULL_INTAKE_HUB_ID} intake
                ON CAST(tda.Intake_Card_Nbr AS STRING) = CAST(intake.Intake_Card AS STRING)
            WHERE 
                tda.TDA_Ownership = '{BQ_OWNERSHIP_FILTER}'
            GROUP BY
                tda.Topic,
                tda.Health_Update,
                tda.Phase,
                tda.Dallas_POC,
                tda.TDA_Ownership,
                tda.Intake_Card_Nbr,
                tda.Intake_n_Testing,
                tda.Deployment
            ORDER BY 
                tda.Phase ASC,
                tda.Topic ASC
            """
            
            logger.info("Executing BigQuery query with Intake Hub join...")
            logger.info(f"Filtering for TDA Ownership = '{BQ_OWNERSHIP_FILTER}'")
            query_job = self.client.query(query)
            rows = query_job.result()
            
            # Convert to list of dictionaries and normalize phases
            data = [dict(row) for row in rows]
            for row in data:
                row['Phase'] = _normalize_phase(row.get('Phase', 'Unknown'))
            
            # Cache the data
            self._data_cache = data
            self._cache_timestamp = datetime.now()
            
            logger.info(f"Fetched {len(data)} records from BigQuery (Dallas POC only)")
            return data
            
        except Exception as e:
            logger.error(f"Error fetching data from BigQuery: {e}")
            return []
    
    def get_unique_phases(self) -> List[str]:
        """Get list of unique phases - returned in TDA progression order"""
        data = self.fetch_all_data()
        phases_found = set()
        for row in data:
            phase = row.get('Phase', 'Unknown')
            if phase:
                phases_found.add(str(phase))
        
        # TDA phase progression order
        phase_order = ['Pending', 'Vet', 'Test', 'Test Markets', 'Roll/Deploy']
        # Return only phases that exist in data, in the correct order
        return [p for p in phase_order if p in phases_found]
    
    def get_unique_health_statuses(self) -> List[str]:
        """Get list of unique health statuses (Dallas POC only)"""
        data = self.fetch_all_data()
        statuses = set()
        for row in data:
            status = row.get('Health Status', 'Unknown')
            if status:
                statuses.add(str(status))
        return sorted(list(statuses))
    
    def get_unique_titles(self) -> List[str]:
        """Get list of unique project titles"""
        data = self.fetch_all_data()
        titles = set()
        for row in data:
            title = row.get('Initiative - Project Title', 'Unknown')
            if title:
                titles.add(str(title))
        return sorted(list(titles))
    
    def get_unique_ownerships(self) -> List[str]:
        """Get list of unique TDA ownerships"""
        data = self.fetch_all_data()
        ownerships = set()
        for row in data:
            ownership = row.get('TDA Ownership', 'Unknown')
            if ownership:
                ownerships.add(str(ownership))
        return sorted(list(ownerships))
    
    def get_at_risk_items(self) -> List[Dict[str, Any]]:
        """Get items with At Risk health status (Needs Attention section)"""
        data = self.fetch_all_data()
        return [row for row in data if str(row.get('Health Status', '')).lower() == 'at risk']
    
    def filter_data(self, phase: str = None, health_status: str = None, 
                   ownership: str = None) -> List[Dict[str, Any]]:
        """Filter data by phase and/or health status (always Dallas POC)"""
        data = self.fetch_all_data()
        
        filtered = data
        
        if phase and phase.lower() != "all":
            filtered = [row for row in filtered if str(row.get('Phase', '')).lower() == phase.lower()]
        
        if health_status and health_status.lower() != "all":
            filtered = [row for row in filtered if str(row.get('Health Status', '')).lower() == health_status.lower()]
        
        # Ownership is always filtered to Dallas POC in the query, no need to filter again
        
        return filtered


# Initialize data manager
data_manager = VETDataManager(client)


# Root route - serve the V.E.T. Dashboard HTML
@app.route('/favicon.ico')
def favicon():
    logo = os.path.join(os.path.dirname(__file__), 'Spark_Blank.png')
    if os.path.exists(logo):
        return send_file(logo, mimetype='image/png', max_age=86400)
    return '', 204

@app.route('/', methods=['GET'])
@app.route('/VET_Executive_Report', methods=['GET'])
def show_dashboard():
    """Serve the V.E.T. Dashboard HTML file"""
    try:
        dashboard_path = os.path.join(os.path.dirname(__file__), 'vet_dashboard.html')
        with open(dashboard_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        return html_content, 200, {'Content-Type': 'text/html; charset=utf-8'}
    except Exception as e:
        logger.error(f"Error serving dashboard: {e}")
        return jsonify({
            'success': False,
            'error': f"Could not load dashboard: {str(e)}"
        }), 500

# API Routes

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'bigquery_connected': client is not None
    })


@app.route('/api/data', methods=['GET'])
def get_data():
    """Get TDA data with optional filtering"""
    try:
        phase = request.args.get('phase', 'All')
        health_status = request.args.get('health_status', 'All')
        force_refresh = request.args.get('refresh', 'false').lower() == 'true'
        
        if force_refresh:
            logger.info("Force refreshing data...")
            data_manager._data_cache = None
            data_manager._cache_timestamp = None
        
        filtered_data = data_manager.filter_data(phase, health_status)
        
        return jsonify({
            'success': True,
            'count': len(filtered_data),
            'phase': phase,
            'health_status': health_status,
            'data': filtered_data,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error in /api/data: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500


@app.route('/api/phases', methods=['GET'])
def get_phases():
    """Get list of unique phases"""
    try:
        phases = data_manager.get_unique_phases()
        return jsonify({
            'success': True,
            'phases': phases,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Error in /api/phases: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/health-statuses', methods=['GET'])
def get_health_statuses():
    """Get list of unique health statuses"""
    try:
        statuses = data_manager.get_unique_health_statuses()
        return jsonify({
            'success': True,
            'health_statuses': statuses,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Error in /api/health-statuses: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500




@app.route('/api/titles', methods=['GET'])
def get_titles():
    """Get list of unique project titles"""
    try:
        titles = data_manager.get_unique_titles()
        return jsonify({
            'success': True,
            'titles': titles,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Error in /api/titles: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/ownerships', methods=['GET'])
def get_ownerships():
    """Get list of unique TDA ownerships"""
    try:
        ownerships = data_manager.get_unique_ownerships()
        return jsonify({
            'success': True,
            'ownerships': ownerships,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Error in /api/ownerships: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/needs-attention', methods=['GET'])
def get_needs_attention():
    """Get At Risk items for Needs Attention section"""
    try:
        at_risk_items = data_manager.get_at_risk_items()
        return jsonify({
            'success': True,
            'count': len(at_risk_items),
            'data': at_risk_items,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Error in /api/needs-attention: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/summary', methods=['GET'])
def get_summary():
    """Get summary statistics"""
    try:
        phase = request.args.get('phase', 'All')
        health_status = request.args.get('health_status', 'All')
        
        filtered_data = data_manager.filter_data(phase, health_status)
        
        summary = {
            'total_projects': len(filtered_data),
            'total_stores': sum([int(row.get('# of Stores', 0) or 0) for row in filtered_data]),
            'by_health_status': {},
            'by_phase': {}
        }
        
        # Count by health status
        for row in filtered_data:
            status = row.get('Health Status', 'Unknown')
            if status:
                summary['by_health_status'][status] = summary['by_health_status'].get(status, 0) + 1
        
        # Count by phase
        for row in filtered_data:
            phase_val = row.get('Phase', 'Unknown')
            if phase_val:
                summary['by_phase'][phase_val] = summary['by_phase'].get(phase_val, 0) + 1
        
        return jsonify({
            'success': True,
            'summary': summary,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error in /api/summary: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/refresh', methods=['GET'])
def refresh_data():
    """Clear cache and refresh data from BigQuery"""
    try:
        global cache_data, cache_timestamp
        cache_data = None
        cache_timestamp = None
        logger.info("Cache cleared, data will be refreshed on next request")
        return jsonify({
            'success': True,
            'message': 'Cache cleared, data will be refreshed',
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Error in /api/refresh: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/export/csv', methods=['GET'])
def export_csv():
    """Export filtered data as CSV"""
    try:
        import csv
        from io import StringIO
        
        phase = request.args.get('phase', 'All')
        health_status = request.args.get('health_status', 'All')
        
        filtered_data = data_manager.filter_data(phase, health_status)
        
        if not filtered_data:
            return jsonify({'success': False, 'error': 'No data to export'}), 400
        
        # Create CSV
        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=filtered_data[0].keys())
        writer.writeheader()
        writer.writerows(filtered_data)
        
        csv_content = output.getvalue()
        
        # Create a temporary file
        temp_file = f"tda_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        return jsonify({
            'success': True,
            'message': 'CSV export ready',
            'data': csv_content
        })
        
    except Exception as e:
        logger.error(f"Error in /api/export/csv: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ── VET PPT Generation Endpoint ──
@app.route('/api/vet/generate-ppt', methods=['POST'])
def generate_vet_ppt():
    """Generate V.E.T. Executive Report PowerPoint (VET-specific generator)"""
    try:
        from vet_ppt_generator import generate_vet_pptx
        
        logger.info("Generating VET Executive Report PPT...")
        pptx_path = generate_vet_pptx()
        
        if not pptx_path:
            return jsonify({
                'success': False,
                'message': 'Failed to generate PPT'
            }), 500
        
        from pathlib import Path
        filename = Path(pptx_path).name
        
        return jsonify({
            'success': True,
            'message': 'PPT generated successfully',
            'file_name': filename,
            'file_path': str(pptx_path),
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f"Error in /api/vet/generate-ppt: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'message': f'Server error: {str(e)}'
        }), 500


# Register PPT service routes (must happen at import time, not just in __main__)
if register_ppt_routes:
    register_ppt_routes(app)
    logger.info("PPT service routes registered")

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5001))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Starting V.E.T. Dashboard backend on port {port} (Dallas VET focus)")
    logger.info(f"BQ Ownership Filter: {BQ_OWNERSHIP_FILTER} (displayed as {DISPLAY_OWNERSHIP_NAME})")
    app.run(host='0.0.0.0', port=port, debug=debug)
