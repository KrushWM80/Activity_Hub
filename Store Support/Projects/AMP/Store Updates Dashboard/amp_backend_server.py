#!/usr/bin/env python3
"""
AMP Dashboard Backend Server
Provides secure BigQuery data access using existing gcloud credentials
No OAuth2 needed - uses application default credentials

Audio Features:
- Summarized MP4 audio generation using Jenny neural voice
- Direct text-to-MP4 synthesis with FFmpeg
"""

from flask import Flask, jsonify, request, send_file, render_template_string
from flask_cors import CORS
from google.cloud import bigquery
import logging
import os
from datetime import datetime, timedelta
import json
import sys
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

# Add MP4 Pipeline to path
sys.path.insert(0, str(Path(__file__).parent.parent / "Zorro" / "Audio"))
try:
    from mp4_pipeline import MP4Pipeline, Voice
    MP4_PIPELINE_AVAILABLE = True
    logger.info("✅ MP4 Pipeline (Jenny voice) available")
except ImportError as e:
    MP4_PIPELINE_AVAILABLE = False
    logger.warning(f"⚠️  MP4 Pipeline not available: {e}")

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
    """Serve dashboard HTML interface"""
    try:
        # Try multiple paths to find index.html
        possible_paths = [
            Path(__file__).parent / 'index.html',
            Path.cwd() / 'index.html',
            Path('C:/Users/krush/OneDrive - Walmart Inc/Documents/VSCode/Activity_Hub/Store Support/Projects/AMP/Store Updates Dashboard/index.html')
        ]
        
        index_html = None
        for path in possible_paths:
            if path.exists():
                index_html = path
                break
        
        if index_html:
            with open(index_html, 'r', encoding='utf-8') as f:
                html_content = f.read()
            logger.info(f"✓ Serving dashboard HTML from: {index_html}")
            return html_content, 200, {'Content-Type': 'text/html; charset=utf-8'}
        else:
            # Fallback to API documentation if index.html not found
            return jsonify({
                'service': 'AMP Dashboard Backend API',
                'version': '1.0',
                'status': 'running',
                'message': 'Note: Dashboard HTML (index.html) not found. Showing API documentation instead.',
                'endpoints': {
                    '/health': 'Health check and connection status',
                    '/api/amp-data': 'Get AMP data with optional filters',
                    '/api/amp-metrics': 'Get summary metrics',
                    '/api/amp-filters': 'Get filter options',
                    '/api/generate-audio': 'Generate summarized MP4 audio (Jenny voice)'
                },
                'bigquery': {
                    'project': PROJECT_ID,
                    'dataset': DATASET_ID,
                    'table': TABLE_ID
                },
                'credentials': {
                    'type': 'Application Default Credentials (gcloud)',
                    'location': '~/.config/gcloud/application_default_credentials.json'
                },
                'audio': {
                    'available': MP4_PIPELINE_AVAILABLE,
                    'voice': 'Jenny Neural (Primary)',
                    'format': 'MP4 (AAC @ 256kbps)'
                }
            })
    except Exception as e:
        logger.error(f"Error serving dashboard: {e}")
        return jsonify({
            'error': 'Failed to load dashboard',
            'details': str(e)
        }), 500


@app.route('/api/config', methods=['GET'])
def api_config():
    """API configuration and documentation endpoint"""
    return jsonify({
        'service': 'AMP Dashboard Backend API',
        'version': '1.0',
        'status': 'running',
        'endpoints': {
            '/health': 'Health check and connection status',
            '/api/amp-data': 'Get AMP data with optional filters',
            '/api/amp-metrics': 'Get summary metrics',
            '/api/amp-filters': 'Get filter options',
            '/api/generate-audio': 'Generate summarized MP4 audio (Jenny voice)'
        },
        'bigquery': {
            'project': PROJECT_ID,
            'dataset': DATASET_ID,
            'table': TABLE_ID
        },
        'credentials': {
            'type': 'Application Default Credentials (gcloud)',
            'location': '~/.config/gcloud/application_default_credentials.json'
        },
        'audio': {
            'available': MP4_PIPELINE_AVAILABLE,
            'voice': 'Jenny Neural (Primary)',
            'format': 'MP4 (AAC @ 256kbps)'
        }
    })



