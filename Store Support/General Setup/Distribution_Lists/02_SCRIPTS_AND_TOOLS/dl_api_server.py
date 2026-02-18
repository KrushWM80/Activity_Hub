#!/usr/bin/env python3
"""
Simple Flask API to serve DL catalog data
Serves the latest CSV file to the DL Selector UI
"""

from flask import Flask, jsonify, send_file
from flask_cors import CORS
import csv
import glob
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for browser access

# Configuration
CSV_PATTERN = "all_distribution_lists_*.csv"


def get_latest_csv():
    """Get the most recent DL catalog CSV file"""
    files = glob.glob(CSV_PATTERN)
    if not files:
        return None
    return max(files, key=os.path.getctime)


@app.route('/api/distribution-lists', methods=['GET'])
def get_distribution_lists():
    """
    Get all distribution lists
    Returns JSON array of DL objects
    """
    
    csv_file = get_latest_csv()
    
    if not csv_file:
        return jsonify({
            'error': 'No distribution list data available',
            'message': 'Run extract_all_dls_optimized.py first'
        }), 404
    
    try:
        dls = []
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                dls.append({
                    'email': row['email'],
                    'name': row['name'],
                    'displayName': row.get('displayName', ''),
                    'description': row.get('description', ''),
                    'memberCount': int(row.get('memberCount', 0)),
                    'category': row.get('category', 'General')
                })
        
        return jsonify({
            'total': len(dls),
            'updated': datetime.fromtimestamp(os.path.getctime(csv_file)).isoformat(),
            'data': dls
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get statistics about DL catalog"""
    
    csv_file = get_latest_csv()
    
    if not csv_file:
        return jsonify({'error': 'No data available'}), 404
    
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            dls = list(reader)
        
        # Calculate stats
        total = len(dls)
        total_members = sum(int(row.get('memberCount', 0)) for row in dls)
        
        categories = {}
        sizes = {'small': 0, 'medium': 0, 'large': 0}
        
        for dl in dls:
            cat = dl.get('category', 'General')
            categories[cat] = categories.get(cat, 0) + 1
            
            count = int(dl.get('memberCount', 0))
            if count < 50:
                sizes['small'] += 1
            elif count < 500:
                sizes['medium'] += 1
            else:
                sizes['large'] += 1
        
        return jsonify({
            'total': total,
            'totalMembers': total_members,
            'avgMembers': total_members // total if total > 0 else 0,
            'categories': categories,
            'sizes': sizes,
            'lastUpdated': datetime.fromtimestamp(os.path.getctime(csv_file)).isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/search', methods=['GET'])
def search_dls():
    """Search distribution lists by keyword"""
    from flask import request
    
    query = request.args.get('q', '').lower()
    category = request.args.get('category', '')
    size = request.args.get('size', '')
    
    if not query and not category and not size:
        return get_distribution_lists()
    
    csv_file = get_latest_csv()
    if not csv_file:
        return jsonify({'error': 'No data available'}), 404
    
    try:
        results = []
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Apply filters
                if query:
                    if not (query in row['name'].lower() or 
                           query in row['email'].lower() or
                           query in row.get('description', '').lower()):
                        continue
                
                if category and row.get('category') != category:
                    continue
                
                if size:
                    count = int(row.get('memberCount', 0))
                    if size == 'small' and count >= 50:
                        continue
                    elif size == 'medium' and (count < 50 or count >= 500):
                        continue
                    elif size == 'large' and count < 500:
                        continue
                
                results.append({
                    'email': row['email'],
                    'name': row['name'],
                    'displayName': row.get('displayName', ''),
                    'description': row.get('description', ''),
                    'memberCount': int(row.get('memberCount', 0)),
                    'category': row.get('category', 'General')
                })
        
        return jsonify({
            'total': len(results),
            'data': results
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/')
def index():
    """Serve the DL Selector UI"""
    return send_file('dl_selector.html')


if __name__ == '__main__':
    print("\n" + "="*70)
    print("  Distribution List Selector API")
    print("="*70)
    print("\n  Starting server...")
    print(f"  UI: http://localhost:5000")
    print(f"  API: http://localhost:5000/api/distribution-lists")
    print("\n  Press Ctrl+C to stop")
    print("="*70 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
