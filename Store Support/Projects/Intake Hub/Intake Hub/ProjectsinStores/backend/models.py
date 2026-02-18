from datetime import datetime
from typing import Optional, List
from enum import Enum

class ProjectStatus(str, Enum):
    ACTIVE = "Active"
    ARCHIVED = "Archived"
    PENDING = "Pending"

class ProjectPhase(str, Enum):
    PLANNING = "Planning"
    EXECUTION = "Execution"
    REVIEW = "Review"
    COMPLETE = "Complete"

class ProjectSource(str, Enum):
    INTAKE_HUB = "Intake Hub"
    OPERATIONS = "Operations"
    REALTY = "Realty"

class Division(str, Enum):
    EAST = "EAST"
    WEST = "WEST"
    NORTH = "NORTH"
    SOUTH = "SOUTH"
    NORTHEAST = "NORTHEAST"
    NORTHWEST = "NORTHWEST"
    SOUTHEAST = "SOUTHEAST"
    SOUTHWEST = "SOUTHWEST"

class Project:
    """
    Represents a project from IH_Intake_Data
    """
    def __init__(self):
        self.project_id: str = ""
        self.project_source: ProjectSource = ProjectSource.INTAKE_HUB
        self.title: str = ""
        self.division: str = ""
        self.region: str = ""
        self.market: str = ""
        self.store: str = ""
        self.store_area: str = ""
        self.business_area: str = ""
        self.phase: str = ""
        self.tribe: str = ""
        self.wm_week: str = ""
        self.fy: str = ""
        self.status: ProjectStatus = ProjectStatus.ACTIVE
        self.store_count: int = 0
        self.owner: str = ""  # Project Owner
        self.partner: str = ""  # Partner name
        self.health: Optional[str] = None  # Project health status
        self.business_type: Optional[str] = None  # Business type
        self.associate_impact: Optional[str] = None  # Impact on associates
        self.customer_impact: Optional[str] = None  # Impact on customers
        self.created_date: Optional[datetime] = None
        self.last_updated: Optional[datetime] = None
        self.description: Optional[str] = None
        # Store location data from Store_Cur_Data table
        self.latitude: Optional[float] = None
        self.longitude: Optional[float] = None
        self.store_address: Optional[str] = None
        self.city: Optional[str] = None
        self.state: Optional[str] = None
        self.zip_code: Optional[str] = None

class StoreCount:
    """
    Aggregated store count data
    """
    def __init__(self):
        self.project_source: ProjectSource = ProjectSource.INTAKE_HUB
        self.division: Optional[str] = None
        self.region: Optional[str] = None
        self.market: Optional[str] = None
        self.total_stores: int = 0
        self.active_projects: int = 0

class FilterCriteria:
    """
    Filter criteria for querying projects
    """
    def __init__(self):
        self.tribe: Optional[List[str]] = None
        self.store: Optional[List[str]] = None
        self.store_area: Optional[List[str]] = None
        self.market: Optional[List[str]] = None
        self.business_area: Optional[List[str]] = None
        self.region: Optional[List[str]] = None
        self.phase: Optional[List[str]] = None
        self.division: Optional[List[str]] = None
        self.project_source: Optional[List[str]] = None
        self.wm_week: Optional[List[str]] = None
        self.fy: Optional[List[str]] = None
        self.status: ProjectStatus = ProjectStatus.ACTIVE  # Default to active only

class ProjectSummary:
    """
    Summary statistics for dashboard
    """
    def __init__(self):
        self.total_active_projects: int = 0
        self.total_stores: int = 0
        self.intake_hub_projects: int = 0
        self.intake_hub_stores: int = 0
        self.realty_projects: int = 0
        self.realty_stores: int = 0
        self.by_division: dict = {}
        self.by_phase: dict = {}
        self.last_updated: datetime = datetime.now()