@app.route('/api/generate-audio', methods=['POST'])
def generate_summarized_audio():
    """
    Generate summarized MP4 audio from activity message using Jenny voice
    
    Request body:
    {
        "message_title": "Activity Title",
        "message_description": "Activity Description",
        "business_area": "Business Area",
        "activity_type": "Action Required | FYI | etc",
        "priority": "high | medium | low"
    }
    
    Returns:
    {
        "success": true/false,
        "audio_url": "/api/audio/<filename>",
        "filename": "summarized_audio_XXXXXXXX.mp4",
        "size_kb": 625.3,
        "duration_seconds": 48,
        "voice": "Jenny"
    }
    """
    try:
        if not MP4_PIPELINE_AVAILABLE:
            return jsonify({
                'success': False,
                'error': 'MP4 Pipeline not available'
            }), 503

        # Get request data
        data = request.get_json()
        
        message_title = data.get('message_title', 'Activity Update')
        message_description = data.get('message_description', 'New activity message')
        business_area = data.get('business_area', 'General')
        activity_type = data.get('activity_type', 'FYI')
        priority = data.get('priority', 'medium')
        
        # Build audio script
        priority_text = 'HIGH PRIORITY' if priority.lower() in ['high', '1'] else 'priority' if priority.lower() in ['medium', '2'] else 'informational'
        
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
        pipeline = MP4Pipeline()
        success, output_file = pipeline.synthesize(
            text=audio_script,
            voice=Voice.JENNY
        )
        
        if not success or not output_file:
            return jsonify({
                'success': False,
                'error': 'Failed to generate audio'
            }), 500
        
        # Get file info
        file_path = Path(output_file)
        file_size_kb = file_path.stat().st_size / 1024
        filename = file_path.name
        
        # Estimate duration (words per minute: ~140)
        word_count = len(audio_script.split())
        duration_seconds = int((word_count / 140) * 60)
        
        logger.info(f"✅ Audio generated: {filename} ({file_size_kb:.1f}KB)")
        
        return jsonify({
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
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/audio/<filename>', methods=['GET'])
def serve_audio(filename):
    """Serve MP4 audio file"""
    try:
        audio_dir = Path(__file__).parent.parent / "Zorro" / "Audio" / "mp4_output"
        file_path = audio_dir / filename
        
        # Security: ensure file is in mp4_output directory
        if not file_path.resolve().parent == audio_dir.resolve():
            return jsonify({'error': 'Invalid file path'}), 403
        
        if not file_path.exists():
            return jsonify({'error': 'Audio file not found'}), 404
        
        logger.info(f"Serving audio: {filename}")
        
        return send_file(
            file_path,
            mimetype='audio/mp4',
            as_attachment=True,
            download_name=filename
        )
        
    except Exception as e:
        logger.error(f"❌ Error serving audio: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == '__main__':
    port = int(os.getenv('PORT', 8081))
    logger.info(f"🚀 Starting AMP Dashboard Backend on http://localhost:{port}")
    logger.info(f"📊 BigQuery: {PROJECT_ID}.{DATASET_ID}.{TABLE_ID}")
    logger.info(f"🔐 Using gcloud application default credentials")
    logger.info(f"🎤 MP4 Audio Generation: {'✅ ENABLED (Jenny voice)' if MP4_PIPELINE_AVAILABLE else '⚠️  DISABLED'}")
    logger.info(f"📖 API docs: http://localhost:{port}/")
    logger.info(f"🎧 Audio endpoint: POST http://localhost:{port}/api/generate-audio")
    
    app.run(host='localhost', port=port, debug=False)
