#!/usr/bin/env python3
"""
ELM Manager Change Detection - Business Dashboard
Flask web application for tracking and visualizing manager changes and email metrics.

Run with: python dashboard.py
Access at: http://localhost:5000
"""

from flask import Flask, render_template, jsonify, request
from datetime import datetime, timedelta
import json
from pathlib import Path
from email_history_logger import EmailHistoryLogger, get_dashboard_metrics

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


# ============================================================================
# DASHBOARD ROUTES
# ============================================================================

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('dashboard.html')


@app.route('/api/metrics')
def api_metrics():
    """Get all dashboard metrics"""
    days = request.args.get('days', 30, type=int)
    metrics = get_dashboard_metrics(days)
    return jsonify(metrics)


@app.route('/api/metrics/summary')
def api_metrics_summary():
    """Get summary KPI cards"""
    days = request.args.get('days', 30, type=int)
    logger = EmailHistoryLogger()
    
    metrics = {
        'total_changes': logger.get_total_changes_detected(days),
        'total_emails': logger.get_total_emails_sent(days),
        'changes_by_role': logger.get_changes_by_role_type(days),
        'unique_dcs': len(logger.get_changes_by_dc(days)),
        'delivery_status': logger.get_email_delivery_confirmations(days),
        'time_period_days': days
    }
    
    return jsonify(metrics)


@app.route('/api/metrics/dc-territory')
def api_dc_territory():
    """Get changes by DC territory"""
    days = request.args.get('days', 30, type=int)
    logger = EmailHistoryLogger()
    
    dc_data = logger.get_changes_by_dc(days)
    
    # Sort by total changes descending
    dc_data_sorted = sorted(dc_data, key=lambda x: x['total_changes'], reverse=True)
    
    return jsonify(dc_data_sorted)


@app.route('/api/metrics/role-type')
def api_role_type():
    """Get changes by role type"""
    days = request.args.get('days', 30, type=int)
    logger = EmailHistoryLogger()
    
    role_data = logger.get_changes_by_role_type(days)
    
    # Format for chart
    formatted = [
        {'role': role, 'count': count}
        for role, count in sorted(role_data.items(), key=lambda x: x[1], reverse=True)
    ]
    
    return jsonify(formatted)


@app.route('/api/metrics/trend')
def api_trend():
    """Get daily trend data"""
    days = request.args.get('days', 30, type=int)
    logger = EmailHistoryLogger()
    
    trend_data = logger.get_daily_trend(days)
    
    return jsonify(trend_data)


@app.route('/api/metrics/delivery-status')
def api_delivery_status():
    """Get email delivery status"""
    days = request.args.get('days', 30, type=int)
    logger = EmailHistoryLogger()
    
    delivery_data = logger.get_email_delivery_confirmations(days)
    
    # Format for chart
    formatted = [
        {'status': status, 'count': count}
        for status, count in delivery_data.items()
    ]
    
    return jsonify(formatted)


@app.route('/api/metrics/dc/<int:dc_number>')
def api_dc_details(dc_number):
    """Get detailed metrics for specific DC"""
    days = request.args.get('days', 30, type=int)
    logger = EmailHistoryLogger()
    
    dc_detail = logger.get_dc_territory_details(dc_number, days)
    
    return jsonify(dc_detail)


@app.route('/api/health')
def api_health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'database': 'email_history.db'
    })


# ============================================================================
# TEMPLATE RENDERING
# ============================================================================

@app.context_processor
def inject_now():
    """Make datetime available in templates"""
    return {
        'now': datetime.now(),
        'today': datetime.now().strftime('%B %d, %Y'),
        'app_name': 'ELM Manager Change Dashboard'
    }


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500


# ============================================================================
# STARTUP
# ============================================================================

if __name__ == '__main__':
    print("\n" + "="*80)
    print("ELM MANAGER CHANGE DETECTION - DASHBOARD")
    print("="*80)
    print("\n✓ Starting Flask server...")
    print("✓ Access dashboard at: http://localhost:5000")
    print("✓ Stop with: Ctrl+C\n")
    print("="*80 + "\n")
    
    app.run(debug=True, host='localhost', port=5000, use_reloader=False)
