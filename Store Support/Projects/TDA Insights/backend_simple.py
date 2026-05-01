#!/usr/bin/env python3
"""
TDA Insights Dashboard Backend - BigQuery Connected
Connects to real BigQuery data from wmt-assetprotection-prod

Authentication Setup:
  Option 1: gcloud auth application-default login
  Option 2: Set GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json
"""

import socket
import json
import threading
import time
from pathlib import Path
import zipfile
import io
import struct
from xml.etree import ElementTree as ET
import os
import base64

# Try to load environment variables from .env file (optional)
try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent / '.env')
except ImportError:
    # dotenv not installed, use environment variables directly
    pass

PORT = 5000
SCRIPT_DIR = Path(__file__).parent

# Try to import BigQuery client
try:
    from google.cloud import bigquery
    from google.oauth2 import service_account
    BQ_AVAILABLE = True
except ImportError:
    BQ_AVAILABLE = False
    print("[WARN] BigQuery libraries not available. Using sample data.")
    print("[HINT] Install: pip install google-cloud-bigquery google-auth python-dotenv")

# BigQuery configuration from environment variables
BQ_PROJECT = os.getenv('GCP_PROJECT_ID', 'wmt-assetprotection-prod')
BQ_DATASET = os.getenv('BIGQUERY_DATASET', 'Store_Support_Dev')
BQ_TABLE = os.getenv('BIGQUERY_TABLE', 'Output_TDA Report')

def get_bigquery_client():
    """Initialize BigQuery client with Application Default Credentials"""
    if not BQ_AVAILABLE:
        return None
    
    try:
        # BigQuery client will automatically use Application Default Credentials
        # This includes: GOOGLE_APPLICATION_CREDENTIALS env var, gcloud auth, etc.
        print(f"[OK] Initializing BigQuery client (using Application Default Credentials)")
        client = bigquery.Client(project=BQ_PROJECT)
        
        print(f"[OK] BigQuery client initialized successfully")
        print(f"   Project: {BQ_PROJECT}")
        print(f"   Dataset: {BQ_DATASET}")
        print(f"   Table: {BQ_TABLE}")
        return client
    except Exception as e:
        print(f"[ERROR] Could not initialize BigQuery client: {e}")
        print(f"[HINT] Make sure you ran: gcloud auth application-default login")
        return None

# ── Temporary data normalization (until BQ data reflects new names) ──
_PHASE_MAP = {'POC/POT': 'Vet', 'Mkt Scale': 'Test Markets'}
_OWNERSHIP_MAP = {'Dallas POC': 'Dallas Team', 'Dallas VET': 'Dallas Team'}

def _normalize_phase(phase):
    return _PHASE_MAP.get(phase, phase)

def _normalize_ownership(raw):
    own = raw or 'No Selection Provided'
    if own in ('No Selection Provided', '*Select Owner'):
        return 'No Selection Provided'
    return _OWNERSHIP_MAP.get(own, own)

def get_bigquery_data():
    """Fetch data from BigQuery"""
    if not BQ_AVAILABLE:
        return None
    
    try:
        client = get_bigquery_client()
        if not client:
            return None
        
        # Query the actual BigQuery table with correct column names
        # Table: Output- TDA Report
        # Columns: Topic, Health_Update, Phase, Dallas_POC, Deployment, Intake_n_Testing, Facility, Facility_Phase
        query = f"""
        SELECT 
            Topic as `Initiative - Project Title`,
            Health_Update as `Health Status`,
            Phase,
            SUM(CASE WHEN Phase = Facility_Phase THEN Facility ELSE 0 END) as `# of Stores`,
            Dallas_POC as `Dallas POC`,
            Intake_n_Testing as `Intake & Testing`,
            Deployment,
            MAX(Intake_Card_Nbr) as `Project ID`,
            COALESCE(TDA_Ownership, 'No Selection Provided') as `TDA Ownership`
        FROM `{BQ_PROJECT}.{BQ_DATASET}.{BQ_TABLE}`
        WHERE Topic IS NOT NULL
        GROUP BY Topic, Health_Update, Phase, Intake_n_Testing, Dallas_POC, Deployment, TDA_Ownership
        ORDER BY Topic
        """
        
        query_job = client.query(query)
        results = query_job.result()
        
        # Convert results to list of dicts
        data = []
        for row in results:
            data.append({
                'Initiative - Project Title': row['Initiative - Project Title'] or 'Unknown',
                'Health Status': row['Health Status'] or 'Unknown',
                'Phase': _normalize_phase(row['Phase'] or 'Unknown'),
                '# of Stores': row['# of Stores'] or 0,
                'Dallas Team': row['Dallas POC'] or 'N/A',
                'Intake & Testing': row['Intake & Testing'] or 'N/A',
                'Deployment': row['Deployment'] or 'N/A',
                'Project ID': row['Project ID'] or 0,
                'TDA Ownership': _normalize_ownership(row['TDA Ownership'])
            })
        
        print(f"[OK] Loaded {len(data)} projects from BigQuery")
        return data
    except Exception as e:
        print(f"[ERROR] BigQuery query failed: {e}")
        print(f"[HINT] Check that table '{BQ_TABLE}' exists and has required columns")
        return None
        return None

# Sample data fallback
SAMPLE_DATA = [
    {
        "Initiative - Project Title": "Sidekick Enhancement",
        "Health Status": "On Track",
        "Phase": "Test",
        "# of Stores": 120,
        "TDA Ownership": "Intake & Test",
        "Intake & Testing": "System testing in progress. All core features validated. Ready for POC expansion.",
        "Dallas Team": "John Smith - Store #4521, TX",
        "Deployment": "Scheduled for 3/15/2026. Training materials prepared. Rollout plan finalized."
    },
    {
        "Initiative - Project Title": "GMD Optimization",
        "Health Status": "At Risk",
        "Phase": "Vet",
        "# of Stores": 95,
        "TDA Ownership": "Intake & Test",
        "Intake & Testing": "POC execution with pilot stores. Initial results show 15% efficiency gains.",
        "Dallas Team": "Jane Doe - Store #2847, TX",
        "Deployment": "Delayed. Addressing performance issues discovered in POC phase. New target: 4/1/2026"
    },
    {
        "Initiative - Project Title": "DSD Redesign",
        "Health Status": "On Track",
        "Phase": "Roll/Deploy",
        "# of Stores": 250,
        "TDA Ownership": "No Selection Provided",
        "Intake & Testing": "All validation complete. Rollout in waves starting Week 3.",
        "Dallas Team": "Bob Wilson - Store #1234, TX",
        "Deployment": "Live in 250 stores as of 2/28/2026. Phase 2 rollout beginning next week."
    },
    {
        "Initiative - Project Title": "Fresh Department Update",
        "Health Status": "Off Track",
        "Phase": "Pending",
        "# of Stores": 180,
        "TDA Ownership": "No Selection Provided",
        "Intake & Testing": "Initial requirements gathering delayed. No testing scheduled yet.",
        "Dallas Team": "Alice Johnson - Pending Assignment",
        "Deployment": "Blocked. Awaiting stakeholder sign-off on requirements."
    },
    {
        "Initiative - Project Title": "Inventory System Migration",
        "Health Status": "On Track",
        "Phase": "Test Markets",
        "# of Stores": 15,
        "TDA Ownership": "Intake & Test",
        "Intake & Testing": "Market testing complete. System scaling for regional rollout.",
        "Dallas Team": "Tom Brown - Store #5678, TX",
        "Deployment": "Regional deployment Q2 2026. Infrastructure scaled for 500+ stores."
    },
]

