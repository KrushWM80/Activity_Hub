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

# Import PPT service
try:
    from ppt_service import register_ppt_routes
except ImportError:
    register_ppt_routes = None

# Configuration
app = Flask(__name__)
CORS(app)

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# BigQuery Configuration
PROJECT_ID = "wmt-assetprotection-prod"
DATASET_ID = "Store_Support_Dev"
TABLE_ID = "Output- TDA Report"  # Note: space before TDA
INTAKE_HUB_TABLE = "IH_Intake_Data"
FULL_TABLE_ID = f"{PROJECT_ID}.{DATASET_ID}.`{TABLE_ID}`"
FULL_INTAKE_HUB_ID = f"{PROJECT_ID}.{DATASET_ID}.{INTAKE_HUB_TABLE}"

# V.E.T. Dashboard specific config
DEFAULT_OWNERSHIP_FILTER = "Dallas POC"

# Initialize BigQuery client
try:
    client = bigquery.Client(project=PROJECT_ID)
    logger.info(f"BigQuery client initialized for project: {PROJECT_ID}")
except Exception as e:
    logger.error(f"Failed to initialize BigQuery client: {e}")
    client = None


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
            logger.error("BigQuery client not initialized")
            return []
        
        try:
            query = f"""
            SELECT 
                tda.`Initiative - Project Title`,
                tda.`Health Status`,
                tda.Phase,
                tda.`# of Stores`,
                tda.`Dallas POC` AS `Executive Notes`,
                tda.`TDA Ownership`,
                tda.Intake_Card_Nbr AS `Project ID`,
                tda.`Intake & Testing`,
                tda.Deployment,
                COALESCE(MIN(intake.WM_Week), 'TBD') AS `WM Week`,
                tda.Region,
                tda.Market,
                tda.`Proposed Date`,
                tda.`Implementation Status`
            FROM 
                `{FULL_TABLE_ID}` tda
            LEFT JOIN 
                `{FULL_INTAKE_HUB_ID}` intake
                ON CAST(tda.Intake_Card_Nbr AS STRING) = CAST(intake.Intake_Card AS STRING)
            WHERE 
                tda.`TDA Ownership` = '{DEFAULT_OWNERSHIP_FILTER}'
            GROUP BY
                tda.`Initiative - Project Title`,
                tda.`Health Status`,
                tda.Phase,
                tda.`# of Stores`,
                tda.`Dallas POC`,
                tda.`TDA Ownership`,
                tda.Intake_Card_Nbr,
                tda.`Intake & Testing`,
                tda.Deployment,
                tda.Region,
                tda.Market,
                tda.`Proposed Date`,
                tda.`Implementation Status`
            ORDER BY 
                tda.Phase ASC,
                tda.`Initiative - Project Title` ASC
            """
            
            logger.info("Executing BigQuery query with Intake Hub join...")
            logger.info(f"Filtering for TDA Ownership = '{DEFAULT_OWNERSHIP_FILTER}'")
            query_job = self.client.query(query)
            rows = query_job.result()
            
            # Convert to list of dictionaries
            data = [dict(row) for row in rows]
            
            # Cache the data
            self._data_cache = data
            self._cache_timestamp = datetime.now()
            
            logger.info(f"Fetched {len(data)} records from BigQuery (Dallas POC only)")
            return data
            
        except Exception as e:
            logger.error(f"Error fetching data from BigQuery: {e}")
            return []
    
    def get_unique_phases(self) -> List[str]:
        """Get list of unique phases"""
        data = self.fetch_all_data()
        phases = set()
        for row in data:
            phase = row.get('Phase', 'Unknown')
            if phase:
                phases.add(str(phase))
        return sorted(list(phases))
    
    def get_unique_health_statuses(self) -> List[str]:
        """Get list of unique health statuses (Dallas POC only)"""
        data = self.fetch_all_data()
        statuses = set()
        for row in data:
            status = row.get('Health Status', 'Unknown')
            if status:
                statuses.add(str(status))
        return sorted(list(statuses))
    
    def get_unique_ownerships(self) -> List[str]:
        """Get list of unique ownerships (returns only Dallas POC for V.E.T.)"""
        return [DEFAULT_OWNERSHIP_FILTER]
    
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
@app.route('/', methods=['GET'])
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


@app.route('/api/ownerships', methods=['GET'])
def get_ownerships():
    """Get list of ownerships (V.E.T. dashboard - always Dallas POC)"""
    try:
        ownerships = data_manager.get_unique_ownerships()
        return jsonify({
            'success': True,
            'ownerships': ownerships,
            'default': DEFAULT_OWNERSHIP_FILTER,
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


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    # Register PPT service routes
    if register_ppt_routes:
        register_ppt_routes(app)
        logger.info("PPT service routes registered")
    
    logger.info(f"Starting V.E.T. Dashboard backend on port {port} (Dallas POC focus)")
    logger.info(f"Default TDA Ownership Filter: {DEFAULT_OWNERSHIP_FILTER}")
    app.run(host='0.0.0.0', port=port, debug=debug)
