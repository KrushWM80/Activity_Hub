"""Pydantic models for Store Meeting Planner"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class RequestStatus(str, Enum):
    PENDING = "Pending"
    REVIEW = "Review"
    APPROVED = "Approved"
    NEEDS_CHANGES = "Needs Changes"
    REJECTED = "Rejected"


class RequestSource(str, Enum):
    FORM = "Form"
    AMP = "AMP"


class MeetingRequest(BaseModel):
    """Maps to store_meeting_request_data BQ table"""
    ID: Optional[str] = None
    Title: str = ""
    Email: str = ""
    Name: str = ""
    AMP_Activity: bool = False
    AMP_Activity_URL: str = ""
    Meeting_Day_of_the_Week: str = ""
    Start_Date: Optional[str] = None
    End_Date: Optional[str] = None
    Meeting_Duration: Optional[int] = None
    AMP_Input: str = ""
    Start_Time: str = ""
    Planner_Cadence: str = ""
    Primary_Language: str = ""
    Role_Type: str = ""
    Meeting_Type: str = ""
    Impacted_Shift: Optional[int] = None
    Store_Selection: str = ""
    Status: str = RequestStatus.PENDING
    Meeting_Reoccurrence: str = "None"
    Meeting_Link: str = ""
    Color_Tag: str = ""
    Compliance_Asset_Id: str = ""
    Submission_Start_time: Optional[str] = None
    Completion_time: str = ""
    Created: str = ""
    Created_By: str = ""
    Modified: str = ""
    Modified_By: str = ""
    Version: str = ""
    # Derived field (not in BQ, used by frontend)
    source: str = RequestSource.FORM
    preview_url: str = ""
    missing_fields: List[str] = []


REQUIRED_FIELDS_FOR_REVIEW = [
    "Title", "Start_Date", "End_Date", "Meeting_Duration",
    "Meeting_Type", "Impacted_Shift", "Store_Selection",
    "Email", "Name"
]


def check_completeness(request: dict) -> tuple[bool, list[str]]:
    """Check if a request has all required fields for Review status.
    Returns (is_complete, list_of_missing_fields)."""
    missing = []
    for field in REQUIRED_FIELDS_FOR_REVIEW:
        val = request.get(field)
        if val is None or val == "" or val == 0:
            missing.append(field)
    return len(missing) == 0, missing


class MeetingRequestSubmit(BaseModel):
    """Fields submitted via the intake form"""
    Title: str
    AMP_Activity: bool = False
    AMP_Activity_URL: str = ""
    Start_Date: str
    End_Date: str
    Meeting_Duration: int
    Meeting_Reoccurrence: str = "None"
    Meeting_Type: str
    Impacted_Shift: int
    Store_Selection: str


class AdminAction(BaseModel):
    """Admin action on a request"""
    status: RequestStatus
    comment: str = ""
    start_time: str = ""
    meeting_link: str = ""


class UserFieldUpdate(BaseModel):
    """User updating missing fields on a Pending request"""
    Meeting_Type: Optional[str] = None
    Impacted_Shift: Optional[int] = None
    Store_Selection: Optional[str] = None
    Meeting_Duration: Optional[int] = None
    Start_Date: Optional[str] = None
    End_Date: Optional[str] = None


class CalendarSlot(BaseModel):
    date: str
    day_of_week: str
    approved_count: int = 0
    max_slots: int = 20
    is_protected_week: bool = False
    wm_week: Optional[int] = None
    fiscal_year: Optional[int] = None


class CalendarEvent(BaseModel):
    """AMP Calendar Event for display on calendar"""
    event_id: str = ""
    title: str = ""
    message_type: str = ""
    start_date: str = ""
    end_date: str = ""
    business_area: str = ""
    author: str = ""
    store_cnt: str = ""
    preview_url: str = ""
    is_protected_week: bool = False
    wm_week: Optional[int] = None


class UserInfo(BaseModel):
    email: str = ""
    username: str = ""
    name: str = ""
    is_admin: bool = False
    auth_method: str = "windows_ad"


class HealthResponse(BaseModel):
    status: str = "ok"
    bigquery_connected: bool = False
    last_amp_sync: Optional[str] = None
    environment: str = "dev"
