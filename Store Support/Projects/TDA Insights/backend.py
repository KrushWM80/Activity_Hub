"""
TDA Insights Dashboard Backend
Fetches data from BigQuery and serves via REST API
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
TABLE_ID = "Output_TDA Report"
FULL_TABLE_ID = f"{PROJECT_ID}.{DATASET_ID}.`{TABLE_ID}`"

# Initialize BigQuery client
try:
    client = bigquery.Client(project=PROJECT_ID)
    logger.info(f"BigQuery client initialized for project: {PROJECT_ID}")
except Exception as e:
    logger.error(f"Failed to initialize BigQuery client: {e}")
    client = None


class TDADataManager:
    """Manages TDA Insights data from BigQuery"""
    
    def __init__(self, bigquery_client):
        self.client = bigquery_client
        self._data_cache = None
        self._cache_timestamp = None
    
    def fetch_all_data(self, force_refresh=False) -> List[Dict[str, Any]]:
        """Fetch all TDA data from BigQuery with caching"""
        
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
                *
            FROM 
                `{FULL_TABLE_ID}`
            ORDER BY 
                `Phase` ASC,
                `Initiative - Project Title` ASC
            """
            
            logger.info("Executing BigQuery query...")
            query_job = self.client.query(query)
            rows = query_job.result()
            
            # Convert to list of dictionaries
            data = [dict(row) for row in rows]
            
            # Cache the data
            self._data_cache = data
            self._cache_timestamp = datetime.now()
            
            logger.info(f"Fetched {len(data)} records from BigQuery")
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
        """Get list of unique health statuses"""
        data = self.fetch_all_data()
        statuses = set()
        for row in data:
            status = row.get('Health Status', 'Unknown')
            if status:
                statuses.add(str(status))
        return sorted(list(statuses))
    
    def filter_data(self, phase: str = None, health_status: str = None) -> List[Dict[str, Any]]:
        """Filter data by phase and/or health status"""
        data = self.fetch_all_data()
        
        filtered = data
        
        if phase and phase != "All":
            filtered = [row for row in filtered if str(row.get('Phase', '')).lower() == phase.lower()]
        
        if health_status and health_status != "All":
            filtered = [row for row in filtered if str(row.get('Health Status', '')).lower() == health_status.lower()]
        
        return filtered


# Initialize data manager
data_manager = TDADataManager(client)


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
    
    logger.info(f"Starting TDA Insights backend on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)
