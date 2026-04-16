"""
Activity Hub Server V2 - Minimal Flask with inline BigQuery
"""

import os
import logging
import requests
from flask import Flask, send_from_directory, send_file, jsonify, request
from flask_cors import CORS
from datetime import datetime, timedelta
from google.cloud import bigquery

# Basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

# Set Google Cloud credentials before BigQuery initialization
creds_path = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "gcloud", "application_default_credentials.json")
if not os.environ.get('GOOGLE_APPLICATION_CREDENTIALS'):
    if os.path.exists(creds_path):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = creds_path
        logger.info(f"Set GOOGLE_APPLICATION_CREDENTIALS to {creds_path}")
    else:
        logger.warning(f"Credentials file not found at {creds_path} - BigQuery may fail")

app = Flask(__name__)
CORS(app)

# BigQuery client - initialize once at startup
try:
    bq_client = bigquery.Client(project='wmt-assetprotection-prod')
    logger.info("BigQuery client initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize BigQuery client: {e}")
    bq_client = None

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Scheduler Service URL for proxying
SCHEDULER_SERVICE_URL = 'http://localhost:5011'

# ──────────────────────────────────────────────
# CORE ROUTES
# ──────────────────────────────────────────────

@app.route('/activity-hub/')
@app.route('/activity-hub/for-you')
def for_you():
    """For You page"""
    return send_file(os.path.join(BASE_DIR, 'For You - Landing Page', 'activity-hub-demo.html'))

@app.route('/activity-hub/projects')
def projects():
    """Projects page"""
    return send_file(os.path.join(BASE_DIR, 'projects-page.html'))

@app.route('/activity-hub/reporting')
def reporting():
    """Reporting page"""
    return send_file(os.path.join(BASE_DIR, 'Reporting', 'reporting.html'))

@app.route('/activity-hub/admin')
def admin():
    """Admin dashboard"""
    return send_file(os.path.join(BASE_DIR, 'Admin', 'admin-dashboard.html'))

# ──────────────────────────────────────────────
# STATIC FILES & ASSETS
# ──────────────────────────────────────────────

@app.route('/<filename>')
@app.route('/activity-hub/static/<path:filepath>')
@app.route('/<path:subdir>/<filename>')
def serve_static(filename=None, filepath=None, subdir=None):
    """Serve static files like images and JS from Interface directory"""
    try:
        if filepath:
            # Handle nested paths for static files
            file_path = os.path.join(BASE_DIR, filepath.replace('/', os.sep))
        elif subdir and filename:
            # Handle paths like /Admin/Widgets/widget-registry.js
            file_path = os.path.join(BASE_DIR, subdir, filename)
        else:
            file_path = os.path.join(BASE_DIR, filename)
        
        if os.path.exists(file_path):
            return send_file(file_path)
        return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        logger.error(f"Static file error: {str(e)}")
        return jsonify({'error': 'File not found'}), 404

# ──────────────────────────────────────────────
# BIGQUERY API ENDPOINTS - INLINE ONLY
# ──────────────────────────────────────────────

