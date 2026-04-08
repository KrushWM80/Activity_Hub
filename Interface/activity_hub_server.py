"""
Activity Hub Server - Flask application serving all Activity Hub pages.
Port: 8088
URL: http://weus42608431466:8088/activity-hub/
"""

import os
import logging
import requests
from flask import Flask, send_from_directory, send_file, abort

# ──────────────────────────────────────────────
# Logging: metadata only (PCI compliance)
# Never log request bodies, file contents, or user-submitted text
# ──────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
# Suppress Werkzeug request body dumping in any mode
logging.getLogger('werkzeug').setLevel(logging.WARNING)

app = Flask(__name__)

# Base directory for all Interface files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STORE_SUPPORT_DIR = os.path.join(os.path.dirname(BASE_DIR), 'Store Support')

# ──────────────────────────────────────────────
# Routes
# ──────────────────────────────────────────────

@app.route('/activity-hub/')
@app.route('/activity-hub/for-you')
def for_you():
    """Main landing page / For You dashboard."""
    return send_file(os.path.join(BASE_DIR, 'For You - Landing Page', 'activity-hub-demo.html'))


@app.route('/activity-hub/projects')
def projects():
    """Projects management page."""
    return send_file(os.path.join(BASE_DIR, 'Projects', 'index.html'))


@app.route('/activity-hub/projects/upload')
def projects_upload():
    """Upload Projects page."""
    return send_file(os.path.join(BASE_DIR, 'Projects', 'Upload Projects', 'index.html'))


@app.route('/activity-hub/reporting')
def reporting():
    """Reporting page (coming soon)."""
    return _coming_soon('Reporting')


@app.route('/activity-hub/teams')
def teams():
    """Teams page (coming soon)."""
    return _coming_soon('Teams')


@app.route('/activity-hub/my-work')
def my_work():
    """My Work page (coming soon)."""
    return _coming_soon('My Work')


@app.route('/activity-hub/settings')
def settings():
    """Settings page (coming soon)."""
    return _coming_soon('Settings')


@app.route('/activity-hub/admin')
def admin():
    """Admin dashboard."""
    return send_file(os.path.join(BASE_DIR, 'Admin', 'admin-dashboard.html'))


# ──────────────────────────────────────────────
# Static file serving
# ──────────────────────────────────────────────

@app.route('/activity-hub/static/for-you/<path:filename>')
def static_for_you(filename):
    """CSS/JS/images for the For You landing page."""
    return send_from_directory(os.path.join(BASE_DIR, 'For You - Landing Page'), filename)


@app.route('/activity-hub/static/projects/<path:filename>')
def static_projects(filename):
    """CSS/JS for Projects pages."""
    return send_from_directory(os.path.join(BASE_DIR, 'Projects'), filename)


@app.route('/activity-hub/static/projects/upload/<path:filename>')
def static_projects_upload(filename):
    """Static assets for Upload Projects."""
    return send_from_directory(os.path.join(BASE_DIR, 'Projects', 'Upload Projects'), filename)


@app.route('/activity-hub/static/admin/<path:filename>')
def static_admin(filename):
    """CSS/JS/JSON for Admin dashboard."""
    return send_from_directory(os.path.join(BASE_DIR, 'Admin'), filename)


@app.route('/activity-hub/static/admin/Data-Bridge/<path:filename>')
def static_admin_data_bridge(filename):
    """Data-Bridge files under Admin."""
    return send_from_directory(os.path.join(BASE_DIR, 'Admin', 'Data-Bridge'), filename)


@app.route('/activity-hub/static/store-support/<path:filename>')
def static_store_support(filename):
    """Serve files from Store Support (e.g., Spark Blank.png logo)."""
    return send_from_directory(STORE_SUPPORT_DIR, filename)


# ──────────────────────────────────────────────
# Logic Rules Engine API Proxy Routes
# ──────────────────────────────────────────────

SCHEDULER_SERVICE_URL = 'http://localhost:5011'

@app.route('/api/logic/metrics')
def get_logic_metrics():
    """Proxy Logic Rules Engine metrics for dashboard display."""
    try:
        response = requests.get(f'{SCHEDULER_SERVICE_URL}/api/v1/logic-metrics', timeout=5)
        if response.status_code == 200:
            return response.json()
        return {'error': 'Service unavailable'}, 503
    except Exception as e:
        return {'error': str(e)}, 500