# Load data at startup
print("\n[*] Loading data from BigQuery...")
BQ_DATA = get_bigquery_data()
DATA = BQ_DATA if BQ_DATA else SAMPLE_DATA
DATA_LAST_REFRESH = time.strftime('%Y-%m-%d %H:%M:%S')

if BQ_DATA:
    DATA_SOURCE = "BigQuery (wmt-assetprotection-prod)"
else:
    DATA_SOURCE = "Sample Data (local)"

def get_sif_aim_data():
    """Fetch SIF/AIM meeting data from Intake Accel Council Data table"""
    if not BQ_AVAILABLE:
        return {'upcoming': [], 'recent_actions': []}
    try:
        client = get_bigquery_client()
        if not client:
            return {'upcoming': [], 'recent_actions': []}
        
        today_str = time.strftime('%Y-%m-%d')
        twenty_one_days_ago = time.strftime('%Y-%m-%d', time.localtime(time.time() - 21 * 86400))
        
        # Try with SIF_OR_AIM_Note column first; fall back without it
        base_cols = """
            Project_Title,
            CAST(Intake_Card_Nbr AS INT64) as Project_ID,
            Meeting_Type,
            SIF_Date,
            AIM_Date"""
        where_clause = f"""
        FROM `{BQ_PROJECT}.{BQ_DATASET}.Output - Intake Accel Council Data`
        WHERE (SIF_Date IS NOT NULL OR AIM_Date IS NOT NULL)
          AND Project_Title IS NOT NULL
          AND COALESCE(CAST(Is_Duplicate_Row AS STRING), '') != 'Yes'
        ORDER BY COALESCE(SIF_Date, AIM_Date) DESC"""
        
        has_note_col = True
        query = f"SELECT {base_cols}, COALESCE(SIF_OR_AIM_Note, '') as SIF_OR_AIM_Note {where_clause}"
        try:
            query_job = client.query(query)
            results = query_job.result()
        except Exception:
            has_note_col = False
            query = f"SELECT {base_cols} {where_clause}"
            query_job = client.query(query)
            results = query_job.result()
        
        upcoming = []
        recent_actions = []
        
        for row in results:
            title = row['Project_Title'] or ''
            project_id = row['Project_ID'] or 0
            meeting_type = row['Meeting_Type'] or ''
            sif_date = str(row['SIF_Date']) if row['SIF_Date'] else None
            aim_date = str(row['AIM_Date']) if row['AIM_Date'] else None
            note = (row['SIF_OR_AIM_Note'] or '') if has_note_col else ''
            
            # Determine which meeting date to use
            # If meeting_type is AIM, use aim_date; if SIF, use sif_date; otherwise use whichever is available
            if meeting_type.upper() == 'AIM' and aim_date:
                meeting_date = aim_date
                meeting_label = 'AIM'
            elif meeting_type.upper() == 'SIF' and sif_date:
                meeting_date = sif_date
                meeting_label = 'SIF'
            elif sif_date and aim_date:
                # Both dates present — create entries for both
                # For SIF
                if sif_date >= today_str:
                    upcoming.append({'title': title, 'project_id': project_id, 'meeting': 'SIF', 'date': sif_date, 'note': note})
                elif sif_date >= twenty_one_days_ago:
                    recent_actions.append({'title': title, 'project_id': project_id, 'meeting': 'SIF', 'date': sif_date, 'note': note})
                # For AIM
                if aim_date >= today_str:
                    upcoming.append({'title': title, 'project_id': project_id, 'meeting': 'AIM', 'date': aim_date, 'note': note})
                elif aim_date >= twenty_one_days_ago:
                    recent_actions.append({'title': title, 'project_id': project_id, 'meeting': 'AIM', 'date': aim_date, 'note': note})
                continue
            elif sif_date:
                meeting_date = sif_date
                meeting_label = 'SIF'
            elif aim_date:
                meeting_date = aim_date
                meeting_label = 'AIM'
            else:
                continue
            
            # Categorize: upcoming (today or future) vs recent actions (past 21 days)
            if meeting_date >= today_str:
                upcoming.append({'title': title, 'project_id': project_id, 'meeting': meeting_label, 'date': meeting_date, 'note': note})
            elif meeting_date >= twenty_one_days_ago:
                recent_actions.append({'title': title, 'project_id': project_id, 'meeting': meeting_label, 'date': meeting_date, 'note': note})
        
        # Sort upcoming by date ascending, recent by date descending
        upcoming.sort(key=lambda x: x['date'])
        recent_actions.sort(key=lambda x: x['date'], reverse=True)
        
        # Deduplicate upcoming and recent action rows by project, meeting, and date
        def dedupe_rows(rows):
            seen = set()
            deduped = []
            for entry in rows:
                key = (entry.get('project_id') or 0, entry.get('meeting') or '', entry.get('date') or '')
                if key not in seen:
                    seen.add(key)
                    deduped.append(entry)
            return deduped
        
        upcoming = dedupe_rows(upcoming)
        recent_actions = dedupe_rows(recent_actions)
        
        unique_upcoming_count = len({
            (entry.get('project_id') or 0, entry.get('meeting') or '', entry.get('date') or '')
            for entry in upcoming
        })
        unique_recent_count = len({
            (entry.get('project_id') or 0, entry.get('meeting') or '', entry.get('date') or '')
            for entry in recent_actions
        })
        
        print(f"[OK] SIF/AIM data: {len(upcoming)} upcoming, {len(recent_actions)} recent actions")
        return {
            'upcoming': upcoming,
            'recent_actions': recent_actions,
            'unique_upcoming_count': unique_upcoming_count,
            'unique_recent_count': unique_recent_count
        }
    except Exception as e:
        print(f"[WARN] SIF/AIM query failed (column may not exist yet): {e}")
        return {'upcoming': [], 'recent_actions': [], 'unique_upcoming_count': 0}

# Load SIF/AIM meeting data (after function is defined)
print("[*] Loading SIF/AIM meeting data...")
SIF_AIM_DATA = get_sif_aim_data()

def refresh_data():
    """Re-fetch data from BigQuery and update the global DATA cache"""
    global DATA, BQ_DATA, DATA_SOURCE, DATA_LAST_REFRESH, SIF_AIM_DATA
    print(f"[{time.strftime('%H:%M:%S')}] Refreshing data from BigQuery...")
    new_data = get_bigquery_data()
    if new_data:
        BQ_DATA = new_data
        DATA = new_data
        DATA_SOURCE = "BigQuery (wmt-assetprotection-prod)"
        DATA_LAST_REFRESH = time.strftime('%Y-%m-%d %H:%M:%S')
        print(f"[OK] Refreshed: {len(DATA)} records loaded")
        SIF_AIM_DATA = get_sif_aim_data()
        return True, len(DATA)
    else:
        print("[WARN] Refresh failed, keeping existing data")
        return False, len(DATA)

