"""
Code Puppy Pages API Endpoint (Python/Flask)
Queries BigQuery for distribution lists

Deploy this to Code Puppy Pages as: /api/distribution-lists
"""

from flask import Flask, jsonify, request
from google.cloud import bigquery
import logging

# Initialize Flask app
app = Flask(__name__)

# Initialize BigQuery client
bigquery_client = bigquery.Client(project='wmt-assetprotection-prod')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.route('/api/distribution-lists', methods=['GET'])
def get_distribution_lists():
    """
    GET /api/distribution-lists
    Returns all distribution lists from BigQuery
    """
    try:
        query = """
            SELECT 
                email,
                name,
                display_name,
                description,
                member_count,
                category
            FROM `wmt-assetprotection-prod.Store_Support_Dev.dl_catalog`
            ORDER BY name
        """
        
        logger.info('Executing BigQuery query...')
        query_job = bigquery_client.query(query)
        results = query_job.result()
        
        # Convert results to list of dictionaries
        rows = []
        for row in results:
            rows.append({
                'email': row.email,
                'name': row.name,
                'display_name': row.display_name,
                'description': row.description,
                'member_count': row.member_count,
                'category': row.category
            })
        
        logger.info(f'Retrieved {len(rows)} distribution lists')
        
        return jsonify(rows), 200
        
    except Exception as error:
        logger.error(f'Error querying BigQuery: {str(error)}')
        return jsonify({
            'error': 'Failed to load distribution lists',
            'message': str(error)
        }), 500


@app.route('/api/distribution-lists/search', methods=['GET'])
def search_distribution_lists():
    """
    GET /api/distribution-lists/search?q=searchTerm
    Search distribution lists by keyword
    """
    try:
        search_term = request.args.get('q', '')
        
        query = """
            SELECT 
                email,
                name,
                display_name,
                description,
                member_count,
                category
            FROM `wmt-assetprotection-prod.Store_Support_Dev.dl_catalog`
            WHERE LOWER(email) LIKE @search_term
               OR LOWER(name) LIKE @search_term
               OR LOWER(description) LIKE @search_term
            ORDER BY name
            LIMIT 100
        """
        
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("search_term", "STRING", f"%{search_term.lower()}%")
            ]
        )
        
        query_job = bigquery_client.query(query, job_config=job_config)
        results = query_job.result()
        
        rows = []
        for row in results:
            rows.append({
                'email': row.email,
                'name': row.name,
                'display_name': row.display_name,
                'description': row.description,
                'member_count': row.member_count,
                'category': row.category
            })
        
        return jsonify(rows), 200
        
    except Exception as error:
        logger.error(f'Error searching BigQuery: {str(error)}')
        return jsonify({
            'error': 'Failed to search distribution lists',
            'message': str(error)
        }), 500


@app.route('/api/distribution-lists/stats', methods=['GET'])
def get_distribution_list_stats():
    """
    GET /api/distribution-lists/stats
    Get statistics about distribution lists
    """
    try:
        query = """
            SELECT 
                category,
                COUNT(*) as count,
                SUM(member_count) as total_members,
                AVG(member_count) as avg_members
            FROM `wmt-assetprotection-prod.Store_Support_Dev.dl_catalog`
            GROUP BY category
            ORDER BY count DESC
        """
        
        query_job = bigquery_client.query(query)
        results = query_job.result()
        
        rows = []
        for row in results:
            rows.append({
                'category': row.category,
                'count': row['count'],
                'total_members': row.total_members,
                'avg_members': float(row.avg_members) if row.avg_members else 0
            })
        
        return jsonify(rows), 200
        
    except Exception as error:
        logger.error(f'Error querying BigQuery: {str(error)}')
        return jsonify({
            'error': 'Failed to load statistics',
            'message': str(error)
        }), 500


# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'distribution-lists-api'}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