@app.route('/api/logic/notifications/today')
def get_notifications_today():
    """Proxy Logic Rules Engine notifications for today."""
    try:
        response = requests.get(f'{SCHEDULER_SERVICE_URL}/api/v1/notifications/today', timeout=5)
        if response.status_code == 200:
            return response.json()
        return {'error': 'Service unavailable'}, 503
    except Exception as e:
        return {'error': str(e)}, 500

@app.route('/api/logic/requests')
def get_logic_requests(status=None):
    """Proxy Logic Requests with optional status filter."""
    try:
        url = f'{SCHEDULER_SERVICE_URL}/api/v1/logic-requests'
        if status:
            url += f'?status={status}'
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.json()
        return {'error': 'Service unavailable'}, 503
    except Exception as e:
        return {'error': str(e)}, 500


# ──────────────────────────────────────────────
# Coming Soon Template
# ──────────────────────────────────────────────

def _coming_soon(page_name):
    """Generate a coming soon page matching Activity Hub styling."""
    nav_items = [
        ('For You', '/activity-hub/for-you', False),
        ('Projects', '/activity-hub/projects', False),
        ('Reporting', '/activity-hub/reporting', page_name == 'Reporting'),
        ('Teams', '/activity-hub/teams', page_name == 'Teams'),
        ('My Work', '/activity-hub/my-work', page_name == 'My Work'),
        ('Settings', '/activity-hub/settings', page_name == 'Settings'),
        ('🔒 Admin', '/activity-hub/admin', False),
    ]
    nav_html = '\n'.join(
        f'<a href="{url}" class="nav-item{" active" if active else ""}">{label}</a>'
        for label, url, active in nav_items
    )
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{page_name} - Activity Hub</title>
    <style>
        :root {{ --walmart-blue: #0071ce; --walmart-yellow: #ffc220; --gray-900: #111827; }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f8fafc; }}
        .header {{ background: linear-gradient(135deg, #0071ce, #004f9a); color: white; padding: 0 2rem; height: 64px; display: flex; align-items: center; }}
        .header-content {{ display: flex; align-items: center; justify-content: space-between; width: 100%; max-width: 1400px; margin: 0 auto; }}
        .logo-section {{ display: flex; align-items: center; gap: 12px; }}
        .spark-logo {{ width: 32px; height: 32px; object-fit: contain; }}
        .nav-items {{ display: flex; gap: 1.5rem; }}
        .nav-item {{ color: rgba(255,255,255,0.85); text-decoration: none; font-size: 0.9rem; padding: 0.5rem 0; }}
        .nav-item:hover {{ color: white; }}
        .nav-item.active {{ color: white; border-bottom: 2px solid var(--walmart-yellow); }}
        .coming-soon {{ display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: calc(100vh - 64px); text-align: center; padding: 2rem; }}
        .coming-soon h1 {{ font-size: 2.5rem; color: var(--gray-900); margin-bottom: 1rem; }}
        .coming-soon p {{ font-size: 1.1rem; color: #6b7280; max-width: 500px; }}
        .coming-soon .icon {{ font-size: 4rem; margin-bottom: 1.5rem; }}
    </style>
</head>
<body>
    <header class="header">
        <div class="header-content">
            <div class="logo-section">
                <img src="/activity-hub/static/store-support/General Setup/Design/Spark Blank.png" alt="Spark" class="spark-logo">
                <h1 style="font-size: 1.25rem;">Activity Hub</h1>
            </div>
            <nav class="nav-items">{nav_html}</nav>
        </div>
    </header>
    <div class="coming-soon">
        <div class="icon">🚧</div>
        <h1>{page_name}</h1>
        <p>This section is under development and will be available soon.</p>
    </div>
</body>
</html>''', 200


# ──────────────────────────────────────────────
# Redirect root
# ──────────────────────────────────────────────

@app.route('/')
def root_redirect():
    from flask import redirect
    return redirect('/activity-hub/')


# ──────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8088))
    print(f'Activity Hub starting on port {port}...')
    print(f'  Local:   http://localhost:{port}/activity-hub/')
    print(f'  Network: http://weus42608431466:{port}/activity-hub/')
    app.run(host='0.0.0.0', port=port, debug=False)