def get_project_detail(project_id_str):
    """Fetch detailed project info for the Project Summary view"""
    if not project_id_str:
        return None
    try:
        from urllib.parse import unquote_plus
        project_id_str = unquote_plus(project_id_str).strip()
    except Exception:
        project_id_str = str(project_id_str).strip()

    detail = None
    if BQ_AVAILABLE:
        try:
            client = get_bigquery_client()
            if client:
                # Query project detail from Intake Accel Council Data
                query = f"""
                SELECT
                    Project_Title,
                    CAST(Intake_Card_Nbr AS INT64) as Project_ID,
                    Owner,
                    Store_Area,
                    Phase,
                    Health_Update,
                    COALESCE(PRESENTATION_SUMMARY, OVERVIEW, '') as Summary,
                    COALESCE(Project_Update, '') as Latest_Update,
                    Count_of_Stores,
                    SIF_Date,
                    AIM_Date,
                    Meeting_Type,
                    PROJECT_START_DATE,
                    PROJECT_END_DATE,
                    TDA_Ownership,
                    Dallas_Vet as Dallas_Vet,
                    Intake_n_Testing,
                    Deployment
                FROM `{BQ_PROJECT}.{BQ_DATASET}.Output - Intake Accel Council Data`
                WHERE CAST(Intake_Card_Nbr AS STRING) = '{project_id_str}'
                  AND COALESCE(CAST(Is_Duplicate_Row AS STRING), '') != 'Yes'
                LIMIT 1
                """
                query_job = client.query(query)
                results = list(query_job.result())
                if results:
                    row = results[0]
                    project_id = row['Project_ID'] or 0
                    metrics = []
                    if project_id:
                        try:
                            metrics_query = f"""
                            SELECT Metric_Name, Metric_Type, Actual, Expected, Impact, Lift, Start_Date, End_Date
                            FROM `{BQ_PROJECT}.Store_Support.Project_Metric_Lift`
                            WHERE Project_ID = {project_id}
                            ORDER BY Metric_Name
                            """
                            metrics_job = client.query(metrics_query)
                            for mrow in metrics_job.result():
                                metrics.append({
                                    'metric_name': mrow['Metric_Name'] or '',
                                    'metric_type': mrow['Metric_Type'] or '',
                                    'actual': float(mrow['Actual']) if mrow['Actual'] is not None else None,
                                    'expected': float(mrow['Expected']) if mrow['Expected'] is not None else None,
                                    'impact': float(mrow['Impact']) if mrow['Impact'] is not None else None,
                                    'lift': mrow['Lift'] or '',
                                    'start_date': str(mrow['Start_Date']) if mrow['Start_Date'] else None,
                                    'end_date': str(mrow['End_Date']) if mrow['End_Date'] else None
                                })
                        except Exception as me:
                            print(f"[WARN] Metrics query failed: {me}")
                    detail = {
                        'title': row['Project_Title'] or '',
                        'project_id': project_id,
                        'owner': row['Owner'] or 'N/A',
                        'team': _normalize_ownership(row['TDA_Ownership']),
                        'store_area': row['Store_Area'] or '',
                        'phase': _normalize_phase(row['Phase'] or ''),
                        'health_status': row['Health_Update'] or '',
                        'summary': row['Summary'] or '',
                        'latest_update': row['Latest_Update'] or '',
                        'store_count': row['Count_of_Stores'] or 0,
                        'dallas_team_notes': row['Dallas_Vet'] or '',
                        'intake_testing_notes': row['Intake_n_Testing'] or '',
                        'deployment_notes': row['Deployment'] or '',
                        'sif_date': str(row['SIF_Date']) if row['SIF_Date'] else None,
                        'aim_date': str(row['AIM_Date']) if row['AIM_Date'] else None,
                        'start_date': str(row['PROJECT_START_DATE']) if row['PROJECT_START_DATE'] else None,
                        'end_date': str(row['PROJECT_END_DATE']) if row['PROJECT_END_DATE'] else None,
                        'metrics': metrics
                    }
                    return detail
        except Exception as e:
            print(f"[WARN] Project detail query failed for '{project_id_str}': {e}")

    # Fallback to cached dashboard data if BQ detail is unavailable
    for row in DATA:
        if str(row.get('Project ID', '')).strip() == project_id_str:
            return {
                'title': row.get('Initiative - Project Title', ''),
                'project_id': row.get('Project ID', 0),
                'owner': 'N/A',
                'team': row.get('TDA Ownership', ''),
                'phase': row.get('Phase', ''),
                'health_status': row.get('Health Status', ''),
                'summary': '',
                'latest_update': '',
                'store_count': row.get('# of Stores', 0),
                'dallas_team_notes': row.get('Dallas Team', ''),
                'intake_testing_notes': row.get('Intake & Testing', ''),
                'deployment_notes': row.get('Deployment', ''),
                'sif_date': None,
                'aim_date': None,
                'start_date': None,
                'end_date': None,
                'metrics': []
            }

    # Last resort: search by exact title match
    for row in DATA:
        if str(row.get('Initiative - Project Title', '')).strip().lower() == project_id_str.lower():
            return {
                'title': row.get('Initiative - Project Title', ''),
                'project_id': row.get('Project ID', 0),
                'owner': 'N/A',
                'team': row.get('TDA Ownership', ''),
                'phase': row.get('Phase', ''),
                'health_status': row.get('Health Status', ''),
                'summary': '',
                'latest_update': '',
                'store_count': row.get('# of Stores', 0),
                'dallas_team_notes': row.get('Dallas Team', ''),
                'intake_testing_notes': row.get('Intake & Testing', ''),
                'deployment_notes': row.get('Deployment', ''),
                'sif_date': None,
                'aim_date': None,
                'start_date': None,
                'end_date': None,
                'metrics': []
            }

    return None
