#!/usr/bin/env python3
"""
Impact Platform Backend API
Serves project data from AH_Projects (manual entries) + IH_Intake_Data (Intake Hub)
Provides endpoints for dashboard, My Projects, and report generation

URL: http://weus42608431466:8088/activity-hub/Impact
"""

import os
import json
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from pathlib import Path
import tempfile
import uuid

from google.cloud import bigquery

# Initialize FastAPI app
app = FastAPI(title="Impact Platform API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
BQ_PROJECT = "wmt-assetprotection-prod"
BQ_DATASET = "Store_Support_Dev"
BQ_TABLE_PROJECTS = "AH_Projects"
BQ_TABLE_INTAKE = "IH_Intake_Data"
BQ_TABLE_INTAKE_OUTPUT = "output-IHAccBQ"
TEMP_DIR = Path(tempfile.gettempdir()) / "impact_reports"
TEMP_DIR.mkdir(exist_ok=True)

# ==================== UTILITY FUNCTIONS ====================
def normalize_health_status(status: Optional[str]) -> str:
    """
    Convert health status from old format (Green/Yellow/Red) to new format (On Track/At Risk/Off Track)
    """
    if not status:
        return "On Track"
    
    status_lower = status.lower().strip()
    
    # Map old values to new values
    if "green" in status_lower or "on track" in status_lower:
        return "On Track"
    elif "yellow" in status_lower or "risk" in status_lower or "at risk" in status_lower:
        return "At Risk"
    elif "red" in status_lower or "off track" in status_lower:
        return "Off Track"
    
    # If already in new format, return as-is
    if status in ["On Track", "At Risk", "Off Track"]:
        return status
    
    return "On Track"  # Default

# ==================== PYDANTIC MODELS ====================
class ProjectBase(BaseModel):
    title: str
    description: Optional[str] = None
    owner_id: str
    owner_name: str
    business_area: str
    health_status: str  # Green, Yellow, Red
    current_wm_week_update: Optional[str] = None
    project_status: str = "Active"  # Active, Inactive

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    health_status: Optional[str] = None
    current_wm_week_update: Optional[str] = None
    project_status: Optional[str] = None

class ProjectResponse(ProjectBase):
    impact_id: str
    latest_update: Optional[str] = None
    latest_update_timestamp: Optional[str] = None
    current_wm_week_update_timestamp: Optional[str] = None
    created_timestamp: str
    source: str  # "Manual Entry", "Intake Hub"

class MetricsResponse(BaseModel):
    project_count: int
    active_projects: int
    projects_updated_this_week: int
    percent_updated: float
    unique_owners: int

# BigQuery Service
class BigQueryService:
    def __init__(self):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(
            os.environ.get('APPDATA', ''), 'gcloud', 'application_default_credentials.json'
        )
        self.client = bigquery.Client(project=BQ_PROJECT)

    def get_all_projects(self, business_area: Optional[str] = None, 
                         owner_id: Optional[str] = None,
                         health_status: Optional[str] = None,
                         status_filter: str = "Active") -> List[dict]:
        """
        Query all projects from AH_Projects (manual entries)
        Can filter by business_area, owner_id, health_status, status
        """
        query = f"""
        SELECT 
            impact_id,
            title,
            description,
            owner_id,
            owner_name,
            business_area,
            health_status,
            latest_update,
            CAST(latest_update_timestamp AS STRING) as latest_update_timestamp,
            current_wm_week_update,
            CAST(current_wm_week_update_timestamp AS STRING) as current_wm_week_update_timestamp,
            project_status,
            CAST(created_timestamp AS STRING) as created_timestamp,
            'Manual Entry' as source
        FROM `{BQ_PROJECT}.{BQ_DATASET}.{BQ_TABLE_PROJECTS}`
        WHERE 1=1
        """
        
        if status_filter:
            query += f" AND project_status = '{status_filter}'"
        if business_area:
            query += f" AND business_area = '{business_area}'"
        if owner_id:
            query += f" AND owner_id = '{owner_id}'"
        if health_status:
            query += f" AND health_status = '{health_status}'"
        
        query += " ORDER BY business_area, title"
        
        try:
            results = self.client.query(query).result()
            projects = [dict(row) for row in results]
            # Normalize health_status for all projects
            for project in projects:
                project['health_status'] = normalize_health_status(project.get('health_status'))
            return projects
        except Exception as e:
            print(f"Error querying projects: {e}")
            return []

    def create_project(self, project: ProjectCreate) -> dict:
        """
        Insert new project into AH_Projects table
        """
        impact_id = str(uuid.uuid4())
        now = datetime.now().isoformat()
        
        query = f"""
        INSERT INTO `{BQ_PROJECT}.{BQ_DATASET}.{BQ_TABLE_PROJECTS}`
        (impact_id, title, description, owner_id, owner_name, business_area, 
         health_status, project_status, created_timestamp, current_wm_week_update_timestamp)
        VALUES
        ('{impact_id}', '{project.title}', '{project.description or ""}', 
         '{project.owner_id}', '{project.owner_name}', '{project.business_area}',
         '{project.health_status}', '{project.project_status}', '{now}', NULL)
        """
        
        try:
            self.client.query(query).result()
            return {"impact_id": impact_id, "status": "created"}
        except Exception as e:
            print(f"Error creating project: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    def update_project(self, impact_id: str, update: ProjectUpdate) -> dict:
        """
        Update project fields in AH_Projects table
        """
        now = datetime.now().isoformat()
        
        set_clause = []
        if update.title:
            set_clause.append(f"title = '{update.title}'")
        if update.description:
            set_clause.append(f"description = '{update.description}'")
        if update.health_status:
            set_clause.append(f"health_status = '{update.health_status}'")
        if update.current_wm_week_update:
            set_clause.append(f"current_wm_week_update = '{update.current_wm_week_update}'")
            set_clause.append(f"current_wm_week_update_timestamp = '{now}'")
            set_clause.append(f"latest_update = '{update.current_wm_week_update}'")
            set_clause.append(f"latest_update_timestamp = '{now}'")
        if update.project_status:
            set_clause.append(f"project_status = '{update.project_status}'")
        
        if not set_clause:
            return {"status": "no_changes"}
        
        query = f"""
        UPDATE `{BQ_PROJECT}.{BQ_DATASET}.{BQ_TABLE_PROJECTS}`
        SET {', '.join(set_clause)}
        WHERE impact_id = '{impact_id}'
        """
        
        try:
            self.client.query(query).result()
            return {"impact_id": impact_id, "status": "updated"}
        except Exception as e:
            print(f"Error updating project: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    def get_metrics(self) -> dict:
        """
        Calculate dashboard metrics
        """
        query = f"""
        SELECT
            COUNT(*) as total_projects,
            SUM(CASE WHEN project_status = 'Active' THEN 1 ELSE 0 END) as active_projects,
            SUM(CASE WHEN current_wm_week_update IS NOT NULL THEN 1 ELSE 0 END) as updated_this_week,
            COUNT(DISTINCT owner_id) as unique_owners
        FROM `{BQ_PROJECT}.{BQ_DATASET}.{BQ_TABLE_PROJECTS}`
        WHERE project_status = 'Active'
        """
        
        try:
            results = list(self.client.query(query).result())
            if results:
                row = results[0]
                total = row['active_projects'] or 1
                updated = row['updated_this_week'] or 0
                percent = (updated / total * 100) if total > 0 else 0
                
                return {
                    "project_count": row['total_projects'] or 0,
                    "active_projects": row['active_projects'] or 0,
                    "projects_updated_this_week": row['updated_this_week'] or 0,
                    "percent_updated": round(percent, 2),
                    "unique_owners": row['unique_owners'] or 0
                }
        except Exception as e:
            print(f"Error calculating metrics: {e}")
        
        return {
            "project_count": 0,
            "active_projects": 0,
            "projects_updated_this_week": 0,
            "percent_updated": 0.0,
            "unique_owners": 0
        }

    def get_intake_hub_projects(self) -> List[dict]:
        """
        Query active projects from Intake Hub output table
        Maps Intake Hub columns to standard project format
        """
        query = f"""
        SELECT 
            CONCAT('IH-', CAST(ROW_NUMBER() OVER (ORDER BY Project_Name) as STRING)) as impact_id,
            Project_Name as title,
            Project_Description as description,
            Project_Lead_ID as owner_id,
            Project_Lead_Name as owner_name,
            Department as business_area,
            Status as health_status,
            Project_Updates as latest_update,
            CURRENT_TIMESTAMP() as latest_update_timestamp,
            Project_Updates as current_wm_week_update,
            CURRENT_TIMESTAMP() as current_wm_week_update_timestamp,
            'Active' as project_status,
            CAST(Created_Date AS STRING) as created_timestamp,
            'Intake Hub' as source
        FROM `{BQ_PROJECT}.{BQ_DATASET}.{BQ_TABLE_INTAKE_OUTPUT}`
        WHERE UPPER(Status) IN ('ACTIVE', 'ON TRACK', 'AT RISK', 'OFF TRACK')
        ORDER BY Project_Name
        """
        
        try:
            results = self.client.query(query).result()
            projects = [dict(row) for row in results]
            # Normalize health_status for all projects
            for project in projects:
                project['health_status'] = normalize_health_status(project.get('health_status'))
            return projects
        except Exception as e:
            print(f"Error querying Intake Hub projects: {e}")
            return []

    def get_all_projects_combined(self, business_area: Optional[str] = None, 
                                   owner_id: Optional[str] = None,
                                   health_status: Optional[str] = None,
                                   status_filter: str = "Active") -> List[dict]:
        """
        Get all projects from both AH_Projects (manual) and Intake Hub
        Combined results with applied filters
        """
        # Get manual projects
        manual_projects = self.get_all_projects(
            business_area=business_area,
            owner_id=owner_id,
            health_status=health_status,
            status_filter=status_filter
        )
        
        # Get Intake Hub projects
        intake_projects = self.get_intake_hub_projects()
        
        # Apply filters to intake hub projects
        if status_filter:
            intake_projects = [p for p in intake_projects if p.get('project_status') == status_filter]
        if business_area:
            intake_projects = [p for p in intake_projects if p.get('business_area') == business_area]
        if owner_id:
            intake_projects = [p for p in intake_projects if p.get('owner_id') == owner_id]
        if health_status:
            intake_projects = [p for p in intake_projects if p.get('health_status') == health_status]
        
        # Combine and sort
        all_projects = manual_projects + intake_projects
        all_projects.sort(key=lambda p: (p.get('business_area', ''), p.get('title', '')))
        
        return all_projects

# Initialize BigQuery service
bq_service = BigQueryService()

# ==================== API ENDPOINTS ====================

@app.get("/api/impact/projects", response_model=List[ProjectResponse])
async def get_projects(
    business_area: Optional[str] = Query(None),
    owner_id: Optional[str] = Query(None),
    health_status: Optional[str] = Query(None),
    status: str = Query("Active")
):
    """
    Get all projects from both manual entries and Intake Hub with optional filters
    """
    projects = bq_service.get_all_projects_combined(
        business_area=business_area,
        owner_id=owner_id,
        health_status=health_status,
        status_filter=status
    )
    return projects

@app.get("/api/impact/projects/{impact_id}", response_model=ProjectResponse)
async def get_project(impact_id: str):
    """
    Get single project by ID
    """
    projects = bq_service.get_all_projects()
    for p in projects:
        if p.get('impact_id') == impact_id:
            return p
    raise HTTPException(status_code=404, detail="Project not found")

@app.post("/api/impact/projects", response_model=dict)
async def create_project(project: ProjectCreate):
    """
    Create new manual project entry
    """
    return bq_service.create_project(project)

@app.put("/api/impact/projects/{impact_id}")
async def update_project(impact_id: str, update: ProjectUpdate):
    """
    Update project fields
    """
    return bq_service.update_project(impact_id, update)

@app.get("/api/impact/metrics", response_model=MetricsResponse)
async def get_metrics():
    """
    Get dashboard metrics
    """
    return bq_service.get_metrics()

@app.get("/api/impact/owners")
async def get_owners():
    """
    Get list of all unique owners for autocomplete/lookup
    """
    projects = bq_service.get_all_projects_combined()
    owners = []
    seen = set()
    for project in projects:
        owner_id = project.get('owner_id')
        owner_name = project.get('owner_name')
        if owner_id and owner_id not in seen:
            owners.append({
                "owner_id": owner_id,
                "owner_name": owner_name
            })
            seen.add(owner_id)
    return sorted(owners, key=lambda x: x.get('owner_name', ''))

@app.get("/api/impact/my-projects")
async def get_my_projects(user_id: str = Query(...)):
    """
    Get projects for specific user (owner)
    """
    projects = bq_service.get_all_projects(owner_id=user_id)
    return projects

@app.post("/api/impact/generate-ppt")
async def generate_ppt_report(
    business_area: Optional[str] = Query(None),
    status: str = Query("Active")
):
    """
    Generate PPT report from both manual and Intake Hub projects
    """
    projects = bq_service.get_all_projects_combined(
        business_area=business_area,
        status_filter=status
    )
    
    # Import report generator
    from impact_report_generator import generate_pptx_report
    
    try:
        pptx_data, report_id = generate_pptx_report(projects)
        download_url = f"/api/impact/download/report/{report_id}.pptx"
        return {
            "status": "generated",
            "report_id": report_id,
            "download_url": download_url,
            "generated_timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PPT generation failed: {str(e)}")

@app.get("/api/impact/download/report/{report_id}.pptx")
async def download_pptx(report_id: str):
    """
    Download generated PPT file
    """
    file_path = TEMP_DIR / f"{report_id}.pptx"
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Report not found")
    
    return FileResponse(file_path, media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation")

@app.get("/api/impact/download/report/{report_id}.pdf")
async def download_pdf(report_id: str):
    """
    Download generated PDF file
    """
    file_path = TEMP_DIR / f"{report_id}.pdf"
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Report not found")
    
    return FileResponse(file_path, media_type="application/pdf")

@app.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {"status": "ok", "timestamp": datetime.now().isoformat()}

# Mount static files for dashboard (MUST be last to avoid blocking API routes)
FRONTEND_DIR = Path(__file__).parent.parent / "frontend_deployment"
if FRONTEND_DIR.exists():
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="static")

# Run server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002, reload=False)
