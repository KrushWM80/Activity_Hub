#!/usr/bin/env python3
"""
AMP Dashboard Backend Server
Provides secure BigQuery data access using existing gcloud credentials
No OAuth2 needed - uses application default credentials
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from google.cloud import bigquery
import logging
from datetime import datetime, timedelta
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

# BigQuery Configuration
PROJECT_ID = 'wmt-assetprotection-prod'
DATASET_ID = 'Store_Support_Dev'
TABLE_ID = 'Output - AMP ALL 2'

# Initialize BigQuery client (uses application default credentials)
try:
    client = bigquery.Client(project=PROJECT_ID)
    logger.info(f"✅ BigQuery client initialized for project: {PROJECT_ID}")
except Exception as e:
    logger.error(f"❌ Failed to initialize BigQuery client: {e}")
    client = None


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'service': 'AMP Dashboard Backend',
        'project': PROJECT_ID,
        'bigquery_connected': client is not None,
        'timestamp': datetime.utcnow().isoformat()
    })


@app.route('/api/amp-data', methods=['GET'])
def get_amp_data():
    """
    Fetch AMP data from BigQuery with optional filters
    
    Query Parameters:
    - division: Filter by division
    - region: Filter by region
    - market: Filter by market
    - facility: Filter by facility
    - week: Filter by WM week
    - activity_type: Filter by activity type
    - store_area: Filter by store area
    - keyword: Search in title/type/area
    - days: Number of days back (default: 90)
    - limit: Max results (default: 1000)
    """
    try:
        if not client:
            return jsonify({'error': 'BigQuery connection not available'}), 503

        # Get query parameters
        filters = {
            'division': request.args.get('division'),
            'region': request.args.get('region'),
            'market': request.args.get('market'),
            'facility': request.args.get('facility'),
            'week': request.args.get('week'),
            'activity_type': request.args.get('activity_type'),
            'store_area': request.args.get('store_area'),
            'keyword': request.args.get('keyword')
        }
        
        days = int(request.args.get('days', 90))
        limit = int(request.args.get('limit', 1000))

        # Build query
        query = build_amp_query(filters, days, limit)
        
        logger.info(f"Executing BigQuery query with filters: {filters}")
        
        # Execute query
        query_job = client.query(query)
        results = query_job.result()

        # Convert results to list of dicts
        data = [dict(row) for row in results]
        
        # Convert datetime objects to ISO strings
        for record in data:
            for key, value in record.items():
                if isinstance(value, (datetime, )):
                    record[key] = value.isoformat()

        logger.info(f"✅ Retrieved {len(data)} records from BigQuery")
        
        return jsonify({
            'success': True,
            'count': len(data),
            'data': data,
            'filters_applied': filters,
            'timestamp': datetime.utcnow().isoformat()
        })

    except Exception as e:
        logger.error(f"❌ Error fetching AMP data: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/amp-metrics', methods=['GET'])
def get_amp_metrics():
    """
    Get summary metrics for AMP data
    
    Returns:
    - total_activities
    - completed_activities
    - in_progress_activities
    - inform_only_activities
    - total_store_impact
    - completion_rate
    """
    try:
        if not client:
            return jsonify({'error': 'BigQuery connection not available'}), 503

        days = int(request.args.get('days', 90))

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
        
        return jsonify({
            'success': True,
            'metrics': metrics,
            'timestamp': datetime.utcnow().isoformat()
        })

    except Exception as e:
        logger.error(f"❌ Error fetching metrics: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/amp-filters', methods=['GET'])
def get_filter_options():
    """
    Get distinct values for filter dropdowns
    
    Returns:
    - divisions
    - regions
    - markets
    - facilities
    - weeks
    - activity_types
    - store_areas
    """
    try:
        if not client:
            return jsonify({'error': 'BigQuery connection not available'}), 503

        days = int(request.args.get('days', 90))

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

        logger.info(f"✅ Retrieved filter options")
        
        return jsonify({
            'success': True,
            'filters': filter_options,
            'timestamp': datetime.utcnow().isoformat()
        })

    except Exception as e:
        logger.error(f"❌ Error fetching filters: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


def build_amp_query(filters, days, limit):
    """Build BigQuery SQL query with filters"""
    
    query = f"""
        WITH amp_data AS (
            SELECT 
                CAST(EXTRACT(WEEK FROM msg_start_dt) AS INT64) as week_number,
                actv_title_home_ofc_nm as activity_title,
                CONCAT('*', COALESCE(CAST(trgt_store_nbr_array[SAFE_OFFSET(0)] AS STRING), 'All Locations')) as location,
                ARRAY_LENGTH(trgt_store_nbr_array) as total_count,
                COUNTIF(store_format = 'SC') as sc_count,
                COUNTIF(store_format = 'NHM') as nhm_count,
                COUNTIF(division = '1') as div1_count,
                COUNTIF(store_format = 'FUEL') as fuel_count,
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


@app.route('/', methods=['GET'])
def root():
    """Root endpoint with API documentation"""
    return jsonify({
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
            'table': TABLE_ID
        },
        'credentials': {
            'type': 'Application Default Credentials (gcloud)',
            'location': '~/.config/gcloud/application_default_credentials.json'
        }
    })


if __name__ == '__main__':
    port = 5000
    logger.info(f"🚀 Starting AMP Dashboard Backend on http://localhost:{port}")
    logger.info(f"📊 BigQuery: {PROJECT_ID}.{DATASET_ID}.{TABLE_ID}")
    logger.info(f"🔐 Using gcloud application default credentials")
    logger.info(f"📖 API docs: http://localhost:{port}/")
    
    app.run(host='localhost', port=port, debug=False)