def generate_minimal_pptx(phase=None):
    """Generate a PPTX file with data organized by phase"""
    pptx_buffer = io.BytesIO()
    
    with zipfile.ZipFile(pptx_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
        # [Content_Types].xml
        content_types = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>
<Override PartName="/ppt/slides/slide1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>
<Override PartName="/ppt/slides/slide2.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>
<Override PartName="/ppt/slides/slide3.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>
<Override PartName="/ppt/slides/slide4.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>
<Override PartName="/ppt/slides/slide5.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>
<Override PartName="/ppt/slides/slide6.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>
</Types>'''
        zf.writestr('[Content_Types].xml', content_types)
        
        # _rels/.rels
        rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="ppt/presentation.xml"/>
</Relationships>'''
        zf.writestr('_rels/.rels', rels)
        
        # ppt/_rels/presentation.xml.rels
        ppt_rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide1.xml"/>
<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide2.xml"/>
<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide3.xml"/>
<Relationship Id="rId4" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide4.xml"/>
<Relationship Id="rId5" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide5.xml"/>
<Relationship Id="rId6" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide6.xml"/>
</Relationships>'''
        zf.writestr('ppt/_rels/presentation.xml.rels', ppt_rels)
        
        # ppt/presentation.xml
        presentation = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:presentation xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
<p:sldIdLst>
<p:sldId id="256" r:id="rId1"/>
<p:sldId id="257" r:id="rId2"/>
<p:sldId id="258" r:id="rId3"/>
<p:sldId id="259" r:id="rId4"/>
<p:sldId id="260" r:id="rId5"/>
<p:sldId id="261" r:id="rId6"/>
</p:sldIdLst>
<p:sldSz cx="9144000" cy="6858000" type="custom"/>
<p:notesSz cx="6858000" cy="9144000"/>
</p:presentation>'''
        zf.writestr('ppt/presentation.xml', presentation)
        
        # Create slides for each phase
        phases_list = ['Pending', 'Vet', 'Test', 'Test Markets', 'Roll/Deploy', 'Summary']
        
        for slide_num, phase_name in enumerate(phases_list, 1):
            # ppt/slides/_rels/slideN.xml.rels
            slide_rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
</Relationships>'''
            zf.writestr(f'ppt/slides/_rels/slide{slide_num}.xml.rels', slide_rels)
            
            # Get data for this phase
            if phase_name == 'Summary':
                phase_data = filter_data()
                title = "TDA Initiatives Summary"
                content = f"Total Initiatives: {len(phase_data)}\n"
                content += f"Total Stores: {sum(int(p.get('# of Stores', 0) or 0) for p in phase_data)}\n\n"
                
                # Count by status
                statuses = {}
                for p in phase_data:
                    status = p.get('Health Status', 'Unknown')
                    statuses[status] = statuses.get(status, 0) + 1
                
                for status, count in statuses.items():
                    content += f"{status}: {count}\n"
            else:
                phase_data = [p for p in filter_data() if p.get('Phase') == phase_name]
                title = f"Phase: {phase_name} ({len(phase_data)} projects)"
                content = ""
                for idx, p in enumerate(phase_data[:10], 1):  # Limit to 10 per slide
                    content += f"\n{idx}. {p['Initiative - Project Title']}\n"
                    content += f"   Status: {p['Health Status']} | Stores: {p['# of Stores']}\n"
            
            slide_xml = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
<p:cSld>
<p:spTree>
<p:nvGrpSpPr>
<p:cNvPr id="1" name="Title"/>
<p:cNvGrpSpPr/>
<p:nvPr/>
</p:nvGrpSpPr>
<p:grpSpPr>
<a:xfrm>
<a:off x="0" y="0"/>
<a:ext cx="9144000" cy="6858000"/>
</a:xfrm>
</p:grpSpPr>
<p:sp>
<p:nvSpPr>
<p:cNvPr id="2" name="Title"/>
<p:cNvSpPr/>
<p:nvPr/>
</p:nvSpPr>
<p:spPr>
<a:xfrm>
<a:off x="457200" y="274638"/>
<a:ext cx="8230200" cy="1476600"/>
</a:xfrm>
</p:spPr>
<p:txBody>
<a:bodyPr/>
<a:lstStyle/>
<a:p>
<a:r>
<a:rPr lang="en-US" sz="4400" bold="1"/>
<a:t>{title}</a:t>
</a:r>
</a:p>
</p:txBody>
</p:sp>
<p:sp>
<p:nvSpPr>
<p:cNvPr id="3" name="Content"/>
<p:cNvSpPr/>
<p:nvPr/>
</p:nvSpPr>
<p:spPr>
<a:xfrm>
<a:off x="457200" y="1905000"/>
<a:ext cx="8230200" cy="4572000"/>
</a:xfrm>
</p:spPr>
<p:txBody>
<a:bodyPr/>
<a:lstStyle/>
<a:p>
<a:r>
<a:rPr lang="en-US" sz="2000"/>
<a:t>{content.replace(chr(10), " ")}</a:t>
</a:r>
</a:p>
</p:txBody>
</p:sp>
</p:spTree>
</p:cSld>
</p:sld>'''
            zf.writestr(f'ppt/slides/slide{slide_num}.xml', slide_xml)
    
    pptx_buffer.seek(0)
    return pptx_buffer.getvalue()

def generate_pptx_from_screenshots(screenshots_data, title="TDA Report"):
    """Generate PPTX from base64 encoded screenshots using pure XML"""
    try:
        pptx_buffer = io.BytesIO()
        image_id = 1
        slide_num = 1
        
        with zipfile.ZipFile(pptx_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
            # Count total slides (title + screenshots)
            total_slides = len(screenshots_data) + 1
            
            # [Content_Types].xml
            content_types = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Default Extension="png" ContentType="image/png"/>
<Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>'''
            
            # Add slide overrides
            for i in range(1, total_slides + 1):
                content_types += f'\n<Override PartName="/ppt/slides/slide{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>'
            
            content_types += '\n</Types>'
            zf.writestr('[Content_Types].xml', content_types)
            
            # _rels/.rels
            rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="ppt/presentation.xml"/>
</Relationships>'''
            zf.writestr('_rels/.rels', rels)
            
            # ppt/_rels/presentation.xml.rels
            ppt_rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'''
            for i in range(1, total_slides + 1):
                ppt_rels += f'\n<Relationship Id="rId{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide{i}.xml"/>'
            ppt_rels += '\n</Relationships>'
            zf.writestr('ppt/_rels/presentation.xml.rels', ppt_rels)
            
            # ppt/presentation.xml
            presentation = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:presentation xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
<p:sldIdLst>'''
            for i in range(1, total_slides + 1):
                presentation += f'\n<p:sldId id="{255+i}" r:id="rId{i}"/>'
            presentation += '\n</p:sldIdLst>\n<p:sldSz cx="9144000" cy="6858000" type="custom"/>\n<p:notesSz cx="6858000" cy="9144000"/>\n</p:presentation>'
            zf.writestr('ppt/presentation.xml', presentation)
            
            # Add title slide
            slide_rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
</Relationships>'''
            zf.writestr(f'ppt/slides/_rels/slide{slide_num}.xml.rels', slide_rels)
            
            # TITLE SLIDE - Matches the dashboard header style (blue bar + Spark logo)
            title_slide = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
<p:cSld>
<p:bg>
<p:bgPr>
<a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill>
<a:effectLst/>
</p:bgPr>
</p:bg>
<p:spTree>
<p:nvGrpSpPr>
<p:cNvPr id="1" name="Title"/>
<p:cNvGrpSpPr/>
<p:nvPr/>
</p:nvGrpSpPr>
<p:grpSpPr>
<a:xfrm>
<a:off x="0" y="0"/>
<a:ext cx="9144000" cy="6858000"/>
</a:xfrm>
</p:grpSpPr>
<!-- Blue header bar across top -->
<p:sp>
<p:nvSpPr>
<p:cNvPr id="2" name="HeaderBar"/>
<p:cNvSpPr/>
<p:nvPr/>
</p:nvSpPr>
<p:spPr>
<a:xfrm>
<a:off x="0" y="0"/>
<a:ext cx="9144000" cy="1143000"/>
</a:xfrm>
<a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
<a:solidFill><a:srgbClr val="3B82F6"/></a:solidFill>
<a:ln><a:noFill/></a:ln>
</p:spPr>
<p:txBody>
<a:bodyPr anchor="ctr" lIns="457200" rIns="91440" tIns="0" bIns="0"/>
<a:lstStyle/>
<a:p>
<a:pPr algn="l"/>
<a:r>
<a:rPr lang="en-US" sz="2800" b="1" dirty="0">
<a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill>
<a:latin typeface="Segoe UI"/>
</a:rPr>
<a:t>TDA Initiatives Insights</a:t>
</a:r>
</a:p>
</p:txBody>
</p:sp>
<!-- Main title centered on slide -->
<p:sp>
<p:nvSpPr>
<p:cNvPr id="3" name="MainTitle"/>
<p:cNvSpPr/>
<p:nvPr/>
</p:nvSpPr>
<p:spPr>
<a:xfrm>
<a:off x="457200" y="2200000"/>
<a:ext cx="8230000" cy="1800000"/>
</a:xfrm>
</p:spPr>
<p:txBody>
<a:bodyPr anchor="ctr"/>
<a:lstStyle/>
<a:p>
<a:pPr algn="ctr"/>
<a:r>
<a:rPr lang="en-US" sz="4000" b="1" dirty="0">
<a:solidFill><a:srgbClr val="1E3A5F"/></a:solidFill>
<a:latin typeface="Segoe UI"/>
</a:rPr>
<a:t>Initiative Status Insights</a:t>
</a:r>
</a:p>
</p:txBody>
</p:sp>
<!-- Subtitle -->
<p:sp>
<p:nvSpPr>
<p:cNvPr id="4" name="Subtitle"/>
<p:cNvSpPr/>
<p:nvPr/>
</p:nvSpPr>
<p:spPr>
<a:xfrm>
<a:off x="457200" y="3900000"/>
<a:ext cx="8230000" cy="800000"/>
</a:xfrm>
</p:spPr>
<p:txBody>
<a:bodyPr anchor="t"/>
<a:lstStyle/>
<a:p>
<a:pPr algn="ctr"/>
<a:r>
<a:rPr lang="en-US" sz="2000" dirty="0">
<a:solidFill><a:srgbClr val="666666"/></a:solidFill>
<a:latin typeface="Segoe UI"/>
</a:rPr>
<a:t>Store Support  |  Asset Protection</a:t>
</a:r>
</a:p>
</p:txBody>
</p:sp>
<!-- Bottom accent line -->
<p:sp>
<p:nvSpPr>
<p:cNvPr id="5" name="AccentLine"/>
<p:cNvSpPr/>
<p:nvPr/>
</p:nvSpPr>
<p:spPr>
<a:xfrm>
<a:off x="0" y="6658000"/>
<a:ext cx="9144000" cy="200000"/>
</a:xfrm>
<a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
<a:solidFill><a:srgbClr val="FFC220"/></a:solidFill>
<a:ln><a:noFill/></a:ln>
</p:spPr>
</p:sp>
</p:spTree>
</p:cSld>
<p:clrMapOvr>
<a:masterClrMapping/>
</p:clrMapOvr>
</p:sld>'''
            zf.writestr(f'ppt/slides/slide{slide_num}.xml', title_slide)
            slide_num += 1
            
            # Add screenshot slides
            for idx, screenshot_info in enumerate(screenshots_data, 1):
                try:
                    image_data = screenshot_info.get('imageData', '')
                    if ',' in image_data:
                        image_data = image_data.split(',')[1]
                    
                    # Decode and store image
                    image_bytes = base64.b64decode(image_data)
                    image_filename = f'image{idx}.png'
                    zf.writestr(f'ppt/media/{image_filename}', image_bytes)
                    
                    # Read PNG dimensions from IHDR chunk
                    img_width_px, img_height_px = 1280, 720  # defaults
                    if len(image_bytes) > 24 and image_bytes[1:4] == b'PNG':
                        img_width_px, img_height_px = struct.unpack('>II', image_bytes[16:24])
                    
                    # Slide dimensions in EMU
                    SLIDE_W = 9144000   # 10in * 914400 EMU/in
                    SLIDE_H = 6858000   # 7.5in * 914400 EMU/in
                    
                    # Always fill full slide width, scale height proportionally
                    aspect = img_height_px / img_width_px if img_width_px > 0 else 0.5625
                    final_w = SLIDE_W
                    final_h = int(SLIDE_W * aspect)
                    
                    # If height exceeds slide, cap at slide height (still full width)
                    if final_h > SLIDE_H:
                        final_h = SLIDE_H
                    
                    # Always top-left: x=0, y=0
                    off_x = 0
                    off_y = 0
                    
                    # Create slide with image
                    slide_rels = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="../media/{image_filename}"/>
</Relationships>'''
                    zf.writestr(f'ppt/slides/_rels/slide{slide_num}.xml.rels', slide_rels)
                    
                    # Image slide XML
                    image_slide = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
<p:cSld>
<p:bg>
<p:bgPr>
<a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill>
<a:effectLst/>
</p:bgPr>
</p:bg>
<p:spTree>
<p:nvGrpSpPr>
<p:cNvPr id="1" name=""/>
<p:cNvGrpSpPr/>
<p:nvPr/>
</p:nvGrpSpPr>
<p:grpSpPr>
<a:xfrm>
<a:off x="0" y="0"/>
<a:ext cx="9144000" cy="6858000"/>
</a:xfrm>
</p:grpSpPr>
<p:pic>
<p:nvPicPr>
<p:cNvPr id="2" name="{image_filename}"/>
<p:cNvPicPr>
<a:picLocks noChangeAspect="1"/>
</p:cNvPicPr>
<p:nvPr/>
</p:nvPicPr>
<p:blipFill>
<a:blip r:embed="rId1"/>
<a:stretch>
<a:fillRect/>
</a:stretch>
</p:blipFill>
<p:spPr>
<a:xfrm>
<a:off x="{off_x}" y="{off_y}"/>
<a:ext cx="{final_w}" cy="{final_h}"/>
</a:xfrm>
<a:prstGeom prst="rect">
<a:avLst/>
</a:prstGeom>
</p:spPr>
</p:pic>
</p:spTree>
</p:cSld>
<p:clrMapOvr>
<a:masterClrMapping/>
</p:clrMapOvr>
</p:sld>'''
                    zf.writestr(f'ppt/slides/slide{slide_num}.xml', image_slide)
                    slide_num += 1
                    
                except Exception as e:
                    print(f"[WARN] Failed to process screenshot {idx}: {e}")
                    continue
        
        pptx_buffer.seek(0)
        return pptx_buffer.getvalue()
        
    except Exception as e:
        print(f"[ERROR] Failed to generate PPTX from screenshots: {e}")
        raise

def filter_data(phases=None, health_statuses=None, titles=None, ownerships=None):
    """Filter data by phases (list), health statuses (list), titles (list), and ownerships (list)"""
    # Always exclude "Complete" phase from dashboard
    EXCLUDED_PHASES = {'Complete'}
    data = [r for r in DATA if r.get("Phase") not in EXCLUDED_PHASES]
    # Handle phases - if specified, further filter
    if phases and len(phases) > 0:
        data = [r for r in data if r.get("Phase") in phases]
    # Handle health statuses - if not specified or empty, return all
    if health_statuses and len(health_statuses) > 0:
        data = [r for r in data if r.get("Health Status") in health_statuses]
    # Handle titles - if specified, filter by project title
    if titles and len(titles) > 0:
        titles_set = set(titles)
        data = [r for r in data if r.get("Initiative - Project Title") in titles_set]
    # Handle ownership filter
    if ownerships and len(ownerships) > 0:
        ownerships_set = set(ownerships)
        data = [r for r in data if (r.get("TDA Ownership") or 'No Selection Provided') in ownerships_set]
    return data

def handle_request(client_socket, addr):
    """Handle a single HTTP request"""
    try:
        # Set generous timeout for large PPT payloads (19 screenshots ~ 30MB)
        client_socket.settimeout(120)
        # Receive request headers first
        request_data = b''
        while b'\r\n\r\n' not in request_data:
            chunk = client_socket.recv(65536)
            if not chunk:
                return
            request_data += chunk
        
        # Extract headers and body separator
        header_end = request_data.find(b'\r\n\r\n')
        headers_raw = request_data[:header_end].decode('utf-8', errors='ignore')
        body_data = request_data[header_end + 4:]
        
        # If Content-Length is set, read remaining body
        content_length = 0
        for line in headers_raw.split('\r\n'):
            if line.lower().startswith('content-length:'):
                content_length = int(line.split(':')[1].strip())
                break
        
        # Read remaining body if Content-Length indicates more data
        while len(body_data) < content_length:
            chunk = client_socket.recv(65536)
            if not chunk:
                break
            body_data += chunk
        
        # Decode body
        body_str = body_data.decode('utf-8', errors='ignore')
        
        request_lines = headers_raw.split('\r\n')
        request_line = request_lines[0] if request_lines else ""
        
        # Parse request
        parts = request_line.split()
        if len(parts) < 2:
            return
        
        method = parts[0]
        full_path = parts[1]
        
        # Parse path and query string
        if '?' in full_path:
            path, query_string = full_path.split('?', 1)
        else:
            path = full_path
            query_string = ""
        
        # Parse query parameters (with support for multiple values)
        query_params = {}
        query_params_multi = {}  # Store lists of values for multi-select
        if query_string:
            for param in query_string.split('&'):
                if '=' in param:
                    key, value = param.split('=', 1)
                    # Proper URL decoding
                    from urllib.parse import unquote_plus
                    value = unquote_plus(value)
                    query_params[key] = value  # Last value wins for backward compat
                    # Also collect all values in a list
                    if key not in query_params_multi:
                        query_params_multi[key] = []
                    query_params_multi[key].append(value)
        
        print(f"[{time.strftime('%H:%M:%S')}] {method} {path}")
        
        # Store request_data for later use
        request_data_str = body_str
        
        # Handle CORS preflight (OPTIONS) for all API routes
        if method == 'OPTIONS':
            cors_response = (
                "HTTP/1.1 204 No Content\r\n"
                "Access-Control-Allow-Origin: *\r\n"
                "Access-Control-Allow-Methods: GET, POST, OPTIONS\r\n"
                "Access-Control-Allow-Headers: Content-Type\r\n"
                "Access-Control-Max-Age: 86400\r\n"
                "Connection: close\r\n\r\n"
            )
            client_socket.sendall(cors_response.encode())
            return
        
        # Handle routes
        if path == '/api/health':
            response_json = json.dumps({
                'status': 'healthy',
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            })
            response = f"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nAccess-Control-Allow-Origin: *\r\nContent-Length: {len(response_json)}\r\nConnection: close\r\n\r\n{response_json}"
            client_socket.sendall(response.encode())
        
        elif path == '/api/refresh':
            success, count = refresh_data()
            response_json = json.dumps({
                'success': success,
                'count': count,
                'source': DATA_SOURCE,
                'last_refresh': DATA_LAST_REFRESH,
                'message': f'Refreshed {count} records from BigQuery' if success else 'Refresh failed, using cached data'
            })
            response = f"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nAccess-Control-Allow-Origin: *\r\nContent-Length: {len(response_json)}\r\nConnection: close\r\n\r\n{response_json}"
            client_socket.sendall(response.encode())
        
        elif path == '/api/data':
            # Get multi-select values for phases and health statuses
            phases = query_params_multi.get('phases', [])
            health_statuses = query_params_multi.get('health_statuses', [])
            titles = query_params_multi.get('titles', [])
            ownerships = query_params_multi.get('ownerships', [])
            data = filter_data(phases=phases if phases else None, health_statuses=health_statuses if health_statuses else None, titles=titles if titles else None, ownerships=ownerships if ownerships else None)
            response_json = json.dumps({
                'success': True,
                'count': len(data),
                'data': data
            })
            response = f"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nAccess-Control-Allow-Origin: *\r\nContent-Length: {len(response_json)}\r\nConnection: close\r\n\r\n{response_json}"
            client_socket.sendall(response.encode())
        
        elif path == '/api/phases':
            # Return phases in proper order
            phases = ['Pending', 'Vet', 'Test', 'Test Markets', 'Roll/Deploy']
            response_json = json.dumps({
                'success': True,
                'phases': phases
            })
            response = f"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nAccess-Control-Allow-Origin: *\r\nContent-Length: {len(response_json)}\r\nConnection: close\r\n\r\n{response_json}"
            client_socket.sendall(response.encode())
        
        elif path == '/api/health-statuses':
            statuses = sorted(set(r.get("Health Status", "Unknown") for r in DATA))
            response_json = json.dumps({
                'success': True,
                'health_statuses': statuses
            })
            response = f"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nAccess-Control-Allow-Origin: *\r\nContent-Length: {len(response_json)}\r\nConnection: close\r\n\r\n{response_json}"
            client_socket.sendall(response.encode())
        
        elif path == '/api/titles':
            # Return sorted unique project titles (excluding Complete phase)
            excluded = {'Complete'}
            titles = sorted(set(r.get("Initiative - Project Title", "Unknown") for r in DATA if r.get("Phase") not in excluded))
            response_json = json.dumps({
                'success': True,
                'titles': titles
            })
            response = f"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nAccess-Control-Allow-Origin: *\r\nContent-Length: {len(response_json)}\r\nConnection: close\r\n\r\n{response_json}"
            client_socket.sendall(response.encode())
        
        elif path == '/api/ownerships':
            excluded = {'Complete'}
            OWNERSHIP_ORDER = ['Dallas Team', 'Intake & Test', 'Deployment', 'No Selection Provided']
            all_ownerships = set((r.get("TDA Ownership") or 'No Selection Provided') for r in DATA if r.get("Phase") not in excluded)
            known_set = set(OWNERSHIP_ORDER)
            unknown_ownerships = sorted(o for o in all_ownerships if o not in known_set)
            ownerships = [o for o in OWNERSHIP_ORDER if o in all_ownerships] + unknown_ownerships
            response_json = json.dumps({
                'success': True,
                'ownerships': ownerships
            })
            response = f"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nAccess-Control-Allow-Origin: *\r\nContent-Length: {len(response_json)}\r\nConnection: close\r\n\r\n{response_json}"
            client_socket.sendall(response.encode())
        
        elif path == '/api/summary':
            data = filter_data()
            # Team counts by TDA Ownership
            dallas_team_count = sum(1 for r in data if r.get('TDA Ownership') == 'Dallas Team')
            intake_test_count = sum(1 for r in data if r.get('TDA Ownership') == 'Intake & Test')
            deployment_count = sum(1 for r in data if r.get('TDA Ownership') == 'Deployment')
            # Operating Model: projects with "Ops Model" or "Operation Model" in title
            import re
            ops_model_pattern = re.compile(r'ops\s*model|operation\s*model', re.IGNORECASE)
            ops_model_count = sum(1 for r in data if ops_model_pattern.search(r.get('Initiative - Project Title', '')))
            # Upcoming count (from SIF/AIM data if available)
            if SIF_AIM_DATA:
                upcoming_count = SIF_AIM_DATA.get('unique_upcoming_count')
                if upcoming_count is None:
                    upcoming_count = len({
                        entry.get('project_id') if entry.get('project_id') else entry.get('title', '')
                        for entry in SIF_AIM_DATA.get('upcoming', [])
                    })
            else:
                upcoming_count = 0

            summary = {
                'total_projects': len(data),
                'total_stores': sum(int(r.get('# of Stores', 0) or 0) for r in data),
                'dallas_team_count': dallas_team_count,
                'intake_test_count': intake_test_count,
                'deployment_count': deployment_count,
                'ops_model_count': ops_model_count,
                'upcoming_count': upcoming_count,
                'by_health_status': {},
                'by_phase': {}
            }
            for r in data:
                status = r.get('Health Status', 'Unknown')
                summary['by_health_status'][status] = summary['by_health_status'].get(status, 0) + 1
                phase = r.get('Phase', 'Unknown')
                summary['by_phase'][phase] = summary['by_phase'].get(phase, 0) + 1
            
            response_json = json.dumps({'success': True, 'summary': summary})
            response = f"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nAccess-Control-Allow-Origin: *\r\nContent-Length: {len(response_json)}\r\nConnection: close\r\n\r\n{response_json}"
            client_socket.sendall(response.encode())
        
        elif path == '/api/sif-aim':
            # Return SIF/AIM meeting data (upcoming + recent 21-day actions)
            response_json = json.dumps({'success': True, 'data': SIF_AIM_DATA})
            response = f"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nAccess-Control-Allow-Origin: *\r\nContent-Length: {len(response_json)}\r\nConnection: close\r\n\r\n{response_json}"
            client_socket.sendall(response.encode())
        
        elif path.startswith('/api/project-detail/'):
            # Return detailed project info for Project Summary view
            project_id_str = path.split('/api/project-detail/')[-1]
            detail = get_project_detail(project_id_str)
            if detail:
                response_json = json.dumps({'success': True, 'project': detail})
                response = f"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nAccess-Control-Allow-Origin: *\r\nContent-Length: {len(response_json)}\r\nConnection: close\r\n\r\n{response_json}"
            else:
                response_json = json.dumps({'success': False, 'error': 'Project not found'})
                response = f"HTTP/1.1 404 Not Found\r\nContent-Type: application/json\r\nAccess-Control-Allow-Origin: *\r\nContent-Length: {len(response_json)}\r\nConnection: close\r\n\r\n{response_json}"
            client_socket.sendall(response.encode())
        
        elif path == '/lib/html2canvas.min.js':
            # Serve html2canvas library from local disk (avoids CDN blocks)
            lib_file = SCRIPT_DIR / 'html2canvas.min.js'
            try:
                if lib_file.exists():
                    with open(lib_file, 'rb') as f:
                        lib_data = f.read()
                    print(f"[OK] Serving html2canvas from local disk ({len(lib_data)} bytes)")
                else:
                    raise FileNotFoundError(f"html2canvas.min.js not found in {SCRIPT_DIR}")
            except Exception as e:
                print(f"[ERROR] Failed to load html2canvas: {e}")
                error_response = f"HTTP/1.1 500 Server Error\r\nContent-Type: text/plain\r\nConnection: close\r\n\r\nFailed to load html2canvas library"
                client_socket.sendall(error_response.encode())
                return
            
            response = (
                f"HTTP/1.1 200 OK\r\n"
                f"Content-Type: application/javascript; charset=utf-8\r\n"
                f"Access-Control-Allow-Origin: *\r\n"
                f"Cache-Control: public, max-age=31536000\r\n"
                f"Content-Length: {len(lib_data)}\r\n"
                f"Connection: close\r\n\r\n"
            )
            client_socket.sendall(response.encode())
            client_socket.sendall(lib_data)
        
        elif path == '/spark-logo.png':
            logo_file = Path(r'C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub\Store Support\General Setup\Design\Spark Blank.png')
            try:
                if logo_file.exists():
                    with open(logo_file, 'rb') as f:
                        logo_data = f.read()
                    response = (
                        f"HTTP/1.1 200 OK\r\n"
                        f"Content-Type: image/png\r\n"
                        f"Access-Control-Allow-Origin: *\r\n"
                        f"Cache-Control: public, max-age=31536000\r\n"
                        f"Content-Length: {len(logo_data)}\r\n"
                        f"Connection: close\r\n\r\n"
                    )
                    client_socket.sendall(response.encode())
                    client_socket.sendall(logo_data)
                else:
                    raise FileNotFoundError("Spark logo not found")
            except Exception as e:
                print(f"[ERROR] Failed to load spark logo: {e}")
                error_response = "HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\nConnection: close\r\n\r\nLogo not found"
                client_socket.sendall(error_response.encode())

        elif path in ('/Spark_Blank.png', '/favicon.ico'):
            logo_file = SCRIPT_DIR / 'Spark_Blank.png'
            try:
                if logo_file.exists():
                    with open(logo_file, 'rb') as f:
                        logo_data = f.read()
                    response = (
                        f"HTTP/1.1 200 OK\r\n"
                        f"Content-Type: image/png\r\n"
                        f"Access-Control-Allow-Origin: *\r\n"
                        f"Cache-Control: public, max-age=86400\r\n"
                        f"Content-Length: {len(logo_data)}\r\n"
                        f"Connection: close\r\n\r\n"
                    )
                    client_socket.sendall(response.encode())
                    client_socket.sendall(logo_data)
                else:
                    client_socket.sendall(b"HTTP/1.1 204 No Content\r\nConnection: close\r\n\r\n")
            except Exception as e:
                print(f"[ERROR] Failed to load Spark_Blank.png: {e}")
                client_socket.sendall(b"HTTP/1.1 204 No Content\r\nConnection: close\r\n\r\n")

        elif path in ('/dashboard.html', '/', '/tda-initiatives-insights'):
            html_file = SCRIPT_DIR / 'dashboard.html'
            if html_file.exists():
                try:
                    with open(html_file, 'r', encoding='utf-8') as f:
                        html = f.read()
                    html_bytes = html.encode('utf-8')
                    response = f"HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\nAccess-Control-Allow-Origin: *\r\nContent-Length: {len(html_bytes)}\r\nConnection: close\r\n\r\n"
                    client_socket.sendall(response.encode('utf-8'))
                    client_socket.sendall(html_bytes)
                except Exception as e:
                    print(f"[ERROR] Failed to serve HTML: {e}")
                    error_response = f"HTTP/1.1 500 Server Error\r\nContent-Type: text/plain\r\nConnection: close\r\n\r\nFailed to load dashboard"
                    client_socket.sendall(error_response.encode())
            else:
                error = "Dashboard not found"
                response = f"HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\nConnection: close\r\n\r\n{error}"
                client_socket.sendall(response.encode())
        
        elif path == '/api/feedback':
            # Accept feedback, log it, and send email notification
            try:
                feedback = json.loads(request_data_str) if request_data_str else {}
                feedback['received_at'] = time.strftime('%Y-%m-%d %H:%M:%S')
                feedback_file = SCRIPT_DIR / 'feedback_log.json'
                existing = []
                if feedback_file.exists():
                    try:
                        existing = json.loads(feedback_file.read_text())
                    except Exception:
                        existing = []
                existing.append(feedback)
                feedback_file.write_text(json.dumps(existing, indent=2))
                print(f"  [Feedback] {feedback.get('category', 'N/A')} - Rating: {feedback.get('rating', 'N/A')}")

                # Send feedback email in background thread
                def _send_feedback_email(fb):
                    try:
                        import win32com.client
                        import pythoncom
                        pythoncom.CoInitialize()
                        print(f"  [Feedback Email] COM initialized, dispatching Outlook...")
                        outlook = win32com.client.Dispatch('Outlook.Application')
                        mail = outlook.CreateItem(0)
                        mail.To = 'kendall.rush@walmart.com; atcteamsupport@walmart.com'
                        mail.Subject = f"TDA Dashboard Feedback — {fb.get('category', 'General')} ({fb.get('received_at', '')})"
                        rating = fb.get('rating', 'N/A')
                        category = fb.get('category', 'N/A')
                        comments = fb.get('comments', 'No comments provided')
                        received = fb.get('received_at', '')
                        mail.HTMLBody = f"""<div style="font-family:Segoe UI,Arial,sans-serif;max-width:600px;">
    <h2 style="color:#1E3A8A;margin-bottom:4px;">TDA Insights Dashboard — Feedback</h2>
    <hr style="border:1px solid #E5E7EB;">
    <table style="border-collapse:collapse;width:100%;margin-top:12px;">
        <tr><td style="padding:8px 12px;font-weight:600;color:#374151;width:140px;">Category</td><td style="padding:8px 12px;">{category}</td></tr>
        <tr style="background:#F9FAFB;"><td style="padding:8px 12px;font-weight:600;color:#374151;">Rating</td><td style="padding:8px 12px;font-size:20px;">{rating}</td></tr>
        <tr><td style="padding:8px 12px;font-weight:600;color:#374151;">Comments</td><td style="padding:8px 12px;">{comments}</td></tr>
        <tr style="background:#F9FAFB;"><td style="padding:8px 12px;font-weight:600;color:#374151;">Submitted</td><td style="padding:8px 12px;">{received}</td></tr>
    </table>
    <p style="color:#6B7280;font-size:12px;margin-top:16px;">This message was sent automatically from the TDA Insights Dashboard.</p>
</div>"""
                        print(f"  [Feedback Email] Calling mail.Send()...")
                        mail.Send()
                        print(f"  [Feedback Email] Sent to kendall.rush@walmart.com, atcteamsupport@walmart.com")
                    except Exception as email_err:
                        import traceback
                        print(f"  [Feedback Email ERROR] {email_err}")
                        traceback.print_exc()
                    finally:
                        try:
                            pythoncom.CoUninitialize()
                        except Exception:
                            pass

                threading.Thread(target=_send_feedback_email, args=(dict(feedback),), daemon=True).start()

                response_json = json.dumps({'success': True})
                response = f"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nAccess-Control-Allow-Origin: *\r\nContent-Length: {len(response_json)}\r\nConnection: close\r\n\r\n{response_json}"
            except Exception as e:
                response_json = json.dumps({'success': False, 'error': str(e)})
                response = f"HTTP/1.1 500 Internal Server Error\r\nContent-Type: application/json\r\nAccess-Control-Allow-Origin: *\r\nContent-Length: {len(response_json)}\r\nConnection: close\r\n\r\n{response_json}"
            client_socket.sendall(response.encode())

        elif path == '/api/ppt/generate-from-screenshots':
            try:
                # Parse JSON from request body
                if not request_data_str:
                    raise ValueError("No request body")
                
                request_json = json.loads(request_data_str)
                
                screenshots = request_json.get('screenshots', [])
                title = request_json.get('title', 'TDA Report')
                
                if not screenshots:
                    raise ValueError("No screenshots provided")
                
                # Generate PPTX from screenshots
                pptx_data = generate_pptx_from_screenshots(screenshots, title)
                filename = f'TDA_Report_{int(time.time())}.pptx'
                
                # Send binary file with proper headers
                response_headers = (
                    f"HTTP/1.1 200 OK\r\n"
                    f"Content-Type: application/vnd.openxmlformats-officedocument.presentationml.presentation\r\n"
                    f"Content-Disposition: attachment; filename=\"{filename}\"\r\n"
                    f"Content-Length: {len(pptx_data)}\r\n"
                    f"Access-Control-Allow-Origin: *\r\n"
                    f"Connection: close\r\n\r\n"
                )
                client_socket.sendall(response_headers.encode())
                client_socket.sendall(pptx_data)
            except Exception as e:
                print(f"[ERROR] Screenshot PPT generation failed: {e}")
                error_response = f"HTTP/1.1 500 Server Error\r\nContent-Type: application/json\r\nConnection: close\r\n\r\n" + json.dumps({'error': str(e)})
                client_socket.sendall(error_response.encode())
        
        elif path == '/api/ppt/generate':
            try:
                # Generate PPTX file
                pptx_data = generate_minimal_pptx()
                filename = f'TDA_Report_{int(time.time())}.pptx'
                
                # Send binary file with proper headers
                response_headers = (
                    f"HTTP/1.1 200 OK\r\n"
                    f"Content-Type: application/vnd.openxmlformats-officedocument.presentationml.presentation\r\n"
                    f"Content-Disposition: attachment; filename=\"{filename}\"\r\n"
                    f"Content-Length: {len(pptx_data)}\r\n"
                    f"Access-Control-Allow-Origin: *\r\n"
                    f"Connection: close\r\n\r\n"
                )
                client_socket.sendall(response_headers.encode())
                client_socket.sendall(pptx_data)
            except Exception as e:
                print(f"[ERROR] PPT generation failed: {e}")
                error_response = f"HTTP/1.1 500 Server Error\r\nContent-Type: application/json\r\nConnection: close\r\n\r\n" + json.dumps({'error': str(e)})
                client_socket.sendall(error_response.encode())
        
        elif path == '/favicon.ico':
            response = "HTTP/1.1 204 No Content\r\nConnection: close\r\n\r\n"
            client_socket.sendall(response.encode())
        
        else:
            response_json = json.dumps({'error': 'Endpoint not found'})
            response = f"HTTP/1.1 404 Not Found\r\nContent-Type: application/json\r\nAccess-Control-Allow-Origin: *\r\nContent-Length: {len(response_json)}\r\nConnection: close\r\n\r\n{response_json}"
            client_socket.sendall(response.encode())
    
    except Exception as e:
        print(f"[ERROR] Error handling request: {e}")
        try:
            error_response = "HTTP/1.1 500 Server Error\r\nContent-Type: text/plain\r\nConnection: close\r\n\r\nServer Error"
            client_socket.sendall(error_response.encode())
        except:
            pass
    
    finally:
        try:
            client_socket.close()
        except:
            pass

def start_server():
    """Start the HTTP server"""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server_socket.bind(('0.0.0.0', PORT))
        server_socket.listen(5)
        
        record_count = len(DATA)
        
        # Get machine hostname for shareable URL
        hostname = socket.gethostname()
        
        print("\n" + "="*60)
        print("[OK] TDA Insights Dashboard Backend")
        print("="*60)
        print(f"[OK] Data Source: {DATA_SOURCE}")
        print(f"[OK] Records Loaded: {record_count}")
        print(f"[OK] Server listening on 0.0.0.0:{PORT} (all interfaces)")
        print(f"[OK] Local:   http://localhost:{PORT}/tda-initiatives-insights")
        print(f"[OK] Network: http://{hostname}:{PORT}/tda-initiatives-insights")
        print(f"[OK] API:     http://localhost:{PORT}/api/data")
        print("="*60)
        print("Press Ctrl+C to stop\n")
        
        while True:
            try:
                client_socket, addr = server_socket.accept()
                thread = threading.Thread(target=handle_request, args=(client_socket, addr), daemon=True)
                thread.start()
            except KeyboardInterrupt:
                print("\n\nShutdown requested...")
                break
            except Exception as e:
                print(f"Error accepting connection: {e}")
    
    except OSError as e:
        print(f"[ERROR] Cannot bind to port {PORT}")
        print(f"  {e}")
        return False
    
    finally:
        server_socket.close()
        print("[OK] Server shut down\n")
    
    return True

if __name__ == '__main__':
    try:
        start_server()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()