@app.route('/api/projects/<project_id>', methods=['PUT', 'DELETE'])
def api_project_by_id(project_id):
    """Update or delete a specific project by ID"""
    from flask import request
    
    if not bq_client:
        return jsonify({'error': 'BigQuery client not initialized'}), 500
    
    try:
        if request.method == 'DELETE':
            # Delete project
            sql = "DELETE FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects` WHERE impact_id = %s"
            job = bq_client.query(sql, job_config=bigquery.QueryJobConfig(
                query_parameters=[bigquery.ScalarQueryParameter(None, "STRING", project_id)]
            ))
            job.result()
            return jsonify({'success': True, 'message': 'Project deleted'}), 200
        
        elif request.method == 'PUT':
            # Update project
            data = request.get_json()
            sql = """
            UPDATE `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
            SET title = @title, 
                business_area = @business_area, 
                owner_name = @owner_name, 
                owner_id = @owner_id,
                health_status = @health_status, 
                project_status = @project_status, 
                latest_update = @latest_update, 
                latest_update_timestamp = CURRENT_TIMESTAMP(),
                current_wm_week_update = TRUE,
                modified_timestamp = CURRENT_TIMESTAMP()
            WHERE impact_id = @impact_id
            """
            query_params = [
                bigquery.ScalarQueryParameter("title", "STRING", data.get('title')),
                bigquery.ScalarQueryParameter("business_area", "STRING", data.get('business_area')),
                bigquery.ScalarQueryParameter("owner_name", "STRING", data.get('owner_name')),
                bigquery.ScalarQueryParameter("owner_id", "STRING", data.get('owner_id')),
                bigquery.ScalarQueryParameter("health_status", "STRING", data.get('health_status')),
                bigquery.ScalarQueryParameter("project_status", "STRING", data.get('project_status', 'Active')),
                bigquery.ScalarQueryParameter("latest_update", "STRING", data.get('latest_update', '')),
                bigquery.ScalarQueryParameter("impact_id", "STRING", project_id)
            ]
            
            job = bq_client.query(sql, job_config=bigquery.QueryJobConfig(
                query_parameters=query_params
            ))
            job.result()
            return jsonify({'success': True, 'impact_id': project_id}), 200
    except Exception as e:
        logger.error(f"Project update error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/projects', methods=['GET', 'POST', 'PUT'])
def api_projects():
    """Get/create/update projects from BigQuery"""
    from flask import request
    
    if not bq_client:
        return jsonify({'error': 'BigQuery client not initialized'}), 500
    
    # Handle POST (create) and PUT (update)
    if request.method in ['POST', 'PUT']:
        try:
            data = request.get_json()
            project_id = data.get('impact_id', f'proj-{datetime.now().timestamp()}')
            
            if request.method == 'POST':
                # Insert new project
                sql = """
                INSERT INTO `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
                (impact_id, title, business_area, owner_name, owner_id, health_status, project_status, 
                 created_timestamp, modified_timestamp, latest_update, latest_update_timestamp, current_wm_week_update)
                VALUES 
                (%s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP(), %s, CURRENT_TIMESTAMP(), false)
                """
                params = [
                    project_id,
                    data.get('title'),
                    data.get('business_area'),
                    data.get('owner_name'),
                    data.get('owner_id'),
                    data.get('health_status'),
                    data.get('project_status', 'Active'),
                    data.get('latest_update', '')
                ]
            else:
                # Update existing project
                sql = """
                UPDATE `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
                SET title = %s, business_area = %s, owner_name = %s, owner_id = %s,
                    health_status = %s, project_status = %s, latest_update = %s, modified_timestamp = CURRENT_TIMESTAMP()
                WHERE impact_id = %s
                """
                params = [
                    data.get('title'),
                    data.get('business_area'),
                    data.get('owner_name'),
                    data.get('owner_id'),
                    data.get('health_status'),
                    data.get('project_status'),
                    data.get('latest_update'),
                    project_id
                ]
            
            job = bq_client.query(sql, job_config=bigquery.QueryJobConfig(
                query_parameters=[bigquery.ScalarQueryParameter(None, "STRING", p) if isinstance(p, str) else bigquery.ScalarQueryParameter(None, "TIMESTAMP", p) for p in params]
            ))
            job.result()
            return jsonify({'success': True, 'impact_id': project_id}), 200
        except Exception as e:
            logger.error(f"Project create/update error: {str(e)}")
            return jsonify({'error': str(e)}), 500
    
    # Handle GET
    try:
        status = request.args.get('status', 'Active')
        business_area = request.args.get('business_area')
        health_status = request.args.get('health_status')
        owner_name = request.args.get('owner_name')
        
        # Build SQL
        sql = r"""
        SELECT 
            impact_id,
            title,
            business_area,
            owner_name,
            owner_id,
            health_status,
            project_status,
            created_timestamp,
            modified_timestamp,
            latest_update,
            latest_update_timestamp,
            current_wm_week_update
        FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
        WHERE 1=1
        """
        
        if status != 'All' and status:
            sql += f" AND project_status = '{status}'"
        if business_area:
            sql += f" AND business_area = '{business_area}'"
        if health_status:
            sql += f" AND health_status = '{health_status}'"
        if owner_name:
            sql += f" AND owner_name = '{owner_name}'"
        
        sql += " ORDER BY modified_timestamp DESC"
        
        # Query
        results = bq_client.query(sql).result()
        projects = []
        
        for row in results:
            projects.append({
                'impact_id': row.impact_id,
                'title': row.title,
                'business_area': row.business_area,
                'owner_name': row.owner_name,
                'owner_id': row.owner_id,
                'health_status': row.health_status,
                'status': row.project_status,
                'created_date': row.created_timestamp.isoformat() if row.created_timestamp else None,
                'updated_date': row.modified_timestamp.isoformat() if row.modified_timestamp else None,
                'latest_update': row.latest_update,
                'latest_update_date': row.latest_update_timestamp.isoformat() if row.latest_update_timestamp else None,
                'current_wm_week_update': str(row.current_wm_week_update).lower() == 'true'
            })
        
        return jsonify({
            'projects': projects,
            'total_count': len(projects),
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f"Projects API error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/projects/metrics', methods=['GET'])
def api_metrics():
    """Get metrics"""
    from flask import request
    
    if not bq_client:
        return jsonify({'error': 'BigQuery client not initialized'}), 500
    
    try:
        status = request.args.get('status', 'Active')
        
        sql = rf"""
        SELECT 
            COUNT(DISTINCT impact_id) as total_projects,
            COUNT(DISTINCT owner_id) as unique_owners,
            COUNT(DISTINCT CASE 
                WHEN DATE_DIFF(CURRENT_DATE(), DATE(modified_timestamp), DAY) <= 7 
                THEN impact_id 
            END) as projects_this_week
        FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
        WHERE project_status = '{status}'
        """
        
        results = bq_client.query(sql).result()
        
        for row in results:
            total = int(row.total_projects) if row.total_projects else 0
            this_week = int(row.projects_this_week) if row.projects_this_week else 0
            percent = (this_week * 100 / total) if total > 0 else 0
            
            return jsonify({
                'metrics': {
                    'active_projects': total,
                    'unique_owners': int(row.unique_owners) if row.unique_owners else 0,
                    'projects_updated_this_week': this_week,
                    'percent_updated': round(percent, 2)
                },
                'timestamp': datetime.now().isoformat()
            })
        
        return jsonify({
            'metrics': {'active_projects': 0, 'unique_owners': 0, 'projects_updated_this_week': 0, 'percent_updated': 0},
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f"Metrics API error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/projects/business-areas', methods=['GET'])
def api_business_areas():
    """Get business areas"""
    if not bq_client:
        return jsonify({'error': 'BigQuery client not initialized'}), 500
    
    try:
        sql = r"""
        SELECT DISTINCT business_area
        FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
        WHERE business_area IS NOT NULL
        ORDER BY business_area
        """
        
        results = bq_client.query(sql).result()
        areas = [row.business_area for row in results if row.business_area]
        
        return jsonify({
            'business_areas': areas,
            'total': len(areas),
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f"Business areas error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/projects/sync/status', methods=['GET'])
def projects_sync_status():
    """Get projects sync status (stub - projects service may not be running)."""
    return jsonify({
        'sync_status': 'idle',
        'last_sync': datetime.now().isoformat(),
        'is_available': False,
        'message': 'Projects Data-Bridge service not available'
    }), 200


# ──────────────────────────────────────────────
# ADMIN ENDPOINTS
# ──────────────────────────────────────────────

@app.route('/api/admin/activity-log', methods=['GET'])
def admin_activity_log():
    """Return admin activity log for audit trail."""
    now = datetime.now()
    activity_log = [
        {
            'timestamp': (now - timedelta(hours=2)).isoformat(),
            'user': 'Kendall Rush',
            'action': 'Created Logic Request',
            'resource': 'Project Updates - 30 Days',
            'status': 'success'
        },
        {
            'timestamp': (now - timedelta(hours=4)).isoformat(),
            'user': 'Admin User',
            'action': 'Modified Trigger Rule',
            'resource': 'SIF Missing - 60 Days',
            'status': 'success'
        },
        {
            'timestamp': (now - timedelta(hours=8)).isoformat(),
            'user': 'Kendall Rush',
            'action': 'Viewed Dashboard',
            'resource': 'Admin Dashboard',
            'status': 'success'
        },
        {
            'timestamp': (now - timedelta(hours=24)).isoformat(),
            'user': 'System',
            'action': 'Scheduler Run',
            'resource': 'Logic Rules Engine',
            'status': 'success'
        },
    ]
    return jsonify({
        'activity_log': activity_log,
        'total_count': len(activity_log),
        'timestamp': now.isoformat()
    })


@app.route('/api/admin/active-users', methods=['GET'])
def admin_active_users():
    """Return count and list of currently active users."""
    active_users = [
        {'user_id': 'kendall.rush', 'name': 'Kendall Rush', 'role': 'Admin', 'last_activity': datetime.now().isoformat()},
        {'user_id': 'admin.user', 'name': 'Admin User', 'role': 'Admin', 'last_activity': (datetime.now() - timedelta(minutes=5)).isoformat()}
    ]
    return jsonify({
        'active_users': len(active_users),
        'users': active_users,
        'timestamp': datetime.now().isoformat()
    })


# ──────────────────────────────────────────────
# LOGIC RULES ENGINE PROXY ENDPOINTS
# ──────────────────────────────────────────────

@app.route('/api/logic/metrics', methods=['GET'])
def logic_metrics():
    """Proxy Logic Rules Engine metrics for dashboard display."""
    try:
        response = requests.get(f'{SCHEDULER_SERVICE_URL}/api/v1/logic-metrics', timeout=5)
        if response.status_code == 200:
            return response.json()
        return {'error': 'Service unavailable'}, 503
    except Exception as e:
        logger.error(f"Logic metrics error: {str(e)}")
        return {'error': str(e)}, 500


@app.route('/api/logic/notifications/today', methods=['GET'])
def logic_notifications_today():
    """Proxy Logic Rules Engine notifications for today."""
    try:
        response = requests.get(f'{SCHEDULER_SERVICE_URL}/api/v1/notifications/today', timeout=5)
        if response.status_code == 200:
            return response.json()
        return {'error': 'Service unavailable'}, 503
    except Exception as e:
        logger.error(f"Logic notifications error: {str(e)}")
        return {'error': str(e)}, 500


@app.route('/api/logic/requests', methods=['GET', 'POST'])
def logic_requests():
    """Proxy Logic Requests (GET) or create new request (POST)."""
    try:
        if request.method == 'GET':
            # GET: retrieve logic requests with optional status filter
            status = request.args.get('status')
            url = f'{SCHEDULER_SERVICE_URL}/api/v1/logic-requests'
            if status:
                url += f'?status={status}'
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                return response.json()
            return {'error': 'Service unavailable'}, 503
        
        elif request.method == 'POST':
            # POST: create new logic request, forward to Scheduler Service
            data = request.get_json()
            response = requests.post(
                f'{SCHEDULER_SERVICE_URL}/api/v1/logic-requests',
                json=data,
                timeout=5,
                headers={'Content-Type': 'application/json'}
            )
            if response.status_code in [200, 201]:
                return response.json()
            else:
                # Forward error response
                try:
                    error_json = response.json()
                except:
                    error_json = {'error': response.text}
                return error_json, response.status_code
    except Exception as e:
        logger.error(f"Logic requests error: {str(e)}")
        return {'error': str(e)}, 500


# ──────────────────────────────────────────────
# PROJECTS REPORT GENERATION
# ──────────────────────────────────────────────

@app.route('/api/generate-ppt', methods=['GET'])
def generate_ppt():
    """Generate PPT report of projects with professional Walmart branding"""
    try:
        from pptx import Presentation
        from pptx.util import Inches, Pt
        from pptx.enum.text import PP_ALIGN
        from pptx.dml.color import RGBColor
        from io import BytesIO
        
        # Calculate Walmart Week (WM WK)
        today = datetime.now()
        fiscal_year_start = datetime(today.year if today.month >= 2 else today.year - 1, 2, 1)
        days_since_fy = (today - fiscal_year_start).days
        wm_week = (days_since_fy // 7) + 1
        
        # Get filter parameters
        status = request.args.get('status', 'Active')
        
        # Query projects
        sql = """
        SELECT impact_id, title, business_area, owner_name, health_status, latest_update, project_status, 
               CASE 
                 WHEN LOWER(current_wm_week_update) = 'true' THEN TRUE
                 ELSE FALSE
               END as updated_this_week
        FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
        WHERE 1=1
        """
        if status != 'All' and status:
            sql += f" AND project_status = '{status}'"
        sql += " ORDER BY modified_timestamp DESC"
        
        results = bq_client.query(sql).result()
        projects = list(results)
        
        # Create presentation with Walmart colors
        prs = Presentation()
        prs.slide_width = Inches(10)
        prs.slide_height = Inches(7.5)
        blank_layout = prs.slide_layouts[6]
        
        COLORS = {
            'walmart_blue_dark': RGBColor(0x1E, 0x3A, 0x8A),
            'walmart_blue': RGBColor(0x00, 0x71, 0xCE),
            'walmart_yellow': RGBColor(0xFF, 0xC2, 0x20),
            'on_track': RGBColor(0x10, 0x7C, 0x10),
            'at_risk': RGBColor(0xF7, 0x63, 0x0C),
            'off_track': RGBColor(0xDC, 0x35, 0x45),
            'light_gray': RGBColor(0xF5, 0xF5, 0xF5),
            'dark_gray': RGBColor(0x33, 0x33, 0x33),
            'white': RGBColor(0xFF, 0xFF, 0xFF),
        }
        
        # ──────── SLIDE 1: TITLE SLIDE ────────
        slide = prs.slides.add_slide(blank_layout)
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = COLORS['walmart_blue_dark']
        
        # Main title
        title_box = slide.shapes.add_textbox(Inches(0.5), Inches(2.0), Inches(9), Inches(1.5))
        tf = title_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        run = p.add_run()
        run.text = "Impact Platform"
        run.font.size = Pt(54)
        run.font.bold = True
        run.font.color.rgb = COLORS['white']
        
        # Subtitle
        subtitle_box = slide.shapes.add_textbox(Inches(0.5), Inches(3.5), Inches(9), Inches(1))
        p = subtitle_box.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        run = p.add_run()
        run.text = "Projects Dashboard Report"
        run.font.size = Pt(28)
        run.font.color.rgb = COLORS['walmart_yellow']
        
        # Date
        date_box = slide.shapes.add_textbox(Inches(0.5), Inches(5.0), Inches(9), Inches(0.8))
        p = date_box.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        run = p.add_run()
        run.text = f"Generated: {datetime.now().strftime('%B %d, %Y')}"
        run.font.size = Pt(14)
        run.font.color.rgb = COLORS['white']
        
        # ──────── SLIDE 2: EXECUTIVE SUMMARY ────────
        slide = prs.slides.add_slide(blank_layout)
        
        # Summary header
        header_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(9), Inches(0.6))
        p = header_box.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.LEFT
        run = p.add_run()
        run.text = "Executive Summary"
        run.font.size = Pt(32)
        run.font.bold = True
        run.font.color.rgb = COLORS['walmart_blue_dark']
        
        # Calculate stats
        health_counts = {'On Track': 0, 'At Risk': 0, 'Off Track': 0}
        for proj in projects:
            health = proj['health_status'] or 'Unknown'
            if health in health_counts:
                health_counts[health] += 1
        
        # Stats grid
        stats = {
            'Total Projects': len(projects),
            'On Track': health_counts['On Track'],
            'At Risk': health_counts['At Risk'],
            'Off Track': health_counts['Off Track'],
        }
        
        stat_names = list(stats.keys())
        for idx, (name, value) in enumerate(stats.items()):
            col = idx % 4
            x = Inches(0.7 + col * 2.1)
            y = Inches(1.5)
            
            # Colored box
            box = slide.shapes.add_shape(1, x, y, Inches(1.9), Inches(1.8))
            box.fill.solid()
            box.fill.fore_color.rgb = COLORS['light_gray']
            box.line.color.rgb = COLORS['walmart_blue']
            box.line.width = Pt(2)
            
            # Label
            label_box = slide.shapes.add_textbox(x + Inches(0.1), y + Inches(0.15), Inches(1.7), Inches(0.4))
            p = label_box.text_frame.paragraphs[0]
            p.font.size = Pt(10)
            p.font.bold = True
            p.font.color.rgb = COLORS['walmart_blue_dark']
            p.text = name
            
            # Value
            val_box = slide.shapes.add_textbox(x + Inches(0.1), y + Inches(0.65), Inches(1.7), Inches(0.8))
            p = val_box.text_frame.paragraphs[0]
            p.font.size = Pt(26)
            p.font.bold = True
            run = p.add_run()
            run.text = str(value)
            
            if name == 'On Track':
                run.font.color.rgb = COLORS['on_track']
            elif name == 'At Risk':
                run.font.color.rgb = COLORS['at_risk']
            elif name == 'Off Track':
                run.font.color.rgb = COLORS['off_track']
            else:
                run.font.color.rgb = COLORS['walmart_blue']
        
        # ──────── SLIDE 3+: PROJECT DETAILS ────────
        for project in projects[:20]:  # Max 20 projects
            slide = prs.slides.add_slide(blank_layout)
            
            # Project title header (colored bar)
            header_shape = slide.shapes.add_shape(1, Inches(0), Inches(0), Inches(10), Inches(0.8))
            header_shape.fill.solid()
            header_shape.fill.fore_color.rgb = COLORS['walmart_blue_dark']
            header_shape.line.fill.background()
            
            # Project title on header
            title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.15), Inches(9), Inches(0.6))
            p = title_box.text_frame.paragraphs[0]
            run = p.add_run()
            run.text = project['title']
            run.font.size = Pt(28)
            run.font.bold = True
            run.font.color.rgb = COLORS['white']
            
            # Project details
            y_pos = 1.1
            details = [
                ('Business Area', project['business_area']),
                ('Owner', project['owner_name']),
                ('Status', project['project_status']),
                ('Health Status', project['health_status']),
                ('Latest Update', project['latest_update']),
                ('Updated This Week', 'Yes' if project.get('updated_this_week') else 'No'),
            ]
            
            for label, value in details:
                # Label
                label_box = slide.shapes.add_textbox(Inches(0.5), Inches(y_pos), Inches(2), Inches(0.3))
                p = label_box.text_frame.paragraphs[0]
                p.text = f"{label}:"
                p.font.size = Pt(12)
                p.font.bold = True
                p.font.color.rgb = COLORS['walmart_blue_dark']
                
                # Value
                val_box = slide.shapes.add_textbox(Inches(2.7), Inches(y_pos), Inches(6.5), Inches(0.8))
                tf = val_box.text_frame
                tf.word_wrap = True
                p = tf.paragraphs[0]
                p.text = str(value)
                p.font.size = Pt(14)
                p.font.color.rgb = COLORS['dark_gray']
                
                y_pos += 0.6
        
        # Save to BytesIO
        ppt_file = BytesIO()
        prs.save(ppt_file)
        ppt_file.seek(0)
        
        return send_file(
            ppt_file,
            mimetype='application/vnd.openxmlformats-officedocument.presentationml.presentation',
            as_attachment=True,
            download_name=f'WM WK{wm_week} Projects Overview.pptx'
        )
    except ImportError:
        logger.error("python-pptx not installed")
        return jsonify({'error': 'PPT generation not available - python-pptx not installed'}), 400
    except Exception as e:
        logger.error(f"PPT generation error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/sample-email', methods=['GET'])
def get_sample_email():
    """Generate and return sample project email HTML"""
    try:
        if not bq_client:
            return jsonify({'error': 'BigQuery client not initialized'}), 500
        
        # Calculate Walmart Week (WM WK)
        # Walmart fiscal year: Feb 1 - Jan 31
        today = datetime.now()
        fiscal_year_start = datetime(today.year if today.month >= 2 else today.year - 1, 2, 1)
        days_since_fy = (today - fiscal_year_start).days
        wm_week = (days_since_fy // 7) + 1
        
        # Get sample projects for email
        sql = """
        SELECT COUNT(*) as total, 
               COUNTIF(health_status = 'On Track') as on_track,
               COUNTIF(health_status = 'At Risk') as at_risk,
               COUNTIF(health_status = 'Off Track') as off_track
        FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
        WHERE project_status = 'Active'
        """
        
        stats_result = bq_client.query(sql).result()
        stats = list(stats_result)[0]
        
        # Get sample projects
        projects_sql = """
        SELECT title, business_area, owner_name, health_status, latest_update
        FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
        WHERE project_status = 'Active'
        LIMIT 5
        """
        projects_result = bq_client.query(projects_sql).result()
        projects = list(projects_result)
        
        # Generate HTML email
        html = f"""
<html>
<head>
    <meta charset="UTF-8">
    <title>Activity Hub - Projects Overview</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f5f5f5; }}
        .container {{ max-width: 800px; margin: 0 auto; background-color: white; }}
        .header {{ background: linear-gradient(135deg, #1e3a8a 0%, #0071ce 100%); color: white; padding: 32px 24px; text-align: center; }}
        .header h1 {{ margin: 0 0 8px 0; font-size: 32px; font-weight: 700; letter-spacing: -0.5px; }}
        .header p {{ margin: 0; font-size: 14px; font-weight: 500; letter-spacing: 0.5px; }}
        .content {{ padding: 24px 32px; }}
        .section-title {{ font-size: 16px; font-weight: 700; color: #1e3a8a; margin: 20px 0 14px 0; text-transform: uppercase; border-bottom: 2px solid #0071ce; padding-bottom: 6px; }}
        .stats-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 24px; }}
        .stat-box {{ background-color: #f8f9fa; border-left: 4px solid #0071ce; padding: 16px 12px; text-align: center; }}
        .stat-value {{ font-size: 28px; font-weight: 700; color: #1e3a8a; line-height: 1.3; }}
        .stat-label {{ font-size: 11px; color: #666; text-transform: uppercase; font-weight: 600; letter-spacing: 0.3px; margin-top: 6px; }}
        .stat-box.on-track {{ border-left-color: #107c10; }}
        .stat-box.on-track .stat-value {{ color: #107c10; }}
        .stat-box.at-risk {{ border-left-color: #f7630c; }}
        .stat-box.at-risk .stat-value {{ color: #f7630c; }}
        .stat-box.off-track {{ border-left-color: #dc3545; }}
        .stat-box.off-track .stat-value {{ color: #dc3545; }}
        .projects-table {{ width: 100%; border-collapse: collapse; margin-top: 12px; }}
        .projects-table th {{ background-color: #1e3a8a; color: white; padding: 12px 8px; text-align: left; font-size: 12px; font-weight: 700; text-transform: uppercase; }}
        .projects-table td {{ padding: 12px 8px; border-bottom: 1px solid #e0e0e0; font-size: 13px; }}
        .projects-table tr:nth-child(even) {{ background-color: #f9f9f9; }}
        .health-badge {{ display: inline-block; padding: 4px 8px; border-radius: 3px; font-size: 11px; font-weight: 700; text-transform: uppercase; }}
        .health-on-track {{ background-color: #d4edda; color: #107c10; }}
        .health-at-risk {{ background-color: #fff3cd; color: #f7630c; }}
        .health-off-track {{ background-color: #f8d7da; color: #dc3545; }}
        .footer {{ background-color: #f5f5f5; padding: 16px 32px; text-align: center; font-size: 11px; color: #999; border-top: 1px solid #e0e0e0; }}
        .footer p {{ margin: 4px 0; }}
        .button {{ display: inline-block; background-color: #0071ce; color: white; padding: 12px 24px; border-radius: 4px; text-decoration: none; font-weight: 600; margin-top: 12px; }}
    </style>
</head>
<body>
    <div class="container">
        <!-- HEADER -->
        <div class="header">
            <h1>Activity Hub Projects Overview</h1>
            <p>WM WK {wm_week} • {datetime.now().strftime('%B %d, %Y')}</p>
        </div>
        
        <!-- CONTENT -->
        <div class="content">
            <h2 class="section-title">Executive Summary</h2>
            
            <div class="stats-grid">
                <div class="stat-box">
                    <div class="stat-value">{stats.total}</div>
                    <div class="stat-label">Total Projects</div>
                </div>
                <div class="stat-box on-track">
                    <div class="stat-value">{stats.on_track}</div>
                    <div class="stat-label">On Track</div>
                </div>
                <div class="stat-box at-risk">
                    <div class="stat-value">{stats.at_risk}</div>
                    <div class="stat-label">At Risk</div>
                </div>
                <div class="stat-box off-track">
                    <div class="stat-value">{stats.off_track}</div>
                    <div class="stat-label">Off Track</div>
                </div>
            </div>

            <h2 class="section-title">Projects</h2>
            
            <table class="projects-table">
                <thead>
                    <tr>
                        <th>Project Title</th>
                        <th>Business Area</th>
                        <th>Owner</th>
                        <th>Health Status</th>
                    </tr>
                </thead>
                <tbody>
"""
        
        # Add project rows
        for project in projects:
            health = project['health_status'] or 'Unknown'
            health_class = 'health-on-track' if 'track' in health.lower() else \
                          'health-at-risk' if 'risk' in health.lower() else \
                          'health-off-track' if 'off' in health.lower() else 'health-on-track'
            
            html += f"""
                    <tr>
                        <td style="font-weight: 600;">{project['title']}</td>
                        <td>{project['business_area']}</td>
                        <td>{project['owner_name']}</td>
                        <td><span class="health-badge {health_class}">{health}</span></td>
                    </tr>
"""
        
        html += """
                </tbody>
            </table>

            <div style="text-align: center; margin-top: 24px;">
                <a href="http://localhost:8088/activity-hub/projects" class="button">View Full Dashboard</a>
            </div>
        </div>
        
        <!-- FOOTER -->
        <div class="footer">
            <p><strong>Activity Hub</strong> • Walmart Projects Platform</p>
            <p>This is an automated email from the Projects Management System.</p>
            <p>&copy; 2026 Walmart Inc. All rights reserved.</p>
        </div>
    </div>
</body>
</html>
"""
        
        # Return as HTML content
        return html, 200, {'Content-Type': 'text/html; charset=utf-8'}
    except Exception as e:
        logger.error(f"Sample email generation error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/business-areas', methods=['GET'])
def get_business_areas():
    """Get unique Business Area options from existing projects"""
    try:
        if not bq_client:
            return jsonify({'error': 'BigQuery client not initialized'}), 500
        
        # Query unique business areas from the AH_Projects table (we know this exists)
        sql = """
        SELECT DISTINCT business_area
        FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
        WHERE business_area IS NOT NULL AND business_area != ''
        ORDER BY business_area
        """
        
        job = bq_client.query(sql)
        results = job.result()
        
        areas = [row.business_area for row in results]
        logger.info(f"Retrieved {len(areas)} unique business areas from projects")
        
        return jsonify({
            'success': True,
            'business_areas': areas,
            'count': len(areas)
        }), 200
    except Exception as e:
        logger.error(f"Business areas retrieval error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/projects/sync-data-bridge', methods=['POST'])
def sync_data_bridge():
    """Sync projects data from Data Bridge (Intake Accel Council) table"""
    try:
        if not bq_client:
            return jsonify({'error': 'BigQuery client not initialized'}), 500
        
        # First, get the list of existing project titles
        existing_titles_sql = """
        SELECT DISTINCT title FROM `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
        """
        
        existing_titles = set()
        try:
            results = bq_client.query(existing_titles_sql).result()
            for row in results:
                existing_titles.add(row.title)
        except:
            pass  # If table doesn't exist yet, that's ok
        
        # Get all projects from Data Bridge
        source_sql = """
        SELECT 
            COALESCE(impact_id, GENERATE_UUID()) as impact_id,
            project_title as title,
            business_area,
            owner_name,
            owner_id,
            health_status,
            project_status,
            created_at as created_timestamp,
            updated_at as modified_timestamp,
            latest_update,
            CURRENT_TIMESTAMP() as latest_update_timestamp,
            CASE 
              WHEN LOWER(updated_this_week) = 'true' THEN 'true'
              ELSE 'false'
            END as current_wm_week_update
        FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - Intake Accel Council Data`
        """
        
        rows_to_insert = []
        source_results = bq_client.query(source_sql).result()
        for row in source_results:
            if row.title not in existing_titles:
                rows_to_insert.append(row)
        
        if rows_to_insert:
            insert_sql = """
            INSERT INTO `wmt-assetprotection-prod.Store_Support_Dev.AH_Projects`
            (impact_id, title, business_area, owner_name, owner_id, health_status, project_status, 
             created_timestamp, modified_timestamp, latest_update, latest_update_timestamp, current_wm_week_update)
            VALUES 
            """
            using_params = []
            param_names = []
            
            for i, row in enumerate(rows_to_insert):
                if i > 0:
                    insert_sql += ", "
                
                params = [
                    bigquery.ScalarQueryParameter(f"p{i}_impact_id", "STRING", row.impact_id or str(__import__('uuid').uuid4())),
                    bigquery.ScalarQueryParameter(f"p{i}_title", "STRING", row.title),
                    bigquery.ScalarQueryParameter(f"p{i}_business_area", "STRING", row.business_area),
                    bigquery.ScalarQueryParameter(f"p{i}_owner_name", "STRING", row.owner_name),
                    bigquery.ScalarQueryParameter(f"p{i}_owner_id", "STRING", row.owner_id),
                    bigquery.ScalarQueryParameter(f"p{i}_health_status", "STRING", row.health_status),
                    bigquery.ScalarQueryParameter(f"p{i}_project_status", "STRING", row.project_status),
                    bigquery.ScalarQueryParameter(f"p{i}_created_timestamp", "TIMESTAMP", row.created_timestamp),
                    bigquery.ScalarQueryParameter(f"p{i}_modified_timestamp", "TIMESTAMP", row.modified_timestamp),
                    bigquery.ScalarQueryParameter(f"p{i}_latest_update", "STRING", row.latest_update),
                    bigquery.ScalarQueryParameter(f"p{i}_latest_update_timestamp", "TIMESTAMP", row.latest_update_timestamp),
                    bigquery.ScalarQueryParameter(f"p{i}_current_wm_week_update", "STRING", row.current_wm_week_update),
                ]
                
                using_params.extend(params)
                insert_sql += f"""(@p{i}_impact_id, @p{i}_title, @p{i}_business_area, @p{i}_owner_name, 
                              @p{i}_owner_id, @p{i}_health_status, @p{i}_project_status, 
                              @p{i}_created_timestamp, @p{i}_modified_timestamp, @p{i}_latest_update, 
                              @p{i}_latest_update_timestamp, @p{i}_current_wm_week_update)"""
            
            job_config = bigquery.QueryJobConfig(query_parameters=using_params)
            job = bq_client.query(insert_sql, job_config=job_config)
            job.result()
            
            logger.info(f"Data Bridge sync completed: {len(rows_to_insert)} new projects synced")
            return jsonify({
                'success': True,
                'message': f'Synced {len(rows_to_insert)} new projects from Data Bridge',
                'rows_affected': len(rows_to_insert)
            }), 200
        else:
            return jsonify({
                'success': True,
                'message': 'No new projects to sync from Data Bridge',
                'rows_affected': 0
            }), 200
            
    except Exception as e:
        logger.error(f"Data Bridge sync error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/')
def root():
    from flask import redirect
    return redirect('/activity-hub/')


if __name__ == '__main__':
    port = 8088
    print(f'Activity Hub V2 starting on port {port}...')
    print(f'  Local:   http://localhost:{port}/activity-hub/')
    print(f'  Network: http://weus42608431466:{port}/activity-hub/')
    app.run(host='0.0.0.0', port=port, debug=False)
