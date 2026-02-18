"""
Email Reporting Models for Intake Hub
Defines data structures for email report configurations and scheduling
"""

from datetime import datetime
from typing import Optional, List, Dict
from enum import Enum
from pydantic import BaseModel, EmailStr, Field


class ReportContentType(str, Enum):
    """Types of content that can be included in reports"""
    OVERVIEW = "Overview"
    MY_ACTIONS = "My Actions"
    COUNTS = "Counts"
    NEW = "New"
    UPCOMING = "Upcoming"
    NOTES = "Notes"
    ACTIVITY_FEED = "Activity Feed"
    ACTIVITY_DETAILS = "Activity Feed - Details"
    ACTIVITY_FILES = "Activity Feed - Files"
    ACTIVITY_LINKS = "Activity Feed - Links"
    ACTIVITY_FLOW = "Activity Feed - Flow"
    ACTIVITY_ACTIONS = "Activity Feed - Actions"
    ACTIVITY_FACILITIES = "Activity Feed - Facilities"


class ReportFrequency(str, Enum):
    """Frequency options for report delivery"""
    DAILY = "Daily"
    WEEKLY = "Weekly"
    BIWEEKLY = "Bi-Weekly"
    MONTHLY = "Monthly"
    CUSTOM = "Custom"


class ReportTimeframe(str, Enum):
    """Timeframe options for report data"""
    CURRENT_DAY = "Current Day"
    CURRENT_WEEK = "Current Week"
    CURRENT_MONTH = "Current Month"
    CURRENT_YEAR = "Current Year"
    LAST_7_DAYS = "Last 7 Days"
    LAST_30_DAYS = "Last 30 Days"
    CUSTOM = "Custom"


class ReportFormat(str, Enum):
    """Format options for report delivery"""
    EMAIL_BODY = "Email Body"
    PDF = "PDF"
    BOTH = "Both"


class ReportColumnConfig(BaseModel):
    """Configuration for which columns to include in report"""
    # Standard columns (always included)
    intake_card_number: bool = True
    title_with_link: bool = True
    facility_total_count: bool = True
    
    # Optional columns
    partner: bool = False
    business_organization: bool = False
    store_area: bool = False
    owner: bool = False
    phase: bool = False
    facility_phase: bool = False
    health: bool = False
    projected_completion_date: bool = False
    implementation_wm_week: bool = False
    director: bool = False
    sr_director: bool = False
    facility_type: bool = False
    sc_count: bool = False
    nhm_count: bool = False
    div1_count: bool = False
    other_count: bool = False


class ReportFilterConfig(BaseModel):
    """Filter configuration for report data"""
    partner: Optional[List[str]] = None
    business_organization: Optional[List[str]] = None
    store_area: Optional[List[str]] = None
    owner: Optional[List[str]] = None
    phase: Optional[List[str]] = None
    facility_phase: Optional[List[str]] = None
    health: Optional[List[str]] = None
    director: Optional[List[str]] = None
    sr_director: Optional[List[str]] = None
    facility_type: Optional[List[str]] = None


class EmailReportConfig(BaseModel):
    """Complete configuration for an email report"""
    config_id: Optional[str] = None  # UUID for existing configs
    user_id: str = Field(..., description="User who owns this configuration")
    report_name: str = Field(..., description="Name for this report configuration")
    
    # Report Content
    content_types: List[ReportContentType] = Field(..., description="Types of content to include")
    columns: ReportColumnConfig = Field(default_factory=ReportColumnConfig)
    filters: ReportFilterConfig = Field(default_factory=ReportFilterConfig)
    
    # Delivery Settings
    frequency: ReportFrequency = Field(..., description="How often to send report")
    delivery_day: Optional[str] = None  # For weekly: "Monday", "Friday", etc.
    delivery_time: str = Field(default="08:00", description="Time to send (HH:MM format)")
    
    # Timeframe
    timeframes: List[ReportTimeframe] = Field(..., description="Data timeframes to include")
    custom_start_date: Optional[datetime] = None
    custom_end_date: Optional[datetime] = None
    
    # Recipients
    primary_email: EmailStr = Field(..., description="Primary recipient email")
    cc_emails: List[EmailStr] = Field(default_factory=list, description="Additional recipients")
    
    # Format
    report_format: ReportFormat = Field(default=ReportFormat.EMAIL_BODY)
    
    # Status
    is_active: bool = Field(default=True, description="Whether this report is active")
    last_sent: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "user123",
                "report_name": "Weekly Partner Status",
                "content_types": ["Overview", "Upcoming", "Notes"],
                "frequency": "Weekly",
                "delivery_day": "Friday",
                "delivery_time": "09:00",
                "timeframes": ["Current Week"],
                "primary_email": "user@walmart.com",
                "cc_emails": ["team@walmart.com"],
                "report_format": "Both"
            }
        }


class ReportConfigCreateRequest(BaseModel):
    """Request to create a new report configuration"""
    user_id: str
    report_name: str
    content_types: List[ReportContentType]
    columns: Optional[ReportColumnConfig] = None
    filters: Optional[ReportFilterConfig] = None
    frequency: ReportFrequency
    delivery_day: Optional[str] = None
    delivery_time: str = "08:00"
    timeframes: List[ReportTimeframe]
    custom_start_date: Optional[datetime] = None
    custom_end_date: Optional[datetime] = None
    primary_email: EmailStr
    cc_emails: List[EmailStr] = []
    report_format: ReportFormat = ReportFormat.EMAIL_BODY
    is_active: bool = True


class ReportConfigUpdateRequest(BaseModel):
    """Request to update an existing report configuration"""
    report_name: Optional[str] = None
    content_types: Optional[List[ReportContentType]] = None
    columns: Optional[ReportColumnConfig] = None
    filters: Optional[ReportFilterConfig] = None
    frequency: Optional[ReportFrequency] = None
    delivery_day: Optional[str] = None
    delivery_time: Optional[str] = None
    timeframes: Optional[List[ReportTimeframe]] = None
    custom_start_date: Optional[datetime] = None
    custom_end_date: Optional[datetime] = None
    primary_email: Optional[EmailStr] = None
    cc_emails: Optional[List[EmailStr]] = None
    report_format: Optional[ReportFormat] = None
    is_active: Optional[bool] = None


class ReportConfigResponse(BaseModel):
    """Response with report configuration"""
    config_id: str
    user_id: str
    report_name: str
    content_types: List[str]
    frequency: str
    delivery_day: Optional[str]
    delivery_time: str
    timeframes: List[str]
    primary_email: str
    cc_emails: List[str]
    report_format: str
    is_active: bool
    last_sent: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    columns: Dict
    filters: Dict


class ReportConfigListResponse(BaseModel):
    """Response with list of report configurations"""
    total: int
    configs: List[ReportConfigResponse]


class ReportGenerationRequest(BaseModel):
    """Request to generate and send a report immediately"""
    config_id: str
    override_email: Optional[EmailStr] = None  # Override recipients for testing


class ReportGenerationResponse(BaseModel):
    """Response after generating a report"""
    success: bool
    message: str
    report_id: Optional[str] = None
    sent_to: List[str]
    generated_at: datetime


class ReportExecutionLog(BaseModel):
    """Log entry for report execution"""
    log_id: str
    config_id: str
    execution_time: datetime
    success: bool
    error_message: Optional[str] = None
    recipients: List[str]
    record_count: int
    report_size_bytes: Optional[int] = None
