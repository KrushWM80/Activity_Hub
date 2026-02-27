"""SQLAlchemy database models for Zorro platform."""

from datetime import datetime
from typing import Optional

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    JSON,
    String,
    Text,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class DesignElementDB(Base):
    """
    Design element storage (replaces JSON file).
    
    Stores character definitions, logos, environments, etc.
    """
    
    __tablename__ = "design_elements"
    
    # Primary key
    id = Column(String(50), primary_key=True)
    
    # Core fields
    name = Column(String(200), nullable=False, index=True)
    type = Column(String(50), nullable=False, index=True)  # character, logo, environment, etc.
    description = Column(Text, nullable=False)
    prompt = Column(Text, nullable=False)
    
    # Metadata
    category = Column(String(100), nullable=True, index=True)
    tags = Column(JSON, nullable=True)  # Array of tag strings
    created_by = Column(String(100), nullable=False)
    facility_id = Column(String(50), nullable=True, index=True)
    
    # Governance
    status = Column(String(50), default="pending", index=True)  # pending, approved, rejected
    approved_by = Column(String(100), nullable=True)
    approved_at = Column(DateTime, nullable=True)
    rejection_reason = Column(Text, nullable=True)
    
    # Additional metadata
    metadata = Column(JSON, nullable=True)  # Flexible storage for brand guidelines, etc.
    
    # Usage tracking
    usage_count = Column(Integer, default=0)
    last_used_at = Column(DateTime, nullable=True)
    
    # Visibility
    visibility = Column(String(50), default="private")  # private, facility, region, company
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    videos = relationship("VideoGenerationDB", back_populates="design_element")
    
    def __repr__(self):
        return f"<DesignElement {self.name} ({self.type})>"


class VideoGenerationDB(Base):
    """
    Video generation history and metadata.
    
    Tracks all generated videos with full context.
    """
    
    __tablename__ = "video_generations"
    
    # Primary key
    id = Column(String(50), primary_key=True)
    
    # Input
    original_message = Column(Text, nullable=False)
    enhanced_prompt = Column(Text, nullable=False)
    negative_prompt = Column(Text, nullable=True)
    
    # Video parameters
    duration = Column(Float, nullable=False)
    aspect_ratio = Column(String(20), nullable=False)
    style = Column(String(100), nullable=True)
    mood = Column(String(100), nullable=True)
    
    # Generation details
    provider = Column(String(50), nullable=False, index=True)  # walmart_media_studio, etc.
    model = Column(String(100), nullable=True)
    status = Column(String(50), default="pending", index=True)  # pending, generating, completed, failed
    
    # Output
    video_path = Column(String(500), nullable=True)
    thumbnail_path = Column(String(500), nullable=True)
    captions_path = Column(String(500), nullable=True)
    audio_desc_path = Column(String(500), nullable=True)
    transcript_path = Column(String(500), nullable=True)
    
    # Metadata
    file_size_bytes = Column(Integer, nullable=True)
    resolution = Column(String(50), nullable=True)
    fps = Column(Float, nullable=True)
    
    # Design element used
    design_element_id = Column(String(50), ForeignKey("design_elements.id"), nullable=True, index=True)
    design_element = relationship("DesignElementDB", back_populates="videos")
    
    # User tracking
    created_by = Column(String(100), nullable=False, index=True)
    facility_id = Column(String(50), nullable=True, index=True)
    
    # AI disclosure
    ai_watermark_applied = Column(Boolean, default=False)
    watermark_text = Column(String(100), nullable=True)
    
    # Error handling
    error_message = Column(Text, nullable=True)
    retry_count = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    
    # Generation time tracking
    @property
    def generation_time_seconds(self) -> Optional[float]:
        """Calculate generation time in seconds."""
        if self.started_at and self.completed_at:
            return (self.completed_at - self.started_at).total_seconds()
        return None
    
    def __repr__(self):
        return f"<VideoGeneration {self.id} ({self.status})>"


class UserActivityDB(Base):
    """
    User activity tracking for analytics.
    
    Tracks user actions for usage metrics and reporting.
    """
    
    __tablename__ = "user_activities"
    
    # Primary key
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # User identification
    user_id = Column(String(100), nullable=False, index=True)
    facility_id = Column(String(50), nullable=True, index=True)
    
    # Activity details
    action = Column(String(100), nullable=False, index=True)  # video_generated, design_created, etc.
    resource_type = Column(String(50), nullable=True)  # video, design_element, etc.
    resource_id = Column(String(50), nullable=True)
    
    # Context
    metadata = Column(JSON, nullable=True)  # Flexible storage for action-specific data
    
    # Timestamps
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    def __repr__(self):
        return f"<UserActivity {self.user_id} - {self.action}>"


class SystemMetricsDB(Base):
    """
    System performance metrics.
    
    Tracks platform health and performance indicators.
    """
    
    __tablename__ = "system_metrics"
    
    # Primary key
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Metric details
    metric_name = Column(String(100), nullable=False, index=True)
    metric_value = Column(Float, nullable=False)
    metric_unit = Column(String(50), nullable=True)
    
    # Context
    tags = Column(JSON, nullable=True)  # Additional dimensions
    
    # Timestamps
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    def __repr__(self):
        return f"<SystemMetric {self.metric_name}: {self.metric_value}>"
