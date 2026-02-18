"""
Admin Dashboard - Flask application for viewing activity logs and feedback
Part of the Manager Change Tracking System
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
from datetime import datetime, timedelta
import json
from pathlib import Path
from feedback_handler import FeedbackHandler
from dc_to_stores_config import DCStoreManagerConfig

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Initialize handlers
feedback_handler = FeedbackHandler()
store_config = DCStoreManagerConfig()

# ==================== ADMIN DASHBOARD ROUTES ====================

@app.route('/admin')
@app.route('/admin/dashboard')
def admin_dashboard():
    """Main admin dashboard showing activity overview"""
    
    # Get stats
    stats = feedback_handler.get_feedback_stats()
    
    # Get recent activity
    recent_activity = feedback_handler.get_activity_log(limit=20)
    
    # Get recent feedback
    recent_feedback = feedback_handler.get_all_feedback(limit=10)
    
    # Calculate metrics
    pending_feedback = len([f for f in recent_feedback if f['status'] == 'new'])
    avg_rating = stats['average_rating']
    
    return render_template('admin_dashboard.html',
        total_feedback=stats['total_feedback'],
        pending_feedback=pending_feedback,
        average_rating=avg_rating,
        status_breakdown=stats['status_breakdown'],
        category_breakdown=stats['category_breakdown'],
        recent_activity=recent_activity,
        recent_feedback=recent_feedback
    )

@app.route('/admin/feedback')
def admin_feedback_list():
    """View all feedback submissions"""
    
    # Get filter parameters
    status = request.args.get('status', None)
    dc = request.args.get('dc', None)
    page = request.args.get('page', 1, type=int)
    
    # Get feedback
    all_feedback = feedback_handler.get_all_feedback(
        status_filter=status,
        dc_filter=dc,
        limit=100
    )
    
    # Pagination
    per_page = 20
    total_pages = (len(all_feedback) + per_page - 1) // per_page
    start = (page - 1) * per_page
    end = start + per_page
    paginated_feedback = all_feedback[start:end]
    
    stats = feedback_handler.get_feedback_stats()
    
    return render_template('admin_feedback_list.html',
        feedback=paginated_feedback,
        current_page=page,
        total_pages=total_pages,
        total_feedback=stats['total_feedback'],
        status_breakdown=stats['status_breakdown'],
        status_filter=status,
        dc_filter=dc
    )

@app.route('/admin/feedback/<int:feedback_id>')
def admin_feedback_detail(feedback_id):
    """View detailed feedback and activity"""
    
    feedback = feedback_handler.get_feedback(feedback_id)
    if not feedback:
        return "Feedback not found", 404
    
    activity = feedback_handler.get_activity_log(feedback_id=feedback_id)
    
    return render_template('admin_feedback_detail.html',
        feedback=feedback,
        activity=activity
    )

@app.route('/admin/feedback/<int:feedback_id>/update', methods=['POST'])
def admin_update_feedback(feedback_id):
    """Update feedback status and notes"""
    
    new_status = request.form.get('status')
    admin_notes = request.form.get('notes')
    admin_user = request.form.get('admin_user', 'Unknown Admin')
    
    feedback_handler.update_feedback_status(
        feedback_id,
        new_status,
        admin_user,
        admin_notes
    )
    
    return redirect(url_for('admin_feedback_detail', feedback_id=feedback_id))

@app.route('/admin/activity')
def admin_activity_log():
    """View complete activity log"""
    
    page = request.args.get('page', 1, type=int)
    event_type = request.args.get('event_type', None)
    
    # Get activity
    activity = feedback_handler.get_activity_log(limit=500)
    
    # Filter by event type if specified
    if event_type:
        activity = [a for a in activity if a['event_type'] == event_type]
    
    # Pagination
    per_page = 50
    total_pages = (len(activity) + per_page - 1) // per_page
    start = (page - 1) * per_page
    end = start + per_page
    paginated_activity = activity[start:end]
    
    # Get unique event types for filter
    all_activity = feedback_handler.get_activity_log(limit=1000)
    event_types = list(set(a['event_type'] for a in all_activity))
    
    return render_template('admin_activity_log.html',
        activity=paginated_activity,
        current_page=page,
        total_pages=total_pages,
        event_types=event_types,
        selected_event_type=event_type
    )

@app.route('/admin/stats')
def admin_stats():
    """View feedback statistics and trends"""
    
    stats = feedback_handler.get_feedback_stats()
    
    # Get all feedback for trend analysis
    all_feedback = feedback_handler.get_all_feedback(limit=500)
    
    # Calculate trends
    today = datetime.now().date()
    last_7_days = sum(1 for f in all_feedback 
                     if datetime.fromisoformat(f['timestamp']).date() >= today - timedelta(days=7))
    last_30_days = sum(1 for f in all_feedback 
                      if datetime.fromisoformat(f['timestamp']).date() >= today - timedelta(days=30))
    
    return render_template('admin_stats.html',
        stats=stats,
        feedback_7d=last_7_days,
        feedback_30d=last_30_days,
        total_feedback=stats['total_feedback']
    )

# ==================== STORE MANAGER DIRECTORY ROUTES ====================

@app.route('/store-manager-directory')
def store_manager_directory():
    """Public directory for DCs to find their store managers"""
    
    # Try to get DC from email in query parameter
    user_email = request.args.get('email', '')
    user_dc = None
    managers = []
    
    if user_email:
        user_dc = feedback_handler.parse_user_email(user_email)
        if user_dc:
            managers = store_config.get_managers_for_dc(user_dc)
    
    return render_template('store_manager_directory.html',
        user_email=user_email,
        user_dc=user_dc,
        managers=managers,
        all_dcs=store_config.get_all_dcs()
    )

@app.route('/api/store-managers/<dc_number>')
def api_get_store_managers(dc_number):
    """API endpoint to get store managers for a DC"""
    
    managers = store_config.get_managers_for_dc(dc_number)
    
    return jsonify({
        "dc": dc_number,
        "managers": managers,
        "total": len(managers)
    })

@app.route('/api/all-dcs')
def api_get_all_dcs():
    """API endpoint to get all DCs"""
    
    dcs = store_config.get_all_dcs()
    
    return jsonify({
        "dcs": dcs,
        "total": len(dcs)
    })

# ==================== FEEDBACK SUBMISSION ROUTES ====================

@app.route('/api/submit-feedback', methods=['POST'])
def api_submit_feedback():
    """API endpoint for feedback submission from email"""
    
    data = request.json
    
    result = feedback_handler.submit_feedback(
        user_email=data.get('user_email'),
        feedback_category=data.get('category'),
        rating=data.get('rating'),
        message=data.get('message'),
        submitted_via=data.get('via', 'web')
    )
    
    return jsonify(result)

@app.route('/feedback/success')
def feedback_success():
    """Thank you page after feedback submission"""
    return render_template('feedback_success.html')

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', 
        error_code=404,
        error_message="Page not found"
    ), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('error.html',
        error_code=500,
        error_message="Internal server error"
    ), 500

# ==================== UTILITIES ====================

@app.context_processor
def inject_now():
    """Make datetime available in templates"""
    return {'now': datetime.now()}

if __name__ == '__main__':
    app.run(
        host='localhost',
        port=5000,
        debug=True
    )
